#!/vendor/bin/sh
# SPDX-FileCopyrightText: 2016-2023 Unisoc (Shanghai) Technologies Co., Ltd
# SPDX-License-Identifier: LicenseRef-Unisoc-General-1.0

init_value=$(eval "cat /proc/sys/vm/swappiness")
is_low_ram_device=$(getprop ro.config.low_ram)

if [[ $is_low_ram_device == *"true"* ]]; then
        target_swappiness=200
else
        target_swappiness=180
fi

while :
do
        swaptotal=$(eval "cat /proc/meminfo | grep SwapTotal | awk '{print \$2}' ")
        if [ $swaptotal -ne 0 ]; then
                echo $target_swappiness > /proc/sys/vm/swappiness
                break
        else
                sleep 2
        fi
done

while :
do
        time=`uptime | awk '{print $3}'`
        if [ $time -lt 6 ]; then
                sleep 10
        else
                echo $init_value > /proc/sys/vm/swappiness
                break
        fi
done

