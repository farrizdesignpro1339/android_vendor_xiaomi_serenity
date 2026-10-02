#!bin/sh

# SPDX-FileCopyrightText: 2016-2023 Unisoc (Shanghai) Technologies Co., Ltd
# SPDX-License-Identifier: LicenseRef-Unisoc-General-1.0

function logcmd()
{
    echo -e "\n"
    echo -n "$@"
    echo -n " on "
    date '+%m-%d %T'
}

function exe_cmd()
{
    logcmd "$@";
    eval $@;
    echo -n "run finished on "
    date '+%m-%d %T'
}


is_ufs=$(getprop ro.boot.boot_devices |awk '{ print (index($1,"ufs")>0)}')
count=0
while true;do
    sysinfo_date=$(date '+%m-%d %T')
    echo "sysinfo_"$count"  on "$sysinfo_date
    b=$(($count % 6))
    if [ $b -eq 0 ]; then
        exe_cmd "cat /proc/meminfo"
        exe_cmd "free"
        exe_cmd "vmstat"
        exe_cmd "df"
        exe_cmd "storaged -u"
        exe_cmd "cat /proc/uid_io/debug"
        exe_cmd "cat /proc/buddyinfo"
        exe_cmd "cat /proc/slabinfo"
        exe_cmd "cat /proc/zoneinfo"
        exe_cmd "cat /proc/vmstat"
        exe_cmd "cat /proc/vmallocinfo"
        exe_cmd "cat /proc/pagetypeinfo"
        exe_cmd "cat /d/wakeup_sources"
        exe_cmd "cat /sys/kernel/debug/binder/failed_transaction_log"
        exe_cmd "cat /sys/kernel/debug/binder/transaction_log"
        exe_cmd "cat /sys/kernel/debug/binder/transactions"
        exe_cmd "cat /sys/kernel/debug/binder/stats"
        exe_cmd "cat /sys/kernel/debug/binder/state"
        exe_cmd "cat /proc/interrupts"
        if [ $is_ufs -eq 1 ]; then
            exe_cmd "cat /sys/block/sda/stat"
        else
            exe_cmd "cat /sys/block/mmcblk0/stat"
        fi
        exe_cmd "cat /dev/blkio/foreground/cgroup.procs"
        exe_cmd "cat /dev/blkio/background/cgroup.procs"
        exe_cmd "cat /sys/fs/cgroup/foreground/cgroup.procs"
        exe_cmd "cat /sys/fs/cgroup/high/cgroup.procs"
        exe_cmd "cat /sys/fs/cgroup/normal/cgroup.procs"
        exe_cmd "cat /sys/fs/cgroup/background/cgroup.procs"
    else
        exe_cmd "storaged -u"
        if [ $is_ufs -eq 1 ]; then
            exe_cmd "cat /sys/block/sda/stat"
        else
            exe_cmd "cat /sys/block/mmcblk0/stat"
        fi

    fi
    count=$(($count+1))
    echo "sysinfo end\n\n\n"
    if [[ $1 == 1 ]]; then
        break
    fi
    #print sysinfo log every 20s
    sleep 20s
done
