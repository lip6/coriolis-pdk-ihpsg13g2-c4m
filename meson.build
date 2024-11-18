
project(
  'c4m-ihpsg13s2-pdk',
   version:  '2024.10.15',
   meson_version: '>= 1.2.0',
)

py       = import( 'python' ).find_installation( pure:false )
py_deps  = dependency( 'python3', required: true )
pdks_dir = py.get_install_dir() / 'pdks' / 'c4m_ihpsg13g2'

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
                   ]

py.install_sources( files(     cells_files), subdir:'pdks/c4m_ihpsg13g2' )
py.install_sources( files( core2chip_files), subdir:'pdks/c4m_ihpsg13g2/core2chip' )
py.install_sources( files(designflow_files), subdir:'pdks/c4m_ihpsg13g2/designflow' )

install_subdir( 'libs.ref' , install_dir:pdks_dir )
install_subdir( 'libs.tech', install_dir:pdks_dir , exclude_directories:['coriolis'] )

