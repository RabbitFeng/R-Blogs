## 加固

**360加固助手**

> 体验不是很好，也不是一定要用吧反正

## [字节对齐](https://developer.android.com/tools/zipalign?hl=zh-cn)

```bash
# macOS 验证字节码对齐
# 【语法】zipalign -c -P 16 -v 4 [existing.apk]

# macOS 字节码对齐
# 【语法】zipalign -P 16 -f -v 4 [infile.apk] [outfile.apk]

```



## 签名

**Android build_tools - apk_signer**

```bash
# macOS对APK签名
# --ks [签名证书路径]
# --ks-key-alias [别名]
# --ks-pass pass:[KeyStore密码]
# --key-pass pass:[签署者的密码]
# --out [output.apk][input.apk]
# 【语法】apksigner sign --ks [签名证书路径] --ks-key-alias [别名] --out [签名后apk路径] [需要签名的apk路径]

# sample
/Users/xxx/Library/Android/sdk/build-tools/29.0.2/apksigner sign --ks /Users/xxx/baidu/ubs/gaia-app-android/app/my-release-key.keystore --ks-key-alias my-release-key.keystore --out /Users/xxx/APK/Gaia/gaia-app-4.0.3-release-jg-signed.apk /Users/xxx/APK/Gaia/gaia-4.0.3-release_403_unsigned.apk

# 验证签名
# 【语法】apksigner verify -v [签名后的apk路径]

/Users/xxx/Library/Android/sdk/build-tools/29.0.2/apksigner verify -v /Users/xxx/APK/Gaia/gaia-app-4.0.3-release-jg-signed.apk
```

