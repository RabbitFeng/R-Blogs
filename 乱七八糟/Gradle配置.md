```groovy
boolean enableLeak = hasProperty("enableLeak") ? "true".equals(property("enableLeak")) : false

android {
    defaultConfig {
          buildConfigField "boolean", "ENABLE_LEAKCANARY", enableLeak ? "true" : "false"
    }
}

dependencies {
     if (enableLeak) {
        // 可以通过参数配置打包 -P enableLeak=true
        debugImplementation 'com.squareup.leakcanary:leakcanary-android:2.14'
    }
}
```

