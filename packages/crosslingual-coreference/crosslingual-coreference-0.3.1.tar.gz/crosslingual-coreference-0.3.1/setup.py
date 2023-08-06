# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crosslingual_coreference', 'crosslingual_coreference.examples']

package_data = \
{'': ['*']}

install_requires = \
['allennlp-models>=2.9,<2.10',
 'allennlp>=2.9,<2.10',
 'cached-path==1.1.2',
 'protobuf>=3.20,<4.0',
 'scipy>=1.7,<2.0',
 'spacy>=3.1,<3.2']

entry_points = \
{'spacy_factories': ['spacy = '
                     'crosslingual_coreference.__init__:make_crosslingual_coreference']}

setup_kwargs = {
    'name': 'crosslingual-coreference',
    'version': '0.3.1',
    'description': 'A multi-lingual approach to AllenNLP CoReference Resolution, along with a wrapper for spaCy.',
    'long_description': '# Crosslingual Coreference\nCoreference is amazing but the data required for training a model is very scarce. In our case, the available training for non-English languages also proved to be poorly annotated. Crosslingual Coreference, therefore, uses the assumption a trained model with English data and cross-lingual embeddings should work for languages with similar sentence structures.\n\n[![Current Release Version](https://img.shields.io/github/release/pandora-intelligence/crosslingual-coreference.svg?style=flat-square&logo=github)](https://github.com/pandora-intelligence/crosslingual-coreference/releases)\n[![pypi Version](https://img.shields.io/pypi/v/crosslingual-coreference.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/crosslingual-coreference/)\n[![PyPi downloads](https://static.pepy.tech/personalized-badge/crosslingual-coreference?period=total&units=international_system&left_color=grey&right_color=orange&left_text=pip%20downloads)](https://pypi.org/project/crosslingual-coreference/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)\n\n# Install\n\n```\npip install crosslingual-coreference\n```\n# Quickstart\n```python\nfrom crosslingual_coreference import Predictor\n\ntext = (\n    "Do not forget about Momofuku Ando! He created instant noodles in Osaka. At"\n    " that location, Nissin was founded. Many students survived by eating these"\n    " noodles, but they don\'t even know him."\n)\n\n# choose minilm for speed/memory and info_xlm for accuracy\npredictor = Predictor(\n    language="en_core_web_sm", device=-1, model_name="minilm"\n)\n\nprint(predictor.predict(text)["resolved_text"])\nprint(predictor.pipe([text])[0]["resolved_text"])\n# Note you can also get \'cluster_heads\' and \'clusters\'\n# Output\n#\n# Do not forget about Momofuku Ando!\n# Momofuku Ando created instant noodles in Osaka.\n# At Osaka, Nissin was founded.\n# Many students survived by eating instant noodles,\n# but Many students don\'t even know Momofuku Ando.\n```\n![](https://raw.githubusercontent.com/Pandora-Intelligence/crosslingual-coreference/master/img/example_en.png)\n\n## Models\nAs of now, there are two models available "spanbert", "info_xlm", "xlm_roberta", "minilm", which scored 83, 77, 74 and 74 on OntoNotes Release 5.0 English data, respectively.\n- The "minilm" model is the best quality speed trade-off for both mult-lingual and english texts.\n- The "info_xlm" model produces the best quality for multi-lingual texts.\n- The AllenNLP "spanbert" model produces the best quality for english texts.\n\n## Chunking/batching to resolve memory OOM errors\n\n```python\nfrom crosslingual_coreference import Predictor\n\npredictor = Predictor(\n    language="en_core_web_sm",\n    device=0,\n    model_name="minilm",\n    chunk_size=2500,\n    chunk_overlap=2,\n)\n```\n\n## Use spaCy pipeline\n```python\nimport spacy\n\ntext = (\n    "Do not forget about Momofuku Ando! He created instant noodles in Osaka. At"\n    " that location, Nissin was founded. Many students survived by eating these"\n    " noodles, but they don\'t even know him."\n)\n\n\nnlp = spacy.load("en_core_web_sm")\nnlp.add_pipe(\n    "xx_coref", config={"chunk_size": 2500, "chunk_overlap": 2, "device": 0}\n)\n\ndoc = nlp(text)\nprint(doc._.coref_clusters)\n# Output\n#\n# [[[4, 5], [7, 7], [27, 27], [36, 36]],\n# [[12, 12], [15, 16]],\n# [[9, 10], [27, 28]],\n# [[22, 23], [31, 31]]]\nprint(doc._.resolved_text)\n# Output\n#\n# Do not forget about Momofuku Ando!\n# Momofuku Ando created instant noodles in Osaka.\n# At Osaka, Nissin was founded.\n# Many students survived by eating instant noodles,\n# but Many students don\'t even know Momofuku Ando.\nprint(doc._.cluster_heads)\n# Output\n#\n# {Momofuku Ando: [5, 6],\n# instant noodles: [11, 12],\n# Osaka: [14, 14],\n# Nissin: [21, 21],\n# Many students: [26, 27]}\n```\n### Visualize spacy pipeline\nThis only works with spacy >= 3.3.\n```python\nimport spacy\nfrom spacy.tokens import Span\nfrom spacy import displacy\n\ntext = (\n    "Do not forget about Momofuku Ando! He created instant noodles in Osaka. At"\n    " that location, Nissin was founded. Many students survived by eating these"\n    " noodles, but they don\'t even know him."\n)\n\nnlp = spacy.load("nl_core_news_sm")\nnlp.add_pipe("xx_coref", config={"model_name": "minilm"})\ndoc = nlp(text)\nspans = []\nfor idx, cluster in enumerate(doc._.coref_clusters):\n    for span in cluster:\n        spans.append(\n            Span(doc, span[0], span[1]+1, str(idx).upper())\n        )\n\ndoc.spans["custom"] = spans\n\ndisplacy.render(doc, style="span", options={"spans_key": "custom"})\n```\n\n## More Examples\n![](https://raw.githubusercontent.com/Pandora-Intelligence/crosslingual-coreference/master/img/example_total.png)\n',
    'author': 'David Berenstein',
    'author_email': 'david.m.berenstein@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pandora-intelligence/crosslingual-coreference',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
