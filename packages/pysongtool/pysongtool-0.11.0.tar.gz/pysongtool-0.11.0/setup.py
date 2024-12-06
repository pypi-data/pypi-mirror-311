from setuptools import setup, find_packages

setup(
    name="pysongtool",
    version="0.11.0",
    author="Murilo R.B Silva",
    description="A Python library that gives musical theory contend.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MuriloRyan/pysongtool",  # Substitua com o link do seu repositório
    packages=find_packages(),
    install_requires=[
        "iniconfig==2.0.0",
        "packaging==24.2",
        "pluggy==1.5.0",
        "pytest==8.3.3",
        "setuptools==75.6.0"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
    ],
    keywords="music theory scales chords intervals",
    license="MIT"
)
