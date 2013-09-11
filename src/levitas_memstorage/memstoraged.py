# -*- coding: utf-8 -*-
# Copyright (C) 2010-2013 Tobias Weber <tobi-weber@gmx.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from multiprocessing.managers import BaseManager

from levitas.lib.settings import Settings
from levitas.lib import utils
from levitas.lib.daemonize import AbstractDaemon

import logging
log = logging.getLogger("levitas_memstorage.memstorage")


class MemStoraged(AbstractDaemon):
    """
    Memstorage server.
    
    
    Example settings
    ================
        memstorage_address = ("127.0.0.1", 54678)
        memstorage_authkey = "my_secret_key"
        memstorage_objects = {"my_dict": dict,
                              "my_list": list,
                              "my_object": my_custom_class}
    """
    
    def __init__(self):
        settings = Settings()
        settings.require("memstorage_address",
            "memstorage_address = (\"127.0.0.1\", 54678)")
        settings.require("memstorage_authkey",
            "memstorage_authkey = \"my_secret_key\"")
        settings.require("memstorage_objects",
            "memstorage_objects = {\"my_dict\": dict,"
                                   "\"my_list\": list,"
                                   "\"my_object\": my_custom_class}")
        self.address = settings.memstorage_address
        self.authkey = settings.memstorage_authkey
        self.objs = settings.memstorage_objects
                
    def start(self):
        try:
            class MemstorageManager(BaseManager):
                pass
            
            for name, klass in self.objs.iteritems():
                log.info("Register object %s - %s" % (name, klass.__name__))
                obj = klass()
                if isinstance(obj, dict):
                    exposed = ( "__contains__", "__delitem__", "__getitem__",
                                "__len__", "__setitem__", "clear", "copy",
                                "get", "has_key", "items", "keys", "pop",
                                "popitem", "setdefault", "update", "values"
                               )
                elif isinstance(obj, list):
                    exposed = ("__add__", "__contains__", "__delitem__",
                               "__delslice__", "__getitem__", "__getslice__",
                               "__len__", "__mul__", "__reversed__", "__rmul__",
                               "__setitem__", "__setslice__", "append", "count",
                               "extend", "index", "insert", "pop", "remove",
                               "reverse", "sort", "__imul__"
                               )
                else:
                    exposed = None
                MemstorageManager.register(name,
                                        callable=lambda: obj,
                                        exposed=exposed)
        except:
            utils.logTraceback()
        try:
            log.info("MemstorageManager (%d) listening on %s" % (os.getpid(),
                                                                 str(self.address)))
            manager = MemstorageManager(address=self.address,
                                     authkey=self.authkey)
            server = manager.get_server()
            server.serve_forever()
        finally:
            log.info("MemstorageManager (%d) stopped" % os.getpid())
            #os._exit(0)

    def stop(self):
        os._exit(0)
    