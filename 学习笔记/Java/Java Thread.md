# Thread

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

```java
/**
 * Allocates a new {@code Thread} object. This constructor has the same
 * effect as {@linkplain #Thread(ThreadGroup,Runnable,String) Thread}
 * {@code (null, null, gname)}, where {@code gname} is a newly generated
 * name. Automatically generated names are of the form
 * {@code "Thread-"+}<i>n</i>, where <i>n</i> is an integer.
 */
public Thread() {
    init(null, null, "Thread-" + nextThreadNum(), 0);
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

在自己的业务里，肯定要避免直接通过`Thread.setDefaultUncaughtExceptionHandler`来处理崩溃问题，

线程中异常的处理流程

- 

## 查看app进程的cpu数量

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



# 线程池

[Java Guide Java 线程池详情](https://javaguide.cn/java/concurrent/java-thread-pool-summary.html#executor-%E6%A1%86%E6%9E%B6%E4%BB%8B%E7%BB%8D)

Java 提供的线程池实现

线程池就是管理一系列线程的资源池，其提供了一种限制和管理线程资源的方式。每个线程池还维护一些基本统计信息，例如已完成任务的数量。池化技术的思想主要是为了减少每次获取资源的消耗，提高对资源的利用率。

- **降低资源消耗**。通过重复利用已创建的线程降低线程创建和销毁造成的消耗。

- **提高响应速度**。当任务到达时，任务可以不需要等到线程创建就能立即执行。

- **提高线程的可管理性**。线程是稀缺资源，如果无限制的创建，不仅会消耗系统资源，还会降低系统的稳定性，使用线程池可以进行统一的分配，调优和监控。

## `Executor` 框架

`Executor` 框架是 Java5 之后引进的，在 Java 5 之后，通过 `Executor` 来启动线程比使用 `Thread` 的 `start` 方法更好，除了更易管理，效率更好（用线程池实现，节约开销）外，还有关键的一点：有助于避免 this 逃逸问题。

![img](https://oss.javaguide.cn/github/javaguide/java/concurrent/executor-class-diagram.png)

`Executor` 框架不仅包括了线程池的管理，还提供了线程工厂、队列以及拒绝策略等，`Executor` 框架让并发编程变得更加简单。

具体要关注的类是`ThreadPoolExecutor`



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

- 
