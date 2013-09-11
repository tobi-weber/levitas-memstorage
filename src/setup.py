# -*- coding: utf-8 -*-
#   Copyright (C) 2010-2013 Tobias Weber <tobi-weber@gmx.de>

import platform
from distutils.core import setup


if platform.system() == "Windows":
    scripts = ["levitas-memstorage-service.py"]
else:
    scripts = ["levitas-memstoraged"]
    
    
setup(
    name = "levitas_memstorage",
    version = "0.0.1",
    description = "Levitas memstorage server and client",
    author = "Tobias Weber",
    author_email = "tobi-weber@gmx.de",
    url = "",
    packages = ["levitas_memstorage"],
    scripts = scripts,
    long_description = """ Levitas memstorage server and client """
)
