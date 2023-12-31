from setuptools import setup, find_packages

setup(
    name='erc5564py',
    version='0.1.0',
    author='Alexander Klein',
    author_email='alexanderjamesklein@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mewmix/erc5564py',
    packages=find_packages(),
    install_requires=[
        'ecdsa',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)

