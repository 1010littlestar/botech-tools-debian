#!/bin/bash


usage() 
{
	echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	echo "+  usage : ./mkdeb.sh <Hi3559AV100_SDK_DIR> [out_dir]                                                      +"
	echo "+  Hi3559AV100_SDK_DIR: Hi3559AV100_SDK_V2.0.3.1 directory path                                          +"
	echo "+  out_dir:  output directory                                                                              +"
	echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
}


CUR_DIR=`pwd`
OUT_DIR="${CUR_DIR}/out"
Hi3559AV100_SDK_DIR=""
SUFFIX=`date +"%Y%m%d%H%M"`

log() {
	cur_date=`date +"%Y-%m-%d %H:%M:%S"`
        echo "$cur_date "$1
}

param_check() {
	if [ $# -eq 1 ]; then
        Hi3559AV100_SDK_DIR="$1"
	elif [ $# -eq 2 ]; then
        Hi3559AV100_SDK_DIR="$1"
        OUT_DIR="$2"
	else
		usage
		return 1
	fi

    if [ ! -d ${Hi3559AV100_SDK_DIR} ]; then
        usage
        echo "${Hi3559AV100_SDK_DIR} is not exist!!"
        return 1
    fi

    rm -rf ${OUT_DIR}
    mkdir -v ${OUT_DIR}

	return 0
}

install_debian_files() {
    debian_dir=${CUR_DIR}/DEBIAN
    if [ ! -d ${debian_dir} ]; then
        echo "Can't find DEBIAN files, please check current path!"
        return 1
    fi 
    cp -a ${debian_dir} ${OUT_DIR}/
    sed -i "/Version:/s/Version:.*/Version: ${SUFFIX}/" ${OUT_DIR}/DEBIAN/control
    log "copy DEBIAN finished"

    return 0
}

install_tool_files() {

    if [ ! -e ${Hi3559AV100_SDK_DIR}/osdrv/tools/board/reg-tools-1.0.0/bin/btools ]; then
        log "Can't fine reg tools, please compile first!!"
        return 1
    fi
    mkdir -pv ${OUT_DIR}/opt/bin/

    # copy reg-tools
    cp -P ${Hi3559AV100_SDK_DIR}/osdrv/tools/board/reg-tools-1.0.0/bin/* ${OUT_DIR}/opt/bin/
    log "copy reg-tools tool finished"

    # copy  temperature tool
    cp ${CUR_DIR}/temperature/temperature.py  ${OUT_DIR}/opt/bin/temperature

    log "copy temperatur tool finished"

    return 0
}

param_check $*
if [ x"1" == x"$?" ]; then
    exit 1;
fi

install_debian_files
if [ x"1" == x"$?" ]; then
    exit 1;
fi

install_tool_files
if [ x"1" == x"$?" ]; then
    exit 1;
fi

dpkg-deb -b ${OUT_DIR} botech-tools-${SUFFIX}.deb

exit 0
