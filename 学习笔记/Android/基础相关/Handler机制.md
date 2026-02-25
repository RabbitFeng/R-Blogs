`IdleHandler`

```java
# MessageQueue.java
/**
 * Callback interface for discovering when a thread is going to block
 * waiting for more messages.
 */
public static interface IdleHandler {
    /**
     * Called when the message queue has run out of messages and will now
     * wait for more.  Return true to keep your idle handler active, false
     * to have it removed.  This may be called if there are still messages
     * pending in the queue, but they are all scheduled to be dispatched
     * after the current time.
     */
    boolean queueIdle();
}
```

`IdleHandler`本身是定义在MessageQueue中的一个接口，和Handler机制中的Handler定义不同。IdleHandler的设计是在``MessageQueue`消息队列为空或者下一个消息尚未到达时使用的。



Looper.loop()会进入一个死循环，循环调用 MessageQueue.next()方法。MessageQueue.next()也是一个死循环，这里怎么做到主线程死循环，但又能响应屏幕事件分发的呢。

触摸事件的分发起点不是在`MessageQueue`中排队，而是在``nativePollOnce()``方法中: 从`dispatchTouchEvent`方法中打印调用链可以看到：

- DOWN, UP 这类事件会从`nativePollOnce()`中得到处理

```
  at androidx.appcompat.view.WindowCallbackWrapper.dispatchTouchEvent(WindowCallbackWrapper.java:70)
  at com.android.internal.policy.DecorView.dispatchTouchEvent(DecorView.java:817)
  at com.android.internal.policy.DecorView.dispatchTouchEvent(DecorView.java:805)
  at android.view.View.dispatchPointerEvent(View.java:15242)
  at android.view.ViewRootImpl$ViewPostImeInputStage.processPointerEvent(ViewRootImpl.java:8344)
  at android.view.ViewRootImpl$ViewPostImeInputStage.onProcess(ViewRootImpl.java:8084)
  at android.view.ViewRootImpl$InputStage.deliver(ViewRootImpl.java:7459)
  at android.view.ViewRootImpl$InputStage.onDeliverToNext(ViewRootImpl.java:7516)
  at android.view.ViewRootImpl$InputStage.forward(ViewRootImpl.java:7482)
  at android.view.ViewRootImpl$AsyncInputStage.forward(ViewRootImpl.java:7664)
  at android.view.ViewRootImpl$InputStage.apply(ViewRootImpl.java:7490)
  at android.view.ViewRootImpl$AsyncInputStage.apply(ViewRootImpl.java:7721)
  at android.view.ViewRootImpl$InputStage.deliver(ViewRootImpl.java:7463)
  at android.view.ViewRootImpl$InputStage.onDeliverToNext(ViewRootImpl.java:7516)
  at android.view.ViewRootImpl$InputStage.forward(ViewRootImpl.java:7482)
  at android.view.ViewRootImpl$InputStage.apply(ViewRootImpl.java:7490)
  at android.view.ViewRootImpl$InputStage.deliver(ViewRootImpl.java:7463)
  at android.view.ViewRootImpl.deliverInputEvent(ViewRootImpl.java:10956)
  at android.view.ViewRootImpl.doProcessInputEvents(ViewRootImpl.java:10858)
  at android.view.ViewRootImpl.enqueueInputEvent(ViewRootImpl.java:10811)
  at android.view.ViewRootImpl$WindowInputEventReceiver.onInputEvent(ViewRootImpl.java:11209)
  at android.view.InputEventReceiver.dispatchInputEvent(InputEventReceiver.java:310)
  
  at android.os.MessageQueue.nativePollOnce(Native Method) // 从nativePollOnce中处理的
  at android.os.MessageQueue.next(MessageQueue.java:374)
  
  at android.os.Looper.loopOnce(Looper.java:163)
  at android.os.Looper.loop(Looper.java:293)
  at android.app.ActivityThread.loopProcess(ActivityThread.java:10022)
  at android.app.ActivityThread.main(ActivityThread.java:10011)
  at java.lang.reflect.Method.invoke(Native Method)
  at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:586)
  at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:1242)
```

```
	//.. 
  at android.view.ViewRootImpl$InputStage.deliver(ViewRootImpl.java:7463)
  at android.view.ViewRootImpl.deliverInputEvent(ViewRootImpl.java:10956)
  at android.view.ViewRootImpl.doProcessInputEvents(ViewRootImpl.java:10858)
  at android.view.ViewRootImpl.enqueueInputEvent(ViewRootImpl.java:10811)
  at android.view.ViewRootImpl$WindowInputEventReceiver.onInputEvent(ViewRootImpl.java:11209)
  
  at android.view.InputEventReceiver.dispatchInputEvent(InputEventReceiver.java:310)
  at android.view.InputEventReceiver.nativeConsumeBatchedInputEvents(Native Method)
  at android.view.InputEventReceiver.consumeBatchedInputEvents(InputEventReceiver.java:283)
  at android.view.ViewRootImpl.doConsumeBatchedInput(ViewRootImpl.java:11115)
  at android.view.ViewRootImpl$ConsumeBatchedInputRunnable.run(ViewRootImpl.java:11401)
  at android.view.Choreographer$CallbackRecord.run(Choreographer.java:1599)
  at android.view.Choreographer.doCallbacks(Choreographer.java:1263)
  at android.view.Choreographer.doFrame(Choreographer.java:1119)
  at android.view.Choreographer$FrameDisplayEventReceiver.run(Choreographer.java:1549)
  at android.os.Handler.handleCallback(Handler.java:966)
  at android.os.Handler.dispatchMessage(Handler.java:110)
  
  at android.os.Looper.loopOnce(Looper.java:205)
  at android.os.Looper.loop(Looper.java:293)
  at android.app.ActivityThread.loopProcess(ActivityThread.java:10022)
  at android.app.ActivityThread.main(ActivityThread.java:10011)
  at java.lang.reflect.Method.invoke(Native Method)
  at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:586)
  at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:1242)
```



对于按下抬起这类的触摸事件来说，`ViewRootImpl`会及时处理`ViewRootImpl.doProcessInputEvents` 对于滑动这类高频事件，会批处理，

1. - `ViewRootImpl` 会配合 `Choreographer`，将一帧时间内（如 16.6ms）产生的多个硬件层面的 Move 采样点合并成一个 `MotionEvent`。你可以通过 `getHistoricalX()` 获取被合并的中间点坐标。

**`nativePollOnce`:**

**阻塞休眠**：当 Java 层的 `MessageQueue` 里没有消息，或者下一条消息还没到执行时间时，主线程会执行到这个方法。此时，线程会交出 CPU 资源，进入一种**“挂起”**状态。

**多路复用监听**：它利用了 Linux 的 **`epoll`** 机制。在休眠的同时，它其实在监听好几个“闹钟”：

1. **Java 消息闹钟**：下一个定时消息的时间到了。
2. **Native 信号**：也就是你最关心的**触摸事件**、传感器数据等通过 `InputChannel`（Socket）传来的信号。
3. **主动唤醒**：其他线程往主线程发了消息，手动捅醒它。``enqueueMessage`

