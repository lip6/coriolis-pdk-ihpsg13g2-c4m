
import os
import subprocess
from   pathlib                     import Path
from   doit.exceptions             import TaskFailed
from   coriolis.designflow.task    import FlowTask, ShellEnv
from   coriolis.designflow.klayout import Klayout


class BadSealRingScript ( Exception ): pass
class BadDrcRules       ( Exception ): pass
class BadDrcRulesFlags  ( Exception ): pass


class DRC ( Klayout ):

    Minimal = 0x0001
    Maximal = 0x0002
    C4M     = 0x0004

    _drcRulesC4M     = None
    _drcRulesMinimal = None
    _drcRulesMaximal = None

    @staticmethod
    def setDrcRules ( rules, flags ):
        if   isinstance(rules,Path): pass
        elif isinstance(rules,str):  rules = Path( rules )
        else:
            raise BadDrcRules( '[ERROR] DRC.setDrcRules(): Should be <str> or <Path> ({})' \
                               .format( rules ))
        if not rules.is_file():
            raise BadDrcRules( '[ERROR] DRC.setDrcRules(): File not found "{}"' \
                               .format( rules ))

        if   flags & DRC.Minimal: DRC._drcRulesMinimal = rules
        elif flags & DRC.Maximal: DRC._drcRulesMaximal = rules
        elif flags & DRC.C4M:     DRC._drcRulesC4M     = rules
        else:
            raise BadDrcRules( '[ERROR] DRC.setDrcRules(): Invalid flags value {}' \
                               .format( flags ))

    @staticmethod
    def mkRule ( rule, depends=[], flags=0 ):
        return DRC( rule, depends, flags )

    def __init__ ( self, rule, depends, flags ):
        from coriolis.helpers.io import ErrorMessage

        if flags & DRC.Minimal:
            rules = DRC._drcRulesMinimal
            tag   = 'minimal'
        elif flags & DRC.Maximal:
            rules = DRC._drcRulesMaximal
            tag   = 'maximal'
        elif flags & DRC.C4M:
            rules = DRC._drcRulesC4M
            tag   = 'c4m'

        env       = {}
        variables = {}
        arguments = [ '-zz' ]
        depends   = FlowTask._normFileList( depends )
        targets   = [ depends[0].with_suffix('.kdrc-report-{}.txt'.format(tag)) ]
        if not rules:
            raise ErrorMessage( 1, 'DRC.doTask(): No DRC rules defined for "{}".'.format( tag ))
        if flags & (DRC.Minimal | DRC.Maximal):
            variables = { 'in_gds'      : depends[0]
                        , 'input'       : depends[0]
                        , 'report'      : targets[0]
                        , 'report_file' : targets[0]
                        }
        elif flags & DRC.C4M:
            env = { 'SOURCE_FILE' : depends[0].as_posix()
                  , 'CELL_NAME'   : depends[0].stem
                  , 'REPORT_FILE' : targets[0].as_posix()
                  }
        super().__init__( rule, targets, depends, rules, arguments, variables, env, flags )
