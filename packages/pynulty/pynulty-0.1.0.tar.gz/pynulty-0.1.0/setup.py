from setuptools import setup, find_packages

setup(
    name="pynulty",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'pytest',
        'setuptools',
    ],
    author="lampadaire",
    author_email="ilovelampadaire@gmail.com",
    description="A version-checker. (Also has some easter eggs.)",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://codeberg.org/Ilovelampadaire/nulty",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
)