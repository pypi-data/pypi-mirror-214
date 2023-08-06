from setuptools import setup, find_packages

VERSION = "0.0.2"
DESCRIPTION = "A python FIX library that supports ARM Macs"
LONG_DESCRIPTION = "A python FIX library that supports ARM Macs"

# Setting up
setup(
    name="quickfix-ch",
    version=VERSION,
    author="Coinhako (Javier)",
    author_email="<javier.phon@coinhako.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION  ,
    packages=find_packages(),
    package_data={
        "": ["_quickfix.*"]
    },
    include_package_data=True,
    install_requires=[],
    keywords=["python", "FIX", "finance"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)