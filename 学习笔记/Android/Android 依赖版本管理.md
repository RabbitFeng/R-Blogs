Gradle 7.0+支持Version Catalog

![image-20250427150807986](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20250427150807986.png)

创建Version Catalog

`gradle`目录下新增`lib.version.toml`文件

![image-20250427150916784](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20250427150916784.png)

***lib.version.toml***

```toml
[versions]
appcompat = "1.3.0"
constraintlayout = "2.1.4"
curtains = "1.2.4"
espressoCore = "3.6.1"
junit = "4.13.2"
junitVersion = "1.2.1"
material = "1.3.0"
okhttp = "4.12.0"
utilcodex = "1.31.1"
viewbinding = "8.5.1"

[libraries]
### androidx
appcompat = { module = "androidx.appcompat:appcompat", version.ref = "appcompat" }
constraintlayout = { module = "androidx.constraintlayout:constraintlayout", version.ref = "constraintlayout" }
viewbinding = { module = "androidx.databinding:viewbinding", version.ref = "viewbinding" }

### google
material = { module = "com.google.android.material:material", version.ref = "material" }
gson = { group = "com.google.code.gson", name = "gson", version = "2.9.1" }

### support
curtains = { module = "com.squareup.curtains:curtains", version.ref = "curtains" }
espresso-core = { module = "androidx.test.espresso:espresso-core", version.ref = "espressoCore" }
ext-junit = { module = "androidx.test.ext:junit", version.ref = "junitVersion" }
junit = { module = "junit:junit", version.ref = "junit" }
okhttp = { module = "com.squareup.okhttp3:okhttp", version.ref = "okhttp" }
utilcodex = { module = "com.blankj:utilcodex", version.ref = "utilcodex" }

[plugins]


```

***build.gradle***

```groovy
dependencies {
    /** Android **/
    api libs.appcompat
    api libs.material
    api libs.viewbinding
    api libs.constraintlayout
}
```

迁移：

`Android Studio` 代码提示，可迁移

![image-20250427151203589](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20250427151203589.png)