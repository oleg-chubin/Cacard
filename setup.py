from setuptools import setup, find_packages

setup(
    name="Cacard",
    version="0.1-dev",
    url='http://businessnetworks.com.ua',
    license='Proprietary',
    description="django calling card",
    author='Obolenskiy',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'': ['*/*.conf']},
    install_requires=[
            'setuptools',
    ],
)
