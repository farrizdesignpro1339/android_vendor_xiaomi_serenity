#!/bin/bash
#
# Copyright (C) 2026 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#
# Setup makefiles for Redmi A5 (serenity)
#

set -e

DEVICE=serenity
VENDOR=xiaomi

MY_DIR="${BASH_SOURCE%/*}"
if [[ ! -d "${MY_DIR}" ]]; then MY_DIR="${PWD}"; fi

ANDROID_ROOT="${MY_DIR}/../../.."

HELPER="${ANDROID_ROOT}/tools/extract-utils/extract_utils.sh"
if [ ! -f "${HELPER}" ]; then
    HELPER="${ANDROID_ROOT}/vendor/lineage/build/tools/extract_utils.sh"
fi

if [ -f "${HELPER}" ]; then
    source "${HELPER}"
    setup_vendor "${DEVICE}" "${VENDOR}" "${ANDROID_ROOT}"
    write_headers
    write_makefiles "${MY_DIR}/proprietary-files.txt" true
    write_footers
else
    echo "serenity-vendor.mk / Android.bp sudah pre-generated gaya gale."
    echo "Untuk regenerate dari dump: python3 /tmp/gen_gale_style.py"
fi
