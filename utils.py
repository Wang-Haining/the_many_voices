import os
import re
from typing import Dict, List, Tuple, Union


def load_corpus(
    corpus_dir: str = "corpus",
) -> Tuple[
    List[Dict[str, Union[Union[int, str]]]],
    List[Dict[str, Union[Union[int, str]]]],
    List[Dict[str, Union[str]]],
]:
    """
    Load data of train, val, and test splits.

    Args:
        corpus_dir: str, path to corpus

    Return:
        tuple, three dictionaries keyed by 'author', 'label', 'text', 'title', and 'text_length'. The first two fields
        were left blank for the test split.

    """

    train, val, test = [], [], []

    for f in os.scandir(corpus_dir):
        if f.path.endswith("txt"):
            if f.name.startswith("train"):
                train.append(
                    {
                        "author": "lx" if "lx" in f.name else "zzr",
                        "label": 1 if "lx" in f.name else 0,
                        "text": open(f, "r").read(),
                        "title": f.name.split("train_lx_")[1][:-4]
                        if "lx" in f.name
                        else f.name.split("train_zzr_")[1][:-4],
                    }
                )
            elif f.name.startswith("val"):
                val.append(
                    {
                        "author": "lx" if "lx" in f.name else "zzr",
                        "label": 1 if "lx" in f.name else 0,
                        "text": open(f, "r").read(),
                        "title": f.name.split("val_lx_")[1][:-4]
                        if "lx" in f.name
                        else f.name.split("val_zzr_")[1][:-4],
                    }
                )
            elif f.name.startswith("test"):
                test.append(
                    {
                        "author": "",
                        "label": "",
                        "text": open(f, "r").read(),
                        "title": f.name[5:][:-4],
                    }
                )
    for s in [train, val, test]:
        for d in s:
            d["text_length"] = len(remove_whitespace(remove_artifact(d["text"])))

    return train, val, test


def remove_artifact(text: str) -> str:
    """
    Substitutes all English characters (e.g., [MASK]) within squared brackets. Those tokens are used to mask direct
    quotes.

    Args:
        text: str, a document found in corpus

    Return:
        text with artifacts removed
    """
    return re.sub(r"\s+", "", re.sub(r"\[([A-Za-z ]+)\]", "", text))


def remove_whitespace(text: str) -> str:
    """
    Remove all whitespaces for text length calculation.

    Args:
        text: str, a document found in corpus

    Return:
        text with whitespaces removed
    """
    return re.sub(r"\s+", "", re.sub(r"\[([A-Za-z ]+)\]", "", text))
