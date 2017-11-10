from setuptools import setup

setup(
    name="blobworld.py",
    version="1.0",
    author="gavin lyons",
    author_email="glyons66@hotmail.com",
    description="pygame automated animation of blobs",
    license=" GPL",
    keywords="pygame",
    url="https://github.com/gavinlyonsrepo/blobworld",
    download_url='https://github.com/gavinlyonsrepo/blobworld/archive/1.0.tar.gz',
    packages=['blobworld','blobclass',],
    install_requires= ['pip'],
    setup_requires = ['pip'],
    scripts=['blobworld/blobworld.py'],
    classifiers=[
        "Topic :: Games",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)