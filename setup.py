from setuptools import setup

setup(
    name="blob_world.py",
    version="1.1",
    author="Gavin Lyons",
    author_email="glyons66@hotmail.com",
    description="pygame automated animation of blobs",
    license="GPL",
    keywords="pygame",
    url="https://github.com/gavinlyonsrepo/blobworld",
    download_url='https://github.com/gavinlyonsrepo/blobworld/archive/1.0.tar.gz',
    packages=['blobworld', 'blobclass', 'blobwork'],
    package_dir={'blobworld': 'blobworld'},
    package_data={'blobworld': ['sounds/*.wav', 'images/*.png']},
    install_requires=['pip', 'numpy', 'pygame'],
    setup_requires=['pip'],
    scripts=['blobworld/blob_world.py'],
    classifiers=[
        "Topic :: Games",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
