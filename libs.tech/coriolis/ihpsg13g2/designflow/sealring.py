
import os
import subprocess
from   pathlib                     import Path
from   doit.exceptions             import TaskFailed
from   coriolis.designflow.task    import FlowTask, ShellEnv
from   coriolis.designflow.klayout import Klayout


class BadSealRingScript ( Exception ): pass


class SealRing ( Klayout ):

    _script = None

    @staticmethod
    def setScript ( script ):
        if   isinstance(script,Path): pass
        elif isinstance(script,str):  script = Path( script )
        else:
            raise BadSealRingScript( '[ERROR] SealRing.setScript(): Should be <str> or <Path> ({})' \
                                   .format( script ))
        if not script.is_file():
            raise BadSealRingScript( '[ERROR] SealRing.setScript(): File not found "{}"' \
                                   .format( script ))
        SealRing._script = script

    @staticmethod
    def mkRule ( rule, targets, size, flags=0 ):
        return SealRing( rule, targets, size, flags )

    def __init__ ( self, rule, targets, size, flags ):
        from coriolis.helpers.io import ErrorMessage

        arguments = [ '-n', 'sg13g2', '-zz' ]
        targets   = FlowTask._normFileList( targets )
        depends   = []
        if not SealRing._script:
            raise ErrorMessage( 1, 'SealRing.doTask(): No script defined.' )
        variables = { 'output' : targets[0]
                    , 'width'  : str(size[0])
                    , 'height' : str(size[1])
                    }
        super().__init__( rule, targets, depends, SealRing._script, arguments, variables, flags )
