# Python Script for controlling IKEA - Tradfri lights


## Requirements
Recommended python version: 3.6.x - 3.7.x, 3.5.3 also supported, but will be deprecated.

## Install dependencies
```shell
$ sudo apt install build-essential autoconf 
```

## Setup
```shell
$ python3 setup.py install
```

The script needs the gateway IP and key, this can be set with the config option. This is only needed on first use, run the command from the directory the script is located, and the ini-file will be created:

```shell
./tradfri.py config IP KEY
```


## Usage
```shell
./tradfri.py --help
```

### List all devices
```shell
./tradfri list
```

### Controll a light
```shell
./tradfri on <ID>
./tradfri off <ID>
./tradfri level <ID> <LEVEL> (Level: 0-254)
./tradfri wb <ID> <WHITEBALANCE> (Whitebalance: cold/normal/warm)
```