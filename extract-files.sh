#!/bin/bash
#
# Copyright (C) 2026 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#
# Extract vendor blobs for Redmi A5 (serenity)
# Build: A15.0.32.0.VGWMIXM | Android 15 | Unisoc ums9230
#

set -e

DEVICE=serenity
VENDOR=xiaomi

# Load extract_utils and do some sanity checks
MY_DIR="${BASH_SOURCE%/*}"
if [[ ! -d "${MY_DIR}" ]]; then MY_DIR="${PWD}"; fi

ANDROID_ROOT="${MY_DIR}/../../.."

# Use Lineage extract-utils if available, else fallback to local dump mode
HELPER="${ANDROID_ROOT}/tools/extract-utils/extract_utils.sh"
if [ ! -f "${HELPER}" ]; then
    HELPER="${ANDROID_ROOT}/vendor/lineage/build/tools/extract_utils.sh"
fi

CLEAN_VENDOR=true
ONLY_COMMON=
ONLY_TARGET=
KANG=
SECTION=

while [ "${#}" -gt 0 ]; do
    case "${1}" in
        --only-common) ONLY_COMMON=true ;;
        --only-target) ONLY_TARGET=true ;;
        -n | --no-cleanup) CLEAN_VENDOR=false ;;
        -k | --kang) KANG="--kang" ;;
        -s | --section)
            SECTION="${2}"
            shift
            CLEAN_VENDOR=false
            ;;
        *) SRC="${1}" ;;
    esac
    shift
done

if [ -z "${SRC}" ]; then
    SRC="adb"
fi

function blob_fixup() {
    case "${1}" in
        # Fix Unisoc camera libs - remove unused dependency if needed
        # (placeholder, sesuaikan setelah coba build)
        vendor/lib64/libunisoc_*|vendor/lib/libunisoc_*)
            ;;
        # Shim untuk fingerprint goodix jika perlu
        vendor/lib64/hw/fingerprint.*|vendor/lib/hw/fingerprint.*)
            ;;
        *)
            return 1
            ;;
    esac
    return 0
}

function blob_fixup_dry() {
    blob_fixup "${1}" ""
}

if [ -f "${HELPER}" ]; then
    source "${HELPER}"
    # Initialize the helper
    setup_vendor "${DEVICE}" "${VENDOR}" "${ANDROID_ROOT}" false "${CLEAN_VENDOR}"

    if [ -z "${ONLY_TARGET}" ]; then
        extract "${MY_DIR}/proprietary-files.txt" "${SRC}" "${KANG}" --section "${SECTION}"
    fi

    "${MY_DIR}/setup-makefiles.sh"
else
    # Fallback: pure local-dump mode (tanpa extract-utils, untuk MIO-KITCHEN)
    echo "extract-utils tidak ditemukan, pakai mode local-dump..."
    DUMP_DIR="${SRC}"
    if [ "${SRC}" = "adb" ]; then
        echo "ERROR: mode fallback butuh path dump lokal."
        echo "Usage: ./extract-files.sh /path/ke/supera5"
        exit 1
    fi
    DEST="${MY_DIR}/proprietary"
    if [ "${CLEAN_VENDOR}" = true ]; then
        rm -rf "${DEST}"
    fi
    mkdir -p "${DEST}"
    COUNT=0
    while read -r line; do
        # skip komentar & baris kosong
        case "$line" in \#*|"") continue;; esac
        # format src[:dst], ambil src
        src_path=$(echo "$line" | cut -d: -f1 | tr -d ' \t-')
        # hapus prefix '-' (optional marker)
        src_path=${src_path#-}
        [ -z "$src_path" ] && continue
        if [ -f "${DUMP_DIR}/${src_path}" ]; then
            mkdir -p "${DEST}/$(dirname ${src_path})"
            cp -p "${DUMP_DIR}/${src_path}" "${DEST}/${src_path}"
            COUNT=$((COUNT+1))
        else
            echo "WARNING: tidak ditemukan: ${src_path}"
        fi
    done < "${MY_DIR}/proprietary-files.txt"
    echo "Selesai: ${COUNT} file disalin ke ${DEST}/"
fi
