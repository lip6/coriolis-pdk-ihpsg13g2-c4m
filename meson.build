
project(
  'coriolis-pdk-ihpsg13s2-c4m',
   version:  '2024.10.15',
   meson_version: '>= 1.2.0',
)

py       = import( 'python' ).find_installation( pure:false )
py_deps  = dependency( 'python3', required: true )
pdks_dir = py.get_install_dir() / 'pdks' / 'ihpsg13g2_c4m'

cells_files = [ 'libs.tech/coriolis/ihpsg13g2/StdCell3V3Lib.py'
              , 'libs.tech/coriolis/ihpsg13g2/StdCell3V3Lib_fix.py'
              , 'libs.tech/coriolis/ihpsg13g2/StdCellLib.py'
              , 'libs.tech/coriolis/ihpsg13g2/StdCellLib_fix.py'
              , 'libs.tech/coriolis/ihpsg13g2/iolib.py'
              , 'libs.tech/coriolis/ihpsg13g2/__init__.py'
              , 'libs.tech/coriolis/ihpsg13g2/techno.py'
              ]

core2chip_files = [ 'libs.tech/coriolis/ihpsg13g2/core2chip/__init__.py'
                  , 'libs.tech/coriolis/ihpsg13g2/core2chip/sg13g2io.py'
                  ]

designflow_files = [ 'libs.tech/coriolis/ihpsg13g2/designflow/__init__.py'
                   , 'libs.tech/coriolis/ihpsg13g2/designflow/filler.py'
                   , 'libs.tech/coriolis/ihpsg13g2/designflow/sealring.py'
                   , 'libs.tech/coriolis/ihpsg13g2/designflow/drc.py'
                   ]

py.install_sources( files(     cells_files), subdir:'pdks/ihpsg13g2_c4m' )
py.install_sources( files( core2chip_files), subdir:'pdks/ihpsg13g2_c4m/core2chip' )
py.install_sources( files(designflow_files), subdir:'pdks/ihpsg13g2_c4m/designflow' )

install_subdir( 'libs.ref' , install_dir:pdks_dir )
install_subdir( 'libs.tech', install_dir:pdks_dir , exclude_directories:['coriolis'] )

install_data( 'libs.tech/coriolis/mos_tt.lib'  , install_dir:pdks_dir )
install_data( 'libs.tech/coriolis/spimodel.cfg', install_dir:pdks_dir )

