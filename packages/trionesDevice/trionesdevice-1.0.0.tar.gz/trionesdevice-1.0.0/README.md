# trionesDevice

The module inspired by [trionesControl](https://github.com/Aritzherrero4/python-trionesControl) module from [Aritz Herrero](https://github.com/Aritzherrero4). 
It provides API to control LED devices using [triones protocol](https://github.com/madhead/saberlight/blob/master/protocols/Triones/protocol.md).
The motivation to build this module was to make it cross-platform using BLEAK module instead of pygatt.

## Requirments
Using BLEAK client this module is supposed to support every platform that BLEAK supports:
+ Windows 10, version 16299 (Fall Creators Update) or greater
+ Linux distributions with BlueZ >= 5.43
+ OS X/macOS support via Core Bluetooth API, from at least OS X version 10.11

## Installation
Install `trionesControl` with pip from PyPI:
```
pip install trionesControl
```
Or clone this repository and use `build` module to generate wheel:
```
python -m build
```


## Licence
MIT Licence - Copyright 2023 Bukreev Dmitriy

For more information, check [LICENCE](https://github.com/DmitriyBukreev/trionesDevice/blob/main/LICENSE) file.