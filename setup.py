import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="conllu2xml",
    version="1.0.0",
    author="Natalia Kuzminykh",
    author_email="contact@nataliakzm.codes",
    description="Converts, clean and parse CoNLL-U files to XML and/or TRF files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nataliakzm/conllu2xml",
    package_dir={
        "conllu2xml": "conllu2xml",
        "conllu2xml.conlluparse": "conllu2xml/conlluparse",
        "conllu2xml.conlluconvert": "conllu2xml/conlluconvert",
        "conllu2xml.ner": "conllu2xml/ner",
    },
    packages=[
        "conllu2xml",
        "conllu2xml.conlluparse",
        "conllu2xml.conlluconvert",
        "conllu2xml.ner",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "argparse",
        "regex",
        "stanza",
        "nltk",
    ],
    python_requires=">=3.8.10",
    zip_safe=False,
)
