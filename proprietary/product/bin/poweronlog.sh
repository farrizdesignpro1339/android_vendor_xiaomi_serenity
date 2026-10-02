#!bin/sh

# SPDX-FileCopyrightText: 2016-2023 Unisoc (Shanghai) Technologies Co., Ltd
# SPDX-License-Identifier: LicenseRef-Unisoc-General-1.0

function logcmd()
{
    echo -e "\n"
}

function exe_cmd()
{
    logcmd "$@";
    eval $@;
}

dstdir="/blackbox/ylog/poweron/"
index=0
max=0
tarfile=0
mkdir -p $dstdir
logSizeInfo=$(du -shk $dstdir)
size=$(echo $logSizeInfo | awk '{print $1}')
if [ "$size" -gt "20*1024" ]; then
    echo "log size more than 20M , exit."
    exe_cmd "rm -rf $dstdir/*"
    exit 1
fi
for dir in $(ls $dstdir)
do
    [ -d $dir ] && echo $dir
    if (($dir < 999)) && (($dir >= 0))
    then
        let "index++"
        if [ $dir -ge $max ];then
            max=$dir
        fi
    else
        echo "dir is bigger 1000"
        exe_cmd "rm -rf $dstdir/*"
        let "index=0"
    fi
done

if [ $index -eq 4 ];then
    let "max++"
    exe_cmd "mkdir $dstdir$max"
    exe_cmd "rm -rf $dstdir$((max-4))"
    exe_cmd "timeout 60 dmesg -Tw > $dstdir$max/kernel.log &"
    exe_cmd "timeout 60 logcat > $dstdir$max/android.log &"
else
    exe_cmd "mkdir $dstdir$index"
    exe_cmd "timeout 60 dmesg -Tw > $dstdir$index/kernel.log &"
    exe_cmd "timeout 60 logcat > $dstdir$index/android.log &"
fi

wait
echo "wait end"

if [ $index -eq 4 ];then
    tarfile=$max
else
    tarfile=$index
fi
cd $dstdir$tarfile
tar -zcvPf log_$tarfile.tar.gz *
exe_cmd "rm -rf $dstdir$tarfile/android.log"
exe_cmd "rm -rf $dstdir$tarfile/kernel.log"

echo "poweronlog end"
