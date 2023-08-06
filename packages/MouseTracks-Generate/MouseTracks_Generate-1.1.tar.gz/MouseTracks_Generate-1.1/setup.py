import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='MouseTracks_Generate',
    version='1.1',
    author='momo',
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'keras',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

