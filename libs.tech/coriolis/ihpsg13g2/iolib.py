
import sys
import os.path
from   coriolis                 import Cfg
from   coriolis.Hurricane       import Technology, DataBase, DbU, Library, Layer,            \
                                       BasicLayer, Cell, Net, Horizontal, Vertical, Contact, \
                                       Rectilinear, Box, Point, Instance, Transformation,    \
                                       NetExternalComponents, Pad, Path, Query
import coriolis.Viewer
from   coriolis.CRL             import AllianceFramework, Gds, LefImport, CellGauge,  \
                                       RoutingGauge, RoutingLayerGauge
from   coriolis.Anabatic        import StyleFlags
from   coriolis.helpers         import trace, l, u, n, overlay, io, ndaTopDir
from   coriolis.helpers.overlay import CfgCache, UpdateSession


__all__ = [ 'setup' ]


def shiftAbTo00 ( cell ):
    if     (cell.getAbutmentBox().getXMin() == 0) \
       and (cell.getAbutmentBox().getYMin() == 0):
        return

    io.vprint( 1, '     - Shifting {} bottom left corner AB to (0,0).'.format( cell.getName() ))
    xyShift  = Point( - cell.getAbutmentBox().getXMin()
                    , - cell.getAbutmentBox().getYMin() ) 
    xyTransf = Transformation( xyShift )
    with UpdateSession():
        cell.setAbutmentBox( cell.getAbutmentBox().translate( xyShift ))
        for instance in cell.getInstances():
            instTransf = instance.getTransformation()
            xyTransf.applyOn( instTransf )
            instance.setTransformation( instTransf )
        for net in cell.getNets():
            for component in net.getComponents():
                component.translate( xyShift )


def _routing ():
    """
    Define the routing gauge for I/O cells along with the various P&R tool parameters.
    """
    with CfgCache(priority=Cfg.Parameter.Priority.ConfigurationFile) as cfg:
        cfg.chip.block.rails.count    = 2 
        cfg.chip.block.rails.hWidth   = u(30.0)
        cfg.chip.block.rails.vWidth   = u(30.0)
        cfg.chip.block.rails.hSpacing = u( 6.0)
        cfg.chip.block.rails.vSpacing = u( 6.0)
        #cfg.chip.padCorner            = 'gf180mcu_fd_io__cor'
        #cfg.chip.padSpacers           = 'gf180mcu_fd_io__fill10,gf180mcu_fd_io__fill5,gf180mcu_fd_io__fill1'
        cfg.chip.padCoreSide          = 'North'
    af = AllianceFramework.get()
    cg = CellGauge.create( 'LEF.IO_Site'
                         , 'Metal2'  # pin layer name.
                         , u(  1.0)  # pitch.
                         , u(180.0)  # cell slice height.
                         , u(  1.0)  # cell slice step.
                         )
    af.addCellGauge( cg )


def _loadIoLib ( pdkDir ):
    """
    Load the I/O cells from the LEF+GDS files.
    """
    cellsDir  = pdkDir / 'libs.ref' / 'sg13g2_io'
    bondDir   = pdkDir / 'libs.ref' / 'sg13g2_pr'
    af        = AllianceFramework.get()
    db        = DataBase.getDB()
    tech      = db.getTechnology()
    rootlib   = db.getRootLibrary()
    ioLib     = Library.create( rootlib, 'iolib'   )
    ioLibGds  = Library.create( ioLib  , 'GDS'     )
    ioLibBond = Library.create( ioLib  , 'GDSBond' )
    LefImport.setMergeLibrary( ioLib )
    LefImport.setGdsForeignLibrary( ioLibGds )
    Gds.load( ioLibGds
            , (cellsDir / 'gds' / 'sg13g2_io.gds').as_posix()
            , Gds.Layer_0_IsBoundary|Gds.NoBlockages )
    Gds.load( ioLibBond
            , (bondDir / 'gds' / 'sg13g2_pr.gds').as_posix()
            , Gds.Layer_0_IsBoundary|Gds.NoBlockages )
    LefImport.load( (pdkDir / 'libs.ref'
                            / 'sg13g2_stdcell'
                            / 'lef'
                            / 'sg13g2_tech.lef').as_posix() )
    io.vprint( 1, '  o  Setup IHP sg13g2 I/O library in {}.'.format( ioLib.getName() ))
    LefImport.load(  (cellsDir / 'lef' / 'sg13g2_io.lef').as_posix() )
    for cell in ioLib.getCells():
        shiftAbTo00( cell )
    af.wrapLibrary( ioLib    , 1 ) 
    af.wrapLibrary( ioLibBond, 2 ) 


def setup ( pdkDir ):
   #with overlay.CfgCache(priority=Cfg.Parameter.Priority.UserFile) as cfg:
   #    cfg.misc.minTraceLevel = 100
   #    cfg.misc.maxTraceLevel = 102
    _routing()
    _loadIoLib( pdkDir )
