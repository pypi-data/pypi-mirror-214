# from sentencepiece import SentencePieceProcessor
# from laserdato import Laser

# # sp = SentencePieceProcessor(
# #     model_file="/home/gauthier.roy/test_python/env_de_test/lib/python3.10/site-packages/laserdato/models/laser2.spm"
# # )

# test = ["This is a sentence", "this is another sentences."]
# laser = Laser()
# embeddings = laser.embed_sentences(sentences=test, verbose=True)
# print(embeddings)
# # print(sp.EncodeAsPieces(tes))
# # print(sp.encode_as_pieces("test"))
import logging
import sys


from laserdato import Laser


# def main():
#     laser = Laser(verbose=True)
#     laser.activateMultiGpuEncoder([0, 1])
#     lang0 = [
#         "I believe",
#         "This is a sentence",
#         "this is another sentences.",
#         "cat",
#         "This should absolutely not be matched with the next one or any other one, and I'm not sure it will be.",
#     ]
#     lang1 = [
#         "C'est une phrase",
#         "chat",
#         "C'est une autre phrase",
#         "J'y crois",
#         "zpoekdpozk",
#     ]
#     aligned_sentences = laser.align_sentences(lang0, lang1)
#     print(aligned_sentences)
#     laser.deactivateMultiGpuEncoder()


# laser.launchMultiGpuEncoder([0, 1])
# print(laser.align_sentences(lang0, lang1))

# if __name__ == "__main__":
#     main()

english_sentences = [
    "I believe",
    "This is a sentence",
    "this is another sentences.",
    "cat",
    "This should absolutely not be matched with the next one or any other one, and I'm not sure it will be.",
]

french_sentences = [
    "C'est une phrase",
    "chat",
    "C'est une autre phrase",
    "J'y crois",
    "zpoekdpozk",
]
laser = Laser()
print(
    laser.align_sentences(
        english_sentences, french_sentences, threshold_score=2, keep_bad_matched=False
    )
)
