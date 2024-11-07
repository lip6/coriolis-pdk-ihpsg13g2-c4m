import os
from pathlib import Path

from coriolis.CRL import Spice

def fix(lib):
    #spiceDir = Path(__file__).parents[7] / 'libs.ref' / 'StdCell3V3Lib' / 'spice'
    spiceDir = Path(__file__).parent / 'libs.ref' / 'StdCell3V3Lib' / 'spice'
    Spice.load( lib, str(spiceDir / 'StdCell3V3Lib.spi'), Spice.PIN_ORDERING )

