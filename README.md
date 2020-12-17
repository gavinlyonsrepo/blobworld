Overview
--------------------------------------------
* Name: blobworld
* Program: python 3.6.3
* Title : This python program will display a pygame based automated blob animation.
* Description: This python program will display a pygame automated blob simulation.
where blobs of various colours move and consume others in a "blobworld".
* Author: G. Lyons
* Source: https://github.com/gavinlyonsrepo/blobworld

Rules
--------------
Starts with default 15 blobs for each of 3 colours, red green and blue

1=absorbs on contact 0=no absorb on contact

| xxx   | red | green | blue |
| ---   | --- | ----  | ---- |
| red   | 1   | 1     | 0    |
| green | 0   | 1     | 1    |
| blue  | 1   | 0     | 1    |

Press p to pause , q to quit

Installation
---------------------

Install from Python package index (pypi)

```sh
pip3 install blobworld
```

A PKGBUILD is available for arch-based linux users. Program is not 
yet in AUR.

Usage
----------------

type in terminal

```sh
blob_world.py
```

Files and setup
-------------------------
blobworld files needed are listed below:

| File Path | Description |
| ------ | ------ |
| blob_world.py | The main python script |
| blob_work.py| python module containing work functions |
| blob_class.py | python module dealing with class for controlling the blob |
| $HOME/.config/blobworld/blobworld.cfg | config file, user made, NOT installed |
| /tmp/bloblogfile.txt | log file |

Config file: The user can create a config file at path in table above.
The config file is NOT installed by setup.py. 
A dummy config file is available in documentation folder at repository

There are three settings. 
Each setting represents starting number of blobs for each colour.
The 3 integer values can be set to zero but sum of values must be between 
1 and 150 


Make sure to include the [MAIN] header and all settings just as below or from the dummy file.

Settings:

>
>[MAIN]
>
>STARTING_BLUE_BLOBS=18
>
>STARTING_RED_BLOBS=20
>
>STARTING_GREEN_BLOBS=23
>


Logging
-----------------
A log file for errors, critical failures and warnings is at 

```sh
/tmp/bloblogfile.log
```

Dependencies
-----------------
Some functions require dependencies packages to be installed.

| Dependencies| Usage |
| ------ | ------ |
| numpy |  calculate if blobs are in collision |
| pygame| python game package |

