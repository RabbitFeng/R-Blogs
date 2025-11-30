[诊断修复ANR Android Developer](http://cdeveloper.android.com/topic/performance/anrs/diagnose-and-fix-anrs?hl=zh-cn)

# Android文件导出

```bash
# 老版本， 可能会遇到些问题
adb pull data/anr/traces.txt

> adb: error: failed to stat remote object 'data/anr/traces.txt': No such file or directory

# 新版本
# 1. 查看traces文件列表
adb shell
cd data/anr
ls -a

> .                            anr_2025-08-28-19-26-10-858
> ..                           anr_2025-08-28-21-16-44-591
> anr_2025-08-28-14-55-20-908  anr_2025-08-28-21-18-59-212
> anr_2025-08-28-14-56-15-698  anr_2025-08-28-21-24-39-165
> anr_2025-08-28-15-20-16-025  anr_2025-08-28-21-28-06-688
> HWBRQ:/data/anr $ 

# 2. 尝试直接导出
adb pull data/anr/xxxx.txt

> adb: error: failed to copy 'data/anr/anr_2025-08-28-19-26-10-858' to './anr_2025-08-28-19-26-10-858': remote open failed: Permission denied

# 3. 若因权限问题直接导出失败，使用bugreport
adb bugreport
adb bugreport ~/anr/traces

> /data/user_de/0/com.android.shell/file.... 33.5 MB/s (11886233 bytes in 0.338s)
> Bug report copied to /Users/xxx/bugreport-BRQ-AL00-HUAWEIBRQ-AL00-2025-08-29-11-09-02.zip
```

