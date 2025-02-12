
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


__all__ = [ 'setup' ]


bondPadCell = None
filler5Cell = None


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


def copyUpInterface ( topCell, instance, padNetName ): 
    transf = instance.getTransformation()
    xShift = transf.getTx()
    yShift = transf.getTy()
    padNet = None
    for net in instance.getMasterCell().getNets():
        if not net.isExternal(): continue

        topNet = topCell.getNet( net.getName() )
        if not topNet:
            topNet = Net.create( topCell, net.getName() )
            topNet.setType     ( net.getType() )
            topNet.setDirection( net.getDirection() )
            topNet.setGlobal   ( net.isGlobal() )
            topNet.setExternal ( True )
            if net.getName() == padNetName:
                padNet = topNet
                if padNetName == 'pad':
                    continue

        for component in NetExternalComponents.get( net ):
            if isinstance(component,Horizontal):
                h = Horizontal.create( topNet
                                     , component.getLayer()
                                     , component.getY() + yShift
                                     , component.getWidth()
                                     , component.getSourceX() + xShift
                                     , component.getTargetX() + xShift )
                NetExternalComponents.setExternal( h )
            elif isinstance(component,Vertical):
                v = Vertical.create( topNet
                                   , component.getLayer()
                                   , component.getX() + xShift
                                   , component.getWidth()
                                   , component.getSourceY() + yShift
                                   , component.getTargetY() + yShift )
                NetExternalComponents.setExternal( v )
            elif isinstance(component,Pad):
                p = Pad.create( topNet
                              , component.getLayer()
                              , component.getBondingBox().translate( xShift, yShift ))
                NetExternalComponents.setExternal( p )
    return padNet


def assembleIoPad ( cell ):
    global bondPadCell
    global filler5Cell

    yShift     = u(80.0)
    padNetName = 'pad'
    with UpdateSession():
        if cell.getName().startswith('sg13g2_Corner'):
            addFiller  = False
            addBondPad = False
            xShift     = u(90.0)
            yShift     = u(90.0)
        elif    cell.getName().startswith('sg13g2_Filler'):
            addFiller  = False
            addBondPad = False
            xShift     = u( 0.0)
            yShift     = u(90.0)
        elif    cell.getName().startswith('sg13g2_IOPadIOVdd') \
             or cell.getName().startswith('sg13g2_IOPadIOVss') \
             or cell.getName().startswith('sg13g2_IOPadVdd'  ) \
             or cell.getName().startswith('sg13g2_IOPadVss'  ):
            addFiller  = True
            addBondPad = True
            xShift     = u( 0.0)
            yShift     = u(90.0)
            if   cell.getName().endswith('PadIOVdd'): padNetName = 'iovdd'
            elif cell.getName().endswith('PadIOVss'): padNetName = 'iovss'
            elif cell.getName().endswith('PadVdd'  ): padNetName = 'vdd'
            elif cell.getName().endswith('PadVss'  ): padNetName = 'vss'
        else:
            addBondPad = True
            addFiller  = True
            xShift     = u( 0.0)
            yShift     = u(90.0)

        extraWidth = 0
        if addFiller:
            extraWidth = filler5Cell.getAbutmentBox().getWidth()

        completeCell = Cell.create( cell.getLibrary(), cell.getName()+'_full' )
        ioInst = Instance.create( completeCell
                                , cell.getName()
                                , cell
                                , Transformation( xShift, yShift, Transformation.Orientation.ID )
                                , Instance.PlacementStatus.FIXED )
        bondInst = None
        if addBondPad:
            bondInst = Instance.create( completeCell
                                      , bondPadCell.getName()
                                      , bondPadCell
                                      , Transformation( u(40.0), u(40.0), Transformation.Orientation.ID )
                                      , Instance.PlacementStatus.FIXED )
        fillerInst = None
        if addFiller:
            fillerINst = Instance.create( completeCell
                                        , filler5Cell.getName()
                                        , filler5Cell
                                        , Transformation( xShift + cell.getAbutmentBox().getWidth()
                                                        , yShift
                                                        , Transformation.Orientation.ID )
                                        , Instance.PlacementStatus.FIXED )
        cellAb = cell.getAbutmentBox()
        completeCell.setAbutmentBox( Box( 0
                                        , 0
                                        , cellAb.getWidth ()+xShift+extraWidth
                                        , cellAb.getHeight()+yShift ))
        if fillerInst:
            copyUpInterface( completeCell, fillerInst )
        padNet = copyUpInterface( completeCell, ioInst, padNetName )

        if not addBondPad:
            return
        if not padNet:
            print( ErrorMessage( 1, 'sg13g2.iolib.assembleIoPad(): No "pad" net in {}.' \
                                    .format(cell.getName()) ))
            return

        topMetal2 = DataBase.getDB().getTechnology().getLayer( 'TopMetal2' )
        Vertical.create( padNet, topMetal2, u(40.0), u(42.0), u(75.0), u(91.0) )
        for net in bondPadCell.getNets():
            for component in net.getComponents():
                if component.getLayer() != topMetal2: continue
                if not isinstance(component,Polygon): continue
                contour = component.getPoints()
                for point in contour:
                    point.translate( xShift + u(40.0), yShift - u(50.0) )
                p = Polygon.create( padNet, component.getLayer(), contour )
                NetExternalComponents.setExternal( p )
                break
        

def assembleIoPads ( library ):
    baseIoPads = []
    for cell in library.getCells():
        if    cell.getName().startswith('sg13g2_Corner') \
           or cell.getName().startswith('sg13g2_Filler') \
           or cell.getName().startswith('sg13g2_IOPad' ):
            baseIoPads.append( cell )
    for cell in baseIoPads:
        assembleIoPad( cell )


def _routing ():
    """
    Define the routing gauge for I/O cells along with the various P&R tool parameters.
    """
    with CfgCache(priority=Cfg.Parameter.Priority.ConfigurationFile) as cfg:
        cfg.chip.block.rails.count    = 2 
        cfg.chip.block.rails.hWidth   = u(40.0)
        cfg.chip.block.rails.vWidth   = u(40.0)
        cfg.chip.block.rails.hSpacing = u( 6.0)
        cfg.chip.block.rails.vSpacing = u( 6.0)
        cfg.chip.padCoreSide          = 'North'
    af = AllianceFramework.get()
    cg = CellGauge.create( 'LEF.IO_Site'
                         , 'Metal2'  # pin layer name.
                         , u(  1.0)  # pitch.
                         , u(270.0)  # cell slice height.
                         , u(  1.0)  # cell slice step.
                         )
    af.addCellGauge( cg )


def _loadIoLib ( pdkDir ):
    """
    Load the I/O cells from the LEF+GDS files.
    """
    global bondPadCell
    global filler5Cell
    
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
            , Gds.Layer_0_IsBoundary|Gds.NoBlockages|Gds.LefForeign )
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
    filler5Cell = ioLib.getCell( 'sg13g2_Filler1000' )
    bondPadCell = ioLibBond.getCell( 'bondpad' )
    if bondPadCell:
        assembleIoPads( ioLib )
    af.wrapLibrary( ioLib    , 1 ) 
    af.wrapLibrary( ioLibBond, 2 ) 


def setup ( pdkDir ):
   #with overlay.CfgCache(priority=Cfg.Parameter.Priority.UserFile) as cfg:
   #    cfg.misc.minTraceLevel = 100
   #    cfg.misc.maxTraceLevel = 102
    _routing()
    _loadIoLib( pdkDir )
