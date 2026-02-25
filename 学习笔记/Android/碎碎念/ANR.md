https://juejin.cn/post/7171684761327370277

# ANR原因

如果 Android 应用的**界面线程处于阻塞状态的时间过长**，会触发“应用无响应”(ANR) 错误。如果应用位于前台，系统会向用户显示一个对话框。

ANR场景

- **输入调度超时**：如果您的应用在 5 秒内未响应输入事件（例如按键或屏幕触摸）。
  - 输入调度超时的原理和其他几类不同，当前事件超时本身不会ANR，只有后续操作事件到来时检查到超时才会ANR；也就是说，即便超时，如果没有Input，也不会造成ANR

- **执行服务**：如果应用声明的服务无法在几秒内完成 `Service.onCreate()` 和 `Service.onStartCommand()`/`Service.onBind()` 执行。
  - **未调用 Service.startForeground()**：如果您的应用使用 `Context.startForegroundService()` 在前台启动新服务，但该服务在 5 秒内未调用 `startForeground()`。

- **intent 广播**：如果 [`BroadcastReceiver`](https://developer.android.com/reference/android/content/BroadcastReceiver?hl=zh-cn) 在设定的一段时间内没有执行完毕。如果应用有任何前台 activity，此超时期限为 5 秒。
- **JobScheduler 互动**：如果 [`JobService`](https://developer.android.com/reference/android/app/job/JobService?hl=zh-cn) 未在几秒钟内从 `JobService.onStartJob()` 或 `JobService.onStopJob()` 返回，或者如果[用户发起的作业](https://developer.android.com/reference/android/app/job/JobParameters?hl=zh-cn#isUserInitiatedJob())启动，而您的应用在调用 `JobService.onStartJob()` 后的几秒内未调用 `JobService.setNotification()`。对于以 Android 13 及更低版本为目标平台的应用，ANR 会保持静默状态，且不会报告给应用。对于以 Android 14 及更高版本为目标平台的应用，ANR 会保持活动状态，并会报告给应用。

# ANR原理

​	[Android ANR机制](https://gityuan.com/2019/04/06/android-anr/)

# ANR数据导出

本地通过adb到处，高版本可以通过bugreport，低版本导出trace文件即可

```
# 高版本
$ adb shell bugreport > bugreport.zip

# 或者直接导出 (较老版本)
$ adb pull /data/anr/traces.txt

# 查看是否存在traces.txt文件
$ adb shell ls -a data/anr/
# 结果示例
# .
# ..
# anr_2026-02-05-13-01-45-246
```



# ANR上报



ANR原因&修复