import setuptools

setuptools.setup(name="rpsbot",
                 author="Elia Toselli",
                 author_email="elia.toselli@outlook.it",
                 py_modules=["rpsbot"],
                 entry_points={'console_scripts': ['rpsbot = rpsbot:main']})