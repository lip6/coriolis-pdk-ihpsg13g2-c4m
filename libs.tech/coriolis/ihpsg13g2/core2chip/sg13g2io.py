
# -*- coding: utf-8 -*-
#
# This file is part of the Coriolis Software.
# Copyright (c) Sorbonne Université 2020-2023, All Rights Reserved
#
# +-----------------------------------------------------------------+
# |                   C O R I O L I S                               |
# |      C u m u l u s  -  P y t h o n   T o o l s                  |
# |                                                                 |
# |  Author      :                    Jean-Paul CHAPUT              |
# |  E-mail      :            Jean-Paul.Chaput@lip6.fr              |
# | =============================================================== |
# |  Python      :       "./core2chip/sg13g2io.py"                  |
# +-----------------------------------------------------------------+

"""
Core2Chip configuration for the IHP sg13g2 I/O pad library.
"""

import sys
import re
from   coriolis.Hurricane         import DbU, DataBase, UpdateSession, Breakpoint, \
                                         Transformation , Instance , Net
from   coriolis.CRL               import Catalog, AllianceFramework
from   coriolis.helpers           import trace
from   coriolis.helpers.io        import ErrorMessage, WarningMessage
from   coriolis.helpers.overlay   import CfgCache
from   coriolis.plugins.core2chip.core2chip import CoreToChip as BaseCoreToChip, IoNet, IoPad


class CoreToChip ( BaseCoreToChip ):
    """
    Provide pad-specific part for IHP sg13g2 I/O pads (works in real mode).
    """
    rePadType = re.compile(r'(?P<type>.+)_(?P<index>[\d]+)$')

    def __init__ ( self, core ):
        with CfgCache() as cfg:
            cfg.chip.useAbstractPads = False
            cfg.chip.mergeIoGround   = False
            self.ioPadNames = { 'in'       :'sg13g2_IOPadIn_full'
                              , 'out'      :'sg13g2_IOPadOut16mA_full'
                              , 'tri_out'  :'sg13g2_IOPadTriOut16mA_full'
                              , 'bidir'    :'sg13g2_IOPadInOut16mA_full'
                              , 'analog'   :'sg13g2_IOPadAnalog_full'
                              , 'vdd'      :'sg13g2_IOPadVdd_full'
                              , 'vss'      :'sg13g2_IOPadVss_full'
                              , 'iovdd'    :'sg13g2_IOPadIOVdd_full'
                              , 'iovss'    :'sg13g2_IOPadIOVss_full'
                              , 'corner'   :'sg13g2_Corner_full'
                              , 'spacer1'  :'sg13g2_Filler200_full'
                              , 'spacer2'  :'sg13g2_Filler400_full'
                              , 'spacer5'  :'sg13g2_Filler1000_full'
                              , 'spacer10' :'sg13g2_Filler2000_full'
                              , 'spacer20' :'sg13g2_Filler4000_full'
                              , 'spacer50' :'sg13g2_Filler10000_full'
                              }
        BaseCoreToChip.__init__ ( self, core )
        self.ringNetNames = { 'iovdd' : None
                            , 'iovss' : None
                            , 'vdd'   : None
                            , 'vss'   : None
                            }
        self.ioPadInfos   = [ BaseCoreToChip.IoPadInfo( IoPad.IN
                                                      , self.ioPadNames['in']
                                                      , 'pad', ['p2c'] )
                            , BaseCoreToChip.IoPadInfo( IoPad.OUT
                                                      , self.ioPadNames['out']
                                                      , 'pad', ['c2p'] )
                            , BaseCoreToChip.IoPadInfo( IoPad.TRI_OUT
                                                      , self.ioPadNames['tri_out']
                                                      , 'pad', ['c2p', 'c2p_en'] )
                            , BaseCoreToChip.IoPadInfo( IoPad.BIDIR
                                                      , self.ioPadNames['bidir']
                                                      , 'pad', ['p2c', 'c2p', 'c2p_en'] )
                            , BaseCoreToChip.IoPadInfo( IoPad.ANALOG
                                                      , self.ioPadNames['analog']
                                                      , 'pad', ['pad', 'padres'] )
                            , BaseCoreToChip.IoPadInfo( IoPad.CORNER
                                                      , self.ioPadNames['corner']
                                                      , None, [] )
                            , BaseCoreToChip.IoPadInfo( IoPad.FILLER
                                                      , self.ioPadNames['spacer1']
                                                      , None, [] )
                            , BaseCoreToChip.IoPadInfo( IoPad.FILLER
                                                      , self.ioPadNames['spacer2']
                                                      , None, [] )
                            , BaseCoreToChip.IoPadInfo( IoPad.FILLER
                                                      , self.ioPadNames['spacer5']
                                                      , None, [] )
                            , BaseCoreToChip.IoPadInfo( IoPad.FILLER
                                                      , self.ioPadNames['spacer10']
                                                      , None, [] )
                            , BaseCoreToChip.IoPadInfo( IoPad.FILLER
                                                      , self.ioPadNames['spacer20']
                                                      , None, [] )
                            , BaseCoreToChip.IoPadInfo( IoPad.FILLER
                                                      , self.ioPadNames['spacer50']
                                                      , None, [] )
                            ]
        self.cornerCount = 0
        self.spacerCount = 0
        self.padSpacers  = []
        self._getPadLib()
        return

    def _getPadLib ( self ):
        """
        Check that the I/O pad library is present and pre-load the spacer cells.
        """
        def _cmpPad ( pad ):
            """Used to sort I/O pads by decreasing width."""
            return pad.getAbutmentBox().getWidth()

        self.padLib = AllianceFramework.get().getLibrary( "iolib" )
        if not self.padLib:
            message = [ 'CoreToChip.libresocio._getPadLib(): Unable to find Alliance "LibreSOCIO" library' ]
            raise ErrorMessage( 1, message )
        for ioPadInfo in self.ioPadInfos:
            if ioPadInfo.flags & IoPad.FILLER: 
                spacerCell = self.padLib.getCell( ioPadInfo.name )
                if spacerCell: self.padSpacers.append( spacerCell )
                else:
                    raise ErrorMessage( 1, 'CoreToChip.sg13g2io._getPadLib(): Missing spacer cell "{}"'.format(spacerName) )
        self.padSpacers = sorted( self.padSpacers, key=_cmpPad, reverse=True )

    def getNetType ( self, netName ):
        if netName.startswith('vss') or netName.startswith('iovss'): return Net.Type.GROUND
        if netName.startswith('vdd') or netName.startswith('iovdd'): return Net.Type.POWER
        return Net.Type.LOGICAL

    def isGlobal ( self, netName ):
        if netName in self.ringNetNames: return True
        return False

    def getCell ( self, masterCellName ):
       #cell = self.padLib.getCell( masterCellName )
        cell = AllianceFramework.get().getCell( masterCellName, Catalog.State.Views )
        if not cell:
            raise ErrorMessage( 1, 'libresocio.getCell(): I/O pad library "%s" does not contain cell named "%s"' \
                                   % (self.padLib.getName(),masterCellName) )
        return cell

    def _buildAllGroundPads ( self, ioPadConf ):
        coreNet   = self.core  .getNet( ioPadConf.coreSupplyNetName )
        coronaNet = self.corona.getNet( ioPadConf.coreSupplyNetName )
        chipNet   = self.chip  .getNet( ioPadConf.coreSupplyNetName )
        padNet    = self.chip  .getNet( ioPadConf.padSupplyNetName  )
        if not coronaNet:
            coronaNet = Net.create( self.corona, ioPadConf.coreSupplyNetName )
            coronaNet.setExternal( True )
            coronaNet.setGlobal  ( True )
            coronaNet.setType    ( Net.Type.GROUND )
            self.icore.getPlug( coreNet ).setNet( coronaNet  )
        if not chipNet:
            chipNet = Net.create( self.chip, ioPadConf.coreSupplyNetName )
            chipNet.setExternal( True )
            chipNet.setType    ( Net.Type.GROUND )
        if not padNet:
            padNet = Net.create( self.chip, ioPadConf.padSupplyNetName )
            padNet.setExternal( True )
            padNet.setType    ( Net.Type.GROUND )
        coronaPlug = self.icorona.getPlug( coronaNet )
        if not coronaPlug.getNet():
            coronaPlug.setNet( chipNet  )
        self.ringNetNames['iovss' ] = padNet
        self.ringNetNames[  'vss' ] = chipNet
        ioPadConf.pads.append( Instance.create( self.chip
                                              , 'p_vss_{}'.format(ioPadConf.index)
                                              , self.getCell(self.ioPadNames['vss']) ) )
        self._connect( ioPadConf.pads[0], chipNet,   'vss' )
        self._connect( ioPadConf.pads[0], padNet , 'iovss' )
        self.groundPadCount += 1
        self.chipPads       += ioPadConf.pads
        ioPadConf.pads.append( Instance.create( self.chip
                                              , 'p_iovss_{}'.format(ioPadConf.index)
                                              , self.getCell(self.ioPadNames['iovss']) ) )
        self._connect( ioPadConf.pads[0], chipNet,   'vss' )
        self._connect( ioPadConf.pads[0], padNet , 'iovss' )
        self.groundPadCount += 1
        self.chipPads       += ioPadConf.pads

    def _buildAllPowerPads ( self, ioPadConf ):
        trace( 550, ',+', '\tsg13g2io.CoreToChip()\n' )
        trace( 550, '\tcoreSupplyNetName="{}"\n'.format( ioPadConf.coreSupplyNetName ))
        trace( 550, '\tpadSupplyNetName ="{}"\n'.format( ioPadConf.padSupplyNetName ))
        coreNet   = self.core  .getNet( ioPadConf.coreSupplyNetName )
        coronaNet = self.corona.getNet( ioPadConf.coreSupplyNetName )
        chipNet   = self.chip  .getNet( ioPadConf.coreSupplyNetName )
        padNet    = self.chip  .getNet( ioPadConf.padSupplyNetName  )
        if not coronaNet:
            coronaNet = Net.create( self.corona, ioPadConf.coreSupplyNetName )
            coronaNet.setExternal( True )
            coronaNet.setGlobal  ( True )
            coronaNet.setType    ( Net.Type.POWER )
            self.icore.getPlug( coreNet ).setNet( coronaNet  )
        if not chipNet:
            chipNet = Net.create( self.chip, ioPadConf.coreSupplyNetName )
            chipNet.setExternal( True )
            chipNet.setType    ( Net.Type.POWER )
            self.icorona.getPlug( coronaNet ).setNet( chipNet  )
        trace( 550, '\tchipNet ="{}"\n'.format( chipNet ))
        if not padNet:
            padNet = Net.create( self.chip, ioPadConf.padSupplyNetName )
            padNet.setExternal( True )
            padNet.setType    ( Net.Type.POWER )
        self.ringNetNames['iovdd'] = padNet
        self.ringNetNames[  'vdd'] = chipNet
        trace( 550, '\tpadNet ="{}"\n'.format( padNet ))
        trace( 550, '\tI/O vdd ="{}"\n'.format( self.getCell(self.ioPadNames['vdd']) ))
        ioPadConf.pads.append( Instance.create( self.chip
                                              , 'p_vdd_{}'.format(ioPadConf.index)
                                              , self.getCell(self.ioPadNames['vdd']) ) )
        self._connect( ioPadConf.pads[0], chipNet,   'vdd' )
        self._connect( ioPadConf.pads[0], padNet , 'iovss' )
        self.powerPadCount += 1
        self.chipPads      += ioPadConf.pads
        trace( 550, '\tI/O IO vdd ="{}"\n'.format( self.getCell(self.ioPadNames['iovdd']) ))
        ioPadConf.pads.append( Instance.create( self.chip
                                              , 'p_iovdd_{}'.format(ioPadConf.index)
                                              , self.getCell(self.ioPadNames['iovdd']) ) )
        self._connect( ioPadConf.pads[0], chipNet,   'vdd' )
        self._connect( ioPadConf.pads[0], padNet , 'iovss' )
        self.powerPadCount += 1
        self.chipPads      += ioPadConf.pads
        trace( 550, '-,' )

   #def _buildCoreGroundPads ( self, ioPadConf ):
   #    coreNet   = self.core  .getNet( ioPadConf.coreSupplyNetName )
   #    coronaNet = self.corona.getNet( ioPadConf.coreSupplyNetName )
   #    chipNet   = self.chip  .getNet( ioPadConf.coreSupplyNetName )
   #    if not coronaNet:
   #        coronaNet = Net.create( self.corona, ioPadConf.coreSupplyNetName )
   #        coronaNet.setExternal( True )
   #        coronaNet.setGlobal  ( True )
   #        coronaNet.setType    ( Net.Type.GROUND )
   #        self.icore.getPlug( coreNet ).setNet( coronaNet  )
   #    if not chipNet:
   #        chipNet = Net.create( self.chip, ioPadConf.coreSupplyNetName )
   #        chipNet.setExternal( True )
   #        chipNet.setType    ( Net.Type.GROUND )
   #    coronaPlug = self.icorona.getPlug( coronaNet )
   #    if not coronaPlug.getNet():
   #        coronaPlug.setNet( chipNet  )
   #    self.ringNetNames['vss'] = chipNet
   #    ioPadConf.pads.append( Instance.create( self.chip
   #                                          , 'p_vss_{}'.format(ioPadConf.index)
   #                                          , self.getCell(self.ioPadNames['vss']) ) )
   #    self._connect( ioPadConf.pads[0], chipNet, 'vss' )
   #    self.groundPadCount += 1
   #    self.chipPads       += ioPadConf.pads
   #
   #def _buildIoGroundPads ( self, ioPadConf ):
   #    padNet = self.chip.getNet( ioPadConf.padSupplyNetName  )
   #    if not padNet:
   #        padNet = Net.create( self.chip, ioPadConf.padSupplyNetName )
   #        padNet.setExternal( True )
   #        padNet.setType    ( Net.Type.GROUND )
   #    self.ringNetNames['iovss'] = padNet
   #    ioPadConf.pads.append( Instance.create( self.chip
   #                                          , 'p_iovss_{}'.format(ioPadConf.index)
   #                                          , self.getCell(self.ioPadNames['iovss']) ) )
   #    self._connect( ioPadConf.pads[0], padNet , 'iovss' )
   #    self.groundPadCount += 1
   #    self.chipPads       += ioPadConf.pads
   #
   #def _buildCorePowerPads ( self, ioPadConf ):
   #    coreNet   = self.core  .getNet( ioPadConf.coreSupplyNetName )
   #    coronaNet = self.corona.getNet( ioPadConf.coreSupplyNetName )
   #    chipNet   = self.chip  .getNet( ioPadConf.coreSupplyNetName )
   #    if not coronaNet:
   #        coronaNet = Net.create( self.corona, ioPadConf.coreSupplyNetName )
   #        coronaNet.setExternal( True )
   #        coronaNet.setGlobal  ( True )
   #        coronaNet.setType    ( Net.Type.POWER )
   #        self.icore.getPlug( coreNet ).setNet( coronaNet  )
   #    if not chipNet:
   #        chipNet = Net.create( self.chip, ioPadConf.coreSupplyNetName )
   #        chipNet.setExternal( True )
   #        chipNet.setType    ( Net.Type.POWER )
   #        self.icorona.getPlug( coronaNet ).setNet( chipNet  )
   #        self.ringNetNames['vdd'] = chipNet
   #    ioPadConf.pads.append( Instance.create( self.chip
   #                                          , 'p_vdd_{}'.format(ioPadConf.index)
   #                                          , self.getCell(self.ioPadNames['vdd']) ) )
   #    self._connect( ioPadConf.pads[0], chipNet, 'vdd' )
   #    self.powerPadCount += 1
   #    self.chipPads      += ioPadConf.pads
   #
   #def _buildIoPowerPads ( self, ioPadConf ):
   #    padNet = self.chip  .getNet( ioPadConf.padSupplyNetName  )
   #    if not padNet:
   #        padNet = Net.create( self.chip, ioPadConf.padSupplyNetName )
   #        padNet.setExternal( True )
   #        padNet.setType    ( Net.Type.POWER )
   #        self.ringNetNames['iovdd'] = padNet
   #    ioPadConf.pads.append( Instance.create( self.chip
   #                                          , 'p_iovdd_{}'.format(ioPadConf.index)
   #                                          , self.getCell(self.ioPadNames['iovdd']) ) )
   #    self._connect( ioPadConf.pads[0], padNet , 'iovdd' )
   #    self.powerPadCount += 1
   #    self.chipPads      += ioPadConf.pads

    def _buildClockPads ( self, ioPadConf ):
        """For "LibreSOCIO" there is no specialized clock I/O pad. So do nothing."""
        pass

    def _connectClocks ( self ):
        """For "LibreSOCIO" there is no pad internal clock ring. So do nothing."""
        pass

    def hasCornerCell ( self ):
        """Overload of CoreToChip, YES we have dedicated corner cells."""
        return True

    def hasFillerCells ( self ):
        """Overload of CoreToChip, YES we have dedicated filler cells."""
        return True

    def getCornerCell ( self ):
        """Return the model of corner cell."""
        return self.getCell( self.ioPadNames['corner'] )

    def createSpacer ( self, gapWidth ):
        """Return a new instance of spacer cell."""
        trace( 550, ',+', '\tsg13g2io.CoreToChip.createSpacer()\n' )
        trace( 550, '\tgapWidth="{}"\n'.format( DbU.getValueString(gapWidth) ))
        spacerCell = None
        for candidate in self.padSpacers:
            trace( 550, '\t| candidate ="{}"\n'.format( candidate ))
            if gapWidth >= candidate.getAbutmentBox().getWidth():
                spacerCell = candidate
                break
        if not spacerCell:
            trace( 550, ',-', '\tNo candidate found\n' )
            return None
        spacer = Instance.create( self.chip
                                , 'pad_spacer_{}'.format( self.spacerCount )
                                , spacerCell )
        self.spacerCount += 1
        self._connect( spacer, self.ringNetNames['iovdd'], 'iovdd' )
        self._connect( spacer, self.ringNetNames[  'vdd'],   'vdd' )
        self._connect( spacer, self.ringNetNames['iovss'], 'iovss' )
        self._connect( spacer, self.ringNetNames[  'vss'],   'vss' )
        trace( 550, ',-', '\tspacer ="{}"\n'.format( spacer ))
        return spacer

    def createCorner ( self, instanceName=None ):
        """Return a new instance of corner cell."""
        if instanceName is None:
            instanceName = 'pad_corner_{}'.format( self.cornerCount )
        corner = Instance.create( self.chip, instanceName, self.getCornerCell() )
        self.cornerCount += 1
        self._connect( corner, self.ringNetNames['vdd'  ],   'vdd' )
        self._connect( corner, self.ringNetNames['iovdd'], 'iovdd' )
        self._connect( corner, self.ringNetNames['vss'  ],   'vss' )
        self._connect( corner, self.ringNetNames['iovss'], 'iovss' )
        return corner
