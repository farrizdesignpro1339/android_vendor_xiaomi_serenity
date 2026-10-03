#
# Automatically generated file. DO NOT MODIFY
#

LOCAL_PATH := $(call my-dir)

ifeq ($(TARGET_DEVICE),serenity)

# Unisoc gralloc.default overrides AOSP generic (same module name).
# Soong can't override Make-defined modules, hence BUILD_PREBUILT here.
include $(CLEAR_VARS)
LOCAL_MODULE := gralloc.default
LOCAL_OVERRIDES_MODULES := gralloc.default
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
LOCAL_MULTILIB := both
LOCAL_SRC_FILES_32 := proprietary/vendor/lib/hw/gralloc.default.so
LOCAL_SRC_FILES_64 := proprietary/vendor/lib64/hw/gralloc.default.so
LOCAL_MODULE_SUFFIX := .so
LOCAL_PROPRIETARY_MODULE := true
LOCAL_MODULE_RELATIVE_PATH := hw
LOCAL_CHECK_ELF_FILES := false
include $(BUILD_PREBUILT)

endif
