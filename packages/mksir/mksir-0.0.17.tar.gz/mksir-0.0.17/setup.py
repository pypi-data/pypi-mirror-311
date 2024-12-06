from setuptools import setup, find_packages

VERSION = '0.0.17'
DESCRIPTION = 'Data-mining tutorials'
LONG_DESCRIPTION = 'A package to help students'

# Setting up
setup(
    name="mksir",
    version=VERSION,
    author="Developer cheetah",
    author_email="",  # Replace with your email
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,  # Include package data specified in MANIFEST.in
    install_requires=[],
    keywords=['datamining', 'tutorial', 'mksir'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)