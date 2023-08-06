# LE core package

This is package of core python utils for LE containing:
- Looger
- Proprietary LeBin protocol
- Proprietary Modbus RTU register map handling - VisualModbus
- Test frame 

## Install

Install or update version
```
pip install lecore
pip install --upgrade lecore
```

## Import

Import package as usual

```python
import lecore
```


# Looger

Class Looger allows for sending debug data into Development Debug Server (DDS) a.k.a. 
Looger. Public instance run on https://looger.jablotron.cz

Create instance when default public endpoint is to be used 

```python
import lecore
looger = lecore.Looger()
```

Set device

```python
looger.set_device(0x111CC1234, 0, None)
```

Send data and log

```python
data = {'data_1': 1, 'data_2': 2}
log = f"Message to log"
looger.send(data, log, 0)
```





