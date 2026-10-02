#!bin/sh

# SPDX-FileCopyrightText: 2016-2023 Unisoc (Shanghai) Technologies Co., Ltd
# SPDX-License-Identifier: LicenseRef-Unisoc-General-1.0

function exe_cmd()
{
    eval $@;
}

#cat /dev/block/by-name/uboot_log | while read line ; do
    #echo $line
#done
exe_cmd "ylogkat -U"

sleep 1024h

echo ubootlog end
