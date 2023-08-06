from embetter.finetune import ForwardFinetuner
from sklearn.feature_extraction.text import CountVectorizer


texts = ["i am positive", "i am negative", "this is neutral"]
labels = ["pos", "neg", "neu"]


def test_forward_finetuner_can_handle_string_classes():
    """https://github.com/koaning/embetter/issues/38"""
    cv = CountVectorizer()
    X_tfm = cv.fit(texts).transform(texts)
    fft = ForwardFinetuner()
    fft.fit(X_tfm.todense(), labels)
