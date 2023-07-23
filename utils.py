"""
This module complements *The Many Voices of Du Ying: Revisiting the Disputed Writings of Lu Xun and Zhou Zuoren*.
It contains helper function for data loading, cleaning, feature engineering, and visualization.
"""

__author__ = "hw56@indiana.edu"
__version__ = "0.1.0"
__license__ = "0BSD"


import os
import re
import matplotlib as mpl
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
        corpus_dir: path to corpus

    Returns:
        Three dictionaries keyed by 'author', 'label', 'text', 'title', and 'text_length'. The first two fields
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


def remove_artifact(document: str) -> str:
    """
    Substitute all English characters (e.g., [MASK]) within squared brackets. Those tokens are used to mask direct
    quotes.

    Args:
        document: a document found in corpus

    Return:
        text with artifacts removed
    """
    return re.sub(r"\s+", "", re.sub(r"\[([A-Za-z ]+)\]", "", document))


def remove_whitespace(document: str) -> str:
    """
    Remove all whitespaces for text length calculation.

    Args:
        document: a document found in corpus

    Return:
        text with whitespaces removed
    """
    return re.sub(r"\s+", "", re.sub(r"\[([A-Za-z ]+)\]", "", document))


def count_frequency(character_ngrams: List[str], document: str) -> List[int]:
    """
    Count frequencies of Chinese function uni/bi/tri/4-grams from a text. A subordinate gram will not be counted twice
    if it is a part of a superior gram. For example, in "这是一个例子，用来展示在数'是'和'而是'时的区别。", we count "是" twice
    (not thrice) and "而是" once.

    Args:
      character_ngrams: a function ngram list with no duplication
      document: a document whose function ngram distribution is of interest

    Return:
      Count of the corresponding ngram wrt `function_ngrams`.

    Example:
      ```python
      > count_frequency(['几', '几几乎', '几几几乎'], "几几几乎几几几乎几几几个个几几乎")
      > [3, 1, 2]
      ```
    """
    # check duplicates
    if len(set(character_ngrams)) != len(character_ngrams):
        raise RuntimeError("Remove duplicates in `function_ngrams`.")
    raw_count_dict = {g: len(re.findall(g, document)) for g in character_ngrams}

    adjusted_count_dict = {}
    max_n = max([len(gram) for gram in character_ngrams])
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
            for gram in [gram for gram in character_ngrams if len(gram) == n]:
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

    return [adjusted_count_dict.get(g) for g in character_ngrams]


def highlight_document(document: str, character_ngrams: List[str], weights: List[float], html_name: str) -> None:
    """
    highlight the given Chinese character ngrams in the document according to their weights and saves the highlighted
    document as an HTML file.

    Args:
        document: the original text document in which to highlight ngrams.
        character_ngrams: a list of character ngrams to be highlighted in the document.
        weights: a list of weights corresponding to the character ngrams. Positive weights are highlighted in plasma
            colormap and negative weights in viridis colormap. The intensity of the color depends on the absolute value
            of the weight.
        html_name: the name of the HTML file to save the highlighted document. The file will be saved in the current
            working directory.

    Returns:
        None. It saves the highlighted document in the `visualization` directory.
    """
    # supply color-blind hue
    cmap_positive = mpl.colormaps['plasma']
    cmap_negative = mpl.colormaps['viridis']

    # sort character_ngrams and weights by n in descending order
    character_ngrams, weights = zip(*sorted(zip(character_ngrams, weights), key=lambda x: -len(x[0])))
    # hash Chinese characters to prevent operations on
    # a subtoken from impacting a longer ngram that contains the subtoken
    # (e.g., the subtoken 是 and the longer ngram 于是).
    hash2ngram = {hash(ngram): ngram for ngram in character_ngrams}

    max_weight = max(max(weights), abs(min(weights)))

    for ngram, weight in zip(character_ngrams, weights):
        if ngram in document:
            if weight > 0:
                color = cmap_positive(abs(weight) / max_weight)
            elif weight < 0:
                color = cmap_negative(abs(weight) / max_weight)
            else:
                continue
            # convert the RGB color to RGBA with transparency, then to the appropriate CSS format
            color = mpl.colors.to_rgb(color)
            # alpha set to 0.5 for 50% transparency
            color = f'rgba({int(color[0] * 255)}, {int(color[1] * 255)}, {int(color[2] * 255)}, 0.5)'
            document = document.replace(ngram, f'''<mark style="background-color:{color};">{hash(ngram)}</mark>''')

    # convert newlines to HTML paragraph breaks
    document = document.replace('\n', '</p><p>')

    # add opening and closing paragraph tags
    document = f'<p>{document}</p>'

    # unhash to ngrams
    for h, g in hash2ngram.items():
        document = document.replace(str(h), g)

    html_output = f"""
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
    {document}
    </body>
    </html>
    """
    # uncomment to get a copy-paste output
    # print(html_output)
    # save the html
    if not os.path.exists('visualization'):
        os.makedirs('visualization')
    with open(f'visualization/{html_name}.html', 'w') as f:
        f.write(html_output)
