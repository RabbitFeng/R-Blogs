# `流程` 

## `View.invalidate`环节都做了什么？

**第一阶段：设置标志位 (Setting Flags)**

当你调用某个 `View` 的 `invalidate()` 时，它内部首先会做两件事：

1. **添加标志位**：给当前的 View 打上 `PFLAG_DIRTY`（脏标记）和 `PFLAG_INVALIDATED` 标签。这告诉系统：“这个 View 的内容过时了，需要重画”。
2. **计算区域**：确定需要重绘的矩形区域（Rect）。

```
void invalidateInternal(int l, int t, int r, int b, boolean invalidateCache,
            boolean fullInvalidate) {
		// 打上Dirty标记
    mPrivateFlags |= PFLAG_DIRTY;
    
}
```



**第二阶段：逐级冒泡 (Parent Invalidation)**

View 自身无法直接触发屏幕刷新，它必须请求父容器。

- View 调用 `mParent.invalidateChild(this, rect)`。
- `ViewGroup` 收到请求后，将区域坐标转换为父容器的坐标系，并继续调用其父容器的方法。
- 这个过程一直向上延伸，直到到达 View 树的顶端：**ViewRootImpl**



**第三阶段：ViewRootImpl 调度 (Scheduling)**

一旦到达 `ViewRootImpl`，它会执行 `scheduleTraversals()` 方法：

1. **发送同步屏障**：防止普通消息阻塞 UI 任务。
2. **向 Choreographer 注册**：正如我们之前讨论的，它请求下一个 VSync 信号。



**第四阶段：执行绘制 (Execution)**

当 VSync 信号到达，`Choreographer` 触发 `doFrame`，最终回到 `ViewRootImpl` 执行 `performTraversals()`：

- 由于是 `invalidate` 触发，系统通常跳过 `onMeasure` 和 `onLayout`（除非标志位显示需要重新布局）。
- 系统根据之前的 `PFLAG_DIRTY` 标记，只对被标记为“脏”的 View 调用 `draw()` -> `onDraw()`。



## LayoutInflater.inflate()环节都做了什么

- **解析 XML**：读取文件并解析标签。

- **反射创建 View**：通过类名反射实例化每一个 View 对象。

- **构建 View 树**：建立层级关系。

能否在子线程``inflate()``

# 线程安全

子线程中操作UI(包括加载布局，更新内容等)，需要考虑的方向：

- **是否存在线程检查**
  - 「FrameWork」: `ViewRootImpl#requestLayout`
- **是否依赖`Looper`实例**
  - `Toast`-> NPE
    - `Toast实例化`会在`getLooper()`方法中检查`looper`是否为空。默认取Looper.myLooper()，接受一个传值，相关Looper传值方法在FrameWork标记为了@Hide
  - `Dialog`-> 无响应
    - `show()`方法通过消息机制



## 子线程是否能更新UI?

一般来说，不能。ViewRootImpl会对`requestLayout`做检查，会触发`android.view.ViewRootImpl$CalledFromWrongThreadException`

```
android.view.ViewRootImpl$CalledFromWrongThreadException: Only the original thread that created a view hierarchy can touch its views.
  at android.view.ViewRootImpl.checkThread(ViewRootImpl.java:12164)
  at android.view.ViewRootImpl.requestLayout(ViewRootImpl.java:2540)
```



技术探讨：子线程当然可以去更新。既然抛出异常的行为来自`ViewRootImpl.requestLayout`的线程检查。**在`ViewRootImpl`实例创建前在子线程去更新就不会触发这个异常**。

`ViewRootImpl`是什么时候创建的呢？`WindowManagerGlobal#addView`，这个时机在``View`布局添加到`Window`时，以Activity的生命周期为例，

- `Activity` 一般是在`onCreate`方法中去`inflate`加载布局，`onResume`中`ViewRootImpl`才创建完成
- `Dialog`原生Dialog的生命周期



## 子线程是否能展示Dialog?

- `android.app.AlertDialog`  ✔︎ 
  - `show()` 方法依赖Handler消息机制，子线程需要`Looper.prepare`和`Looper.loop`

- `androidx.appcompact.app.AlertDialog` ✘
  - 线程检查





触摸事件 - 绘制 - 消息机制



`Android`主线程，以`ActivityThread.main()`为入口，通过`Looper.loop()`方法进入一个死循环，同时通过`Linux`的`epoll`机制平衡随时待命和低能耗。

-> **按下** -> `nativePollOnce` -> **ViewRootImpl**-> 

