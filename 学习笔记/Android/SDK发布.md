## Library模块配置

在Library模块build.gradle中新增发布配置

```groovy
plugins {
    id 'com.android.library'
  	// 新增mavan-publish配置 gradle
    id 'maven-publish'
}

// 从local.properties中读取数据; 比如发布到GithubPackage,配置name和password
def localProperties = new Properties()
localProperties.load(new FileInputStream(rootProject.file("local.properties")))

publishing {
    publications {
        // 名字自定义
        rabbitLib(MavenPublication) {
            groupId "com.rabbit"
            artifactId "base-android"
            version "0.0.1-alpha"
          	// 发布产物配置，这样发布的pom文件是携带依赖的
            afterEvaluate {
                from(components["release"])
            }
        }
    }

    repositories {
        // 发布到Github Package配置
        maven {
            name "GithubPackages"
            url uri("https://maven.pkg.github.com/RabbitFeng/AndroidPublishDemo")
            credentials {
                username = localProperties.getProperty("gpr.usr")
                // local.properties 文件下定义gpr.usr，即Github用户名
                password = localProperties.getProperty("gpr.key")
                // local.properties 文件下定义gpr.key，即Github Token, 需要权限`write:package`!!!
            }
        }

        // 发布到本地仓库配置
        maven {
            name "local"
            url = layout.buildDirectory.dir("repo")
        }
    }
}

```

![image-20250425152216490](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20250425152216490.png)

