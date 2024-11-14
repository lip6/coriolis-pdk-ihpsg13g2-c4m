#!/bin/sh

    rootDir="${HOME}/coriolis-2.x"
   buildDir="${rootDir}/release/build-ihp"
 installDir="${rootDir}/release/install"
 rm -rf ${buildDir}
 rm -rf ${installDir}/lib64/python3.9/site-packages/pdks/c4m_ihpsg13g2
 meson setup --prefix ${installDir} ${buildDir}
 meson install -C ${buildDir}
