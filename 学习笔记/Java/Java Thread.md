# Thread

[Thread-Android Developer](https://developer.android.com/reference/java/lang/Thread#Thread())

## 1.1 Thread类结构

### 类声明

`Thread`类实现`Runnable`接口，内部持有`Runnable`对象；

```java
public
class Thread implements Runnable {
  	private Runnable target;
  
    @Override
    public void run() {
        if (target != null) {
            target.run();
        }
    }
}
```

### 构造方法

`Thread`构造方法最后都会执行`init`

```java
 
    public Thread() {
        init(null, null, "Thread-" + nextThreadNum(), 0);
    }

    public Thread(Runnable target) {
        init(null, target, "Thread-" + nextThreadNum(), 0);
    }

    Thread(Runnable target, AccessControlContext acc) {
        init(null, target, "Thread-" + nextThreadNum(), 0, acc, false);
    }

    public Thread(ThreadGroup group, Runnable target) {
        init(group, target, "Thread-" + nextThreadNum(), 0);
    }

    public Thread(String name) {
        init(null, null, name, 0);
    }

    public Thread(ThreadGroup group, String name) {
        init(group, null, name, 0);
    }

    public Thread(Runnable target, String name) {
        init(null, target, name, 0);
    }

    public Thread(ThreadGroup group, Runnable target, String name) {
        init(group, target, name, 0);
    }

    public Thread(ThreadGroup group, Runnable target, String name,
                  long stackSize) {
        init(group, target, name, stackSize);
    }
```

### ThreadGroup

`ThreadGroup`（线程组）是Java中用于组织线程的一种结构，它提供了对线程的层次化管理。通过线程组，可以将一组线程组织成一个树状结构，方便对线程进行统一控制和管理。

### State

线程的状态，在`Thread`中定义为枚举

```java
    /**
     * A thread state.  A thread can be in one of the following states:
     * @since   1.5
     * @see #getState
     */
    public enum State {
        /**
         * Thread state for a thread which has not yet started.
         */
        NEW,

        /**
         * Thread state for a runnable thread.  A thread in the runnable
         * state is executing in the Java virtual machine but it may
         * be waiting for other resources from the operating system
         * such as processor.
         */
        RUNNABLE,

        /**
         * Thread state for a thread blocked waiting for a monitor lock.
         * A thread in the blocked state is waiting for a monitor lock
         * to enter a synchronized block/method or
         * reenter a synchronized block/method after calling
         * {@link Object#wait() Object.wait}.
         */
        BLOCKED,

        /**
         * Thread state for a waiting thread.
         * A thread is in the waiting state due to calling one of the
         * following methods:
         * <ul>
         *   <li>{@link Object#wait() Object.wait} with no timeout</li>
         *   <li>{@link #join() Thread.join} with no timeout</li>
         *   <li>{@link LockSupport#park() LockSupport.park}</li>
         * </ul>
         *
         * <p>A thread in the waiting state is waiting for another thread to
         * perform a particular action.
         *
         * For example, a thread that has called <tt>Object.wait()</tt>
         * on an object is waiting for another thread to call
         * <tt>Object.notify()</tt> or <tt>Object.notifyAll()</tt> on
         * that object. A thread that has called <tt>Thread.join()</tt>
         * is waiting for a specified thread to terminate.
         */
        WAITING,

        /**
         * Thread state for a waiting thread with a specified waiting time.
         * A thread is in the timed waiting state due to calling one of
         * the following methods with a specified positive waiting time:
         * <ul>
         *   <li>{@link #sleep Thread.sleep}</li>
         *   <li>{@link Object#wait(long) Object.wait} with timeout</li>
         *   <li>{@link #join(long) Thread.join} with timeout</li>
         *   <li>{@link LockSupport#parkNanos LockSupport.parkNanos}</li>
         *   <li>{@link LockSupport#parkUntil LockSupport.parkUntil}</li>
         * </ul>
         */
        TIMED_WAITING,

        /**
         * Thread state for a terminated thread.
         * The thread has completed execution.
         */
        TERMINATED;
    }
```



## 1.2 异常处理

**Java**

﻿`Thread`中包含一个名为`uncaughtExceptionHandler`的成员变量和`defaultUncaughtExceptionHandler`的静态变量；

线程任务抛出异常未被`try-catch`时，线程被杀，`uncaughtExceptionHandler.uncaughtException()`方法被回调；

线程池中线程任务抛出异常未被`try-catch`会导致该线程被杀，之后会创建新线程处理后续任务;



```
/**
 * Dispatch an uncaught exception to the handler. This method is
 * intended to be called only by the JVM.
 */
private void dispatchUncaughtException(Throwable e) {
    getUncaughtExceptionHandler().uncaughtException(this, e);
}
```



**特别的：**Java的线程池模型中有`ScheduledThreadPoolExecutor`的线程池实现，比如`Executors.newSingleThreadScheduledExecutor()`。该线程池在调用`execute`方法时会将`Runnable`对象封装成`ScheduledFutureTask`(父类`FutureTask`)。任务执行时`FutureTask.run`会对`Runnable`做异常捕获，**不再抛出异常和打印堆栈**。



**Android**

﻿`Android`平台，`Android`初始化时设置了`Thread`全局的`uncaughtExceptionHandler`，当线程任务抛出异常未被`try-catch`在`uncaughtExceptionHandler. uncaughtException()`中**会主动杀死当前进程并退出，见下图**；

同样的，当使用`ScheduledThreadPoolExecutor`时，异常在`FutureTask`捕获，也不会打印异常堆栈。此时线程也没有死掉。

![image-20250529174530412](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20250529174530412.png)

![image-20250529174551454](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20250529174551454.png)

在自己的业务里，避免直接通过`Thread.setDefaultUncaughtExceptionHandler`来处理崩溃问题，

### 查看app进程的cpu数量

### 1. adb shell

```
# 1. 查看包的进程信息，取进程号
adb shell ps|grep <package>

# 2. 查看指定进程的状态信息
adb shell cat /proc/<pid>/status

# 3. 获取详细线程列表
$adb shell -T | grep <pid>

# 4. 获取线程数量
$adb shell ps -T | grep <pid> | wc -l
```

### 2. Android Studio CPU Prifiler

使用时很卡，不关注了。。。



## 1.3 守护线程

### **JVM 程序在什么情况下能够正常退出？**

​	The Java Virtual Machine exits when the only threads running are all daemon threads.

​	**当 JVM 中不存在任何一个正在运行的非守护线程时，则 JVM 进程即会退出。**

### **守护线程和普通线程的区别**

- 均是`Thread`；通过成员变量`daemon`标识

  - `Thread` 实例化时，`daemon`被赋值，通过`this.daemon = parent.isDaemon`

  - ```java
    private void init(ThreadGroup g, Runnable target, String name,
                      long stackSize, AccessControlContext acc,
                      boolean inheritThreadLocals) {
      	// ...
        Thread parent = currentThread();
      
    	  this.daemon = parent.isDaemon();
      	// ...
    }
    ```

- 当有普通线程运行时JVM不会退出；

**Sample1: 创建非守护线程**

```java
public class MainEntrance {
    public static void main(String[] args) {
        Runtime.getRuntime().addShutdownHook(new Thread(() -> System.out.println("JVM退出！")));

        Thread thread = new Thread(() -> {
            while (true) {
                try {
                    TimeUnit.SECONDS.sleep(1);
                    System.out.println("线程运行");
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        });
        thread.start();

        try {
            TimeUnit.SECONDS.sleep(5);
            System.out.println("主线程结束");
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}
```

程序运行结果：

``` bash
线程运行
线程运行
线程运行
线程运行
主线程结束
线程运行
线程运行
线程运行
...
```

**Sample2: 创建守护线程**

```java
public class MainEntrance {
    public static void main(String[] args) {
        Runtime.getRuntime().addShutdownHook(new Thread(() -> System.out.println("JVM退出！")));

        Thread thread = new Thread(() -> {
            while (true) {
                try {
                    TimeUnit.SECONDS.sleep(1);
                    System.out.println("线程运行");
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        });
        // 设置为守护线程
        thread.setDaemon(true);
        thread.start();

        try {
            TimeUnit.SECONDS.sleep(5);
            System.out.println("主线程结束");
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}
```

**程序运行结果：**

```bash
线程运行
线程运行
线程运行
线程运行
主线程结束
JVM退出！
```

使用实例

正常业务逻辑可能不会涉及到；一个经典的守护线程实例就是**垃圾回收线程**

## 1.4 生命周期/底层原理

涉及创建、调度和状态管理

### 线程创建

Java中创建线程的两种方式：继承Thread类或实现Runnable接口；最终都会调用操作系统提供的线程创建接口；

线程创建后Thread类会进入`init`方法对`Thread` 做初始化；`init`方法对参数有：线程组、线程名、runnable对象等

```java
    /**
     * Initializes a Thread.
     *
     * @param g the Thread group
     * @param target the object whose run() method gets called
     * @param name the name of the new Thread
     * @param stackSize the desired stack size for the new thread, or
     *        zero to indicate that this parameter is to be ignored.
     * @param acc the AccessControlContext to inherit, or
     *            AccessController.getContext() if null
     * @param inheritThreadLocals if {@code true}, inherit initial values for
     *            inheritable thread-locals from the constructing thread
     */
    private void init(ThreadGroup g, Runnable target, String name,
                      long stackSize, AccessControlContext acc,
                      boolean inheritThreadLocals) {
      	// 线程名不为空，如果没有指定线程名，会有全局自增id来生成 Thread-123
        if (name == null) {
            throw new NullPointerException("name cannot be null");
        }
      
      	//
    }      
```



### native方法

#### `registerNatives()`

类加载时静态方法

```java
public
class Thread implements Runnable {
    /* Make sure registerNatives is the first thing <clinit> does. */
    private static native void registerNatives();
    static {
        registerNatives();
    }
  
  	// ...
}
```



# 并发技术

[Object - Java 8](https://docs.oracle.com/javase/8/docs/api/java/lang/Object.html)

## 线程并发

### synchronized



### wait()/notify()/notifyAll()

```tex
This method should only be called by a thread that is the owner of this object's monitor. A thread becomes the owner of the object's monitor in one of three ways:

By executing a synchronized instance method of that object.
By executing the body of a synchronized statement that synchronizes on the object.
For objects of type Class, by executing a synchronized static method of that class.
```



### 对象头/monitor

[对象头](https://www.cnblogs.com/hongdada/p/14087177.html)

## 线程池

[Java Guide Java 线程池详情](https://javaguide.cn/java/concurrent/java-thread-pool-summary.html#executor-%E6%A1%86%E6%9E%B6%E4%BB%8B%E7%BB%8D)

[Java Guid Java 线程池最佳实践](https://javaguide.cn/java/concurrent/java-thread-pool-best-practices.html)

Java 提供的线程池实现

线程池就是管理一系列线程的资源池，其提供了一种限制和管理线程资源的方式。每个线程池还维护一些基本统计信息，例如已完成任务的数量。池化技术的思想主要是为了减少每次获取资源的消耗，提高对资源的利用率。

- **降低资源消耗**。通过重复利用已创建的线程降低线程创建和销毁造成的消耗。

- **提高响应速度**。当任务到达时，任务可以不需要等到线程创建就能立即执行。

- **提高线程的可管理性**。线程是稀缺资源，如果无限制的创建，不仅会消耗系统资源，还会降低系统的稳定性，使用线程池可以进行统一的分配，调优和监控。

### `Executor` 框架

`Executor` 框架是 Java5 之后引进的，在 Java 5 之后，通过 `Executor` 来启动线程比使用 `Thread` 的 `start` 方法更好，除了更易管理，效率更好（用线程池实现，节约开销）外，还有关键的一点：有助于避免 this 逃逸问题。

![img](https://oss.javaguide.cn/github/javaguide/java/concurrent/executor-class-diagram.png)

`Executor` 框架不仅包括了线程池的管理，还提供了线程工厂、队列以及拒绝策略等，`Executor` 框架让并发编程变得更加简单。

具体要关注的类是`ThreadPoolExecutor`，另外一种是``ScheduledThreadPoolExecutor` 



### 线程池参数

```java
    /**
     * 用给定的初始参数创建一个新的ThreadPoolExecutor。
     */
    public ThreadPoolExecutor(int corePoolSize,//线程池的核心线程数量
                              int maximumPoolSize,//线程池的最大线程数
                              long keepAliveTime,//当线程数大于核心线程数时，多余的空闲线程存活的最长时间
                              TimeUnit unit,//时间单位
                              BlockingQueue<Runnable> workQueue,//任务队列，用来储存等待执行任务的队列
                              ThreadFactory threadFactory,//线程工厂，用来创建线程，一般默认即可
                              RejectedExecutionHandler handler//拒绝策略，当提交的任务过多而不能及时处理时，我们可以定制策略来处理任务
                               ) {
        if (corePoolSize < 0 ||
            maximumPoolSize <= 0 ||
            maximumPoolSize < corePoolSize ||
            keepAliveTime < 0)
            throw new IllegalArgumentException();
        if (workQueue == null || threadFactory == null || handler == null)
            throw new NullPointerException();
        this.corePoolSize = corePoolSize;
        this.maximumPoolSize = maximumPoolSize;
        this.workQueue = workQueue;
        this.keepAliveTime = unit.toNanos(keepAliveTime);
        this.threadFactory = threadFactory;
        this.handler = handler;
    }
```



`ThreadPoolExecutor` 3 个最重要的参数：

- `corePoolSize` : 核心线程数，任务队列未达到队列容量时，最大可以同时运行的线程数量。
- `maximumPoolSize` : 任务队列中存放的任务达到队列容量的时候，当前可以同时运行的线程数量变为最大线程数。
- `workQueue`: 新任务来的时候会先判断当前运行的线程数量是否达到核心线程数，如果达到的话，新任务就会被存放在队列中。

`ThreadPoolExecutor`其他常见参数 :

- `keepAliveTime`:线程池中的线程数量大于 `corePoolSize` 的时候，如果这时没有新的任务提交，核心线程外的线程不会立即销毁，而是会等待，直到等待的时间超过了 `keepAliveTime`才会被回收销毁。
- `unit` : `keepAliveTime` 参数的时间单位。
- `threadFactory` :executor 创建新线程的时候会用到。
- `handler` :拒绝策略（后面会单独详细介绍一下）



## **发散：**

- 一般情况下我们不会直接直接创建线程，而是使用线程池；

- 线程池的设计：

  - **产品**：侧重完整解决方案；监控、治理

    - 产品包含多条业务，每个业务都可能会维护自己的一套线程池；三方SDK也会存在线程池；

    https://tech.qimao.com/xian-cheng-shu-liang-you-hua/

    https://juejin.cn/post/6850037281621803015

  - **业务使用**：`Executors`；三方框架的线程池设计；

  - **技术原理**：从Thread入手 从0～1来设计线程池 ==> ThreadPoolExecutor的设计原理

    - 线程管理 核心线程+最大线程；核心线程销毁；阻塞队列

  - 都要从`java.util.concurrent`的角度出发

- 异常处理

- corePool Size

  - 怎么取

- 开源框架中是怎么设计的线程池

  - Glide
  - RxJava
  - OkHttp

线程池设计优化

-  `Executors.newSingleThreadExecutor`方法创建的线程池优化
- `ScheduleThreadPool`中运行的任务如果抛出异常是catch不到的。即便是配置`setUncaughtExceptionHandler`。根本原因是提交到该线程池的`Runnable`会被做一层`FutureTask`封装。



注意：

- 有界队列设置队列容量，否则有可能OOM
- ThreadLocal
  - 脏数据

