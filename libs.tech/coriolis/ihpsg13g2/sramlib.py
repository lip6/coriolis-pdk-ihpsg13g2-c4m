

import sys
import os.path
from   coriolis                 import Cfg
from   coriolis.Hurricane       import Technology, DataBase, DbU, Library, Layer,            \
                                       BasicLayer, Cell, Net, Horizontal, Vertical, Contact, \
                                       Rectilinear, Box, Point, Instance, Transformation,    \
                                       NetExternalComponents, Pad, Path, Query, Polygon
import coriolis.Viewer
from   coriolis.CRL             import AllianceFramework, Gds, LefImport, CellGauge,  \
                                       RoutingGauge, RoutingLayerGauge
from   coriolis.Anabatic        import StyleFlags
from   coriolis.helpers         import trace, l, u, n, overlay, io, ndaTopDir
from   coriolis.helpers.io      import ErrorMessage
from   coriolis.helpers.overlay import CfgCache, UpdateSession


def _loadSramLib ( pdkDir ):
    """
    Load the SRAM macros from the LEF+GDS files.
    """
    
    cellsDir   = pdkDir / 'libs.ref' / 'sg13g2_sram'
    af         = AllianceFramework.get()
    db         = DataBase.getDB()
    tech       = db.getTechnology()
    rootlib    = db.getRootLibrary()
    sramLib    = Library.create( rootlib, 'sramlib'   )
    sramLibGds = Library.create( sramLib, 'GDS'     )
    io.vprint( 1, '  o  Setup IHP sg13g2 SRAM library in {}.'.format( sramLib.getName() ))
    LefImport.setMergeLibrary( sramLib )
    LefImport.setGdsForeignLibrary( sramLibGds )
    Gds.load( sramLibGds
            , (cellsDir / 'gds' / 'RM_IHPSG13_1P_256x64_c2_bm_bist.gds').as_posix()
            , Gds.Layer_0_IsBoundary|Gds.NoBlockages|Gds.LefForeign )
    LefImport.load( (pdkDir / 'libs.ref'
                            / 'sg13g2_stdcell'
                            / 'lef'
                            / 'sg13g2_tech.lef').as_posix() )
    LefImport.load(  (cellsDir / 'lef' / 'RM_IHPSG13_1P_256x64_c2_bm_bist.lef').as_posix() )
    af.wrapLibrary( sramLib   , AllianceFramework.AppendLibrary ) 
    af.wrapLibrary( sramLibGds, AllianceFramework.AppendLibrary ) 


def setup ( pdkDir ):
    #with overlay.CfgCache(priority=Cfg.Parameter.Priority.UserFile) as cfg:
    #    cfg.misc.minTraceLevel = 100
    #    cfg.misc.maxTraceLevel = 102
    _loadSramLib( pdkDir )
