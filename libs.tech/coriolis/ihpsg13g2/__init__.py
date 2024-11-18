
from pathlib import Path
from coriolis.designflow.technos import Where
from coriolis.designflow.task    import ShellEnv
from .designflow.filler          import Filler


__all__ = [ 'setup', 'pdkMasterTop', 'pdkIHPTop' ]


pdkMasterTop = None
pdkIHPTop    = None


def setup ( checkToolkit=None ):
    global pdkMasterTop
    global pdkIHPTop

    from coriolis                    import Cfg 
    from coriolis                    import Viewer
    from coriolis                    import CRL 
    from coriolis.helpers            import overlay, l, u, n
    from coriolis.designflow.yosys   import Yosys
    from coriolis.designflow.klayout import Klayout, DRC
    from .techno                     import setup as techno_setup 
    from .StdCellLib                 import setup as StdCellLib_setup
    from .StdCell3V3Lib              import setup as StdCell3V3Lib_setup
    from .iolib                      import setup as io_setup
    
    with overlay.CfgCache(priority=Cfg.Parameter.Priority.UserFile) as cfg:
        cfg.misc.catchCore     = False
        cfg.misc.minTraceLevel = 12300
        cfg.misc.maxTraceLevel = 12400
        cfg.misc.info          = False
        cfg.misc.paranoid      = False
        cfg.misc.bug           = False
        cfg.misc.logMode       = True
        cfg.misc.verboseLevel1 = True
        cfg.misc.verboseLevel2 = True

    pdkMasterTop = Path( __file__ ).parent
    pdkIHPTop    = pdkMasterTop.parent / 'ihpsg13g2'

    Where( checkToolkit )

    techno_setup()
    StdCellLib_setup()
    io_setup( pdkIHPTop )

    liberty      = pdkMasterTop / 'libs.ref' / 'StdCellLib' / 'liberty' / 'StdCellLib_nom.lib'
   #kdrcRules    = pdkMasterTop / 'libs.tech' / 'klayout' / 'share' / 'C4M.IHPSG13G2.drc'
    kdrcRules    = pdkIHPTop    / 'libs.tech' / 'klayout' / 'tech' / 'drc' / 'sg13g2_minimal.lydrc'
    lypFile      = pdkIHPTop    / 'libs.tech' / 'klayout' / 'tech' / 'sg13g2.lyp'
    fillerScript = pdkIHPTop    / 'libs.tech' / 'klayout' / 'tech' / 'scripts' / 'filler.py'
    
    with overlay.CfgCache(priority=Cfg.Parameter.Priority.UserFile) as cfg:
        cfg.etesian.graphics    = 3
        cfg.etesian.spaceMargin = 0.10
        cfg.katana.eventsLimit  = 4000000
        af  = CRL.AllianceFramework.get()
        lg5 = af.getRoutingGauge('StdCellLib').getLayerGauge( 5 )
        lg5.setType( CRL.RoutingLayerGauge.PowerSupply )
        env = af.getEnvironment()
        env.setCLOCK( '^sys_clk$|^ck|^jtag_tck$' )

    Yosys.setLiberty( liberty )
    Klayout.setLypFile( lypFile )
    DRC.setDrcRules( kdrcRules )
    ShellEnv.CHECK_TOOLKIT = Where.checkToolkit.as_posix()
    shellEnv = ShellEnv()
    shellEnv[ 'PDK_ROOT' ] = pdkIHPTop.parent.as_posix()
    shellEnv[ 'PDK'      ] = 'ihpsg13g2'
    shellEnv.export()
    Filler.setScript( fillerScript )
