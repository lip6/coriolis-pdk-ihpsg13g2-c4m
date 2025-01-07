
    version="2024.10.15"
     obsDir="../coriolis-obs/home:jpc-lip6/coriolis-pdk-ihpsg13g2-c4m"

 printHelp () {
   echo ""
   echo "  Usage: uploadOBSs.sh [--sources] [--docs] [--commit] [--run]"
   echo ""
   echo "  Options:"
   echo "    [--sources] : Build an archive from the HEAD of the current branch."
   echo "    [--commit]  : Push the files (commit) on the remote builder repository."
   echo "                  This will effectively triggers the rebuild of the packages."
   echo "                  OBS local repository is hardwired to:"
   echo "                      \"${obsDir}\""
   echo "    [--run]     : Perform all actions at once."
   echo ""

 }

 if [ $# -eq 0 ]; then printHelp; fi

    githash=`git log -1 --pretty=format:%h`
  doSources="false"
     doDocs="false"
     doVEnv="false"
   doCommit="false"
 badAgument=""
 while [ $# -gt 0 ]; do
   case $1 in
     --sources) doSources="true";;
     --commit)  doCommit="true";;
     --run)     doSources="true"
                doDocs="true"
                doVEnv="true"
                doCommit="true";;
     *)         badArgument="$1";;
   esac
   shift
 done
 if [ ! -z "${badArgument}" ]; then
   echo "[ERROR] uploadOBS.sh: Unknown argument \"${badArgument}\"."
   exit 1
 fi

 echo "Running uploadOBSs.sh"
 echo "* Using HEAD githash as release: ${githash}."
 if [ "${doSources}" = "true" ]; then
   echo "* Making source file archive from Git HEAD ..."
   ./packaging/git-archive-all.sh -v --prefix coriolis-pdk-ihpsg13g2-c4m-2024.10.15/ \
                                     --format tar.gz \
                                     coriolis-pdk-ihpsg13g2-c4m-${version}.tar.gz
 fi

 echo "* Update files in OBS project directory."
 echo "  OBS package directory: \"${obsDir}\"."
 for distribFile in packaging/coriolis-pdk-ihpsg13g2-c4m.spec      \
                    packaging/coriolis-pdk-ihpsg13g2-c4m-rpmlintrc \
                    packaging/patchvenv.sh                         \
                    venv-al9-2.5.5.tar.gz                          \
                    coriolis-pdk-ihpsg13g2-c4m-${version}.tar.gz   \
                    packaging/coriolis-pdk-ihpsg13g2-c4m.dsc       \
                    packaging/coriolis-pdk-ihpsg13g2-c4m-rpmlintrc \
                    packaging/debian.changelog                     \
                    packaging/debian.control                       \
                    packaging/debian.copyright                     \
                    packaging/debian.rules                         \
                    ; do
   if [ ! -f "${distribFile}" ]; then continue; fi
   if [[ "${distribFile}" == packaging* ]]; then
     echo "  - copy ${distribFile}."
     cp ${distribFile} ${obsDir}
   else
     echo "  - move ${distribFile}."
     mv ${distribFile} ${obsDir}
   fi
 done
 
 sed -i "s,^Release: *1,Release:        <CI_CNT>.<B_CNT>.${githash}," ${obsDir}/coriolis-pdk-ihpsg13g2-c4m.spec
 if [ "${doCommit}" = "true" ]; then
   pushd ${obsDir}
   osc commit
   popd
 fi

