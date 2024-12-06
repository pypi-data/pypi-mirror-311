######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.32                                                                                #
# Generated on 2024-11-26T19:51:56.476506                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.event_logger


class DebugEventLogger(metaflow.event_logger.NullEventLogger, metaclass=type):
    @classmethod
    def get_worker(cls):
        ...
    ...

class DebugEventLoggerSidecar(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    ...

