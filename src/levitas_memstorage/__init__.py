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

import time
import logging

from memstorage import MemstorageClient

log = logging.getLogger("levitas_memstorage")


class MemstorageConnectError(Exception):
    pass


def memstorage():
    """
    Create a memstorage client.
    Example:
    
        from levitas_memstorage import memstorage, MemstorageConnectError
        try:
            client = memstorage()
        except MemstorageConnectError, err:
            log.error(err)
            log.debug("Retry connect in 5 seconds")
            time.sleep(5)
    
    """
    return MemstorageClient().getClient()

            
