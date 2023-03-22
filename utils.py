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


def count_frequency(function_ngrams: List[str], text: str) -> List[int]:
    """
    Count frequencies of Chinese function uni/bi/tri/4-grams from a text. A subordinate gram will not be counted twice
    if it is a part of a superior gram. For example, in "这是一个例子，用来展示在数'是'和'而是'时的区别。", we count "是" twice
    (not thrice) and "而是" once.

    Args:
      function_ngrams: list of str, a function ngram list with no duplication
      text: str, a document whose function ngram distribution is of interest

    Return:
      list of int, count of the corresponding ngram wrt `function_ngrams`.

    Example:
      ```python
      > count_frequency(['几', '几几乎', '几几几乎'], "几几几乎几几几乎几几几个个几几乎")
      > [3, 1, 2]
      ```
    """
    # check duplicates
    if len(set(function_ngrams)) != len(function_ngrams):
        raise "Remove duplicates in `function_ngrams`."
    raw_count_dict = {g: len(re.findall(g, text)) for g in function_ngrams}

    adjusted_count_dict = {}
    max_n = max([len(gram) for gram in function_ngrams])
    for n in range(1, max_n + 1)[::-1]:  # tri/bi/uni/4-grams
        if n == max_n:
            adjusted_count_dict.update(
                {
                    gram: count
                    for gram, count in raw_count_dict.items()
                    if len(gram) == n
                }
            )
        else:
            longer_than_n_adjusted_count_dict_tmp = {
                gram: count
                for gram, count in adjusted_count_dict.items()
                if len(gram) > n
            }
            for gram in [gram for gram in function_ngrams if len(gram) == n]:
                deduct_count = 0
                for longer_gram in longer_than_n_adjusted_count_dict_tmp.keys():
                    if gram in longer_gram:
                        multiplier = len(re.findall(gram, longer_gram))
                        deduct_count += (
                            longer_than_n_adjusted_count_dict_tmp.get(longer_gram)
                            * multiplier
                        )
                adjusted_count_dict.update(
                    {gram: raw_count_dict.get(gram) - deduct_count}
                )

    return [adjusted_count_dict.get(g) for g in function_ngrams]
