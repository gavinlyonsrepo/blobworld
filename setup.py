from distutils.core import setup

setup(
    name="blobworld",
    version="1.1.2",
    author="Gavin Lyons",
    author_email="glyons66@hotmail.com",
    description="pygame automated animation of blobs",
    license="GPL",
    keywords="pygame",
    url="https://github.com/gavinlyonsrepo/blobworld",
    download_url='https://github.com/gavinlyonsrepo/blobworld/archive/1.1.tar.gz',
    packages=['blobworld','blobclass','blobwork',],
    #package_dir={'blobworld': 'blobworld'}
    data_files=[('/usr/share/sounds/blobworld', ['blobworld/sounds/kill.wav', 'blobworld/sounds/start.wav', 'blobworld/sounds/pause.wav' , 'blobworld/sounds/end.wav']),
                 ('/usr/share/pixmaps/', ['blobworld/images/blobicon.png'])],
    install_requires=['pip','numpy','pygame',],
    setup_requires=['pip'],
    scripts=['blobworld/blob_world.py'],
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
