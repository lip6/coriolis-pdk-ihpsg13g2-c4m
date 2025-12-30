
from pathlib import Path
from coriolis.designflow.technos import Where
from coriolis.designflow.task    import ShellEnv
from .designflow.filler          import Filler
from .designflow.sealring        import SealRing


__all__ = [ 'setup', 'pdkMasterTop', 'pdkIHPTop' ]


pdkMasterTop = None
pdkIHPTop    = None


def setup ( checkToolkit=None ):
    global pdkMasterTop
    global pdkIHPTop

    from coriolis                     import Cfg 
    from coriolis                     import Viewer
    from coriolis                     import CRL 
    from coriolis.helpers             import overlay, l, u, n
    from coriolis.designflow.yosys    import Yosys
    from coriolis.designflow.iverilog import Iverilog
    from coriolis.designflow.klayout  import Klayout
    from coriolis.designflow.lvx      import Lvx
    from coriolis.designflow.x2y      import x2y
    from coriolis.designflow.tasyagle import TasYagle
    from .designflow.drc              import DRC
    from .techno                      import setup as techno_setup 
    from .StdCellLib                  import setup as StdCellLib_setup
    from .StdCell3V3Lib               import setup as StdCell3V3Lib_setup
    from .sramlib                     import setup as sram_setup
    from .iolib                       import setup as io_setup
    
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
    sram_setup( pdkIHPTop )
    io_setup( pdkIHPTop )

    liberty        = pdkMasterTop / 'libs.ref' / 'StdCellLib' / 'liberty' / 'StdCellLib_nom.lib'
    stdCellLibVlog = pdkMasterTop / 'libs.ref' / 'StdCellLib' / 'verilog' / 'StdCellLib.v'
    spiceCells     = pdkMasterTop / 'libs.ref' / 'StdCellLib' / 'spice'
    ngspiceTech    = pdkIHPTop    / 'libs.tech' / 'ngspice'
    verilogATech   = pdkIHPTop    / 'libs.tech' / 'verilog-a'
    klayoutTech    = pdkIHPTop    / 'libs.tech' / 'klayout'
    klayoutHome    = Path().home() / '.klayout'
    kdrcScript     = klayoutTech  / 'tech' / 'drc' / 'run_drc.py'
    lypFile        = klayoutTech  / 'tech' / 'sg13g2.lyp'
    fillerScript   = klayoutTech  / 'tech' / 'scripts' / 'filler.py'
    sealRingScript = klayoutTech  / 'tech' / 'scripts' / 'sealring.py'
    
    with overlay.CfgCache(priority=Cfg.Parameter.Priority.UserFile) as cfg:
        cfg.etesian.graphics    = 3
        cfg.etesian.spaceMargin = 0.10
        cfg.katana.eventsLimit  = 4000000
        af  = CRL.AllianceFramework.get()
        lg5 = af.getRoutingGauge('StdCellLib').getLayerGauge( 5 )
        lg5.setType( CRL.RoutingLayerGauge.PowerSupply )
        env = af.getEnvironment()
        env.setCLOCK( '^sys_clk$|^ck|^jtag_tck$' )
        env.setSCALE_X( 100 )

    Yosys.setLiberty( liberty )
    shellEnv = ShellEnv( 'IHP SG13G2 Alliance Environment' )
    shellEnv[ 'MBK_CATA_LIB' ] = shellEnv[ 'MBK_CATA_LIB' ] + ':' + spiceCells.as_posix()
    shellEnv.export()

    Iverilog.setStdCellLib( stdCellLibVlog )

    Klayout.setLypFile( lypFile )
    DRC.setScript( kdrcScript )
    ShellEnv.CHECK_TOOLKIT = Where.checkToolkit.as_posix()
    ShellEnv.PDK_ROOT      = pdkIHPTop.parent.as_posix()
    ShellEnv.PDK           = 'ihpsg13g2'
    ShellEnv.KLAYOUT_PATH  = '{}:{}'.format( klayoutHome, klayoutTech )
    ShellEnv.KLAYOUT_HOME  = '{}'.format( klayoutHome )
    Filler  .setScript( fillerScript )
    SealRing.setScript( sealRingScript )

    TasYagle.flags         = TasYagle.Transistor
    TasYagle.SpiceType     = 'hspice'
    TasYagle.SpiceTrModel  = [ 'mos_tt.lib' ]
    TasYagle.OSDIdlls      = [ verilogATech / 'psp103' / 'psp103.osdi'
                             , verilogATech / 'psp103' / 'psp103t.osdi'
                             , verilogATech / 'psp103' / 'psp103_nqs.osdi'
                             ]
    TasYagle.MBK_CATA_LIB  = '.:' + (ngspiceTech / 'models').as_posix() \
                           + ':' + (pdkMasterTop).as_posix() \
                           + ':' + (pdkMasterTop/'libs.ref'/'StdCellLib'/'spice').as_posix()
    Lvx.MBK_CATA_LIB  = TasYagle.MBK_CATA_LIB
    x2y.MBK_CATA_LIB  = TasYagle.MBK_CATA_LIB
    TasYagle.MBK_SPI_MODEL = pdkMasterTop / 'spimodel.cfg'
    TasYagle.Temperature   = 25.0
    TasYagle.VddSupply     = 1.8 
    TasYagle.VddName       = 'vdd'
    TasYagle.VssName       = 'vss'
    TasYagle.ClockName     = 'm_clock'

