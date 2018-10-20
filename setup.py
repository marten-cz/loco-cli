from setuptools import setup

setup(
    name="loco-cli",
    version="0.2.5rc1",
    author='Martin Malek',
    author_email='martin.malek@pagewiser.com',
    url='https://pypi.python.org/pypi/loco-cli/',
    download_url='https://github.com/marten-cz/loco-cli',
    packages=['localise'],
    description='Command line utiltiy for Localise.biz.',
    install_requires=[
        "requests>=2.10.0,<3.0",
        "colorama>=0.2.5,<=0.3.3",
        "pyyaml>=3.11,<4.0",
        "six>=1.11.0,<2.0"
    ],
    entry_points={
        'console_scripts': [
            'loco-cli = localise.localise:main',
        ]
    },
    license="MIT",
    platforms="any",
    classifiers=["Development Status :: 3 - Alpha",
                 "Environment :: Console",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: OS Independent",
                 "Topic :: Software Development :: Localization",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3"
                 ]
)
