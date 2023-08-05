from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = "girlfriendpy",
    version = "0.3",
    py_modules = ["gf"],
    install_requires = [],
    description = "i think i have a gf i dont entirely know how a gf is defined but i think she is so i made this library to help me",
    long_description=long_description,
    long_description_content_type='text/markdown',
)