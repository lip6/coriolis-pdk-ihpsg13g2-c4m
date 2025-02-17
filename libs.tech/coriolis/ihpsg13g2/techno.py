
# Autogenerated file
# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
# Autogenerated file. Changes will be overwritten.

from coriolis import CRL, Hurricane, Viewer, Cfg
from coriolis.Hurricane import (
    Technology, DataBase, DbU, Library,
    Layer, BasicLayer,
    Cell, Net, Horizontal, Vertical, Rectilinear, Box, Point,
    NetExternalComponents,
)
from coriolis.technos.common.colors import toRGB
from coriolis.technos.common.patterns import toHexa
from coriolis.helpers import u
from coriolis.helpers.technology import createBL, createVia
from coriolis.helpers.overlay import CfgCache
from coriolis.helpers.analogtechno import Length, Area, Unit, Asymmetric, loadAnalogTechno

__all__ = ["analogTechnologyTable", "setup"]

analogTechnologyTable = (
    ('Header', 'IHPSG13G2', DbU.UnitPowerMicro, 'alpha'),
    ('PhysicalGrid', 0.005, Length, ''),

    ('minWidth', 'NWell', 0.62, Length, ''),
    ('minSpacing', 'NWell', 0.62, Length, ''),
    ('minWidth', 'pSD', 0.31, Length, ''),
    ('minSpacing', 'pSD', 0.31, Length, ''),
    ('minArea', 'pSD', 0.25, Area, ''),
    ('minWidth', 'ThickGateOx', 0.86, Length, ''),
    ('minSpacing', 'ThickGateOx', 0.86, Length, ''),
    ('minWidth', 'GatPoly', 0.13, Length, ''),
    ('minSpacing', 'GatPoly', 0.18, Length, ''),
    ('minArea', 'GatPoly', 0.09, Area, ''),
    ('minWidth', 'Activ', 0.15, Length, ''),
    ('minSpacing', 'Activ', 0.21, Length, ''),
    ('minArea', 'Activ', 0.122, Area, ''),
    ('minEnclosure', 'NWell', 'Activ', (0.31, 0.31), Length|Asymmetric, ''),
    ('minSpacing', 'NWell', 'Activ',  (0.31, 0.31), Length|Asymmetric, ''),
    # TODO for Activ:
    #    allow_in_substrate, implant_abut, allow_contactless_implant, allow_well_crossing
    ('minWidth', 'Metal1', 0.16, Length, ''),
    ('minSpacing', 'Metal1', 0.18, Length, ''),
    ('minArea', 'Metal1', 0.09, Area, ''),
    ('minWidth', 'Metal2', 0.2, Length, ''),
    ('minSpacing', 'Metal2', 0.21, Length, ''),
    ('minArea', 'Metal2', 0.144, Area, ''),
    ('minWidth', 'Metal3', 0.2, Length, ''),
    ('minSpacing', 'Metal3', 0.21, Length, ''),
    ('minArea', 'Metal3', 0.144, Area, ''),
    ('minWidth', 'Metal4', 0.2, Length, ''),
    ('minSpacing', 'Metal4', 0.21, Length, ''),
    ('minArea', 'Metal4', 0.144, Area, ''),
    ('minWidth', 'Metal5', 0.2, Length, ''),
    ('minSpacing', 'Metal5', 0.21, Length, ''),
    ('minArea', 'Metal5', 0.144, Area, ''),
    ('minWidth', 'TopMetal1', 1.64, Length, ''),
    ('minSpacing', 'TopMetal1', 1.64, Length, ''),
    ('minWidth', 'TopMetal2', 2.0, Length, ''),
    ('minSpacing', 'TopMetal2', 2.0, Length, ''),
    ('minWidth', 'Cont', 0.16, Length, ''),
    ('maxWidth', 'Cont', 0.16, Length, ''),
    ('minSpacing', 'Cont', 0.18, Length, ''),
    ('minEnclosure', 'Activ', 'Cont', (0.07, 0.07), Length|Asymmetric, ''),
    ('minEnclosure', 'GatPoly', 'Cont', (0.07, 0.07), Length|Asymmetric, ''),
    ('minEnclosure', 'Metal1', 'Cont', (0.0, 0.08), Length|Asymmetric, ''),
    ('minWidth', 'Via1', 0.19, Length, ''),
    ('maxWidth', 'Via1', 0.19, Length, ''),
    ('minSpacing', 'Via1', 0.22, Length, ''),
    ('minEnclosure', 'Metal1', 'Via1', (0.01, 0.05), Length|Asymmetric, ''),
    ('minEnclosure', 'Metal2', 'Via1', (0.005, 0.05), Length|Asymmetric, ''),
    ('minWidth', 'Via2', 0.19, Length, ''),
    ('maxWidth', 'Via2', 0.19, Length, ''),
    ('minSpacing', 'Via2', 0.22, Length, ''),
    ('minEnclosure', 'Metal2', 'Via2', (0.005, 0.05), Length|Asymmetric, ''),
    ('minEnclosure', 'Metal3', 'Via2', (0.005, 0.05), Length|Asymmetric, ''),
    ('minWidth', 'Via3', 0.19, Length, ''),
    ('maxWidth', 'Via3', 0.19, Length, ''),
    ('minSpacing', 'Via3', 0.22, Length, ''),
    ('minEnclosure', 'Metal3', 'Via3', (0.005, 0.05), Length|Asymmetric, ''),
    ('minEnclosure', 'Metal4', 'Via3', (0.005, 0.05), Length|Asymmetric, ''),
    ('minWidth', 'Via4', 0.19, Length, ''),
    ('maxWidth', 'Via4', 0.19, Length, ''),
    ('minSpacing', 'Via4', 0.22, Length, ''),
    ('minEnclosure', 'Metal4', 'Via4', (0.005, 0.05), Length|Asymmetric, ''),
    ('minEnclosure', 'Metal5', 'Via4', (0.005, 0.05), Length|Asymmetric, ''),
    ('minWidth', 'TopVia1', 0.42, Length, ''),
    ('maxWidth', 'TopVia1', 0.42, Length, ''),
    ('minSpacing', 'TopVia1', 0.42, Length, ''),
    ('minEnclosure', 'Metal5', 'TopVia1', (0.01, 0.01), Length|Asymmetric, ''),
    ('minEnclosure', 'TopMetal1', 'TopVia1', (0.42, 0.42), Length|Asymmetric, ''),
    ('minWidth', 'TopVia2', 0.9, Length, ''),
    ('maxWidth', 'TopVia2', 0.9, Length, ''),
    ('minSpacing', 'TopVia2', 1.06, Length, ''),
    ('minEnclosure', 'TopMetal1', 'TopVia2', (0.5, 0.5), Length|Asymmetric, ''),
    ('minEnclosure', 'TopMetal2', 'TopVia2', (0.5, 0.5), Length|Asymmetric, ''),
    # ('minTransistorL', 'hvmosgate', 0.45, Length, ''),
    # ('minTransistorW', 'hvmosgate', 0.3, Length, ''),
    # ('minGateExtension', 'Activ', 'hvmosgate', 0.23, Length|Asymmetric, ''),
    # ('minGateExtension', 'GatPoly', 'hvmosgate', 0.18, Length|Asymmetric, ''),
    # ('minGateSpacing', 'hvmosgate', 0.25, Length, ''),
    # ('minGateSpacing', 'Cont', 'hvmosgate', 0.11, Length|Asymmetric, ''),
    # ('minGateExtension', 'Activ', 'lvmosgate', 0.23, Length|Asymmetric, ''),
    # ('minGateExtension', 'GatPoly', 'lvmosgate', 0.18, Length|Asymmetric, ''),
    # ('minGateSpacing', 'Cont', 'lvmosgate', 0.11, Length|Asymmetric, ''),
    # ('minGateEnclosure', 'pSD', 'sg13g2_hv_pmos', (0.4, 0.4), Length|Asymmetric, ''),
    # ('minGateEnclosure', 'pSD', 'sg13g2_lv_pmos', (0.3, 0.3), Length|Asymmetric, ''),
    ('minWidth', 'Passiv', 40.0, Length, ''),
    ('minSpacing', 'Passiv', 3.5, Length, ''),
    ('minEnclosure', 'TopMetal2', 'Passiv', (2.1, 2.1), Length|Asymmetric, ''),
    ('minWidth', 'EXTBlock', 0.31, Length, ''),
    ('minSpacing', 'EXTBlock', 0.31, Length, ''),
    ('minWidth', 'SalBlock', 0.42, Length, ''),
    ('minSpacing', 'SalBlock', 0.42, Length, ''),
    # ('minWidth', 'Rppd', 0.5, Length, ''),
    # ('minSpacing', 'Rppd', 0.18, Length, ''),
    # ('minEnclosure', 'SalBlock', 'GatPoly', 0.2, Length|Asymmetric, ''),
    # ('minWidth', 'Rsil', 0.5, Length, ''),
    # ('minSpacing', 'Rsil', 0.18, Length, ''),
    # ('minEnclosure', 'RES', 'GatPoly', 0.0, Length|Asymmetric, ''),
    # ('minWidth', 'pdiode', 0.48, Length, ''),
    # ('minEnclosure', 'Recog.dio', 'Activ', (0.02, 0.02), Length|Asymmetric, ''),
    # ('minWidth', 'ndiode', 0.48, Length, ''),
    # ('minEnclosure', 'Recog.dio', 'Activ', (0.02, 0.02), Length|Asymmetric, ''),
    ('minSpacing', 'EXTBlock', 'pSD', 0.31, Length|Asymmetric, ''),
    ('minSpacing', 'Activ', 'ThickGateOx', 0.27, Length|Asymmetric, ''),
    # ('minSpacing', 'gate:mosfet:sg13g2_lv_nmos', 'pSD', 0.3, Length|Asymmetric, ''),
    # ('minSpacing', 'gate:mosfet:sg13g2_hv_nmos', 'pSD', 0.4, Length|Asymmetric, ''),
    ('minSpacing', 'GatPoly', 'EXTBlock', 0.18, Length|Asymmetric, ''),
    ('minSpacing', 'Activ', 'pSD', 0.18, Length|Asymmetric, ''),
    ('minSpacing', 'SalBlock', 'Activ', 0.2, Length|Asymmetric, ''),
    ('minSpacing', 'SalBlock', 'GatPoly', 0.2, Length|Asymmetric, ''),
    ('minSpacing', 'SalBlock', 'Cont', 0.2, Length|Asymmetric, ''),
    ('minSpacing', 'Activ', 'GatPoly', 0.07, Length|Asymmetric, ''),
    ('minSpacing', 'Cont', 'Activ', 0.14, Length|Asymmetric, ''),
    #('minSpacing', 'NWell', 'Activ', 0.24, Length|Asymmetric, ''),
)

def _setup_techno():
    db = DataBase.create()
    CRL.System.get()

    tech = Technology.create(db, 'IHPSG13G2')

    DbU.setPrecision(2)
    DbU.setPhysicalsPerGrid(0.005, DbU.UnitPowerMicro)
    with CfgCache(priority=Cfg.Parameter.Priority.ConfigurationFile) as cfg:
        cfg.gdsDriver.metricDbu = 1e-09
        cfg.gdsDriver.dbuPerUu = 0.001
    DbU.setGridsPerLambda(26)
    DbU.setSymbolicSnapGridStep(DbU.fromGrid(1.0))
    DbU.setPolygonStep(DbU.fromGrid(1.0))
    DbU.setStringMode(DbU.StringModePhysical, DbU.UnitPowerMicro)

    createBL(
        tech, 'NWell', BasicLayer.Material.nWell,
        size=u(0.62), spacing=u(0.62), gds2Layer=31, gds2DataType=0,
    )
    createBL(
        tech, 'NWell.pin', BasicLayer.Material.nWell,
        gds2Layer=31, gds2DataType=2,
    )
    createBL(
        tech, 'PWell.block', BasicLayer.Material.pWell,
        size=u(0.62), spacing=u(0.62), gds2Layer=46, gds2DataType=21,
    )
    createBL(
        tech, 'nSD', BasicLayer.Material.nImplant,
        size=u(0.31), spacing=u(0.31), area=0.25, gds2Layer=7, gds2DataType=0,
    )
    createBL(
        tech, 'nSD.block', BasicLayer.Material.nImplant,
        size=u(0.31), spacing=u(0.31), area=0.25, gds2Layer=7, gds2DataType=21,
    )
    createBL(
        tech, 'pSD', BasicLayer.Material.pImplant,
        size=u(0.31), spacing=u(0.31), area=0.25, gds2Layer=14, gds2DataType=0,
    )
    createBL(
        tech, 'ThickGateOx', BasicLayer.Material.other,
        gds2Layer=44, gds2DataType=0,
    )

    createBL(
        tech, 'GatPoly', BasicLayer.Material.poly,
        size=u(0.13), spacing=u(0.18), area=0.09, gds2Layer=5, gds2DataType=0,
    )
    createBL(
        tech, 'GatPoly.pin', BasicLayer.Material.other,
        gds2Layer=5, gds2DataType=2,
    )
    createBL(
        tech, 'GatPoly.nofill', BasicLayer.Material.blockage,
        gds2Layer=5, gds2DataType=23,
    )

    createBL(
        tech, 'Activ', BasicLayer.Material.active,
        size=u(0.15), spacing=u(0.21), area=0.122, gds2Layer=1, gds2DataType=0,
    )
    createBL(
        tech, 'Activ.pin', BasicLayer.Material.other,
        gds2Layer=1, gds2DataType=2,
    )
    createBL(
        tech, 'Activ.mask', BasicLayer.Material.other,
        gds2Layer=1, gds2DataType=20,
    )
    createBL(
        tech, 'Activ.nofill', BasicLayer.Material.blockage,
        gds2Layer=1, gds2DataType=23,
    )
    createBL(
        tech, 'Activ.noqrc', BasicLayer.Material.other,
        gds2Layer=1, gds2DataType=28,
    )

    createBL(
        tech, 'Cont', BasicLayer.Material.cut,
        size=u(0.16), spacing=u(0.18), gds2Layer=6, gds2DataType=0,
    )
    createBL(
        tech, 'Cont.nofill', BasicLayer.Material.blockage,
        size=u(0.16), spacing=u(0.18), gds2Layer=6, gds2DataType=23,
    )

    createBL(
        tech, 'Metal1', BasicLayer.Material.metal,
        size=u(0.16), spacing=u(0.18), area=0.09, gds2Layer=8, gds2DataType=0,
    )
    createBL(
        tech, 'Metal1.pin', BasicLayer.Material.other,
        gds2Layer=8, gds2DataType=2,
    )
    createBL(
        tech, 'Metal1.filler', BasicLayer.Material.blockage,
        gds2Layer=8, gds2DataType=22,
    )
    createBL(
        tech, 'Metal1.nofill', BasicLayer.Material.blockage,
        gds2Layer=8, gds2DataType=23,
    )
    createBL(
        tech, 'Metal1.res', BasicLayer.Material.other,
        gds2Layer=8, gds2DataType=29,
    )
    createBL(
        tech, 'Metal1_iprobe', BasicLayer.Material.other,
        size=u(0.16), spacing=u(0.18), area=0.09, gds2Layer=8, gds2DataType=33,
    )
    createBL(
        tech, 'Metal1_diffprb', BasicLayer.Material.other,
        size=u(0.16), spacing=u(0.18), area=0.09, gds2Layer=8, gds2DataType=34,
    )
    createBL(
        tech, 'Metal1.noqrc', BasicLayer.Material.blockage,
        gds2Layer=8, gds2DataType=28,
    )

    createBL(
        tech, 'Via1', BasicLayer.Material.cut,
        size=u(0.19), spacing=u(0.22), gds2Layer=19, gds2DataType=0,
    )
    createBL(
        tech, 'Via1.nofill', BasicLayer.Material.blockage,
        size=u(0.19), spacing=u(0.22), gds2Layer=19, gds2DataType=23,
    )

    createBL(
        tech, 'Metal2', BasicLayer.Material.metal,
        size=u(0.2), spacing=u(0.21), area=0.144, gds2Layer=10, gds2DataType=0,
    )
    createBL(
        tech, 'Metal2.pin', BasicLayer.Material.other,
        gds2Layer=10, gds2DataType=2,
    )
    createBL(
        tech, 'Metal2.filler', BasicLayer.Material.other,
        gds2Layer=10, gds2DataType=22,
    )
    createBL(
        tech, 'Metal2.nofill', BasicLayer.Material.blockage,
        gds2Layer=10, gds2DataType=23,
    )
    createBL(
        tech, 'Metal2.noqrc', BasicLayer.Material.blockage,
        gds2Layer=10, gds2DataType=28,
    )

    createBL(
        tech, 'Via2', BasicLayer.Material.cut,
        size=u(0.19), spacing=u(0.22), gds2Layer=29, gds2DataType=0
    )
    createBL(
        tech, 'Via2.nofill', BasicLayer.Material.blockage,
        size=u(0.19), spacing=u(0.22), gds2Layer=29, gds2DataType=23
    )

    createBL(
        tech, 'Metal3', BasicLayer.Material.metal,
        size=u(0.2), spacing=u(0.21), area=0.144, gds2Layer=30, gds2DataType=0,
    )
    createBL(
        tech, 'Metal3.pin', BasicLayer.Material.other,
        gds2Layer=30, gds2DataType=2
    )
    createBL(
        tech, 'Metal3.noqrc', BasicLayer.Material.blockage,
        gds2Layer=30, gds2DataType=28,
    )
    createBL(
        tech, 'Metal3.filler', BasicLayer.Material.blockage,
        gds2Layer=30, gds2DataType=22,
    )
    createBL(
        tech, 'Metal3.nofill', BasicLayer.Material.blockage,
        gds2Layer=30, gds2DataType=23,
    )

    createBL(
        tech, 'Via3', BasicLayer.Material.cut,
        size=u(0.19), spacing=u(0.22), gds2Layer=49, gds2DataType=0,
    )
    createBL(
        tech, 'Via3.nofill', BasicLayer.Material.blockage,
        size=u(0.19), spacing=u(0.22), gds2Layer=49, gds2DataType=23,
    )

    createBL(
        tech, 'Metal4', BasicLayer.Material.metal,
        size=u(0.2), spacing=u(0.21), area=0.144, gds2Layer=50, gds2DataType=0,
    )
    createBL(
        tech, 'Metal4.pin', BasicLayer.Material.other,
        gds2Layer=50, gds2DataType=2,
    )
    createBL(
        tech, 'Metal4.filler', BasicLayer.Material.other,
        gds2Layer=50, gds2DataType=22,
    )
    createBL(
        tech, 'Metal4.nofill', BasicLayer.Material.blockage,
        gds2Layer=50, gds2DataType=23,
    )
    createBL(
        tech, 'Metal4.noqrc', BasicLayer.Material.blockage,
        gds2Layer=50, gds2DataType=28,
    )

    createBL(
        tech, 'Via4', BasicLayer.Material.cut,
        size=u(0.19), spacing=u(0.22), gds2Layer=66, gds2DataType=0,
    )
    createBL(
        tech, 'Via4.nofill', BasicLayer.Material.blockage,
        size=u(0.19), spacing=u(0.22), gds2Layer=66, gds2DataType=23,
    )

    createBL(
        tech, 'Metal5', BasicLayer.Material.metal,
        size=u(0.2), spacing=u(0.21), area=0.144, gds2Layer=67, gds2DataType=0,
    )
    createBL(
        tech, 'Metal5.pin', BasicLayer.Material.other,
        gds2Layer=67, gds2DataType=2,
    )
    createBL(
        tech, 'Metal5.filler', BasicLayer.Material.other,
        gds2Layer=67, gds2DataType=2,
    )
    createBL(
        tech, 'Metal5.nofill', BasicLayer.Material.blockage,
        gds2Layer=67, gds2DataType=23,
    )
    createBL(
        tech, 'Metal5.noqrc', BasicLayer.Material.blockage,
        gds2Layer=67, gds2DataType=28,
    )

    createBL(
        tech, 'TopVia1', BasicLayer.Material.cut,
        size=u(0.42), spacing=u(0.42), gds2Layer=125, gds2DataType=0,
    )
    createBL(
        tech, 'TopVia1.nofill', BasicLayer.Material.blockage,
        size=u(0.42), spacing=u(0.42), gds2Layer=125, gds2DataType=23,
    )

    createBL(
        tech, 'TopMetal1', BasicLayer.Material.metal,
        size=u(1.64), spacing=u(1.64), gds2Layer=126, gds2DataType=0,
    )
    createBL(
        tech, 'TopMetal1.pin', BasicLayer.Material.other,
        gds2Layer=126, gds2DataType=2,
    )
    createBL(
        tech, 'TopMetal1.nofill', BasicLayer.Material.blockage,
        gds2Layer=126, gds2DataType=23,
    )
    createBL(
        tech, 'TopMetal1.noqrc', BasicLayer.Material.blockage,
        gds2Layer=126, gds2DataType=28,
    )

    createBL(
        tech, 'TopVia2', BasicLayer.Material.cut,
        size=u(0.9), spacing=u(1.06), gds2Layer=133, gds2DataType=0,
    )
    createBL(
        tech, 'TopVia2.nofill', BasicLayer.Material.blockage,
        size=u(0.9), spacing=u(1.06), gds2Layer=133, gds2DataType=23,
    )

    createBL(
        tech, 'TopMetal2', BasicLayer.Material.metal,
        size=u(2.0), spacing=u(2.0), gds2Layer=134, gds2DataType=0,
    )
    createBL(
        tech, 'TopMetal2.pin', BasicLayer.Material.other,
        gds2Layer=134, gds2DataType=2,
    )
    createBL(
        tech, 'TopMetal2.nofill', BasicLayer.Material.blockage,
        gds2Layer=134, gds2DataType=23,
    )


    # Out of order from substrate distance
    # ====================================

    createBL(
        tech, 'Substrate', BasicLayer.Material.other,
        gds2Layer=40, gds2DataType=0,
    )
    createBL(
        tech, 'Passiv', BasicLayer.Material.cut,
        size=u(40.0), spacing=u(3.5), gds2Layer=9, gds2DataType=0,
    )
    createBL(
        tech, 'EXTBlock', BasicLayer.Material.other,
        size=u(0.31), spacing=u(0.31), gds2Layer=111, gds2DataType=0,
    )
    createBL(
        tech, 'RES', BasicLayer.Material.other,
        gds2Layer=24, gds2DataType=0,
    )
    createBL(
        tech, 'TRANS', BasicLayer.Material.other,
        gds2Layer=26, gds2DataType=0,
    )
    createBL(
        tech, 'IND', BasicLayer.Material.other,
        gds2Layer=27, gds2DataType=0,
    )
    createBL(
        tech, 'IND.pin', BasicLayer.Material.other,
        gds2Layer=27, gds2DataType=2,
    )
    createBL(
        tech, 'IND.datatype_4', BasicLayer.Material.other,
        gds2Layer=27, gds2DataType=4,
    )
    createBL(
        tech, 'IND.text', BasicLayer.Material.other,
        gds2Layer=27, gds2DataType=25,
    )
    createBL(
        tech, 'SalBlock', BasicLayer.Material.other,
        gds2Layer=28, gds2DataType=0,
    )
    createBL(
        tech, 'nBuLay', BasicLayer.Material.other,
        gds2Layer=32, gds2DataType=0,
    )
    createBL(
        tech, 'EmWind', BasicLayer.Material.other,
        gds2Layer=33, gds2DataType=0,
    )
    createBL(
        tech, 'MIM', BasicLayer.Material.other,
        gds2Layer=36, gds2DataType=0,
    )
    createBL(
        tech, 'Recog.dio', BasicLayer.Material.other,
        gds2Layer=99, gds2DataType=31,
    )
    createBL(
        tech, 'Recog.esd', BasicLayer.Material.other,
        gds2Layer=99, gds2DataType=30,
    )
    createBL(
        tech, 'HeatTrans', BasicLayer.Material.other,
        gds2Layer=51, gds2DataType=0,
    )
    createBL(
        tech, 'HeatRes', BasicLayer.Material.other,
        gds2Layer=52, gds2DataType=0,
    )
    createBL(
        tech, 'MemCap', BasicLayer.Material.other,
        gds2Layer=69, gds2DataType=0,
    )
    createBL(
        tech, 'PolyRes', BasicLayer.Material.other,
        gds2Layer=128, gds2DataType=0,
    )
    createBL(
        tech, 'EmWiHV', BasicLayer.Material.other,
        gds2Layer=156, gds2DataType=0,
    )
    createBL(
        tech, 'Vmim', BasicLayer.Material.other,
        gds2Layer=129, gds2DataType=0,
    )
    createBL(
        tech, 'NoRCX', BasicLayer.Material.other,
        gds2Layer=148, gds2DataType=0,
    )
    createBL(
        tech, 'DeepVia', BasicLayer.Material.other,
        gds2Layer=152, gds2DataType=0,
    )
    createBL(
        tech, 'gds236.datatype_0', BasicLayer.Material.other,
        gds2Layer=236, gds2DataType=0,
    )
    createBL(
        tech, 'gds236.datatype_1', BasicLayer.Material.other,
        gds2Layer=236, gds2DataType=1,
    )
    createBL(
        tech, 'EdgeSeal.datatype_0', BasicLayer.Material.other,
        gds2Layer=39, gds2DataType=0,
    )
    createBL(
        tech, 'EdgeSeal.datatype_4', BasicLayer.Material.other,
        gds2Layer=39, gds2DataType=4,
    )
    createBL(
        tech, 'dfpad', BasicLayer.Material.other,
        gds2Layer=41, gds2DataType=0,
    )
    createBL(
        tech, 'dfpad.pillar', BasicLayer.Material.other,
        gds2Layer=41, gds2DataType=35,
    )
    createBL(
        tech, 'TEXT', BasicLayer.Material.other,
        gds2Layer=63, gds2DataType=0,
    )
    createBL(
        tech, 'Recog', BasicLayer.Material.other,
        gds2Layer=99, gds2DataType=0,
    )
    createBL(
        tech, 'Recog.tsv', BasicLayer.Material.other,
        gds2Layer=99, gds2DataType=32,
    )
    createBL(
        tech, 'prBoundary', BasicLayer.Material.other,
        gds2Layer=189, gds2DataType=0,
    )

    Substrate_Label = createBL( tech, 'Substrate_Label', BasicLayer.Material.info, gds2Layer=40 , gds2DataType=25 )
    Metal1_Label    = createBL( tech, 'Metal1_Label'   , BasicLayer.Material.info, gds2Layer=8  , gds2DataType=25 )
    Metal2_Label    = createBL( tech, 'Metal2_Label'   , BasicLayer.Material.info, gds2Layer=10 , gds2DataType=25 )
    Metal3_Label    = createBL( tech, 'Metal3_Label'   , BasicLayer.Material.info, gds2Layer=30 , gds2DataType=25 )
    Metal4_Label    = createBL( tech, 'Metal4_Label'   , BasicLayer.Material.info, gds2Layer=50 , gds2DataType=25 )
    Metal5_Label    = createBL( tech, 'Metal5_Label'   , BasicLayer.Material.info, gds2Layer=67 , gds2DataType=25 )
    TopMetal1_Label = createBL( tech, 'TopMetal1_Label', BasicLayer.Material.info, gds2Layer=126, gds2DataType=25 )
    TopMetal2_Label = createBL( tech, 'TopMetal2_Label', BasicLayer.Material.info, gds2Layer=134, gds2DataType=25 )

    # ContLayers
    # GatePoly<>Cont<>Metal1
    createVia(
        tech, 'GatPoly_Via1_Metal1', 'GatPoly', 'Cont', 'Metal1',
        u(0.16),
    )
    # Activ<>Cont<>Metal1
    createVia(
        tech, 'Activ_Via1_Metal1', 'Activ', 'Cont', 'Metal1',
        u(0.16),
    )

    # ViaLayers
    # Metal1<>Via1<>Metal2
    createVia(
        tech, 'Metal1_Via1_Metal2', 'Metal1', 'Via1', 'Metal2',
        u(0.19),
    )
    # Metal2<>Via2<>Metal3
    createVia(
        tech, 'Metal2_Via2_Metal3', 'Metal2', 'Via2', 'Metal3',
        u(0.19),
    )
    # Metal3<>Via3<>Metal4
    createVia(
        tech, 'Metal3_Via3_Metal4', 'Metal3', 'Via3', 'Metal4',
        u(0.19),
    )
    # Metal4<>Via4<>Metal5
    createVia(
        tech, 'Metal4_Via4_Metal5', 'Metal4', 'Via4', 'Metal5',
        u(0.19),
    )
    # Metal5<>TopVia1<>TopMetal1
    createVia(
        tech, 'Metal5_TopVia1_TopMetal1', 'Metal5', 'TopVia1', 'TopMetal1',
        u(0.42),
    )
    # TopMetal1<>TopVia2<>TopMetal2
    createVia(
        tech, 'TopMetal1_TopVia2_TopMetal2', 'TopMetal1', 'TopVia2', 'TopMetal2',
        u(0.9),
    )

    # Blockages
    tech.getLayer('GatPoly'  ).setBlockageLayer( tech.getLayer('GatPoly.nofill') )
    tech.getLayer('Activ'    ).setBlockageLayer( tech.getLayer('Activ.nofill') )
    tech.getLayer('Metal1'   ).setBlockageLayer( tech.getLayer('Metal1.nofill') )
    tech.getLayer('Metal2'   ).setBlockageLayer( tech.getLayer('Metal2.nofill') )
    tech.getLayer('Metal3'   ).setBlockageLayer( tech.getLayer('Metal3.nofill') )
    tech.getLayer('Metal4'   ).setBlockageLayer( tech.getLayer('Metal4.nofill') )
    tech.getLayer('Metal5'   ).setBlockageLayer( tech.getLayer('Metal5.nofill') )
    tech.getLayer('TopMetal1').setBlockageLayer( tech.getLayer('TopMetal1.nofill') )
    tech.getLayer('TopMetal2').setBlockageLayer( tech.getLayer('TopMetal2.nofill') )
    tech.getLayer('Cont'     ).setBlockageLayer( tech.getLayer('Cont.nofill') )
    tech.getLayer('Via1'     ).setBlockageLayer( tech.getLayer('Via1.nofill') )
    tech.getLayer('Via2'     ).setBlockageLayer( tech.getLayer('Via2.nofill') )
    tech.getLayer('Via3'     ).setBlockageLayer( tech.getLayer('Via3.nofill') )
    tech.getLayer('Via4'     ).setBlockageLayer( tech.getLayer('Via4.nofill') )
    tech.getLayer('TopVia1'  ).setBlockageLayer( tech.getLayer('TopVia1.nofill') )
    tech.getLayer('TopVia2'  ).setBlockageLayer( tech.getLayer('TopVia2.nofill') )

    # Coriolis internal layers
    createBL(
        tech, 'text.cell', BasicLayer.Material.other,
    )
    createBL(
        tech, 'text.instance', BasicLayer.Material.other,
    )
    createBL(
        tech, 'SPL1', BasicLayer.Material.other,
    )
    createBL(
        tech, 'AutoLayer', BasicLayer.Material.other,
    )
    createBL(
        tech, 'gmetalh', BasicLayer.Material.metal,
    )
    createBL(
        tech, 'gcontact', BasicLayer.Material.cut,
    )
    createBL(
        tech, 'gmetalv', BasicLayer.Material.metal,
    )

    # Resistors
    # ResistorLayer.create(tech, 'Rppd', 'GatPoly', 'SalBlock')
    # ResistorLayer.create(tech, 'Rsil', 'GatPoly', 'RES')

    # Capacitors

    # Transistors
    # GateLayer.create(tech, 'hvmosgate', 'Activ', 'GatPoly', 'ThickGateOx')
    # GateLayer.create(tech, 'lvmosgate', 'Activ', 'GatPoly')
    # TransistorLayer.create(tech, 'sg13g2_hv_nmos', 'hvmosgate', ())
    # TransistorLayer.create(tech, 'sg13g2_hv_pmos', 'hvmosgate', 'pSD', 'NWell')
    # TransistorLayer.create(tech, 'sg13g2_lv_nmos', 'lvmosgate', ())
    # TransistorLayer.create(tech, 'sg13g2_lv_pmos', 'lvmosgate', 'pSD', 'NWell')

    # Bipolars

def _setup_display():
    # ----------------------------------------------------------------------
    # Style: Alliance.Classic [black]

    threshold = 0.2 if Viewer.Graphics.isHighDpi() else 0.1

    style = Viewer.DisplayStyle( 'Alliance.Classic [black]' )
    style.setDescription( 'Alliance Classic Look - black background' )
    style.setDarkening  ( Viewer.DisplayStyle.HSVr(1.0, 3.0, 2.5) )

    # Viewer.
    style.addDrawingStyle( group='Viewer', name='fallback'      , color=toRGB('Gray238'    ), border=1, pattern='55AA55AA55AA55AA' )
    style.addDrawingStyle( group='Viewer', name='background'    , color=toRGB('Gray50'     ), border=1 )
    style.addDrawingStyle( group='Viewer', name='foreground'    , color=toRGB('White'      ), border=1 )
    style.addDrawingStyle( group='Viewer', name='rubber'        , color=toRGB('192,0,192'  ), border=4, threshold=0.02 )
    style.addDrawingStyle( group='Viewer', name='phantom'       , color=toRGB('Seashell4'  ), border=1 )
    style.addDrawingStyle( group='Viewer', name='boundaries'    , color=toRGB('wheat1'     ), border=2, pattern='0000000000000000', threshold=0 )
    style.addDrawingStyle( group='Viewer', name='prBoundary'    , color=toRGB('wheat1'     ), border=2, pattern='0000000000000000', threshold=0 )
    style.addDrawingStyle( group='Viewer', name='marker'        , color=toRGB('80,250,80'  ), border=1 )
    style.addDrawingStyle( group='Viewer', name='selectionDraw' , color=toRGB('White'      ), border=1 )
    style.addDrawingStyle( group='Viewer', name='selectionFill' , color=toRGB('White'      ), border=1 )
    style.addDrawingStyle( group='Viewer', name='grid'          , color=toRGB('White'      ), border=1, threshold=2.0 )
    style.addDrawingStyle( group='Viewer', name='spot'          , color=toRGB('White'      ), border=2, threshold=6.0 )
    style.addDrawingStyle( group='Viewer', name='ghost'         , color=toRGB('White'      ), border=1 )
    style.addDrawingStyle( group='Viewer', name='text.ruler'    , color=toRGB('White'      ), border=1, threshold=  0.0 )
    style.addDrawingStyle( group='Viewer', name='text.instance' , color=toRGB('White'      ), border=1, threshold=400.0 )
    style.addDrawingStyle( group='Viewer', name='text.reference', color=toRGB('White'      ), border=1, threshold=200.0 )
    style.addDrawingStyle( group='Viewer', name='undef'         , color=toRGB('Violet'     ), border=0, pattern='2244118822441188' )

    # Active Layers.
    style.addDrawingStyle(group='Active Layers', name='NWell', color=toRGB('Tan'), pattern=toHexa('urgo.8'), border=1, threshold=threshold)
    style.addDrawingStyle(group='Active Layers', name='pSD', color=toRGB('Yellow'), pattern=toHexa('antihash0.8'), border=1, threshold=threshold)
    style.addDrawingStyle(group='Active Layers', name='EXTBlock', color=toRGB('Yellow'), pattern=toHexa('antihash0.8'), border=1, threshold=threshold)
    style.addDrawingStyle(group='Active Layers', name='Activ', color=toRGB('White'), pattern=toHexa('antihash0.8'), border=1, threshold=threshold)
    style.addDrawingStyle(group='Active Layers', name='Activ.pin', color=toRGB('White'), pattern=toHexa('antihash0.8'), border=2, threshold=threshold)
    style.addDrawingStyle(group='Active Layers', name='GatPoly', color=toRGB('Red'), pattern=toHexa('antihash0.8'), border=1, threshold=threshold)
    style.addDrawingStyle(group='Active Layers', name='GatPoly.pin', color=toRGB('Red'), pattern=toHexa('antihash0.8'), border=2, threshold=threshold)

    # Routing Layers.
    style.addDrawingStyle(group='Routing Layers', name='Metal1', color=toRGB('Blue'), pattern=toHexa('slash.8'), border=1, threshold=threshold)
    style.addDrawingStyle(group='Routing Layers', name='Metal1.pin', color=toRGB('Blue'), pattern=toHexa('slash.8'), border=2, threshold=threshold)
    style.addDrawingStyle(group='Routing Layers', name='Metal2', color=toRGB('Aqua'), pattern=toHexa('poids4.8'), border=1, threshold=threshold)
    style.addDrawingStyle(group='Routing Layers', name='Metal2.pin', color=toRGB('Aqua'), pattern=toHexa('poids4.8'), border=2, threshold=threshold)
    style.addDrawingStyle(group='Routing Layers', name='Metal3', color=toRGB('LightPink'), pattern=toHexa('poids4.8'), border=1, threshold=threshold)
    style.addDrawingStyle(group='Routing Layers', name='Metal3.pin', color=toRGB('LightPink'), pattern=toHexa('poids4.8'), border=2, threshold=threshold)
    style.addDrawingStyle(group='Routing Layers', name='Metal4', color=toRGB('Green'), pattern=toHexa('poids4.8'), border=1, threshold=threshold)
    style.addDrawingStyle(group='Routing Layers', name='Metal4.pin', color=toRGB('Green'), pattern=toHexa('poids4.8'), border=2, threshold=threshold)
    style.addDrawingStyle(group='Routing Layers', name='Metal5', color=toRGB('Yellow'), pattern=toHexa('poids4.8'), border=1, threshold=threshold)
    style.addDrawingStyle(group='Routing Layers', name='Metal5.pin', color=toRGB('Yellow'), pattern=toHexa('poids4.8'), border=2, threshold=threshold)
    style.addDrawingStyle(group='Routing Layers', name='TopMetal1', color=toRGB('Violet'), pattern=toHexa('poids4.8'), border=1, threshold=threshold)
    style.addDrawingStyle(group='Routing Layers', name='TopMetal1.pin', color=toRGB('Violet'), pattern=toHexa('poids4.8'), border=2, threshold=threshold)
    style.addDrawingStyle(group='Routing Layers', name='TopMetal2', color=toRGB('Red'), pattern=toHexa('poids4.8'), border=1, threshold=threshold)
    style.addDrawingStyle(group='Routing Layers', name='TopMetal2.pin', color=toRGB('Red'), pattern=toHexa('poids4.8'), border=2, threshold=threshold)

    # Cuts (VIA holes).
    style.addDrawingStyle(group='Cuts (VIA holes)', name='Cont', color=toRGB('0,150,150'), threshold=threshold)
    style.addDrawingStyle(group='Cuts (VIA holes)', name='Via1', color=toRGB('Aqua'), threshold=threshold)
    style.addDrawingStyle(group='Cuts (VIA holes)', name='Via2', color=toRGB('LightPink'), threshold=threshold)
    style.addDrawingStyle(group='Cuts (VIA holes)', name='Via3', color=toRGB('Green'), threshold=threshold)
    style.addDrawingStyle(group='Cuts (VIA holes)', name='Via4', color=toRGB('Yellow'), threshold=threshold)
    style.addDrawingStyle(group='Cuts (VIA holes)', name='TopVia1', color=toRGB('Violet'), threshold=threshold)
    style.addDrawingStyle(group='Cuts (VIA holes)', name='TopVia2', color=toRGB('Red'), threshold=threshold)
    style.addDrawingStyle(group='Cuts (VIA holes)', name='Passiv', color=toRGB('Blue'), threshold=threshold)

    # Filler Layers.
    style.addDrawingStyle(group='Filler Layers', name='Metal1.filler', color=toRGB('Blue'), pattern=toHexa('slash.8'), border=2, threshold=threshold)
    style.addDrawingStyle(group='Filler Layers', name='Metal2.filler', color=toRGB('Aqua'), pattern=toHexa('poids4.8'), border=2, threshold=threshold)
    style.addDrawingStyle(group='Filler Layers', name='Metal3.filler', color=toRGB('LightPink'), pattern=toHexa('poids4.8'), border=2, threshold=threshold)
    style.addDrawingStyle(group='Filler Layers', name='Metal4.filler', color=toRGB('Green'), pattern=toHexa('poids4.8'), border=2, threshold=threshold)
    style.addDrawingStyle(group='Filler Layers', name='Metal5.filler', color=toRGB('Yellow'), pattern=toHexa('poids4.8'), border=2, threshold=threshold)
    style.addDrawingStyle(group='Filler Layers', name='TopMetal1.filler', color=toRGB('Violet'), pattern=toHexa('poids4.8'), border=2, threshold=threshold)
    style.addDrawingStyle(group='Filler Layers', name='TopMetal2.filler', color=toRGB('Red'), pattern=toHexa('poids4.8'), border=2, threshold=threshold)
    style.addDrawingStyle(group='Filler Layers', name='Cont.filler', color=toRGB('0,150,150'), threshold=threshold)
    style.addDrawingStyle(group='Filler Layers', name='Via1.filler', color=toRGB('Aqua'), threshold=threshold)
    style.addDrawingStyle(group='Filler Layers', name='Via2.filler', color=toRGB('LightPink'), threshold=threshold)
    style.addDrawingStyle(group='Filler Layers', name='Via3.filler', color=toRGB('Green'), threshold=threshold)
    style.addDrawingStyle(group='Filler Layers', name='Via4.filler', color=toRGB('Yellow'), threshold=threshold)
    style.addDrawingStyle(group='Filler Layers', name='TopVia1.filler', color=toRGB('Violet'), threshold=threshold)
    style.addDrawingStyle(group='Filler Layers', name='TopVia2.filler', color=toRGB('Red'), threshold=threshold)
    style.addDrawingStyle(group='Filler Layers', name='Passiv.filler', color=toRGB('Blue'), threshold=threshold)

    # Blockages.
    style.addDrawingStyle(group='Blockages', name='GatPoly.nofill', color=toRGB('Blue'), pattern=toHexa('slash.8'), border=4, threshold=threshold)
    style.addDrawingStyle(group='Blockages', name='Activ.nofill', color=toRGB('Aqua'), pattern=toHexa('poids4.8'), border=4, threshold=threshold)
    style.addDrawingStyle(group='Blockages', name='Metal1.nofill', color=toRGB('LightPink'), pattern=toHexa('poids4.8'), border=4, threshold=threshold)
    style.addDrawingStyle(group='Blockages', name='Metal2.nofill', color=toRGB('Green'), pattern=toHexa('poids4.8'), border=4, threshold=threshold)
    style.addDrawingStyle(group='Blockages', name='Metal3.nofill', color=toRGB('Yellow'), pattern=toHexa('poids4.8'), border=4, threshold=threshold)
    style.addDrawingStyle(group='Blockages', name='Metal4.nofill', color=toRGB('Violet'), pattern=toHexa('poids4.8'), border=4, threshold=threshold)
    style.addDrawingStyle(group='Blockages', name='Metal5.nofill', color=toRGB('Red'), pattern=toHexa('poids4.8'), border=4, threshold=threshold)
    style.addDrawingStyle(group='Blockages', name='TopMetal1.nofill', color=toRGB('Blue'), pattern=toHexa('poids4.8'), border=4, threshold=threshold)
    style.addDrawingStyle(group='Blockages', name='TopMetal2.nofill', color=toRGB('Aqua'), pattern=toHexa('poids4.8'), border=4, threshold=threshold)
    style.addDrawingStyle(group='Blockages', name='Cont.nofill', color=toRGB('LightPink'), pattern=toHexa('poids4.8'), border=4, threshold=threshold)
    style.addDrawingStyle(group='Blockages', name='Via1.nofill', color=toRGB('Green'), pattern=toHexa('poids4.8'), border=4, threshold=threshold)
    style.addDrawingStyle(group='Blockages', name='Via2.nofill', color=toRGB('Yellow'), pattern=toHexa('poids4.8'), border=4, threshold=threshold)
    style.addDrawingStyle(group='Blockages', name='Via3.nofill', color=toRGB('Violet'), pattern=toHexa('poids4.8'), border=4, threshold=threshold)
    style.addDrawingStyle(group='Blockages', name='Via4.nofill', color=toRGB('Red'), pattern=toHexa('poids4.8'), border=4, threshold=threshold)
    style.addDrawingStyle(group='Blockages', name='TopVia1.nofill', color=toRGB('Blue'), pattern=toHexa('poids4.8'), border=4, threshold=threshold)
    style.addDrawingStyle(group='Blockages', name='TopVia2.nofill', color=toRGB('Aqua'), pattern=toHexa('poids4.8'), border=4, threshold=threshold)

    # Group: Text.
    style.addDrawingStyle( group='Text', name='TEXT'           , color=toRGB('White'    ), border=1, threshold=400.0 )
    style.addDrawingStyle( group='Text', name='Substrate_Label', color=toRGB('Red'      ), pattern='55AA55AA55AA55AA'         , threshold=threshold )
    style.addDrawingStyle( group='Text', name='Metal1_Label'   , color=toRGB('Blue'     ), pattern=toHexa('poids2.8'         ), threshold=threshold )
    style.addDrawingStyle( group='Text', name='Metal2_Label'   , color=toRGB('Aqua'     ), pattern=toHexa('light_antihash0.8'), threshold=threshold )
    style.addDrawingStyle( group='Text', name='Metal3_Label'   , color=toRGB('LightPink'), pattern=toHexa('light_antihash1.8'), threshold=threshold )
    style.addDrawingStyle( group='Text', name='Metal4_Label'   , color=toRGB('Green'    ), pattern=toHexa('light_antihash2.8'), threshold=threshold )
    style.addDrawingStyle( group='Text', name='Metal5_Label'   , color=toRGB('Yellow'   ), pattern='1144114411441144'         , threshold=threshold )
    style.addDrawingStyle( group='Text', name='TopMetal1_Label', color=toRGB('Violet'   ), pattern=toHexa('poids4.8'         ), threshold=threshold )
    style.addDrawingStyle( group='Text', name='TopMetal2_Label', color=toRGB('Red'      ), pattern=toHexa('poids4.8'         ), threshold=threshold )

    # Knick & Kite.
    style.addDrawingStyle( group='Knik & Kite', name='SPL1'           , color=toRGB('Red'        ) )
    style.addDrawingStyle( group='Knik & Kite', name='AutoLayer'      , color=toRGB('Magenta'    ) )
    style.addDrawingStyle( group='Knik & Kite', name='gmetalh'        , color=toRGB('128,255,200'), pattern=toHexa('antislash2.32'    ), border=1 )
    style.addDrawingStyle( group='Knik & Kite', name='gmetalv'        , color=toRGB('200,200,255'), pattern=toHexa('light_antihash1.8'), border=1 )
    style.addDrawingStyle( group='Knik & Kite', name='gcontact'       , color=toRGB('255,255,190'),                                      border=1 )
    style.addDrawingStyle( group='Knik & Kite', name='Anabatic::Edge' , color=toRGB('255,255,190'), pattern='0000000000000000'         , border=4, threshold=0.02 )
    style.addDrawingStyle( group='Knik & Kite', name='Anabatic::GCell', color=toRGB('255,255,190'), pattern='0000000000000000'         , border=2, threshold=threshold )

    Viewer.Graphics.addStyle( style )

    # ----------------------------------------------------------------------
    # Style: Alliance.Classic [white].

    style = Viewer.DisplayStyle( 'Alliance.Classic [white]' )
    style.inheritFrom( 'Alliance.Classic [black]' )
    style.setDescription( 'Alliance Classic Look - white background' )
    style.setDarkening  ( Viewer.DisplayStyle.HSVr(1.0, 3.0, 2.5) )

    style.addDrawingStyle( group='Viewer', name='background', color=toRGB('White'), border=1 )
    style.addDrawingStyle( group='Viewer', name='foreground', color=toRGB('Black'), border=1 )
    style.addDrawingStyle( group='Viewer', name='boundaries', color=toRGB('Black'), border=1, pattern='0000000000000000' )
    Viewer.Graphics.addStyle( style )

    Viewer.Graphics.setStyle( 'Alliance.Classic [black]' )

def setup():
    _setup_techno()
    _setup_display()
    loadAnalogTechno(analogTechnologyTable, __file__)
    try:
        from .techno_fix import fix
    except:
        pass
    else:
        fix()
