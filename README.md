# proprietary_vendor_xiaomi_serenity

Vendor blobs **Redmi A5 (serenity)** — layout ngikutin
[proprietary_vendor_xiaomi_gale](https://github.com/Mayuri-Chan/proprietary_vendor_xiaomi_gale/tree/lineage-22.2).

- Build: `A15.0.32.0.VGWMIXM` (Android 15, vendor SDK 33)
- SoC: Unisoc ums9230
- Dump: `supera5/` (MIO-KITCHEN), blobs di-hardlink ke `proprietary/` (0 byte ekstra)

## Isi (kayak gale)

| File | Asal |
|---|---|
| `proprietary/` | 21.379 blobs: `vendor odm product system_ext` |
| `serenity-vendor.mk` | `PRODUCT_COPY_FILES` (19.583, sorted) + `PRODUCT_PACKAGES` (1.071: 879 lib, 161 bin, 31 apk) |
| `Android.bp` | 1.071 prebuilt: `cc_prebuilt_library_shared`, `cc_prebuilt_binary`, `android_app_import` (shared_libs dari `readelf`, tanpa suffix `.so`) |
| `BoardConfigVendor.mk` | `AB_OTA_PARTITIONS` (32, dari `ro.odm.ab_ota_partitions`) |
| `Android.mk` | guard `TARGET_DEVICE=serenity` (dump ini nggak ada radio `.img`, jadi kosong — wajar) |
| `proprietary-files.txt` | source of truth untuk regenerate (biasanya tinggal di device tree) |
| `extract-files.sh` / `setup-makefiles.sh` | tooling kitchen (fallback local-dump) |

## Yang sengaja di-exclude

GMS/Go apps, `product/media`, `odm/logo`, `build*.prop`, symlink toybox,
`vendor_dlkm`/`system_dlkm` (`*.ko` — urus dari kernel source), `system/` AOSP.

## Regenerate

```bash
python3 /tmp/gen_gale_style.py   # butuh dump supera5/ + proprietary-files.txt
```

## Catatan Unisoc

- `vendor/firmware` (18rb file tuning kamera) masuk `COPY_FILES` — jangan dihapus.
- `system_ext/framework/*.jar` ikut sebagai copy (bukan `dex_import` kayak gale) — konfigurasi boot jars tetap di device tree.
- Belum ada `install_symlink` compat (gale punya 6, misal `lib64/libmtk_drvb.so -> mt6768/...`). Tambahkan bila linker ngeluh pas boot.
