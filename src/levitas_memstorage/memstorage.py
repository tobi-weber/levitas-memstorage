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
import logging
from threading import Thread
from time import sleep
from multiprocessing.managers import BaseManager
from levitas.lib.singleton import ProcessBork
from levitas.lib.settings import Settings

log = logging.getLogger("levitas_memstorage.memstorage")


class MemstorageClient(ProcessBork):
    """
    Memstorage client.
    
    
    Example settings
    ================
        memstorage_address = ("127.0.0.1", 54678)
        memstorage_authkey = "my_secret_key"
        memstorage_objects = {"my_dict": dict,
                              "my_list": list,
                              "my_object": my_custom_class}
    """
    
    def __init__(self):
        self.manager = None
        self.connected = False
    
    @classmethod
    def getClient(cls):
        client = cls.getInstance()
        if not client.isConnected():
            client.connect()
        return client
    
    def create(self):
        settings = Settings()
        settings.require("memstorage_address",
                         "memstorage_address = (\"127.0.0.1\", 54678)")
        settings.require("memstorage_authkey",
                         "memstorage_authkey = \"my_secret_key\"")
        settings.require("memstorage_objects",
                         "memstorage_objects = "
                         "{\"my_dict\": dict, "
                         "\"my_list\": list, "
                         "\"my_object\": my_custom_class}")
        address = settings.memstorage_address
        authkey = settings.memstorage_authkey
        objs = settings.memstorage_objects
        
        class MemstorageManager(BaseManager):
            pass
        
        for name in objs.iterkeys():
            log.info("Register object %s" % name)
            MemstorageManager.register(name)
        self.manager = MemstorageManager(address=address,
                                         authkey=authkey)
        # Make references of the manager-objects to this object
        for name in objs.iterkeys():
            setattr(self, name, getattr(self.manager, name))
        
    def connect(self):
        if self.manager is None:
            self.create()
        if not self.connected:
            t = Thread(name="MemstorageClient connect",
                       target=self.manager.connect,
                       args=())
            t.setDaemon(True)
            t.start()
            i = 0
            while t.isAlive() and i <= 1000:
                sleep(0.001)
                i += 1
            if i < 1000:
                self.connected = True
                log.info("MemstorageClient (%d ) created" % os.getpid())
            else:
                from levitas_memstorage import MemstorageConnectError
                raise MemstorageConnectError("Cannot connect to memstoraged. "
                                             "Is memstoraged running?")
        
    def isConnected(self):
        return self.connected
