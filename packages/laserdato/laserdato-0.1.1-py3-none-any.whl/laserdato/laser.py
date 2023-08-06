from .embed.embed import embed_sentences
import numpy as np
from .get_model import load_or_download_file
from .lib.constants import laser3_langs, langs_with_specific_vocab

from .align import get_best_neighbors, match_sentences_with_best_neighbors
from .embed.encoder import load_model
from .embed.multiGpuEncoder import MultiGpuEncoder


def align_with_embeddings(
    embeddings_lang0,
    embeddings_lang1,
    sentences_lang0,
    sentences_lang1,
    threshold_score=0,
    keep_bad_matched=False,
):
    """
    Align sentences based on their embeddings
    :param threshold_score: minimum score to keep a match
    """
    best_neighbors, scores = get_best_neighbors(embeddings_lang0, embeddings_lang1)
    return match_sentences_with_best_neighbors(
        sentences_lang0,
        sentences_lang1,
        best_neighbors,
        scores,
        threshold_score,
        keep_bad_matched=keep_bad_matched,
    )


class Laser:
    def _load_encoder(
        self,
        hugging_face=False,
        max_sentences=10000,
        max_tokens=12000,
        sort_kind="mergesort",
    ):
        version = 0
        if self.lang:
            version = 1
            pt = load_or_download_file(f"laser3-{self.lang}.v{version}.pt")
        else:
            pt = load_or_download_file("laser2.pt")
        if self.lang and self.lang in langs_with_specific_vocab:
            self.spm = load_or_download_file(
                f"laser3-{self.lang}.v{version}.spm"
            ).as_posix()
            load_or_download_file(f"laser3-{self.lang}.v{version}.cvocab")
        else:
            self.spm = str(load_or_download_file("laser2.spm").as_posix())
            load_or_download_file("laser2.cvocab")
        encoder = load_model(
            encoder=str(pt),
            spm_model=self.spm,
            verbose=self.verbose,
            hugging_face=hugging_face,
            max_sentences=max_sentences,
            max_tokens=max_tokens,
            sort_kind=sort_kind,
        )
        return encoder

    def __init__(
        self,
        lang: str = None,
        target_device: int = None,
        cpu: bool = False,
        verbose=False,
    ):
        """
        :param lang: only to be specified if using laser3, must be in laser3_langs. If None, will use laser2
        :param target_device: ids of a GPU to use for embedding, if None, will use the first GPU available. If you want to use multiple GPUs, use launchMultiGpuEncoder
        :param cpu: if True, will use CPU for embedding and ignore target_devices
        :param verbose: if True, will print some information about the embedding process
        """
        if cpu and target_device is not None:
            raise ValueError("Cannot specify cpu=True and target_device")
        self.cpu = cpu
        self.set_lang(lang=lang)
        self.multiGpu = False
        self.verbose = verbose
        self.encoder = self._load_encoder()
        self.encoder._choose_encoder_device(cpu=cpu, device=target_device)

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def set_lang(self, lang: str):
        if lang and lang not in laser3_langs:
            raise ValueError(f"Language {lang} not supported")
        self.lang = lang

    def activateMultiGpuEncoder(self, target_devices: list[int]):
        """
        :param target_devices: list of GPU ids to use for embedding
        Don't forget to close the encoder with closeMultiGpuEncoder
        """
        if self.cpu:
            raise ValueError("Cannot launch multiGpuEncoder with cpu=True")
        new_encoder = self._load_encoder()
        self.multiGpuEncoder = MultiGpuEncoder(target_devices, new_encoder)
        self.multiGpu = True

    def deactivateMultiGpuEncoder(self):
        if self.multiGpu == False:
            raise ValueError("Cannot close multiGpuEncoder, it is not open")
        self.multiGpuEncoder.delete()
        self.multiGpu = False

    def embed_sentences(self, sentences: list[str]) -> list[np.ndarray]:
        """
        :param sentences: list of sentences to embed
        :return: list of embeddings
        """
        embeddings = embed_sentences(
            sentences=sentences,
            encoder=self.encoder,
            verbose=self.verbose,
            spm_model=self.spm,
        )
        return embeddings

    def align_sentences(
        self,
        sentences_lang0: list[str],
        sentences_lang1: list[str],
        threshold_score: float = 0,
        keep_bad_matched: bool = False,
    ) -> list[tuple[str, str, int]]:
        """
        Not compatible with laser3, if you want to use laser3 lang, use align_with_embeddings directly
        Align two lists of sentences using xSIM and the LASER embeddings
        :param sentences_lang0: list of sentences in lang0
        :param sentences_lang1: list of sentences in lang1
        :param threshold_score: if the score of the alignment is below this threshold, the alignment is considered bad
        :param keep_bad_matched: if True it keep sentence with no match as (sentence_1,None,0), if False it just removes them
        :return: list of tuples with at each time the lang0 sentence, the lang1 corresponding sentence and the alignment score. The order of sentences_lang0 is preserved.
        """
        embeddings_lang0 = self.embed_sentences(sentences=sentences_lang0)
        embeddings_lang1 = self.embed_sentences(sentences=sentences_lang1)
        return align_with_embeddings(
            embeddings_lang0,
            embeddings_lang1,
            sentences_lang0,
            sentences_lang1,
            threshold_score=threshold_score,
            keep_bad_matched=keep_bad_matched,
        )
