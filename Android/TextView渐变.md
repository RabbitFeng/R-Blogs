# 1. `TextView`字体渐变色(线性渐变)及动效

## **需求**

- 文本渐变色（从左向右的两种颜色的渐变）
- 使用动画过渡到另一种渐变色

图示：

> `Color.RED` - `Color.GREEN`

![image-20210901211202353](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20210901211202353.png)

> `Color.BLUE` - `Colot.YELLOW`

![image-20210901211143614](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20210901211143614.png)

## **核心内容**

### 1.  着色器(`Shader`)

> https://developer.android.google.cn/reference/kotlin/android/graphics/Shader?hl=en

![image-20210901195557326](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20210901195557326-16443889282661.png)

`Shader`共有`5`个子类：

- `LinearGradient`：线性渲染器
- `SweepGradient`：梯度渲染器(扫描渲染)
- `RadialGradient`：环形渲染器
- `BitmapShader`：图像渲染器
- `ComposeShader`：组合渲染器

### 2.  属性动画

> **`API 11+`**提供了属性动画
>
> 移步`Android Developer`：`https://developer.android.com/guide/topics/graphics/prop-animation?hl=zh-cn#value-animator`

**估值器(`TypeEvaluator`)**

> 设置属性值从初始值过渡到结束值的变化具体数值

提供了以下几种估值器实现方式

>`IntEvaluator`：以整型的形式从初始值 - 结束值 进行过渡
>`FloatEvaluator`：以浮点型的形式从初始值 - 结束值 进行过渡
>`ArgbEvaluator`：以`Argb`类型的形式从初始值 - 结束值 进行过渡
>`TypeEvaluator`：自定义估值器



**插值器(`Interpolator`)**

> 估值器定义了属性动画如何计算指定的属性的值。

系统内置插值器：

| 作用                | Java类                                     |
| ------------------- | ------------------------------------------ |
| 匀速                | `LinearInterpolator`                       |
| 加速                | `AccelerateInterpolator`                   |
| 减速                | `DecelerateInterpolator`                   |
| 加速-减速           | `AccelerateDecelerateInterpolator`         |
| 退后-加速           | `AnticipateInterpolator`                   |
| 退后-加速-超出      | `AnticipateOvershootInterpolator`          |
| 超出                | `OvershootInterpolator`                    |
| 周期                | `CycleInterpolator`                        |
| 弹性球              | `BounceInterpolator`                       |
| **Android 5.0新增** | **`androidx.interpolator.view.animation`** |
| 加速-匀速           | `FastOutLinearInInterpolator`              |
| 匀速-减速           | `LinearOutSlowInInterpolator`              |
| 加速-减速           | `FastOutSlowInInterpolator`                |

![4834678-dacd871ac5adc8ab](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/4834678-dacd871ac5adc8ab.webp)

自定义插值器



**`ValueAnimator`**

- 属性动画中的核心类。直接子类包括`ObjectAnimator`和`TimeAnimator`；
- 通过设置监听器(`ValueAnimator.AnimatorUpdateListener`)可以得到某数值从初始值到结束值的一系列变化；
- 通过设置对象的属性值（颜色、透明度、位置等）实现动画。

初始化方法：

> - `ValueAnimator.ofInt(int... values)`：至少提供两个整型参数，获取整型值变化 （左闭右闭区间）
> - `ValueAnimator.ofArgb(int... values)`：至少提供两个整型表示的颜色值，获取颜色变化（左闭右闭区间）
> - `ValueAnimator.ofFloat(float... values)`：至少提供两个浮点型参数，获取浮点值变化（左闭右闭区间）
> - `ValueAnimator.ofObject(TypeEvaluator evaluator, Object... values)`：
> - `ValueAnimator.ofPropertyValuesHolder(PropertyValuesHolder... values)`： （没用过）

使用方法：

1. Java代码（推荐）

```java
// 创建ValueAnimator
ValueAnimator valueAnimator = ValueAnimator.ofInt(0, 100); 
// 设置持续时间
valueAnimator.setDuration(1000);
// 添加监听器
valueAnimator.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {
    @Override
    public void onAnimationUpdate(ValueAnimator animation) {
        // 获取变化值
        int animationValue = (int) animation.getAnimatedValue();
        // 设置控件属性值，如位置颜色等。
        binding.tvText.setWidth(animationValue);
        ...       
    }
});
// 还可以添加AnimatorListenerAdaper获取运行状态的回调
valueAnimator.addListener(new AnimatorListenerAdapter() {
    @Override
    public void onAnimationCancel(Animator animation) {
        super.onAnimationCancel(animation);
    }

    @Override
    public void onAnimationEnd(Animator animation) {
        super.onAnimationEnd(animation);
    }

    @Override
    public void onAnimationRepeat(Animator animation) {
        super.onAnimationRepeat(animation);
    }

    @Override
    public void onAnimationStart(Animator animation) {
        super.onAnimationStart(animation);
    }

    @Override
    public void onAnimationPause(Animator animation) {
        super.onAnimationPause(animation);
    }

    @Override
    public void onAnimationResume(Animator animation) {
        super.onAnimationResume(animation);
    }

    @Override
    public void onAnimationStart(Animator animation, boolean isReverse) {
    }

    @Override
    public void onAnimationEnd(Animator animation, boolean isReverse) {
    }
});

// ValueAnimator对应的操作
valueAnimator.start(); 
valueAnimator.pause();
valueAnimator.resume();
valueAnimator.cancel();
valueAnimator.end();
valueAnimator.reverse();
// ValueAnimator对应状态
valueAnimator.isStarted();
valueAnimator.isRunning();
valueAnimator.isPaused();

...
```

2. `xml`资源文件

推荐使用`Java`，即便是使用了`xml`文件定义，最后还要解析为`Java`

> 补充说明，开发过程中修改`xml`文件的代价更小，改动`java`文件需要`build`项目

通过在 XML 中定义动画，您可以轻松地在多个 Activity 中重复使用动画，还能更轻松地修改动画序列。

---

## 实现过程

### 1.  文字渐变色

#### **`Demo01`: 文字渐变色**

> **实现方式**
>
> - 为`TextView`的`Paint`设置着色器`LinearGradient`并重绘

```java
public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";

    private ActivityMainBinding binding;

    /**
     * 预设颜色
     */
    public static final int COLOR_1 = Color.RED;
    public static final int COLOR_2 = Color.GREEN;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        init();
    }zhe

    private void init() {
        binding.btnExecute.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // 着色器-线性渐变
                LinearGradient lg1 = new LinearGradient(0, 0, binding.tvText.getWidth(), 0, COLOR_1, COLOR_2, Shader.TileMode.CLAMP);
                binding.tvText.getPaint().setShader(lg1);
                binding.tvText.invalidate();
            }
        });
    }
}
```

> **说明**
>
> - **初始化`LinearGradient`需要获取控件的宽度(或高度)。需要注意控件创建、测量和布局顺序，避免获取到`width()`为0**

![image-20210901211202353](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20210901211202353.png)

### 2.  文字渐变色的更换

#### **`Demo02`：文本渐变色的更换**

> **实现方式**
>
> - 两个`LinearGradien`
>
> - 使用标志位`flag`（或其他方式)控制使用哪一个`LinearGradient`作为`TextView`的着色器

```java
public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";

    private ActivityMainBinding binding;

    /**
     * 预设颜色
     */
    public static final int COLOR_1 = Color.RED;
    public static final int COLOR_2 = Color.GREEN;
    public static final int COLOR_3 = Color.BLUE;
    public static final int COLOR_4 = Color.YELLOW;

    /**
     * 标志位，文本状态
     */
    private boolean flag = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        init();
    }

    private void init() {
        binding.btnExecute.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                LinearGradient lg1 = new LinearGradient(0, 0, binding.tvText.getWidth(), 0, COLOR_1, COLOR_2, Shader.TileMode.CLAMP);
                LinearGradient lg2 = new LinearGradient(0, 0, binding.tvText.getWidth(), 0, COLOR_3, COLOR_4, Shader.TileMode.CLAMP);
                flag = !flag;
                binding.tvText.getPaint().setShader(flag ? lg2 : lg1);
                binding.tvText.invalidate();
            }
        });
    }
}
```

> **说明**
>
> - 使用两个（或任意数量）`LinearGradient`，通过标志位`flag`为`Paint`设置着色器并重绘。

![image-20210902190937381](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20210902190937381.png)

![image-20210902191007770](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20210902191007770.png)

### 3. 文本渐变色动画

>基于`Demo02`做一些思考，同时也要结合动画的实现方式。
>
>- 属性动画
>
>用于设置控件的属性，比如位置、透明度、背景色等。
>
>- 估值器
>
>`Android API`提供了估值器实现：
>
> - `整数型 IntEvaluator`
>
> - `浮点型 FloatEvaluator`
>
> - `颜色 ArgbEvaluator`
>
>- `自定义估值器 TypeEvaluator`
>
> 从一种颜色过渡到另一种颜色容易联想到使用`ArgbEvaluator`，那么使用`ValueAnimator.ofArgb()`方法，创建两个`ValueAnimator`获取 
>
> - 起始位置颜色`COLOR_1 -> COLOR_3`
> - 结束位置颜色`COLOR_2 -> COLOR_4`
>
> 然后获取每次变化的起始位置颜色和结束位置颜色并以此更新`LinearGradient`，为`TextView`设置着色器并重绘，似乎是一个不错的方案。可惜的是，查看`LinearGradient`源码或文档，发现并没有提供所期待的`setStartColor`和`setEndColor`方法来用于更新`LinearGradient`。`LinearGradient`所提供给的是来自其父类`Shader`的两个方法。(`Matrix` 矩阵？告辞告辞……)
>
> ![image-20210902194814639](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20210902194814639.png)
>
> 那么只能获取到颜色值并创建一个新的`LinearGradient`？？貌似是可行的……但绝对并不是一个理想的方式(`短时间内创建大量对象`、`GC`、`内存抖动`这种）
>
> 几种或许可行的思路：
>
> - 不能更新`LinearGradient`只能去不断创建。抛开`ValueAnimator`更新值的时间间隔，两个`ValueAnimator`之间的执行顺序，若执行`1s`的动画，如果每`100ms`做一次重绘，那也只需要创建大概20次`LinearGradient`（起始位置颜色+结束位置颜色），使用数据结构保存下来，那么就可以对其进行复用。听起来不错（码+1）
> - 另一种方式可以设置`TextView`的`alpha`值也就是透明度来实现`淡出淡入`的动画效果。（码+1+！）
> - 还有一种方式(先卖个关子，`无奖竞猜?`)
>
> 基于上述三种思路，依次实现一个`Demo`

#### **`Demo03_1`：创建并复用`LinearGradient`**

> 先不考虑复用，直接跑。使用

```java
public class MainActivity extends AppCompatActivity implements ValueAnimator.AnimatorUpdateListener {
    private static final String TAG = "MainActivity";

    private ActivityMainBinding binding;

    /**
     * 预设颜色
     */
    public static final int COLOR_1 = Color.RED;
    public static final int COLOR_2 = Color.GREEN;
    public static final int COLOR_3 = Color.BLUE;
    public static final int COLOR_4 = Color.YELLOW;

    private int startColor = COLOR_1;
    private int endColor = COLOR_2;

    private ValueAnimator startColorAnimator;
    private ValueAnimator endColorAnimator;

    private long duration = 1000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        init();
    }


    private void init() {
        startColorAnimator = ValueAnimator.ofArgb(COLOR_1, COLOR_3);
        endColorAnimator = ValueAnimator.ofArgb(COLOR_2, COLOR_4);

        startColorAnimator.setDuration(duration);
        endColorAnimator.setDuration(duration);

        startColorAnimator.addUpdateListener(this);
        endColorAnimator.addUpdateListener(this);

        binding.btnExecute.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startColorAnimator.start();
                endColorAnimator.start();
            }
        });
    }

    // 记录一下onAnimationUpdate执行的次数
    private static int count = 0;

    @Override
    public void onAnimationUpdate(ValueAnimator animation) {
        Log.d(TAG, "onAnimationUpdate: " + (++count));
        int color = (int) animation.getAnimatedValue();
        if (animation == startColorAnimator) {
            startColor = color;
        } else {
            endColor = color;
        }

        LinearGradient linearGradient = new LinearGradient(0, 0, binding.tvText.getWidth(), 0, startColor, endColor, Shader.TileMode.CLAMP);
        binding.tvText.getPaint().setShader(linearGradient);
        binding.tvText.invalidate();
    }
}
```

![LinearGradient_1](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/LinearGradient_1.gif)

`BA~NICE~`(手动`GIF`)

看一下`onAnimationUpdate`执行次数

![image-20210902203605636](../../../git-typora/mine/Record/images/image-20210902203605636.png)

（手贱党乱入）

![image-20210902203811413](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20210902203811413.png)

……`优化ing`

```java
public class MainActivity extends AppCompatActivity implements ValueAnimator.AnimatorUpdateListener {
    private static final String TAG = "MainActivity";

    private ActivityMainBinding binding;

    /**
     * 预设颜色
     */
    public static final int COLOR_1 = Color.RED;
    public static final int COLOR_2 = Color.GREEN;
    public static final int COLOR_3 = Color.BLUE;
    public static final int COLOR_4 = Color.YELLOW;

    private int startColor = COLOR_1;
    private int endColor = COLOR_2;

    private ValueAnimator startColorAnimator;
    private ValueAnimator endColorAnimator;

    private long duration = 1000;

    /**
     * 设置时间阈值，过滤阈值内的颜色变化
     */
    private final long timeThreshold = 100;

    /**
     * 上次执行时间
     */
    private long lastExecuteTime = 0;

    /**
     * 当前时间
     */
    private long currentTime;

    /**
     * 动画开始时间
     */
    private long startTime;

    /**
     * 缓存LinearGradient
     */
    private SparseArray<LinearGradient> linearGradientSparseArray = new SparseArray<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        init();
    }

    private void init() {
        startColorAnimator = ValueAnimator.ofArgb(COLOR_1, COLOR_3);
        endColorAnimator = ValueAnimator.ofArgb(COLOR_2, COLOR_4);

        startColorAnimator.setDuration(duration);
        endColorAnimator.setDuration(duration);

        startColorAnimator.addUpdateListener(this);
        endColorAnimator.addUpdateListener(this);

        binding.btnExecute.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startTime = System.currentTimeMillis();
                startColorAnimator.start();
                endColorAnimator.start();
            }
        });
    }

    private static int count = 0;

    @Override
    public void onAnimationUpdate(ValueAnimator animation) {
        currentTime = System.currentTimeMillis();
        // 过滤掉时间阈值内的变化值
        if (currentTime - lastExecuteTime < timeThreshold) {
            return;
        }
        lastExecuteTime = currentTime;
        // 自定义key的映射规则：当前时间与开始时间的差值，除以时间阈值`timeThreshold`映射到[0-N]
        int key = (int) ((currentTime - startTime) / timeThreshold);
        LinearGradient linearGradient = linearGradientSparseArray.get(key);
        if (linearGradient == null) {
            Log.d(TAG, "onAnimationUpdate: new LinearGradient" + (++count));
            int color = (int) animation.getAnimatedValue();
            if (animation == startColorAnimator) {
                startColor = color;
            } else {
                endColor = color;
            }
            linearGradient = new LinearGradient(0, 0, binding.tvText.getWidth(), 0, startColor, endColor, Shader.TileMode.CLAMP);
            linearGradientSparseArray.put(key, linearGradient);
        }
        binding.tvText.getPaint().setShader(linearGradient);
        binding.tvText.invalidate();
    }
}
```

![LinearGradient_缓存](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/LinearGradient_%E7%BC%93%E5%AD%98.gif)

![image-20210903104440921](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20210903104440921.png)

> 两次执行也仅创建了10个对象，所以基于时间阈值使用缓存策略是可行。并且动画效果也可（能看出稍有卡顿，毕竟是每`100ms`执行获得一种渐变色，简单粗暴的方式是降低时间阈值，比如设置为`50ms`即可获得更好的动画表现）

> 那么至此，一次单程动画需要创建 `duration/timeThreshold`个`LinearGradient`对象……做一下小学数学，间隔`1m`种一棵树，共需要11棵树……很容易就看出其实这样的写法会舍弃起始和终止状态的准确色值（也可以做一些优化，但是个人觉得没有必要了）。基于上面的实现方式，做动画的返程，也就是撤销过程。

回顾一下`ValueAnimator`提供的`API`中的`reverse`，也很好奇它的一个实现方式。

![image-20210903110226193](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20210903110226193.png)

也就是说，调用`ValueAnimator#reverse`会使得其取值（视觉表现为动画）的原路返回。这就很有帮助了，否则还要写一个`ValueAnimator`的返程动画。另外继续看：如果动画正在运行那么会撤回；如果动画未运行，则会从`END`向`START`运行。

> `Tips`
>
> - `ValueAnimator#start()`方法每次调用会使得动画从`START`向`END`重新运行一次。
> - 如果调用了`ValueAnimator#reverse()`，动画会在当前位置撤销回`START`，结束动画之前再次调用`reverse()`，动画又会从当前位置撤销回`END`。
> - 如果为`ValueAnimator`添加了监听器`AnimatorListenerAdapter`获取到`onAnimationStart()`回调，切记这个方法不止在单程的动画(`START- END`)时触发，同样在返程时(`END - START`)也会触发。`onAnimationEnd()`同理。
> - 如果在`RUNNING`过程中`reverse`，这一次的返程动画是不会再次回调`onAnimationStart()`的，动画结束后会回调`onAnimationEnd()`，之后再`start()`或者`reverse()`启动动画才会再次调用`onAnimationStart()`方法。强调一下这一点，因为如果需要在代码逻辑中添加对于`REVERSING`的控制（`API`中是没有提供方法直观表明是否在`isReversing`的，估计和频繁`reverse()`使动画返回横跳有关，并不好定义去其状态 -- `撤销撤销撤销状态`？？禁止套娃。另外，现在`onAnimationStart`和`ValueAnimator#start()`已经使得`start`这个概念很容易被曲解了）

......`Reversing`

```java
public class MainActivity extends AppCompatActivity implements ValueAnimator.AnimatorUpdateListener {
    private static final String TAG = "MainActivity";

    private ActivityMainBinding binding;

    /**
     * 预设颜色
     */
    public static final int COLOR_1 = Color.RED;
    public static final int COLOR_2 = Color.GREEN;
    public static final int COLOR_3 = Color.BLUE;
    public static final int COLOR_4 = Color.YELLOW;

    private int startColor = COLOR_1;
    private int endColor = COLOR_2;

    private ValueAnimator startColorAnimator;
    private ValueAnimator endColorAnimator;

    private long duration = 1000;

    /**
     * 设置时间阈值，过滤阈值内的颜色变化
     */
    private final long timeThreshold = 50;

    /**
     * 动画播放时间
     */
    private long currentPlayTime = 0;

    /**
     * 缓存LinearGradient
     */
    private SparseArray<LinearGradient> linearGradientSparseArray = new SparseArray<>();

    /**
     * 标志位，是否可执行撤销
     */
    private boolean canReverse = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        init();
    }

    private void init() {
        startColorAnimator = ValueAnimator.ofArgb(COLOR_1, COLOR_3);
        endColorAnimator = ValueAnimator.ofArgb(COLOR_2, COLOR_4);

        startColorAnimator.setDuration(duration);
        endColorAnimator.setDuration(duration);

        startColorAnimator.addUpdateListener(this);
        endColorAnimator.addUpdateListener(this);

        startColorAnimator.addListener(new AnimatorListenerAdapter() {
            @Override
            public void onAnimationStart(Animator animation) {
                super.onAnimationStart(animation);
            }
        });

        binding.btnExecute.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (!canReverse) {
                    canReverse = true;
                    startColorAnimator.start();
                    endColorAnimator.start();
                }
            }
        });

        binding.btnReverse.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (canReverse) {
                    canReverse = false;
                    startColorAnimator.reverse();
                    endColorAnimator.reverse();
                }
            }
        });

    }

    private static int count = 0;

    @Override
    public void onAnimationUpdate(ValueAnimator animation) {

        currentPlayTime = animation.getCurrentPlayTime();
        // 映射到key
        int key = (int) (currentPlayTime / timeThreshold);
        if (!canReverse) {
            key = linearGradientSparseArray.size() - key - 1;
        }
        LinearGradient linearGradient = linearGradientSparseArray.get(key);
        if (linearGradient == null) {
            Log.d(TAG, "onAnimationUpdate: new LinearGradient" + (++count));
            int color = (int) animation.getAnimatedValue();
            if (animation == startColorAnimator) {
                startColor = color;
            } else {
                endColor = color;
            }
            linearGradient = new LinearGradient(0, 0, binding.tvText.getWidth(), 0, startColor, endColor, Shader.TileMode.CLAMP);
            linearGradientSparseArray.put(key, linearGradient);
        }
        if (binding.tvText.getPaint().getShader() != linearGradient) {
            binding.tvText.getPaint().setShader(linearGradient);
            binding.tvText.invalidate();
        }
    }
}
```

![LinearGradient_reverse](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/LinearGradient_reverse.gif)

> 添加标志位`canReverse`标识是否可执行撤销，在点击事件中手动更新。（也可以通过为`ValueAnimator`添加监听器来实现）
>
> 现在的文本默认是无状态的，渐变并没有能够自动上色。原因在于操作在了`Activity`创建过程，此时`View`绘制还未开始。所以为了使得文本初始时即有颜色，就要通过在其他方式（比如在其他生命周期或者获得控件绘制的相关信息）
>
> 为`TextView`控件添加`OnLayoutChangeListener`即可解决

```java
binding.tvText.addOnLayoutChangeListener(new View.OnLayoutChangeListener() {
    @Override
    public void onLayoutChange(View v, int left, int top, int right, int bottom, int oldLeft, int oldTop, int oldRight, int oldBottom) {
        LinearGradient linearGradient = new LinearGradient(0, 0, right - left, 0, startColor, endColor, Shader.TileMode.CLAMP);
        linearGradientSparseArray.put(0, linearGradient);
        binding.tvText.getPaint().setShader(linearGradient);
        binding.tvText.invalidate();
    }
});
```

> **小结：**
>
> - 使用`LinearGradient`为`TextView`绘制渐变色是我所知的最简单的做法（目前来看也是唯一做法）
> - 但是`LinearGradient`似乎只能初始化设定颜色值，所以需要不断创建。
> - 使用某种规则（比如时间阈值或者进度）实现缓存策略可以降低不断创建`LinearGradient`的开销。但是当动画时间延长以及多个控件需要执行动画时，仍会在内存中保留大量的`LinearGradient`对象。
> - 代码逻辑放在`Activity`中，复用性极差。应当考虑自定义`View`方式为它做封装。

#### **`Demo03_2`：使用透明度控制渐变色动画**

>  有了`Demo03_1`的基础，直接用动画

```java
public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";

    private ActivityMainBinding binding;

    /**
     * 预设颜色
     */
    public static final int COLOR_1 = Color.RED;
    public static final int COLOR_2 = Color.GREEN;
    public static final int COLOR_3 = Color.BLUE;
    public static final int COLOR_4 = Color.YELLOW;

    private long duration = 1000;

    private LinearGradient lg1;
    private LinearGradient lg2;

    private ValueAnimator alphaAnimator;

    private float oldValueAnimation = 1.0f;

    private boolean canReverse;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        init();
    }

    private void init() {
        alphaAnimator = ValueAnimator.ofFloat(1, -1);
        alphaAnimator.setDuration(duration);
        alphaAnimator.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {
            @Override
            public void onAnimationUpdate(ValueAnimator animation) {
                float animatedValue = (float) animation.getAnimatedValue();
                if (oldValueAnimation > 0 && animatedValue <= 0) { // 正值过渡到负值
                    binding.tvText.getPaint().setShader(lg2);
                    binding.tvText.invalidate();
                } else if (oldValueAnimation < 0 && animatedValue >= 0) {
                    binding.tvText.getPaint().setShader(lg1);
                    binding.tvText.invalidate();
                }
                oldValueAnimation = animatedValue;
                binding.tvText.setAlpha(Math.abs(oldValueAnimation));
            }
        });

        binding.btnExecute.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (!canReverse) {
                    canReverse = true;
                    alphaAnimator.start();
                }
            }
        });

        binding.btnReverse.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (canReverse) {
                    canReverse = false;
                    alphaAnimator.reverse();
                }
            }
        });

        binding.tvText.addOnLayoutChangeListener(new View.OnLayoutChangeListener() {
            @Override
            public void onLayoutChange(View v, int left, int top, int right, int bottom, int oldLeft, int oldTop, int oldRight, int oldBottom) {
                lg1 = new LinearGradient(0, 0, right - left, 0, COLOR_1, COLOR_2, Shader.TileMode.CLAMP);
                lg2 = new LinearGradient(0, 0, right - left, 0, COLOR_3, COLOR_4, Shader.TileMode.CLAMP);
                binding.tvText.getPaint().setShader(canReverse ? lg2 : lg1);
                binding.tvText.invalidate();
            }
        });

    }
}
```

> **小结**
>
> - 创建两个`LinearGradient`，设置控件透明度实现动画效果；
> - 控件透明度变为0（或者接近0）时使用`SetShader()`并重绘；
> - 优点在于动画效果不依赖于大量的`LinearGradient`对象，逻辑比较简单，控制好边界即可

#### **`Demo03_3`：使用`Matrix`渐变色动画**

![image-20210903154518137](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20210903154518137.png)

> 首先看一下`LinearGradient`的`API`，可用的是继承自父类`Shader`的`getLocalMatrix`以及`setLocalMatrix`。
>
> 简单了解`Matrix`会知道，`Matrix`是用于处理图形的`3*3`的矩阵，可用于缩放、平移、错切之类操作的运算。
>
> 这里只需了解其`public`方法中的`translate`即平移。

> 猜想：通过`Matrix`来平移`LinearGradient`……会不会使得着色器渲染的位置发生偏移？？

```java
package com.rabbit.example;

import android.graphics.Color;
import android.graphics.LinearGradient;
import android.graphics.Matrix;
import android.graphics.Shader;
import android.os.Bundle;
import android.view.View;

import androidx.appcompat.app.AppCompatActivity;

import com.rabbit.example.databinding.ActivityMainBinding;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";

    private ActivityMainBinding binding;

    /**
     * 预设颜色
     */
    public static final int COLOR_1 = Color.RED;
    public static final int COLOR_2 = Color.GREEN;

    private LinearGradient linearGradient;

    private Matrix matrix = new Matrix();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        init();
    }

    private void init() {
        binding.btnExecute.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                matrix.setTranslate(binding.tvText.getWidth() / 2f, 0f);
                linearGradient.setLocalMatrix(matrix);
                binding.tvText.invalidate();
            }
        });

        binding.tvText.addOnLayoutChangeListener(new View.OnLayoutChangeListener() {
            @Override
            public void onLayoutChange(View v, int left, int top, int right, int bottom, int oldLeft, int oldTop, int oldRight, int oldBottom) {
                linearGradient = new LinearGradient(0, 0, right - left, 0, COLOR_1, COLOR_2, Shader.TileMode.CLAMP);
                binding.tvText.getPaint().setShader(linearGradient);
                binding.tvText.invalidate();
            }
        });
    }
}
```



![matrix_demo](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/matrix_demo.gif)

> 如预期：`matrx.translate()`配合`linearGradient.setLocalMatrix()`确实可以使得着色器对文本的渲染平移一段指定的距离。(因为`LinearGradient`使用的是`TileMode.CLAMP`的填充模式，所以边缘之外会填充边缘色的纯色)。

> 另外值得一提的是，`LinearGradient`本质是着色器，从直观感受上来看，它的功能就在于描述`View`在特定位置的颜色信息。
>
> 参考其构造方法，可以传入`int[] colors`的颜色数组，同时使用`int[] positions`描述其颜色的位置信息（`0f-1f`）。这样就可以将多个颜色保存在同一个`LinearGradient`中了。同时还能得到相邻两个颜色之间过渡的渐变色。
>
> 那么，只需要将`LinearGradient`的x轴渐变色设置为从`0`-`Width`（若采用两种渐变色，每种渐变色包含首尾两种颜色，为了实现良好的动效，这个宽度应当至少为原`TextView`的两倍或者三倍），然后通过`Matrix`进行平移即可完成动画效果。

![image-20210903161732982](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20210903161732982.png)

![gradient_matrix](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/gradient_matrix.gif)



至此，文本渐变色以及文本渐变色过渡动画已经实现了，但是所有的控制逻辑都放在了`Activity`中，使用繁琐且复用性极差。

#### **`Demo04`：自定义View实现文本渐变色以及渐变动画**

***`GradientTextView.java`***

```java
public class GradientTextView extends AppCompatTextView {
    private static final String TAG = "GradientTextView";

    //// xml属性值 ///
    /**
     * 渐变色方向
     */
    private int gradientOrientation;

    public static final int ORIENTATION_LEFT_TO_RIGHT = 0x00; // 渐变方向-从左向右
    public static final int ORIENTATION_TOP_TO_BOTTOM = 0x01; // 渐变方向-从顶向底

    /**
     * 文字渐变颜色
     * 0 - 开始位置颜色 startColorFrom
     * 1 - 结束位置颜色 endColorFrom
     * 2 - 开始位置颜色 startColorTo
     * 3 - 结束位置颜色 endColorTo
     */
    private int[] textGradientColors = new int[4];

    /**
     * 背景渐变色
     */
    private int[] backgroundGradientColor = new int[4];

    /**
     * 描边渐变色
     */
    private int[] strokeGradientColor = new int[4];

    /**
     * 动画持续时间
     */
    private long duration;

    /**
     * 动画状态
     */
    private int status;
    public static final int STATUS_FROM = 0x00; // 动画状态-From
    public static final int STATUS_TO = 0x01; // 动画状态-To

    /**
     * 文字渐变
     */
    private boolean isTextGradientEnable;

    /**
     * 背景渐变
     */
    private boolean isBackgroundGradientEnable;

    /**
     * 描边渐变
     */
    private boolean isStrokeGradientEnable;

    /**
     * 圆角
     */
    private int radius;

    /**
     * 描边宽度
     */
    private int strokeWidth;

    /**
     * 颜色对应位置
     */
    public static float[] POSITIONS = new float[]{0.0f, 0.25f, 0.75f, 1.0f};

    /**
     * 线性渐变色-文字
     */
    private LinearGradient textLinearGradient;

    /**
     * 描边画笔
     */
    private Paint strokePaint = new Paint(Paint.ANTI_ALIAS_FLAG);

    /**
     * 描边路径
     */
    private Path strokePath = new Path();

    /**
     * 背景渐变色
     */
    private GradientDrawable backgroundGradientDrawable = new GradientDrawable();

    /**
     * 当前背景渐变色
     */
    private int[] currentBackgroundColors = new int[2];

    /**
     * 线性渐变色-边框渐变色
     */
    private LinearGradient strokeLinearGradient;

    /**
     * 变换矩阵
     */
    private final Matrix matrix = new Matrix();

    /**
     * 着色器偏移量
     */
    private float shaderOffset = 0f;

    /**
     * 偏移量取值器
     */
    private ValueAnimator offsetAnimator;

    /**
     * Animation回调
     */
    @Nullable
    private OnAnimationListener onAnimationListener;

    /**
     * 标志位-动画是否可撤销
     */
    private boolean canReverse = false;

    private int defaultTextColor = Color.WHITE;

    public GradientTextView(@NonNull Context context) {
        super(context);
        init();
    }

    public GradientTextView(@NonNull Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init();
        TypedArray typedArray = context.obtainStyledAttributes(attrs, R.styleable.GradientTextView);
        gradientOrientation = typedArray.getInt(R.styleable.GradientTextView_gradientOrientation, ORIENTATION_LEFT_TO_RIGHT);
        duration = typedArray.getInt(R.styleable.GradientTextView_animationDuration, 2000);
        status = typedArray.getInt(R.styleable.GradientTextView_status, STATUS_FROM);

        textGradientColors[0] = typedArray.getColor(R.styleable.GradientTextView_textStartColorFrom, Color.BLACK);
        textGradientColors[1] = typedArray.getColor(R.styleable.GradientTextView_textEndColorFrom, Color.BLACK);
        textGradientColors[2] = typedArray.getColor(R.styleable.GradientTextView_textStartColorTo, Color.BLACK);
        textGradientColors[3] = typedArray.getColor(R.styleable.GradientTextView_textEndColorTo, Color.BLACK);
        isTextGradientEnable = typedArray.getBoolean(R.styleable.GradientTextView_textGradientEnable, false);

        backgroundGradientColor[0] = typedArray.getColor(R.styleable.GradientTextView_textStartColorFrom, Color.BLACK);
        backgroundGradientColor[1] = typedArray.getColor(R.styleable.GradientTextView_textEndColorFrom, Color.BLACK);
        backgroundGradientColor[2] = typedArray.getColor(R.styleable.GradientTextView_textStartColorTo, Color.BLACK);
        backgroundGradientColor[3] = typedArray.getColor(R.styleable.GradientTextView_textEndColorTo, Color.BLACK);
        isBackgroundGradientEnable = typedArray.getBoolean(R.styleable.GradientTextView_backgroundGradientEnable, false);

        strokeGradientColor[0] = typedArray.getColor(R.styleable.GradientTextView_textStartColorFrom, Color.BLACK);
        strokeGradientColor[1] = typedArray.getColor(R.styleable.GradientTextView_textEndColorFrom, Color.BLACK);
        strokeGradientColor[2] = typedArray.getColor(R.styleable.GradientTextView_textStartColorTo, Color.BLACK);
        strokeGradientColor[3] = typedArray.getColor(R.styleable.GradientTextView_textEndColorTo, Color.BLACK);
        isStrokeGradientEnable = typedArray.getBoolean(R.styleable.GradientTextView_strokeGradientEnable, false);
        radius = typedArray.getDimensionPixelSize(R.styleable.GradientTextView_radius, 0);
        typedArray.recycle();
    }

    /**
     * 初始化
     */
    private void init() {
        initAnimator();
    }

    /**
     * 初始化ValueAnimator
     */
    private void initAnimator() {
        offsetAnimator = ValueAnimator.ofFloat(0, 2);
        offsetAnimator.setDuration(duration);
        offsetAnimator.setInterpolator(new LinearInterpolator());
        offsetAnimator.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {
            @Override
            public void onAnimationUpdate(ValueAnimator animation) {
                if (isTextGradientEnable || isStrokeGradientEnable) {
                    shaderOffset = (float) animation.getAnimatedValue() * (isOrientationHorizontal() ? getWidth() : getHeight());
                    matrix.setTranslate(isOrientationHorizontal() ? -shaderOffset : 0,
                            isOrientationHorizontal() ? 0 : -shaderOffset);
                }

                if (isTextGradientEnable) {
                    textLinearGradient.setLocalMatrix(matrix);
                }

                if (isStrokeGradientEnable) {
                    strokeLinearGradient.setLocalMatrix(matrix);
                }

                if (isBackgroundGradientEnable) {
                    float animatedFraction = animation.getAnimatedFraction();
                    currentBackgroundColors[0] = getGradientColor(animatedFraction, backgroundGradientColor[0], backgroundGradientColor[2]);
                    currentBackgroundColors[1] = getGradientColor(animatedFraction, backgroundGradientColor[1], backgroundGradientColor[3]);
                    backgroundGradientDrawable.setColors(currentBackgroundColors);
                }

                postDelayed(() -> {
                    if (isBackgroundGradientEnable) {
                        setBackground(backgroundGradientDrawable);
                    }
                    invalidate();
                }, 100);
            }
        });

        offsetAnimator.addListener(new AnimatorListenerAdapter() {
            @Override
            public void onAnimationStart(Animator animation, boolean isReverse) {
                if (onAnimationListener != null) {
                    onAnimationListener.onAnimationStart(animation, isReverse);
                }
            }

            @Override
            public void onAnimationEnd(Animator animation, boolean isReverse) {
                if (onAnimationListener != null) {
                    onAnimationListener.onAnimationEnd(animation, isReverse);
                }
            }
        });

    }

    @Override
    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        super.onSizeChanged(w, h, oldw, oldh);

        shaderOffset = (offsetAnimator.getAnimatedValue() == null ? 0 : (float) offsetAnimator.getAnimatedValue()) * getWidth();
        matrix.setTranslate(isOrientationHorizontal() ? -shaderOffset : 0, isOrientationHorizontal() ? 0 : -shaderOffset);

        textLinearGradient = new LinearGradient(0, 0, isOrientationHorizontal() ? 3 * w : 0, isOrientationHorizontal() ? 0 : 3 * h, textGradientColors, POSITIONS, Shader.TileMode.CLAMP);
        textLinearGradient.setLocalMatrix(matrix);

        strokeLinearGradient = new LinearGradient(0, 0, 3 * w, 0, strokeGradientColor, POSITIONS, Shader.TileMode.CLAMP);
        strokeLinearGradient.setLocalMatrix(matrix);

        setAlpha(1.0f);
//        if (isTextGradientEnable) {
//            setTextColor(Color.WHITE);
//        }
        getPaint().setShader(isTextGradientEnable ? textLinearGradient : null);

        backgroundGradientDrawable.mutate();
        backgroundGradientDrawable.setSize(w / 2, h);
        backgroundGradientDrawable.setOrientation(GradientDrawable.Orientation.LEFT_RIGHT);
        backgroundGradientDrawable.setGradientType(GradientDrawable.LINEAR_GRADIENT);
        backgroundGradientDrawable.setShape(GradientDrawable.RECTANGLE);
        backgroundGradientDrawable.setCornerRadius(radius);

//        setBackgroundGradientEnable(isBackgroundGradientEnable);
        if (isBackgroundGradientEnable) {
            setBackground(backgroundGradientDrawable);
        }

        int offset = (strokeWidth + 1) >> 1;
        strokePaint.setShader(strokeLinearGradient);
        strokePath.reset();
        strokePath.addRoundRect(new RectF(offset, offset, w - offset, h - offset), radius, radius, Path.Direction.CW);

        if (status == STATUS_TO) {
            executeAnimation();
        }
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        if (isStrokeGradientEnable) {
            canvas.drawPath(strokePath, strokePaint);
        }
    }

    public void setOnAnimationListener(@Nullable OnAnimationListener onAnimationListener) {
        this.onAnimationListener = onAnimationListener;
    }

    public void setTextGradientEnable(boolean textGradientEnable) {
        isTextGradientEnable = textGradientEnable;
        getPaint().setShader(isTextGradientEnable ? textLinearGradient : null);
        invalidate();
    }

    public void setBackgroundGradientEnable(boolean backgroundGradientEnable) {
        isBackgroundGradientEnable = backgroundGradientEnable;
        setBackground(isBackgroundGradientEnable ? backgroundGradientDrawable : null);
    }

    public void setStrokeGradientEnable(boolean strokeGradientEnable) {
        isStrokeGradientEnable = strokeGradientEnable;
    }

    public void startAnimation() {
        if (!offsetAnimator.isRunning() && !canReverse) {
            offsetAnimator.start();
            canReverse = true;
        }
    }

    public void reverseAnimation() {
        if (!offsetAnimator.isRunning() && canReverse) {
            offsetAnimator.reverse();
            canReverse = false;
        }
    }

    public void executeAnimation() {
        if (offsetAnimator.isRunning()) {
            offsetAnimator.start();
            offsetAnimator.end();
            canReverse = true;
        }
    }

    @Override
    public void setTextColor(int color) {
        if (defaultTextColor != color) {
            defaultTextColor = color;
        }
        super.setTextColor(color);
    }

    @Override
    public void setTextColor(ColorStateList colors) {
        super.setTextColor(colors);
    }

    private boolean isOrientationHorizontal() {
        return gradientOrientation == ORIENTATION_LEFT_TO_RIGHT;
    }

    private boolean isOrientationVertical() {
        return !isOrientationHorizontal();
    }

    private int getGradientColor(@FloatRange(from = 0f, to = 1.0f) float fraction, @ColorInt int startColor, @ColorInt int endColor) {
        // 按ARGB通道拆分
        int startA = (startColor >> 24) & 0xFF;
        int startR = (startColor >> 16) & 0xFF;
        int startG = (startColor >> 8) & 0xFF;
        int startB = startColor & 0xFF;

        int endA = (endColor >> 24) & 0xFF;
        int endR = (endColor >> 16) & 0xFF;
        int endG = (endColor >> 8) & 0xFF;
        int endB = endColor & 0xFF;

        int targetA = (int) (startA + (endA - startA) * fraction);
        int targetR = (int) (startR + (endR - startR) * fraction);
        int targetG = (int) (startG + (endG - startG) * fraction);
        int targetB = (int) (startB + (endB - startB) * fraction);

        return targetA << 24 | targetR << 16 | targetG << 8 | targetB;
    }
}
```

***`OnAnimationListener.java`***

```java
public interface OnAnimationListener {
    void onAnimationStart(Animator animation, boolean isReverse);

    void onAnimationEnd(Animator animation,boolean isReverse);
}
```

>  
