from setuptools import setup, find_packages

setup(
    name='conllu2xml',
    version='1.0',
    description='Converts, clean and parse CoNLL-U files to XML and/or TRF files',
    author='Natalia Kuzminykh',
    author_email='	contact@nataliakzm.codes',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'argparse',
        'codecs',
        'os',
        're',
        'stanza'
    ]
)
