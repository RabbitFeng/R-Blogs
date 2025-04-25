## Library模块配置

在Library模块build.gradle中新增发布配置

```groovy
plugins {
    id 'com.android.library'
  	// 新增mavan-publish配置 gradle
    id 'maven-publish'
}


```

![image-20250425152216490](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20250425152216490.png)