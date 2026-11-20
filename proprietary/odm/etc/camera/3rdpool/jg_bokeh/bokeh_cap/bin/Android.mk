#
# SPDX-FileCopyrightText: 2022-2024 Unisoc (Shanghai) Technologies Co., Ltd
# SPDX-License-Identifier: LicenseRef-Unisoc-General-1.0
#
# Copyright 2022-2024 Unisoc (Shanghai) Technologies Co., Ltd.
# Licensed under the Unisoc General Software License, version 1.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://www.unisoc.com/en_us/license/UNISOC_GENERAL_LICENSE_V1.0-EN_US
# Software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OF ANY KIND, either express or implied.
# See the Unisoc General Software License, version 1.0 for more details.
#

LOCAL_PATH := $(call my-dir)

# 定义 bokeh_cap bin 资源安装模块
include $(CLEAR_VARS)

LOCAL_MODULE := jg_bokeh_cap_bin
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_PATH := $(TARGET_OUT_ODM)/etc/camera/3rdpool/jg_bokeh/bokeh_cap/bin
LOCAL_MODULE_TAGS := optional

# 安装时执行的命令：递归复制整个目录
LOCAL_POST_INSTALL_CMD := \
    mkdir -p $(LOCAL_MODULE_PATH) && \
    cp -rf $(LOCAL_PATH)/* $(LOCAL_MODULE_PATH)/

include $(BUILD_PHONY_PACKAGE)
