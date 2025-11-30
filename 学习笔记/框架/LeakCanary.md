## LeakCanary集成后为什么有新的图标

`taskAffinity`  



![image-20250704151509444](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20250704151509444.png)



LeakCanary免注册逻辑

通过`ContentProvider`自动初始化`leakcanary.internal.MainProcessAppWatcherInstaller` ；对于页面的监听通过Curtains框架处理的；`Curtains`会通过``Hook`技术代理 `WindowManagerGlobal#mViews`

>  `WindowManagerGlobal#mViews` 本质是一个`ArrayList` 但是被`Curtains`代理没有维护原列表；如果业务自己的逻辑有同样的`Hook`点，在实际运行时会被`Curtains`代理替换掉，导致自己的`Hook`失效
>
> 尤其自己的`Hook`逻辑是在`ContentProvider`做的；这种情况下即便是考虑到`ContentProvider`初始化，并声明了`initOrder`，仍然可能会出现某些环境下打出的包，在不同的设备上还是会被替代的问题（这块不太确定是因为什么原因导致的）
>
> 有个解决方案是通过反射去触发一次`Curtains`框架的懒加载。

![image-20250704151659082](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20250704151659082.png)
