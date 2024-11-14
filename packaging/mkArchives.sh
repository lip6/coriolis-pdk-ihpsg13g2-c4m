
    version="2024.10.15"
     obsDir="../coriolis-obs/home:jpc-lip6/c4m-ihpsg13g2-pdk"

 printHelp () {
   echo ""
   echo "  Usage: mkArchives.sh [--sources] [--docs] [--venv] [--commit] [--run]"
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
   echo "[ERROR] mkArchive.sh: Unknown argument \"${badArgument}\"."
   exit 1
 fi

 echo "Running mkArchives.sh"
 echo "* Using HEAD githash as release: ${githash}."
 if [ "${doSources}" = "true" ]; then
   echo "* Making source file archive from Git HEAD ..."
   ./packaging/git-archive-all.sh -v --prefix c4m-ihpsg13g2-pdk-2024.10.15/ \
                                     --format tar.gz \
                                     c4m-ihpsg13g2-pdk-${version}.tar.gz
 fi

 echo "* Update files in OBS project directory."
 echo "  OBS package directory: \"${obsDir}\"."
 for distribFile in packaging/c4m-ihpsg13g2-pdk.spec      \
                    packaging/c4m-ihpsg13g2-pdk-rpmlintrc \
                    packaging/patchvenv.sh                \
                    venv-al9-2.5.5.tar.gz                 \
                    c4m-ihpsg13g2-pdk-${version}.tar.gz   \
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
 
 sed -i "s,^Release: *1,Release:        <CI_CNT>.<B_CNT>.${githash}," ${obsDir}/c4m-ihpsg13g2-pdk.spec
 if [ "${doCommit}" = "true" ]; then
   pushd ${obsDir}
   osc commit
   popd
 fi

