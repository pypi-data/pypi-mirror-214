from setuptools import setup, find_packages


VERSION = '0.0.3'
DESCRIPTION = 'basic test2'
LONG_DESCRIPTION = 'second dev test'

# Setting up
setup(
    name="theamazingtestfirstofitskind",
    version=VERSION,
    author="lotan hakli shel ashkelon",
    author_email="<lotanagar@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python',  'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
    ]
)