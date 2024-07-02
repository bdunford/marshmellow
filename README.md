# Marshmello
A utility for creating __golang__ structs from json for the purpose of marshalling/unmarshalling. Ideal for consuming API with golang.



### Install
```
pip install git+https://github.com/bdunford/marshmellow
```


### Usage

```
user@host:~/$marshmellow -h
usage: marshmellow [-h] [-n NAME] filename

Takes a json file and outputs golang structs for json Marshalling and Unmarshalling.

positional arguments:
  filename    json input file

optional arguments:
  -h, --help  show this help message and exit
  -n NAME     Name of the outer most go struct

Example: marshmellow ./results.json -n Results
```
