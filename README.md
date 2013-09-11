Levitas Memstorage
==================

This package provides a memstorage server and client
based on pythons multiprocessing module.


Installation
============

Basic installation
-------------------

```
cd src
python setup.py install
```

Build API documentation
-----------------------

```
cd src
epydoc -v --html --debug --no-sourcecode --graph all --output=../api levitas
```

Makefile installation
---------------------

Install on local system:

* make install

Generate a deb package:

* make deb

Generate API documentation:

* make doc

Get rid of scratch and byte files:

* make clean


Configuration
=============

Levitas settings module entries for memstorage:
```python
memstorage_address = ("127.0.0.1", 54678)
memstorage_authkey = "my_secret_key"
memstorage_objects = {"my_dict": dict,
                      "my_list": list,
                      "my_object": my_custom_class}
```

Memstorage server
=================

Linux/Unix
----------

```
Usage: levitas-memstoraged [OPTION] {start|stop|restart|foreground}

Options:
  -h, --help            show this help message and exit
  -l LOGFILE, --logfile=LOGFILE
                        Path to logfile (optional)
  -c LOGFILECOUNT, --logfilecount=LOGFILECOUNT
                        Count of old logfiles to be saved. (default: 0)
  -v, --verbose         
  -s SETTINGS_MODULE, --settings=SETTINGS_MODULE
                        settings module (required)
  -p PIDFILE, --pidfile=PIDFILE
                        pidfile
```

Example, if the settings module is a python module **my_site/settings.py**:

```
levitas-memstoraged -s my_site.settings -v foreground
```

Windows
-------

```
Usage: C:\Python27\Scripts\levitas-memstorage-service.py [OPTION] {start|stop|remove|install}

Options:
  -h, --help            show this help message and exit
  -n NAME, --name=NAME  Servicename (default: levitasMemstorage)
  -d DISPLAYNAME, --displayname=DISPLAYNAME
                        Displayname (default: Levitas Memstorage)
  -a, --stayalive       Service will stop on logout if False (default: True)
  -l LOGFILE, --logfile=LOGFILE
                        Path to logfile (optional)
  -c LOGFILECOUNT, --logfilecount=LOGFILECOUNT
                        Count of old logfiles to be saved. (default: 0)
  -v, --verbose
  -s SETTINGS_MODULE, --settings=SETTINGS_MODULE
                        settings module (required)
```

Install levitas memstorage server as a windows service and start it:
```
C:\Python27/Scripts\levitas-memstorage-service.py -s my_site.settings -l C:\levitasmemstorage.log -v install
C:\Python27/Scripts\levitas-memstorage-service.py start
```

Example
=======

Create a settings.py module:
```python
memstorage_address = ("127.0.0.1", 54678)
memstorage_authkey = "my_secret_key"
memstorage_objects = {"my_dict": dict}
```

Start the memstorage server:
```
levitas-memstoraged -s settings -v foreground
```

Now you can access the memstorage
```python
from levitas_memstorage import memstorage

# Get a proxy object of my_dict
my_dict = memstorage().my_dict()

# Write something into the dict
my_dict["some_key"] = "some_value"
```



