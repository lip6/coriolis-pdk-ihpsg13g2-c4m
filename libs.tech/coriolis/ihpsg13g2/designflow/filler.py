
import os
import subprocess
from   pathlib                     import Path
from   doit.exceptions             import TaskFailed
from   coriolis.designflow.task    import FlowTask, ShellEnv
from   coriolis.designflow.klayout import Klayout


class BadFillerScript ( Exception ): pass


class Filler ( Klayout ):

    NoActiv = 0x0010
    NoMetal = 0x0020

    _script = None

    @staticmethod
    def setScript ( script ):
        if   isinstance(script,Path): pass
        elif isinstance(script,str):  script = Path( script )
        else:
            raise BadFillerScript( '[ERROR] Filler.setScript(): Should be <str> or <Path> ({})' \
                                   .format( script ))
        if not rules.is_file():
            raise BadFillerScript( '[ERROR] Filler.setScript(): File not found "{}"' \
                                   .format( script ))
        Filler._script = rules

    @staticmethod
    def mkRule ( rule, targets, depends, flags=0 ):
        return Filler( rule, targets, depends, flags )

    def __init__ ( self, rule, targets, depends, flags ):
        from coriolis.helpers.io import ErrorMessage

        arguments = [ '-n', 'sg13g2', '-zz' ]
        targets   = FlowTask._normFileList( targets )
        depends   = FlowTask._normFileList( depends )
        if not Filler._script:
            raise ErrorMessage( 1, 'Filler.doTask(): No script defined.' )
        variables = { 'output_file' : targets[0] }
        if flags & Filler.NoActiv: variables[ 'no_activ' ] = None
        if flags & Filler.NoMetal: variables[ 'no_metal' ] = None
        super().__init__( rule, targets, depends, Filler._script, arguments, variables, flags )
