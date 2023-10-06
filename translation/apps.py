import torch
from django.apps import AppConfig

from utils.utils import Translation, TranslationEn
from utils.transformer import Seq2SeqTransformer


EMB_SIZE = 512
NHEAD = 8
FFN_HID_DIM = 512
NUM_ENCODER_LAYERS = 4
NUM_DECODER_LAYERS = 4
DROP_OUT = 0.1

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
NEWARI_TRANSFORMER = "translation/torch_models/english-newari.pth"
ENGLISH_TRANSFORMER = "translation/torch_models/newari-english.pth"

ENGLISH_VOCAB = "translation/vocabs/english_vocab.pth"
NEWARI_VOCAB = "translation/vocabs/newari_vocab.pth"

ENGLISH_VOCAB_EN = "translation/vocabs/english_vocab_en.pth"
NEWARI_VOCAB_EN = "translation/vocabs/newari_vocab_en.pth"

def load_model(src_lang, tgt_lang, transformer_path):
    translation = Translation(src_lang, tgt_lang, DEVICE)
    src_vocab_size, tgt_vocab_size = translation.len_vocab()

    transformer = Seq2SeqTransformer(
        NUM_ENCODER_LAYERS,
        NUM_DECODER_LAYERS,
        EMB_SIZE,
        NHEAD,
        src_vocab_size,
        tgt_vocab_size,
        FFN_HID_DIM,
        DROP_OUT,
    )

    transformer.load_state_dict(torch.load(transformer_path, map_location=DEVICE))
    transformer = transformer.to(DEVICE)

    return transformer, translation

def load_model_en(src_lang, tgt_lang, transformer_path):
    translation = TranslationEn(src_lang, tgt_lang, DEVICE)
    src_vocab_size, tgt_vocab_size = translation.len_vocab()

    transformer = Seq2SeqTransformer(
        NUM_ENCODER_LAYERS,
        NUM_DECODER_LAYERS,
        EMB_SIZE,
        NHEAD,
        src_vocab_size,
        tgt_vocab_size,
        FFN_HID_DIM,
        DROP_OUT,
    )

    transformer.load_state_dict(torch.load(transformer_path, map_location=DEVICE))
    transformer = transformer.to(DEVICE)

    return transformer, translation


newari_transformer, newari_translator = None, None


class TranslationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "translation"

    def ready(self) -> None:
        global newari_transformer, newari_translator, english_translator, english_transformer
        newari_transformer, newari_translator = load_model(
            ENGLISH_VOCAB, NEWARI_VOCAB, NEWARI_TRANSFORMER
        )
        english_transformer, english_translator = load_model_en(
            NEWARI_VOCAB_EN, ENGLISH_VOCAB_EN, ENGLISH_TRANSFORMER
        )
