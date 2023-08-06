from setuptools import setup

setup(
    name='frosty-dag',
    version='0.0.1',
    description='Implementation of the FROSTY algorithm',
    author='Joshua Bang',
    author_email='joshuaybang@gmail.com',
    url='https://github.com/joshuaybang/frosty-dag',
    keywords='bayesian network structure learning',
    packages=['frosty'],
    python_requires='>=3.6, <3.10',
    install_requires=['numpy', 'scipy', 'Cython',
                      'skggm', 'scikit-sparse', 'robust-selection', 'networkx'],
)