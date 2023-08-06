from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='frosty-dag',
    version='0.0.2',
    description='Implementation of the FROSTY algorithm',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Joshua Bang',
    author_email='joshuaybang@gmail.com',
    url='https://github.com/joshuaybang/frosty-dag',
    keywords='bayesian network structure learning',
    packages=['frosty'],
    python_requires='>=3.6, <3.10',
    install_requires=['numpy', 'scipy', 'Cython',
                      'skggm', 'scikit-sparse', 'robust-selection', 'networkx'],
)