
from pathlib import Path
from coriolis.designflow.technos import Where
from coriolis.designflow.task    import ShellEnv


__all__ = [ 'setup' ]


def setup ( checkToolkit=None ):
    from coriolis                    import Cfg 
    from coriolis                    import Viewer
    from coriolis                    import CRL 
    from coriolis.helpers            import overlay, l, u, n
    from coriolis.designflow.yosys   import Yosys
    from coriolis.designflow.klayout import DRC
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

    Where( checkToolkit )

    techno_setup()
    StdCellLib_setup()
    io_setup( pdkMasterTop.parent / 'ihpsg13g2' )

    liberty   = pdkMasterTop / 'libs.ref' / 'StdCellLib' / 'liberty' / 'StdCellLib_nom.lib'
    kdrcRules = pdkMasterTop / 'libs.tech' / 'klayout' / 'share' / 'C4M.IHPSG13G2.drc'
    
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
    DRC.setDrcRules( kdrcRules )
    ShellEnv.CHECK_TOOLKIT = Where.checkToolkit.as_posix()
