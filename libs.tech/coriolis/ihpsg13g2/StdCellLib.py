# SPDX-License-Identifier: GPL-2.0-or-later
from pathlib import Path

from coriolis import CRL, Hurricane, Viewer, Cfg, Spice
from coriolis.Hurricane import (
    Technology, DataBase, DbU, Library,
    Layer, BasicLayer,
    Cell, Net, Horizontal, Vertical, Rectilinear, Box, Point,
    Instance, Transformation,
    NetExternalComponents,
)
from coriolis.helpers import u, l
from coriolis.helpers.technology import setEnclosures
from coriolis.helpers.overlay import CfgCache, UpdateSession

from .arrakeen import c4m_ihpsg13g2, c4m_tech, c4m_export


__all__ = ["setup"]

def createRL(tech, net, layer, coords):
    coords = [Point(u(x), u(y)) for x,y in coords]
    Rectilinear.create(net, tech.getLayer(layer), coords)

def _routing():
    af = CRL.AllianceFramework.get()
    db = DataBase.getDB()
    tech = db.getTechnology()

    rg = CRL.RoutingGauge.create('StdCellLib')
    rg.setSymbolic(False)
    metal = tech.getLayer('Metal1')
    via = tech.getLayer('Metal1_Via1_Metal2')
    setEnclosures(via, metal, (u(0.01), u(0.05)))
    rg.addLayerGauge(CRL.RoutingLayerGauge.create(
        metal, CRL.RoutingLayerGauge.Vertical, CRL.RoutingLayerGauge.PinOnly, 0, 0.0,
        u(0.0), u(0.5), u(0.21), u(0.16), u(0.19), u(0.18),
    ))
    metal = tech.getLayer('Metal2')
    via = tech.getLayer('Metal1_Via1_Metal2')
    setEnclosures(via, metal, (u(0.01), u(0.05)))
    via = tech.getLayer('Metal2_Via2_Metal3')
    setEnclosures(via, metal, (u(0.05), u(0.05)))
    rg.addLayerGauge(CRL.RoutingLayerGauge.create(
        metal, CRL.RoutingLayerGauge.Horizontal, CRL.RoutingLayerGauge.Default, 1, 0.0,
        u(0.0), u(0.5), u(0.29), u(0.21), u(0.19), u(0.21),
    ))
    metal = tech.getLayer('Metal3')
    via = tech.getLayer('Metal2_Via2_Metal3')
    setEnclosures(via, metal, (u(0.05), u(0.05)))
    via = tech.getLayer('Metal3_Via3_Metal4')
    setEnclosures(via, metal, (u(0.05), u(0.05)))
    rg.addLayerGauge(CRL.RoutingLayerGauge.create(
        metal, CRL.RoutingLayerGauge.Vertical, CRL.RoutingLayerGauge.Default, 2, 0.0,
        u(0.0), u(0.5), u(0.29), u(0.2), u(0.19), u(0.21),
    ))
    metal = tech.getLayer('Metal4')
    via = tech.getLayer('Metal3_Via3_Metal4')
    setEnclosures(via, metal, (u(0.05), u(0.05)))
    via = tech.getLayer('Metal4_Via4_Metal5')
    setEnclosures(via, metal, (u(0.125), u(0.05)))
    rg.addLayerGauge(CRL.RoutingLayerGauge.create(
        metal, CRL.RoutingLayerGauge.Horizontal, CRL.RoutingLayerGauge.Default, 3, 0.0,
        u(0.0), u(0.5), u(0.29), u(0.2), u(0.19), u(0.21),
    ))
    metal = tech.getLayer('Metal5')
    via = tech.getLayer('Metal4_Via4_Metal5')
    setEnclosures(via, metal, (u(0.125), u(0.05)))
    via = tech.getLayer('Metal5_TopVia1_TopMetal1')
    setEnclosures(via, metal, (u(0.01), u(0.74)))
    rg.addLayerGauge(CRL.RoutingLayerGauge.create(
        metal, CRL.RoutingLayerGauge.Vertical, CRL.RoutingLayerGauge.Default, 4, 0.0,
        u(0.0), u(0.65), u(0.39), u(0.2), u(0.42), u(0.21),
    ))
    metal = tech.getLayer('TopMetal1')
    via = tech.getLayer('Metal5_TopVia1_TopMetal1')
    setEnclosures(via, metal, (u(0.42), u(0.74)))
    via = tech.getLayer('TopMetal1_TopVia2_TopMetal2')
    setEnclosures(via, metal, (u(0.55), u(0.5)))
    rg.addLayerGauge(CRL.RoutingLayerGauge.create(
        metal, CRL.RoutingLayerGauge.Horizontal, CRL.RoutingLayerGauge.Default, 5, 0.0,
        u(0.0), u(3.54), u(1.9), u(1.64), u(0.9), u(1.64),
    ))
    metal = tech.getLayer('TopMetal2')
    via = tech.getLayer('TopMetal1_TopVia2_TopMetal2')
    setEnclosures(via, metal, (u(0.55), u(0.5)))
    rg.addLayerGauge(CRL.RoutingLayerGauge.create(
        metal, CRL.RoutingLayerGauge.Vertical, CRL.RoutingLayerGauge.PowerSupply, 6, 0.0,
        u(0.0), u(4.0), u(2.0), u(2.0), u(0.9), u(2.0),
    ))
    af.addRoutingGauge(rg)
    af.setRoutingGauge('StdCellLib')

    cg = CRL.CellGauge.create(
        'StdCellLib', 'Metal2',
        u(0.576), u(5.76), u(0.8),
    )
    af.addCellGauge(cg)
    af.setCellGauge('StdCellLib')

    # Place & Route setup
    with CfgCache(priority=Cfg.Parameter.Priority.ConfigurationFile) as cfg:
        env = af.getEnvironment()
        env.setRegister('^dff.*')
        cfg.lefImport.minTerminalWidth = 0.0
        cfg.crlcore.groundName = 'vss'
        cfg.crlcore.powerName = 'vdd'
        cfg.etesian.aspectRatio = 1.00
        cfg.etesian.aspectRatio = [10, 1000]
        cfg.etesian.spaceMargin = 0.10
        cfg.etesian.uniformDensity = True
        cfg.etesian.densityVariation = 0.05
        cfg.etesian.routingDriven = False
        cfg.etesian.latchUpDistance = u(30.0 - 1.0)
        cfg.etesian.diodeName = 'diode_w1'
        cfg.etesian.antennaInsertThreshold = 0.50
        cfg.etesian.tieName = None
        cfg.etesian.antennaGateMaxWL = u(500.0)
        cfg.etesian.antennaDiodeMaxWL = u(50000.0)
        cfg.etesian.feedNames = 'tie,decap_w0'
        cfg.etesian.defaultFeed = 'tie'
        cfg.etesian.cell.zero = 'zero_x1'
        cfg.etesian.cell.one = 'one_x1'
        cfg.etesian.bloat = 'disabled'
        cfg.etesian.effort = 2
        cfg.etesian.effort = (
            ('Fast', 1),
            ('Standard', 2),
            ('High', 3 ),
            ('Extreme', 4 ),
        )
        cfg.etesian.graphics = 2
        cfg.etesian.graphics = (
            ('Show every step', 1),
            ('Show lower bound', 2),
            ('Show result only', 3),
        )
        cfg.anabatic.routingGauge = 'StdCellLib'
        cfg.anabatic.globalLengthThreshold = 1450
        cfg.anabatic.saturateRatio = 0.90
        cfg.anabatic.saturateRp = 10
        cfg.anabatic.topRoutingLayer = 'TopMetal1'
        cfg.anabatic.edgeLength = 24
        cfg.anabatic.edgeWidth = 4
        cfg.anabatic.edgeCostH = 9.0
        cfg.anabatic.edgeCostK = -10.0
        cfg.anabatic.edgeHInc = 1.0
        cfg.anabatic.edgeHScaling = 1.0
        cfg.anabatic.globalIterations = 20
        cfg.anabatic.globalIterations = [ 1, 100 ]
        cfg.anabatic.gcell.displayMode = 1
        cfg.anabatic.gcell.displayMode = (("Boundary", 1), ("Density", 2))
        cfg.anabatic.searchHalo = 2
        cfg.katana.trackFill = 0
        cfg.katana.runRealignStage = True
        cfg.katana.hTracksReservedMin   = 4
        cfg.katana.hTracksReservedLocal = 20
        cfg.katana.hTracksReservedLocal = [0, 30]
        cfg.katana.vTracksReservedMin   = 4
        cfg.katana.vTracksReservedLocal = 20
        cfg.katana.vTracksReservedLocal = [0, 30]
        cfg.katana.termSatReservedLocal = 8
        cfg.katana.termSatThreshold = 9
        cfg.katana.eventsLimit = 4000002
        cfg.katana.ripupCost = 3
        cfg.katana.ripupCost = [0, None]
        cfg.katana.strapRipupLimit = 16
        cfg.katana.strapRipupLimit = [1, None]
        cfg.katana.localRipupLimit = 9
        cfg.katana.localRipupLimit = [1, None]
        cfg.katana.globalRipupLimit = 5
        cfg.katana.globalRipupLimit = [1, None]
        cfg.katana.longGlobalRipupLimit = 5
        cfg.chip.padCoreSide = 'South'

    # Plugins setup
    with CfgCache(priority=Cfg.Parameter.Priority.ConfigurationFile) as cfg:
        cfg.viewer.minimumSize = 500
        cfg.viewer.pixelThreshold = 10
        cfg.chip.block.rails.count = 5
        cfg.chip.block.rails.hWidth = u(2.68)
        cfg.chip.block.rails.vWidth = u(2.68)
        cfg.chip.block.rails.hSpacing = u(0.7)
        cfg.chip.block.rails.vSpacing = u(0.7)
        cfg.chip.supplyRailWidth = u(20.0)
        cfg.chip.supplyRailPitch = u(40.0)
        cfg.clockTree.placerEngine = 'Etesian'
        cfg.block.spareSide = 8*u(5.76)
        cfg.spares.buffer = 'buf_x4'
        cfg.spares.hfnsBuffer = 'buf_x4'
        cfg.spares.maxSinks = 31


def setup():
    from c4m.flexcell import coriolis_export_spec

    af = CRL.AllianceFramework.get()
    db = DataBase.getDB()
    tech = db.getTechnology()
    rootlib = db.getRootLibrary()

    lib = c4m_export.library2library(
        lib=c4m_ihpsg13g2.stdcelllib,
        pin_prim=c4m_tech.primitives["Metal1"], pin_dir="vertical",
        excl_cells=("Gallery",), spec=coriolis_export_spec,
        hurtech=tech, hurrootlib=rootlib,
    )
    _routing()

    spiceDir = Path(__file__).parent / 'libs.ref' / 'StdCellLib' / 'spice'
    Spice.load( lib, str(spiceDir / 'StdCellLib.spi'), Spice.PIN_ORDERING )
    for cell in lib.getCells():
        cell.setTerminalNetlist( True )

    return lib
