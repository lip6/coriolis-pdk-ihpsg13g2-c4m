
import os
import sys
import subprocess
from   pathlib                     import Path
from   doit.exceptions             import TaskFailed
from   coriolis.designflow.task    import FlowTask, ShellEnv
from   coriolis.designflow.klayout import Klayout, ShowDRC


class BadDRCScript ( Exception ): pass


class DRC ( FlowTask ):

    FlatMode      = 0x00010000
    DeepMode      = 0x00020000
    PreCheckDRC   = 0x00040000
    NoFeol        = 0x00080000
    NoBeol        = 0x00100000
    NoDensity     = 0x00200000
    NoExtraRules  = 0x00400000
    NoOffgrid     = 0x00800000
    NoRecommended = 0x01000000
    DensityOnly   = 0x02000000
    Antenna       = 0x04000000
    AntennaOnly   = 0x08000000

    _script = None

    @staticmethod
    def setScript ( script ):
        if   isinstance(script,Path): pass
        elif isinstance(script,str):  script = Path( script )
        else:
            raise BadDRCScript( '[ERROR] DRC.setScript(): Should be <str> or <Path> ({})' \
                                   .format( script ))
        if not script.is_file():
            raise BadDRCScript( '[ERROR] DRC.setScript(): File not found "{}"' \
                                   .format( script ))
        DRC._script = script

    @staticmethod
    def mkRule ( rule, depends, flags=0 ):
        return DRC( rule, depends, flags )

    def __init__ ( self, rule, depends, flags ):
        from coriolis.helpers.io import ErrorMessage

        if not DRC._script:
            raise ErrorMessage( 1, 'DRC.doTask(): No script defined.' )

        depends = FlowTask._normFileList( depends )
        targets = [ depends[0].stem + '_' + depends[0].stem + '_full.lyrdb' ]
        super().__init__( rule, targets, depends )
        self.flags   = flags
        self.command = [ 'python3', DRC._script.as_posix(), '--path={}'.format( depends[0].as_posix() ) ]
        if self.flags & DRC.FlatMode:      self.command += [ '--run_mode=flat' ] 
        if self.flags & DRC.DeepMode:      self.command += [ '--run_mode=deep' ] 
        if self.flags & DRC.PreCheckDRC:   self.command += [ '--precheck_drc' ] 
        if self.flags & DRC.NoFeol:        self.command += [ '--no_feol' ] 
        if self.flags & DRC.NoBeol:        self.command += [ '--no_beol' ]
        if self.flags & DRC.NoDensity:     self.command += [ '--no_density' ]
        if self.flags & DRC.NoExtraRules:  self.command += [ '--disable_extra_rules' ]
        if self.flags & DRC.DensityOnly:   self.command += [ '--density_only' ]
        if self.flags & DRC.Antenna:       self.command += [ '--antenna' ]
        if self.flags & DRC.AntennaOnly:   self.command += [ '--antenna_only' ]
        if self.flags & DRC.NoOffgrid:     self.command += [ '--no_offgrid' ]
        if self.flags & DRC.NoRecommended: self.command += [ '--no_recommended' ]
        self.addClean( self.targets )
        self.addCleanGlob( Path.cwd(), 'drc_run_*' )
        ShowDRC( 'showdrc', self.file_depend(0), self.file_target(0) )

    def __repr__ ( self ):
        return '<{}>'.format( ' '.join(self.command) )

    def doTask ( self ):
        from coriolis.helpers.io import ErrorMessage

        print( '   -> Run "{}"'.format( ' '.join(self.command) ))
        shellEnv = ShellEnv()
        shellEnv[ 'PYTHONPATH' ] = '/usr/lib64/klayout/pymod'
        shellEnv.export()
        state      = subprocess.run( self.command )
        drcRunDirs = [runDir for runDir in Path.cwd().glob( 'drc_run_*' )]
        drcRunDirs.sort( key=lambda runDir : runDir.stat().st_mtime, reverse=True )
        if drcRunDirs:
            latestLyrdb = self.file_target(0)
            if latestLyrdb.is_symlink():
                latestLyrdb.unlink()
            latestLyrdb.symlink_to( drcRunDirs[0] / latestLyrdb.name )
        if state.returncode:
            e = ErrorMessage( 1, 'DRC.doTask(): UNIX command failed ({}).' \
                                 .format( state.returncode ))
            return TaskFailed( e )
        return self.checkTargets( 'DRC.doTask' )

    def asDoitTask ( self ):
        taskDatas = { 'basename' : self.basename
                    , 'actions'  : [ self.doTask ]
                    , 'doc'      : 'Run {}.'.format( self )
                    , 'targets'  : self.targets
                    , 'file_dep' : self.file_dep
                    }
        return taskDatas


#class BadSealRingScript ( Exception ): pass
#class BadDrcRules       ( Exception ): pass
#class BadDrcRulesFlags  ( Exception ): pass
#
#
#class DRC ( Klayout ):
#
#    Minimal       = 0x0001
#    Maximal       = 0x0002
#    C4M           = 0x0004
#    SHOW_ERRORS   = 0x0800
#    CHECK_DENSITY = 0x1000
#
#    _drcRulesC4M     = None
#    _drcRulesMinimal = None
#    _drcRulesMaximal = None
#
#    @staticmethod
#    def setDrcRules ( rules, flags ):
#        if   isinstance(rules,Path): pass
#        elif isinstance(rules,str):  rules = Path( rules )
#        else:
#            raise BadDrcRules( '[ERROR] DRC.setDrcRules(): Should be <str> or <Path> ({})' \
#                               .format( rules ))
#        if not rules.is_file():
#            raise BadDrcRules( '[ERROR] DRC.setDrcRules(): File not found "{}"' \
#                               .format( rules ))
#
#        if   flags & DRC.Minimal: DRC._drcRulesMinimal = rules
#        elif flags & DRC.Maximal: DRC._drcRulesMaximal = rules
#        elif flags & DRC.C4M:     DRC._drcRulesC4M     = rules
#        else:
#            raise BadDrcRules( '[ERROR] DRC.setDrcRules(): Invalid flags value {}' \
#                               .format( flags ))
#
#    @staticmethod
#    def mkRule ( rule, depends=[], flags=0 ):
#        return DRC( rule, depends, flags )
#
#    def __init__ ( self, rule, depends, flags ):
#        from coriolis.helpers.io import ErrorMessage
#        checkDensity = False
#
#        if flags & DRC.Minimal:
#            rules = DRC._drcRulesMinimal
#            tag   = 'minimal'
#        elif flags & DRC.Maximal:
#            rules = DRC._drcRulesMaximal
#            tag   = 'maximal'
#        elif flags & DRC.C4M:
#            rules = DRC._drcRulesC4M
#            tag   = 'c4m'
#        if flags & DRC.CHECK_DENSITY:
#            checkDensity = True
#
#        env       = {}
#        variables = {}
#        arguments = [ '-zz' ]
#        depends   = FlowTask._normFileList( depends )
#        targets   = [ depends[0].with_suffix('.drc_{}.lyrdb'.format(tag)) ]
#        if not rules:
#            raise ErrorMessage( 1, 'DRC.doTask(): No DRC rules defined for "{}".'.format( tag ))
#        if flags & (DRC.Minimal | DRC.Maximal):
#            variables = { 'in_gds'      : depends[0]
#                        , 'input'       : depends[0]
#                        , 'report'      : targets[0]
#                        , 'report_file' : targets[0]
#                        }
#        elif flags & DRC.C4M:
#            env = { 'SOURCE_FILE' : depends[0].as_posix()
#                  , 'CELL_NAME'   : depends[0].stem
#                  , 'REPORT_FILE' : targets[0].as_posix()
#                  }
#        if not checkDensity: variables[ 'densityRules' ] = 'false'
#        super().__init__( rule, targets, depends, rules, arguments, variables, env, flags )
#
#    def doTask ( self ):
#        from coriolis.helpers.io import ErrorMessage
#
#        shellEnv = ShellEnv()
#        for variable, value in self.env.items():
#            shellEnv[ variable ] = value
#        shellEnv.export()
#        state = subprocess.run( self.command )
#        if state.returncode:
#            e = ErrorMessage( 1, 'Klayout.doTask(): UNIX command failed ({}).' \
#                                 .format( state.returncode ))
#            return TaskFailed( e )
#        state = subprocess.run( [ 'grep', '--count'
#                                , '-e', 'edge-pair'
#                                , '-e', 'polygon'
#                                , self.file_target(0).as_posix() ]  )
#        if not state.returncode:
#            if self.flags & DRC.SHOW_ERRORS:
#                showdrc = ShowDRC( self.basename+'_show', self.file_depend(0), self.file_target(0) )
#                subprocess.run( showdrc.command )
#            return False
#        return self.checkTargets( 'Klayout.doTask' )
