from pangeamt_nlp.translation_model.translation_model_factory import (
    TranslationModelFactory,
)
import logging
from pangeamt_nlp.seg import Seg
from nteu_corporate_engine.pipeline import Pipeline
from typing import Dict, List
from asyncio import Lock
import math
import itertools
import numpy as np

NO_LONELY_TRANSLATABLE_CHARS = "/n/t \u200b"

class Engine:
    def __init__(self, config: Dict, log_file: str = None, dbug: bool = False):
        self.setup_log(log_file, dbug)
        self._config = config
        self._pipeline = Pipeline(self._config)
        self._model = self.load_model()
        online_learning_args = config["translation_engine_server"].get(
            "online_learning", None
        )
        if online_learning_args is not None:
            self._model.setup_online_trainer(online_learning_args)

    def load_model(self):
        name = self._config["translation_model"]["name"]
        args = self._config["translation_model"]["args_decoding"]
        if self._config["translation_engine_server"]["gpu"]:
            args["gpu"] = 0
        model_path = self._config["translation_engine_server"]["model_path"]
        if args == {}:
            msg = f"Loading Model -> {name} with default args"
        else:
            msg = f"Loading Model -> {name} with arguments {args}."
        logging.info(msg)
        translation_model = TranslationModelFactory.get_class(name)
        return translation_model(model_path, **args)

    async def translate(self, srcs: List, n_best: int = 1):
        best_translations = []
        best_scores = []
        if self._config["translation_model"]["name"] == "onmt":
            translations = self._model.translate(srcs, n_best=n_best)
            for translation in translations:
                self.log_translation(translation)
                best_translations.append(translation.pred_sents[0].sentence)
                best_scores.append(translation.pred_sents[0].score)

        elif self._config["translation_model"]["name"] == "marianmt":
            args_dec = self._config["translation_model"]["args_decoding"]
            if not args_dec["in_training_servers"]:
                best_translations = self._model.translate(srcs, n_best=n_best)
            else:
                model_path = self._config["translation_engine_server"]["model_path"]
                marian_path = self._config["translation_model"]["marian_path"]
                if self._config["translation_engine_server"]["gpu"]:
                    gpu = 0
                else:
                    gpu = None
                best_translations = self._model.translate_training_servers(
                    srcs, model_path, marian_path, gpu
                )
            for translation in best_translations:
                self.log_translation(translation)
        return best_translations,best_scores


    def split_sentence(self, seg_src: str, max_len: int):

        chunked_input = []
        rest_seg = seg_src
        separators = [".","?","!",":",";"]
        while len(rest_seg) > max_len:
            good_str = rest_seg[:max_len]
            last_separators = []
            for separator in separators:
                last_separators.append(good_str.rfind(separator))
        
            last_sep = max(last_separators)
            if last_sep == -1:
                last_sep = good_str.rfind(" ")
            
            if last_sep == -1:
                last_sep = max_len
            
            rest_seg = rest_seg[last_sep+1:].strip()
            final_segment = good_str[:last_sep+1].strip()

            seg = Seg(final_segment)
            await self._pipeline.preprocess(seg)
            chunked_input.append(seg.src)

        if rest_seg.strip(NO_LONELY_TRANSLATABLE_CHARS) != "":
            seg = Seg(rest_seg)
            await self._pipeline.preprocess(seg)
            chunked_input.append(seg.src)

        return chunked_input


    async def process_batch(self, batch: List, lock: Lock = None):
        srcs = []
        segs = []
        ans = []
        
        no_trans_ind = []
        no_trans_score = []
        no_trans_trad = []

        max_len = 600
        
        for i, src in enumerate(batch):
            
            seg = Seg(src)

            # Model can not translate only spaces, new lines, tabs...
            if src.strip(NO_LONELY_TRANSLATABLE_CHARS) == "":
                no_trans_ind.append(i)
                no_trans_score.append(0)
                no_trans_trad.append(seg.src)
            
            # Model does not translate properly son long segments
            # So we split long segments and translate them before 
            elif len(seg.src) > max_len:
                logging.info("Splitting too long segment: "+ str(seg.src))
                logging.info("With len: "+ str(len(seg.src)))
                
                seg.src = seg.src.strip()
                chunked_segment = self.split_sentence(seg.src, max_len)
                if lock is not None:
                    async with lock:
                        translations,scores = await self.translate(chunked_segment)
                else:
                    translations,scores = await self.translate(chunked_segment)
                
                trans = " ".join(translations)
                score = sum(scores) / len(scores)
                
                no_trans_ind.append(i)
                no_trans_trad.append(trans)
                no_trans_score.append(score)

                await self._pipeline.preprocess(seg)

            else:
                await self._pipeline.preprocess(seg)
                srcs.append(seg.src)

            segs.append(seg)


        # If there is nothing to translate skip translation
        if len(no_trans_ind) != len(batch):

            # Only for GPU
            if self._config["translation_engine_server"]["gpu"]:
                biggest = len(max(srcs, key=len))
                # change batch size depending on max sentence length to not overload gpu
                batch_size = 32
                logging.info("MAX CHARACTERS SENTENCE: " + str(biggest))
                logging.info("LEN BATCH TO TRANSLATE: " + str(len(srcs)))
                logging.info("BATCH SIZE USED: " + str(batch_size))

                if batch_size >= len(srcs):
                    if lock is not None:
                        async with lock:
                            translations,scores = await self.translate(srcs)
                    else:
                        translations,scores = await self.translate(srcs)

                else:
                    translations = []
                    scores = []
                    iters = math.ceil(len(srcs)/batch_size)
                    for i in range(iters):
                        if lock is not None:
                            async with lock:
                                trans,scs = await self.translate(srcs[i*batch_size:(i+1)*batch_size])
                        else:
                            trans,scs = await self.translate(srcs[i*batch_size:(i+1)*batch_size])

                        translations = translations + trans
                        scores = scores + scs

            # Only for CPU
            else:
                if lock is not None:
                    async with lock:
                        translations,scores = await self.translate(srcs)
                else:
                    translations,scores = await self.translate(srcs)

        else:                      
            logging.info("Nothing to translate in "+ str(batch))
            translations = []  
            scores = []

        # We add back eliminated alements
        for e, score, trad in zip(no_trans_ind, no_trans_score, no_trans_trad):
            translations.insert(e, trad)
            scores.insert(e, score)
        
        final_scores = [np.e**(s)*10 for s in scores]

        for translation, seg in zip(translations, segs):
            seg.tgt_raw = translation
            seg.tgt = seg.tgt_raw
            if seg.tgt_raw.strip(NO_LONELY_TRANSLATABLE_CHARS) != "":
                await self._pipeline.postprocess(seg)
            ans.append(seg.tgt)
            logging.info(
                f"Translated -> {seg.src_raw} -> {seg.src} "
                f"-> {seg.tgt_raw} -> {seg.tgt}"
            )
        return ans, final_scores

    async def online_train(self, batch: List, num_steps: int = 1, lock: Lock = None):
        tus = []
        for src, tgt in [tu for tu in batch]:
            seg = Seg(src, tgt)
            await self._pipeline.process_train(seg)
            tus.append((seg.src, seg.tgt))
        if lock is not None:
            async with lock:
                self._model.online_train(tus, num_steps)
        else:
            self._model.online_train(tus, num_steps)

    @classmethod
    def setup_log(cls, log_file: str = None, dbug: bool = None):
        hdlrs = [logging.StreamHandler()]
        if log_file is not None:
            hdlrs.append(logging.FileHandler(log_file))
        cls.lvl = logging.DEBUG if dbug else logging.INFO
        logging.basicConfig(
            handlers=hdlrs,
            level=cls.lvl,
            format="%(asctime)s :: %(levelname)s :: %(message)s",
        )

    def log_translation(self, translation: "Translation"):
        if self.lvl == logging.DEBUG:
            n_best = len(translation)
            log_msg = (
                f"For sentence {translation.pred_sents[0].src_raw}",
                f"{n_best}-best translations:",
            )
            logging.debug(log_msg)
            f = "\nOption #{0} with score {1}:\n{2}\nAttention:\n"
            for i, prediction in enumerate(translation.pred_sents):
                log_msg = f.format(i, prediction.score, prediction.sentence)
                table = prediction.get_pretty_attention()
                if table is not None:
                    table_fields = table._field_names
                    table_width = len(table_fields)
                    for column_index in range(0, table_width, 3):
                        f_index = column_index
                        l_index = min([column_index + 3, table_width])
                        fields_to_take = table_fields[f_index:l_index]
                        str_to_add = table.get_string(fields=fields_to_take) + "\n"
                        log_msg += str_to_add
                logging.debug(log_msg)
