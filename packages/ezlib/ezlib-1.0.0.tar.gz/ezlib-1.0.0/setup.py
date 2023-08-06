import setuptools

setuptools.setup(name="ezlib",
                 author="Elia Toselli",
                 author_email="elia.toselli@outlook.it",
                 py_modules=["ezlib"],
                 entry_points={'console_scripts': ['ezip = ezlib:ezip',
                                                   'unezip = ezlib:unezip',
                                                   'ezcat = ezlib:ezcat']})