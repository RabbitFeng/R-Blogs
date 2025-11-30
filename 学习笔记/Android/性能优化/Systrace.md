[Android Systrace 基础知识 -- Systrace 简介](https://www.androidperformance.com/2019/05/28/Android-Systrace-About/)

[Android Studio 了解Systrace](https://source.android.com/docs/core/tests/debug/systrace?hl=zh-cn)

Systrace自动插桩

## ﻿[背景](http://tekes.baidu-int.com/docs-v2/#/references/topics/performance/public/perftools/systrace/systrace?id=背景)﻿

手机百度在低端机有严重的性能问题，需要全面彻底的分析低端机性能问题，Android可选工具有，TraceView和Systrace，TraceView有严重的运行时开销，不能反应真实耗时，Systrace由于内核支持，对性能损耗较小，因此选择systrace。

Android Systrace是google强推的性能分析神器，基于sample的，需要手动写代码在方法前后插入Trace。如果要分析全流程，使用比较复杂，不够便捷，为了提高性能分析的效率，开发了Systrace自动插桩工具，自动插入Trace代码，提高分析效率。

## ﻿[可以解决什么问题](http://tekes.baidu-int.com/docs-v2/#/references/topics/performance/public/perftools/systrace/systrace?id=可以解决什么问题)﻿

***\*1.获取App所有线程的方法调用\****

***\*2.获取Android系统的关键调用，如binder、view绘制、ams等系统服务的关键Trace\****

***\*3.获取CPU调度信息、锁、内存等信息\****

## ﻿[Systrace简介](http://tekes.baidu-int.com/docs-v2/#/references/topics/performance/public/perftools/systrace/systrace?id=systrace简介)﻿

Systrace是Android4.1中新增的性能数据采样和分析工具。它的思想很朴素，在系统的一些关键链路（比如`System Service`，`虚拟机`，`Binder驱动`）插入一些信息（Trace），通过Trace的开始和结束来确定某个核心过程的执行时间，然后把这些Trace信息收集起来得到系统关键路径的运行时间信息，进而得到整个系统的运行性能信息。Android Framework里面一些重要的模块都插入了Trace信息（Java层的通过android.os.Trace类完成，native层通过ATrace宏完成），用户App中可以添加自定义的Trace，这样就组成了一个完成的性能分析系统。

### ﻿[添加Trace](http://tekes.baidu-int.com/docs-v2/#/references/topics/performance/public/perftools/systrace/systrace?id=添加trace)﻿

```plain
class Test {
     public void test() {
         Trace.benginSection("test");
         // 方法体
         Trace.endSection();
     }
}
```

***\*注：beginSection和endSection需要成对调用，否则会导致Trace异常，出现did not finish的问题\****

### ﻿[Systrace组成](http://tekes.baidu-int.com/docs-v2/#/references/topics/performance/public/perftools/systrace/systrace?id=systrace组成)﻿

***\*内核部分\****：Systrace 利用了 Linux Kernel 中的 ftrace 功能。ftrace 是 Linux 内核中的调试跟踪机制。

***\*数据采集部分\****：Java层的通过android.os.Trace类完成，Native层通过ATrace宏完成。应用程序可把统计信息输出给ftrace。同时，Android 还有一个 atrace 程序，它可以从 ftrace 中读取统计信息然后交给数据分析工具来处理。

***\*数据分析工具\****：Android 提供一个 systrace.py（ python 脚本文件，位于 Android SDK目录/platform-tools/systrace 中，其内部将调用 atrace 程序）用来配置数据采集的方式（如采集数据的标签、输出文件名等）和收集 ftrace 统计数据并生成一个结果网页文件供用户查看。

![img](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/imageDownloadAddress-20250702105046609.png)

### ﻿[Systrace脚本](http://tekes.baidu-int.com/docs-v2/#/references/topics/performance/public/perftools/systrace/systrace?id=systrace脚本)﻿

手机上App上的环境准备好以后，打开PC端的命令行；进入systrace的目录，也即(假设$ANDROID_HOME是你Android SDK的根目录）：

```plain
cd $ANDROID_HOME/platform-tools/systrace
```

然后执行如下命令：

```plain
python systrace.py -t 10 sched gfx view wm am app webview -a <package-name>
```

其中package-name为App的包名

这样，`systrace.py`这个脚本就通过adb给手机发送了收集trace的通知；与此同时，可以在手机上进行你需要分析的操作，比如点击Launcher中App的Icon启动App
，或者进入某个Activity开始滑动ListView/RecyclerView。经过你指定的时间之后（以上是10s），就会有trace数据生成在当前目录，默认是`trace.html`；用Chrome浏览器打开即可。

举例：

```plain
python systrace.py dalvik app sched idle frep load view -b 90960 -a com.baidu.searchbox  -o xiaomi_cold_start_normal.html
```

﻿`systrace.py`命令的一般用法是：

```plain
python systrace.py [options] [category1 [category2 ...]]
```

其中，`[options]`是一些命令参数，`[category]`等是你感兴趣的系统模块，比如view代表view系统（包含绘制流程），am代表ActivityManager（包含Activity创建过程等）；分析不同问题的时候，可以选择不同你感兴趣的模块。需要重复的是，尽可能缩小需要Trace的模块，其一是数据量小易与分析；其二，虽然systrace本身开销很小，但是缩小需要Trace的模块也能减少运行时开销。比如你分析卡顿的时候，`power`,`webview`就几乎是无用的。

﻿`[option]`中比较重要的几个参数如下：

```plain
-a <package_name>：这个选项可以开启指定包名App中自定义Trace Label的Trace功能。也就是说，如果你在代码中使用了`Trace.beginSection("tag")`, `Trace.endSection`；默认情况下，你的这些代码是不会生效的，因此，这个选项一定要开启！
﻿
-b 90960 表示buffer size，如果抓到的systrace用Chrome浏览器打开后发现解析有问题，可以尝试加大buffer size，操作时间越长，-b buffer
 size 就要跟着增大
﻿
-t N：用来指定Trace运行的时间，取决于你需要分析过程的时间；还是那句话，在需要的时候尽可能缩小时间；当然，绝对不要把时间设的太短导致你操作没完Trace就跑完了，这样会出现Did not finish 的标签，分析数据就基本无效了。
﻿
-l：这个用来列出你分析的那个手机系统支持的Trace模块；也就是上面命令中 [category1]能使用的部分；不同版本的系统能支持的模块是不同的，一般来说，高版本的支持的模块更多。
﻿
-o FILE：指定trace数据文件的输出路径，如果不指定就是当前目录的trace.html。
```

﻿`systrace.py -l`可以输出手机能支持的Trace模块，而且输出还给出了此模块的用途；常用的模块如下：

```plain
app:应用的跟踪信息，如果没有则不支持收集APP的Trace
﻿
sched: CPU调度的信息，非常重要；你能看到CPU在每个时间段在运行什么线程；线程调度情况，比如锁信息。
﻿
gfx：Graphic系统的相关信息，包括SerfaceFlinger，VSYNC消息，Texture，RenderThread等；分析卡顿非常依赖这个。
﻿
view: View绘制系统的相关信息，比如onMeasure，onLayout等；对分析卡顿比较有帮助。
﻿
am：ActivityManager调用的相关信息；用来分析Activity的启动过程比较有效。
﻿
dalvik: 虚拟机相关信息，比如GC停顿等。
﻿
binder_driver: Binder驱动的相关信息，如果你怀疑是Binder IPC的问题，不妨打开这个。
﻿
core_services: SystemServer中系统核心Service的相关信息，分析特定问题用。
```

## ﻿[Systrace自动插桩工具](http://tekes.baidu-int.com/docs-v2/#/references/topics/performance/public/perftools/systrace/systrace?id=systrace自动插桩工具)﻿

Systrace自动插桩工具是一个gradle编译插件，通过ASM字节码修改框架，在编译期间动态修改字节码，在App所有代码的方法开始和结束点插入Trace代码。从而达到跟踪所有方法的方案。

### ﻿[插桩方案](http://tekes.baidu-int.com/docs-v2/#/references/topics/performance/public/perftools/systrace/systrace?id=插桩方案)﻿

Systrace采样代码Trace.beginSection和Trace.endSection需要在各种复杂情况下成对调用。理想的方案是使用Try-Finally包裹，如下所示：

```plain
class Test {
     public void test() {
       try {
             Trace.benginSection("com.sample.systrace.Test.test.()V");
             // 方法体
         } finally {
             Trace.endSection();
         }
     }
}
```

这种方式可以保证Trace.beginSection和Trace.endSection无论是运行代码发生异常，还是提前return都能成对调用。但是由于在字节码的指令里，没有finally指令，只有try-catch指令，try-finally其实是用try-catch间接实现的。示例代码如下：

```plain
class Test {
    public void testMethod(boolean a, boolean b) {
        try {
            Trace.beginSection("TestNewClass.testMethod.()V");
            if (!a) {
                throw new RuntimeException("test throw");
            }
        if (b) {
            Trace.endSection();
            return;
        }
        Trace.endSection();
        } catch(throwable e) {
            Trace.endSection();
            throw e;
        }
    }
}
```

这种实现逻辑：
a) try catch住整个方法体，在方法开始点插入Trace.beginSection，并且在catch块开始点插入Trace.endSection()，并且抛出捕获的异常。
b) 各种return结束结束指令前面插入Trace.endSection()。
c) 忽略athrow指令，不在athrow前面插入Trace.endSection()，由catch块统一处理。
这种实现就是try-finally的间接实现，从而完全保证Trace.beginSection和Trace.endSection的成对执行。

### ﻿[插桩优化和其他功能](http://tekes.baidu-int.com/docs-v2/#/references/topics/performance/public/perftools/systrace/systrace?id=插桩优化和其他功能)﻿

#### ﻿[支持release收集Trace](http://tekes.baidu-int.com/docs-v2/#/references/topics/performance/public/perftools/systrace/systrace?id=支持release收集trace)﻿

Systrace官方文档说待trace的App必须是debuggable的，想要尽可能的反应真实的性能，我们需要在release包上也支持收集Trace日志。
分析systrace源码之后 ，发现这个条件只是个障眼法而已；我们可以手动开启App的自定义Label的Trace功能，方法也很简单，调用一个函数即可；但是这个函数是SDK @hide的，我们需要反射调用：

```plain
Class<?> trace = Class.forName("android.os.Trace");
Method setAppTracingAllowed = trace.getDeclaredMethod("setAppTracingAllowed", boolean.class);
setAppTracingAllowed.invoke(null, true);
```

Systrace插件实现是在App的Application attachBaseContext中，通过ASM动态增加以上代码，动态打开Release包的Trace收集。

#### ﻿[插桩方法过滤](http://tekes.baidu-int.com/docs-v2/#/references/topics/performance/public/perftools/systrace/systrace?id=插桩方法过滤)﻿

对于一些简单的get、set、空方法会进行一些自动过滤

#### ﻿[插桩黑白名单机制](http://tekes.baidu-int.com/docs-v2/#/references/topics/performance/public/perftools/systrace/systrace?id=插桩黑白名单机制)﻿

支持增加编译时配置黑白名单，规则如下：

```plain
# 可以将某个class加入白名单中
-keepclass com/sample/systrace/TestIgnoreFile
# 可以将某个package加入白名单中
-keeppackage android
-keeppackage org
# 为注释内容，会忽略
﻿
# 指定该类下所有方法都插桩
-unkeepclass com.sample.systrace.Test
# 指定该包下所有类的方法都插桩
-unkeeppackage com.sample.systrace
```

***\*case分享：\****
下面的Trace是分析EventBus耗时问题，手百老版本EventBus是用rxjava实现，调用栈很深，这块Trace收集也会有性能损耗，层级越深，性能损耗越大。这种情况会误导有性能问题，把rx
相关的包加入白名单不插桩，性能问题不存在了，或者很小。
最佳实践：把一些调用层级很深的类，不进行插桩，如：rxjava、okhttp相关类等

![img](https://ku.baidu-int.com/wiki/attach/image/api/imageDownloadAddress?attachId=257c4d835c204c6f8bad64a37bf4b732&docGuid=XoQc760mC7bM3u)



字节Btrace

