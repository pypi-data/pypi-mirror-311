from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Sending API request via internet'
LONG_DESCRIPTION = 'A package that allows to build api request, add body, header and authorization and send the request'


setup(
    name="konnekt",
    version=VERSION,
    author="Alok Solanky",
    author_email="pbadgly@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'send', 'request', 'get put post delete', 'internet', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

