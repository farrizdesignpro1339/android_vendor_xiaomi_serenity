#!bin/sh

# SPDX-FileCopyrightText: 2016-2023 Unisoc (Shanghai) Technologies Co., Ltd
# SPDX-License-Identifier: LicenseRef-Unisoc-General-1.0

function exe_cmd()
{
  eval $@;
}

unset LOG_PATH
LOG_PATH=$(getprop persist.unipnp.standby_log_path)
LOG_PATH="${LOG_PATH:-/data/ylog/standbylog}"
DIR_MAX_SIZE=10240

if [ ! -d "${LOG_PATH}" ]; then
  exe_cmd "mkdir -p ${LOG_PATH}"
  exe_cmd "chmod -R 777 ${LOG_PATH}"
fi

function limit_dir_size() {
  while true
  do
    dir_size=$(du -s "${LOG_PATH}" | cut -f1)
    if [ "$dir_size" -lt $DIR_MAX_SIZE ]; then
      break
    else
      old_file=$(ls -tr "$LOG_PATH"/standby_* | head -n 1)
      rm -rf "$old_file"
    fi
  done
}

anomaly_time=$(date "+%Y_%m%d_%H%M%S")

exe_cmd "dmesg -T > $LOG_PATH/standby_kernel_log_${anomaly_time}.txt"
exe_cmd "logcat -d > $LOG_PATH/standby_android_log_${anomaly_time}.txt"
exe_cmd "dumpsys sensorservice > $LOG_PATH/standby_dump_sensor_${anomaly_time}.txt"
exe_cmd "dumpsys deviceidle > $LOG_PATH/standby_dump_deviceidle_${anomaly_time}.txt"
exe_cmd "dumpsys location > $LOG_PATH/standby_dump_location_${anomaly_time}.txt"
exe_cmd "dumpsys bluetooth_manager > $LOG_PATH/standby_dump_bluetooth_manager_${anomaly_time}.txt"
exe_cmd "dumpsys secure_element > $LOG_PATH/standby_dump_secure_element_${anomaly_time}.txt"

exe_cmd "setprop persist.unipnp.standbylogcat false"

limit_dir_size

echo "done"