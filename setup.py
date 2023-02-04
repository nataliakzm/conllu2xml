from setuptools import setup, find_packages

setup(
    name='conllu2xml',
    version='0.1',
    description='Converts, clean and parse CoNLL-U files to XML and/or TRF files',
    url='#',
    author='Natalia Kuzminykh',
    author_email='	contact@nataliakzm.codes',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'conllu2xml',
        'conlluparse',
        'argparse',
        'codecs',
        'os',
        're',
        'stanza'
    ],
    zip_safe=False
)
