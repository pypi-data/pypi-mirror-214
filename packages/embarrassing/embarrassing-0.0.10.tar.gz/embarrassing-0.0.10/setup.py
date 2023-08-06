from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="embarrassing",
    version="0.0.10",
    description="A package to embarrassingly parallelize your code",
    author="Raphaël Côté",
    author_email="cotlarrc@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    # url="<package-url>",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "tqdm",
        "joblib"
    ],
)
