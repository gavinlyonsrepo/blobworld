from setuptools import setup

setup(
    name="blobworld",
    version="1.2.3",
    author="Gavin Lyons",
    author_email="glyons66@hotmail.com",
    description="pygame automated animation of blobs",
    license="GPL",
    keywords="pygame",
    url="https://github.com/gavinlyonsrepo/blobworld",
    download_url='https://github.com/gavinlyonsrepo/blobworld/archive/1.2.tar.gz',
    packages=['blobworld','blobclass','blobwork',],
    include_package_data = True,
    install_requires=['pip','numpy','pygame',],
    setup_requires=['pip'],
    scripts=['blobworld/blob_world.py'],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
