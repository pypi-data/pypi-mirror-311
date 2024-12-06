######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.32.1+obcheckpoint(0.1.4);ob(v1)                                                   #
# Generated on 2024-11-26T19:30:33.225816                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

