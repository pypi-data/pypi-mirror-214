# lxml_to_dict
conversor lxml a dict

<!-- [![PyPI version](https://badge.fury.io/py/nazk.svg)](https://pypi.org/project/nazk/) -->

## Descripción
* Esta es una actualizacion al paquete oficial de `Criva` [https://github.com/CRiva/lxml_to_dict] para uso con python 3.9

## Instalación
```
pip install lxml-to-dict-total
```

## Uso básico
```python
from lxml_to_dict import lxml_to_dict
 
lxml_to_dict(<the lxml.objectfy.Element>)

root = objectify.Element("root")            # <root></root>
b = objectify.SubElement(root, "b")         # <root><b></b></root>
b = objectify.SubElement(root, "b")         # <root><b></b><b></b></root>
a = objectify.SubElement(root, "a")         # <root><b></b><b></b><a></a></root>
lxml_to_dict(root)                          # {'root': {'b': None, 'b1': None, 'a': None}}
```