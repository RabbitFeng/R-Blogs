# `Window`、`WindowManager`

---

> `Window`表示窗口的概念，日常开发一般不会遇到，特殊情况下如开发一个悬浮窗就会用到`Window`实现。`PhoneWindow`是唯一实现类。`Window`的具体实现位于`WindowManagerService`中
>
> `WindowManager`是外界访问`Window`的入口。`Window`具体是现在`WindowManagerService`中。`WindowManager`和`WindowManagerService`的交互是`IPC`过程。

## 1. `Window`和`WindowManager`

一般流程：

在`AndroidManifest`清单列表中声明权限（如果不声明，在系统权限列表中可能找不到，权限也无法开启）

```xml
    <!-- 应用外悬浮球 -->
    <uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />
    <uses-permission android:name="android.permission.SYSTEM_OVERLAY_WINDOW" />
```

`Java`代码中的流程：

```java
// 在四大组件中获取`WindowManager`
WindowManager windowManager = getWindowManager(); // Activity
// WindowManager windowManager = (WindowManager)context.getSystemService(Context.WINDOW_SERVICE);// Context
WindowManager.LayoutParams layoutParams = new WindowManager.LayoutParams() {
    {
        type = Build.VERSION.SDK_INT >= Build.VERSION_CODES.O ?
            TYPE_APPLICATION_OVERLAY : TYPE_PHONE;
        width = WRAP_CONTENT;
        height = WRAP_CONTENT;
        flags = FLAG_NOT_TOUCH_MODAL | FLAG_NOT_FOCUSABLE;
        format = PixelFormat.TRANSLUCENT;
        layoutAnimationParameters = new LayoutAnimationController.AnimationParameters();
    }
};

// 动态权限申请
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
    if (!PermissionUtils.isGrantedDrawOverlays()) {
        PermissionUtils.requestDrawOverlays(new PermissionUtils.SimpleCallback() {
            @Override
            public void onGranted() {
                windowManager.addView(floatBinding.getRoot(), layoutParams);
            }

            @Override
            public void onDenied() {

            }
        });
    } else {
        try {
            if (floatBinding.getRoot().getWindowToken() == null) {
                windowManager.addView(floatBinding.getRoot(), layoutParams);
            }
        } catch (WindowManager.BadTokenException | WindowManager.InvalidDisplayException | SecurityException e) {
            e.printStackTrace();
        }
    }
}
```

`WindowManager.LayoutParams`中声明了`Window`的参数，其中

`Flags`表示了`Window`显示特性，常用的选项：

- `FLAG_NOT_FOCUSABLE`

  表示`Window`不需要获取焦点，也不需要接收各种输入事件。此标记会同时启用`FLAG_NOT_TOUCH_MODEL`，最终时间会直接传递给下层的具有焦点的`Window`

- `FLAG_NOT_TOUCH_MODEL`

  在此模式下，系统会将当前`Window`区域以外的单击事件传递给底层的`Window`，当前`Window`区域内的单击事件则自己处理。这个标记比较重要，一般来说都需要开启此标记，否则其他`Window`无法收到单击事件。

- `FLOAG_SHOW_WHEN_LOCKED`

  此模式下，`Window`可以展示在锁屏界面