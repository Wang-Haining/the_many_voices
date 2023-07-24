# The Many Voices

[![en](https://img.shields.io/badge/lang-en-green.svg)](https://codeberg.org/haining/the_many_voices/src/branch/main/README.md)
[![zh](https://img.shields.io/badge/lang-zh-green.svg)](https://codeberg.org/haining/the_many_voices/src/branch/main/README.zh.md)

This repository hosts the corpus and scripts for reproducing the findings of *The Many Voices of Du Ying: Revisiting 
the Disputed Writings of Lu Xun and Zhou Zuoren*.

## Tutorial

We provide Colab notebooks for reproducing the results.
- [Main experiment](https://colab.research.google.com/drive/1gYdugVvy_4R2IU3J1oASK5BgV3EiB9Gb?usp=sharing), including 
data loading, feature engineering, build a classifier, explaining and visualizing the
results.
- [Exploratory data analysis](https://colab.research.google.com/drive/1ryNXKcRrnvPEs61udXisuaHi2bEMbCWQ?usp=sharing), 
 including feature selection and examination of correlation of the features.

Note that, the notebooks are for pedagogical purposes. See rigorous reproduction in [Reproduction](#reproduction).

## Reproduction

```python3.10
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```


## Corpus

| Split      | Title                                                                        | Author/Pseudonym |
|------------|------------------------------------------------------------------------------|------------------|
| Train      | Lessons from the History of Science (科学史教篇)                                  | Lu xun           |
|            | On the Aberrant Development of Culture (文化偏至论)                               | Lu xun           |
|            | Preface to Midst the Wild Carpathians (《匈奴奇士录》序)                             | Zhou Zuoren      |
|            | Preface to Charcoal Drawing (《炭画》序)                                          | Zhou Zuoren      |
|            | Preface to The Lost History of Red Star (《红星佚史》序)                            | Zhou Zuoren      |
|            | Preface to The Yellow Rose (《黄蔷薇》序)                                          | Zhou Zuoren      |
|            | A Brief Discussion on Fairy Tales (童话略论)                                     | Zhou Zuoren      |
|            | A Study on Fairy Tales (童话研究)                                                | Zhou Zuoren      |
| Validation | On Radium (说镭)                                                               | Lu xun           |
|            | On the Power of Mara Poetry (摩罗诗力说)                                          | Lu xun           |
|            | Preface to Qiucao Garden Diary (《秋草园日记》序)                                    | Zhou Zuoren      |
|            | An Addendum to Yisi Diary (乙巳日记附记一则)                                         | Zhou Zuoren      |
|            | A Glimpse of Jiangnan Examinees (江南考先生之一斑)                                   | Zhou Zuoren      |
|            | Plight and Broil in a Steamboat (汽船之窘况及苦热)                                   | Zhou Zuoren      |
| Test       | Looking at the Land of Yue (望越篇)                                             | Du Ying          |
|            | Looking at the Country of China (望华国篇)                                       | Du Ying          |
|            | People of Yue, Forget Not Your Ancestors' Instructions (尔越人毋忘先民之训)           | Du               |
|            | Where Has the Character of the Republic Gone? (民国之征何在)                       | Du               |


## License

The corpus is designated to the public domain. All other materials are licensed under 0BSD.

[//]: # (## Citation)

[//]: # (TODO)

[//]: # ()
[//]: # (## Demo)

[//]: # (TODO)

## Contact
- [rwxiexin@shnu.edu.cn](mailto:rwxiexin@shnu.edu.cn) for general questions. 
- [hw56@indiana.edu](mailto:hw56@indiana.edu) for reproduction.

## Acknowledgements

The project is supported by the National Social Science Foundation of China (22CTQ041).