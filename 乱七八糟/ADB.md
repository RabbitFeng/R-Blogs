# Android Debug Brige

[Android 调试桥 (adb)](https://developer.android.com/tools/adb?hl=zh-cn)

Android 调试桥 (`adb`) 是一种功能多样的命令行工具，可让您与设备进行通信。`adb` 命令可用于执行各种设备操作，例如安装和调试应用。`adb` 提供对 Unix shell（可用来在设备上运行各种命令）的访问权限。它是一种客户端-服务器程序，包括以下三个组件：

- **客户端**：用于发送命令。客户端在开发机器上运行。您可以通过发出 `adb` 命令从命令行终端调用客户端。
- **守护程序 (adbd)**：用于在设备上运行命令。守护程序在每个设备上作为后台进程运行。
- **服务器**：用于管理客户端与守护程序之间的通信。服务器在开发机器上作为后台进程运行。

`adb` 包含在 Android SDK 平台工具软件包中。您可以使用 [SDK 管理器](https://developer.android.com/studio/intro/update?hl=zh-cn#sdk-manager)下载此软件包，该管理器会将其安装在 `android_sdk/platform-tools/` 下。

## adb 的工作原理

当您启动某个 `adb` 客户端时，该客户端会先检查是否有 `adb` 服务器进程已在运行。如果没有，它会启动服务器进程。服务器在启动后会与本地 TCP 端口 5037 绑定，并监听 `adb` 客户端发出的命令。

**注意**：所有 `adb` 客户端均使用端口 5037 与 `adb` 服务器通信。

然后，服务器会与所有正在运行的设备建立连接。它通过扫描 5555 到 5585 之间（该范围供前 16 个模拟器使用）的奇数号端口查找模拟器。服务器一旦发现 `adb` 守护程序 (adbd)，便会与相应的端口建立连接。

每个模拟器都使用一对按顺序排列的端口：一个用于控制台连接的偶数号端口，另一个用于 `adb` 连接的奇数号端口。例如：

模拟器 1，控制台：5554
模拟器 1，`adb`：5555
模拟器 2，控制台：5556
模拟器 2，`adb`：5557
依此类推。

如上所示，在端口 5555 处与 `adb` 连接的模拟器与控制台监听端口为 5554 的模拟器是同一个。

服务器与所有设备均建立连接后，您便可以使用 `adb` 命令访问这些设备。由于服务器管理与设备的连接，并处理来自多个 `adb` 客户端的命令，因此您可以从任意客户端或从某个脚本控制任意设备。

## 启用详细日志记录功能

[Firebase Analytics](https://firebase.google.cn/docs/analytics/events?hl=zh-cn&platform=android)

```
adb shell setprop log.tag.FA VERBOSE
adb shell setprop log.tag.FA-SVC VERBOSE
adb logcat -v time -s FA FA-SVC
```



[Android Developers命令行工具](https://developer.android.com/tools/adb?hl=zh-cn#shellcommands)



## 获取屏幕控件及布局

```bash
adb shell uiautomator dump /sdcard/window_dump.xml
```



https://blog.51cto.com/u_16213459/13137848





