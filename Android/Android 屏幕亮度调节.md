# Android系统屏幕亮度调节

---

## 1. 获取、设置`Android`系统屏幕亮度

### 获取系统屏幕亮度值

   `Android`提供了获取和设置系统亮度值的接口方便调用。
   ***获取亮度值***

   ```java
   public static int getBrightness() {
       try {
           return Settings.System.getInt(Utils.getApp().getContentResolver(),
                                         Settings.System.SCREEN_BRIGHTNESS);
       } catch (Settings.SettingNotFoundException e) {
           e.printStackTrace();
       }
       return 0;
   }
   ```

在原生`Android`系统中，获取的亮度值是`[0,255]`范围内的整型数值。

>  但是值得一提的是，部分手机厂商（尤其是国内手机厂商）会修改这个范围；另外，最小值也未必是`0`。

因此，考虑一般的情境下，获取应该是亮度百分比，`[0, 255]`范围边界值就不怎么值得参考了。这时候要考虑获取屏幕最大亮度和最小亮度值。

   ***获取亮度最大值、最小值***

   ```java
   // 代码写得太好以至于不好好写注释
   public static int getMaxBrightness() {
       int brightnessSettingMaximumId = Utils.getApp().getResources().getIdentifier("config_screenBrightnessSettingMaximum", "integer", "android");
       return Utils.getApp().getResources().getInteger(brightnessSettingMaximumId);
   }
   
   // 代码写得太好以至于不好好写注释
   public static int getMinBrightness() {
       int brightnessSettingMinimumId = Utils.getApp().getResources().getIdentifier("config_screenBrightnessSettingMinimum", "integer", "android");
       return Utils.getApp().getResources().getInteger(brightnessSettingMinimumId);
   }
   ```

使用上述的两种方式就可以获取到大多数手机真实的屏幕亮度最大值了。

之所以这样说是因为在部分厂商的部分机型上(`One Plus`)，通过`getMaxBrightness`获取到的最大值是`255`，但是通过`getBrighness`方法能够得到实际最大值是`1023`。所以上述的两个方法在特殊情况下是不可靠的。这里有一个弥补措施：

***特殊机型获取屏幕最大亮度***

   ```java
   /**
    * 需要使用反射获取屏幕亮度最大值的机型
    */
   private static Set<String> SHOULD_USE_REFLECT = new HashSet<String>() {{
       add("OnePlus");
   }};
   
   /**
    * 特殊机型的适配
    */
   public static int getMaxBrightnessReflect() {
       PowerManager powerManager = (PowerManager) Utils.getApp().getSystemService(Context.POWER_SERVICE);
       if (powerManager != null) {
           Field[] fields = powerManager.getClass().getDeclaredFields();
           for (Field field : fields) {
               if (field.getName().equals("BRIGHTNESS_ON")) {
                   field.setAccessible(true);
                   try {
                       return (int) field.get(powerManager);
                   } catch (IllegalAccessException e) {
                       return 0;
                   }
               }
           }
       }
       return 0;
   }
   ```

***优化`getMaxBrightness()`***

```java
/**
 * 获取设备屏幕亮度最大值
 * 部分机型获取不到真实的亮度最大值，需要用反射的方式读取(getMaxBrightnessReflect)
 */
public static int getMaxBrightness() {
    int brightnessSettingMaximumId = Utils.getApp().getResources().getIdentifier("config_screenBrightnessSettingMaximum", "integer", "android");
    int maxBrightness = Utils.getApp().getResources().getInteger(brightnessSettingMaximumId);
    return shouldUseReflect() ? Math.max(maxBrightness, getMaxBrightnessReflect()) : maxBrightness;
}

/**
 * 是否应该使用反射方式读取屏幕亮度最大值
 */
private static boolean shouldUseReflect() {
    return SHOULD_USE_REFLECT.contains(getDeviceBrand());
}
```



###    设置系统屏幕亮度值

在设置系统屏幕亮度之前需要了解：

- 设置屏幕亮度需要申请`WRITE_SETTING`权限。高版本需要动态申请
- `Android 2.1`引入了屏幕亮度自动调节的机制，如果要设置屏幕亮度，最好将屏幕亮度调节模式设置为手动调节。当然也需要申请`WRITE_SETTING`权限

  首先需要在`AndroidManifest.xml`文件中声明权限

   ***`AndroidManifest.xml`***

   ```java
   <uses-permission android:name="android.permission.WRITE_SETTINGS"
       tools:ignore="ProtectedPermissions" />
   ```

在代码中去动态申请权限：

> 搬轮子预警！
>
> 动态申请权限这里使用的是`BlankJ`工具类框架中的实现方法。

   ***设置屏幕亮度、屏幕亮度调节模式***

   ```java
   public static void setBrightness(int brightnessPercent) {
       // 对哦，这个API只能在M及以上的版本使用
       if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
           if (!PermissionUtils.isGrantedWriteSettings()) {
               PermissionUtils.requestWriteSettings(new PermissionUtils.SimpleCallback() {
                   @Override
                   public void onGranted() {
                       setBrightnessManualMode();
                       Settings.System.putInt(Utils.getApp().getContentResolver(), 
                                              Settings.System.SCREEN_BRIGHTNESS,
                                              brightness);
                   }
   
                   @Override
                   public void onDenied() {
   
                   }
               });
           } else { 
               setBrightnessManualMode();
               Settings.System.putInt(Utils.getApp().getContentResolver(), 
                                      Settings.System.SCREEN_BRIGHTNESS,
                                      brightness);
           }
       }
   }
   
   /**
    * 设置屏幕亮度调节模式为手动调节
    */
   private static void setBrightnessManualMode() {
       try {
           int mode = Settings.System.getInt(Utils.getApp().getContentResolver(), Settings.System.SCREEN_BRIGHTNESS_MODE);
           // 如果当前亮度模式是自动调节模式
           if (mode == Settings.System.SCREEN_BRIGHTNESS_MODE_AUTOMATIC) {
               if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                   if (!PermissionUtils.isGrantedWriteSettings()) {
                       PermissionUtils.requestWriteSettings(new PermissionUtils.SimpleCallback() {
                           @Override
                           public void onGranted() {
                               Settings.System.putInt(Utils.getApp().getContentResolver(),
                                                      Settings.System.SCREEN_BRIGHTNESS_MODE,
                                                      Settings.System.SCREEN_BRIGHTNESS_MODE_MANUAL);
                           }
   
                           @Override
                           public void onDenied() {
   
                           }
                       });
                   } else {
                       Settings.System.putInt(Utils.getApp().getContentResolver(),
                                              Settings.System.SCREEN_BRIGHTNESS_MODE,
                                              Settings.System.SCREEN_BRIGHTNESS_MODE_MANUAL);
                   }
               }
           }
       } catch (Settings.SettingNotFoundException e) {
           e.printStackTrace();
       }
   }
   ```

***设置屏幕亮度调节模式为手动调节***

   ```java
   /**
    * 设置屏幕亮度调节模式为手动调节
    */
   private static void setScreenManualMode() {
       try {
           int mode = Settings.System.getInt(appContext.getContentResolver(), Settings.System.SCREEN_BRIGHTNESS_MODE);
           if (mode == Settings.System.SCREEN_BRIGHTNESS_MODE_AUTOMATIC) {
               if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                   if (!PermissionUtils.isGrantedWriteSettings()) {
                       PermissionUtils.requestWriteSettings(new PermissionUtils.SimpleCallback() {
                           @Override
                           public void onGranted() {
                               Settings.System.putInt(appContext.getContentResolver(),
                                                      Settings.System.SCREEN_BRIGHTNESS_MODE,
                                                      Settings.System.SCREEN_BRIGHTNESS_MODE_MANUAL);
                           }
   
                           @Override
                           public void onDenied() {
   
                           }
                       });
                   } else {
                       Settings.System.putInt(appContext.getContentResolver(),
                                              Settings.System.SCREEN_BRIGHTNESS_MODE,
                                              Settings.System.SCREEN_BRIGHTNESS_MODE_MANUAL);
                   }
               }
           }
       } catch (Settings.SettingNotFoundException e) {
           e.printStackTrace();
       }
   }
   ```

> `注：`在前面有提到一般场景下，我们或许需要获取和设置的是亮度值的比值。至此我们好像已经获取到了计算亮度比值所需的必要数值。只需要做一道小学计算题就能求解了，这里列出`核心算法`：
>
> - 获取屏幕亮度比值：
>
>   `float brightnessPer = (float) getBrightness / (getMaxBrightness() - getMinBrightness())`
>
> - 设置屏幕亮度：
>
>   `brightness = (int) (getMinBrightness + beightnessPer * (getMaxBrightness() - getMinBrightness()))`
>
> if ( `Android P-`版本 ) 
>
> ​		完结撒花！！！
>
> else
>
> ​		GOTO: `Android P`的变化

## 2. `Android P`的变化

不卖关子的说，人眼感知亮度是基于`对数`而不是`线性`感知亮度的。为了匹配这种感知差异，`Android P+`版本调整了亮度线性变化的逻辑，更新了通知栏和系统设置应用程序中的亮度滑块`UI`，

   > `https://www.stkent.com/2018/11/12/more-on-android-pies-brightness-control-changes.html`

但是人眼对于亮度的感知并不是严格的`对数`，所以最终的拟合曲线是由`对数曲线`和`伽马曲线`拼接起来的，称为`Hybrid Log-Gamma(HLG)`。

`Android 9+`的`BrightnessUtils`类中提供了亮度滑块值和亮度值的非线性映射关系。

> `亮度值 Brightness`： 屏幕亮度实际值，一般范围是`[0, 255]`，认为是线性变化的。
>
> `亮度调节滑块值 sliderVal`：这个值被映射到了`Gamma`值。范围是`[GAMMA_SPACE_MIN, GAMMA_SPACE_MAX]`

   

## 3. `Android`屏幕亮度调节适配

### 1. `Android`版本适配

   所幸呢，这个非线性的关系在`Android Open Source Project`中是可以找到的，以`API 30`中的`BrightnessUtils`为例来看。代码不长，但是注释很重要。

   ***`om.android.settingslib.display.BrightnessUtils  API 30`***

   ```java
public class BrightnessUtils {

    public static final int GAMMA_SPACE_MIN = 0;
    public static final int GAMMA_SPACE_MAX = 65535;

    // Hybrid Log Gamma constant values
    private static final float R = 0.5f;
    private static final float A = 0.17883277f;
    private static final float B = 0.28466892f;
    private static final float C = 0.55991073f;

    /**
     * A function for converting from the gamma space that the slider works in to the
     * linear space that the setting works in.
     *
     * The gamma space effectively provides us a way to make linear changes to the slider that
     * result in linear changes in perception. If we made changes to the slider in the linear space
     * then we'd see an approximately logarithmic change in perception (c.f. Fechner's Law).
     *
     * Internally, this implements the Hybrid Log Gamma electro-optical transfer function, which is
     * a slight improvement to the typical gamma transfer function for displays whose max
     * brightness exceeds the 120 nit reference point, but doesn't set a specific reference
     * brightness like the PQ function does.
     *
     * Note that this transfer function is only valid if the display's backlight value is a linear
     * control. If it's calibrated to be something non-linear, then a different transfer function
     * should be used.
     *
     * @param val The slider value.
     * @param min The minimum acceptable value for the setting.
     * @param max The maximum acceptable value for the setting.
     * @return The corresponding setting value.
     */
    public static final int convertGammaToLinear(int val, int min, int max) {
        final float normalizedVal = MathUtils.norm(GAMMA_SPACE_MIN, GAMMA_SPACE_MAX, val);
        final float ret;
        if (normalizedVal <= R) {
            ret = MathUtils.sq(normalizedVal / R);
        } else {
            ret = MathUtils.exp((normalizedVal - C) / A) + B;
        }

        // HLG is normalized to the range [0, 12], so we need to re-normalize to the range [0, 1]
        // in order to derive the correct setting value.
        return Math.round(MathUtils.lerp(min, max, ret / 12));
    }

    /**
     * Version of {@link #convertGammaToLinear} that takes and returns float values.
     * TODO(flc): refactor Android Auto to use float version
     *
     * @param val The slider value.
     * @param min The minimum acceptable value for the setting.
     * @param max The maximum acceptable value for the setting.
     * @return The corresponding setting value.
     */
    public static final float convertGammaToLinearFloat(int val, float min, float max) {
        final float normalizedVal = MathUtils.norm(GAMMA_SPACE_MIN, GAMMA_SPACE_MAX, val);
        final float ret;
        if (normalizedVal <= R) {
            ret = MathUtils.sq(normalizedVal / R);
        } else {
            ret = MathUtils.exp((normalizedVal - C) / A) + B;
        }

        // HLG is normalized to the range [0, 12], ensure that value is within that range,
        // it shouldn't be out of bounds.
        final float normalizedRet = MathUtils.constrain(ret, 0, 12);

        // Re-normalize to the range [0, 1]
        // in order to derive the correct setting value.
        return MathUtils.lerp(min, max, normalizedRet / 12);
    }

    /**
     * A function for converting from the linear space that the setting works in to the
     * gamma space that the slider works in.
     *
     * The gamma space effectively provides us a way to make linear changes to the slider that
     * result in linear changes in perception. If we made changes to the slider in the linear space
     * then we'd see an approximately logarithmic change in perception (c.f. Fechner's Law).
     *
     * Internally, this implements the Hybrid Log Gamma opto-electronic transfer function, which is
     * a slight improvement to the typical gamma transfer function for displays whose max
     * brightness exceeds the 120 nit reference point, but doesn't set a specific reference
     * brightness like the PQ function does.
     *
     * Note that this transfer function is only valid if the display's backlight value is a linear
     * control. If it's calibrated to be something non-linear, then a different transfer function
     * should be used.
     *
     * @param val The brightness setting value.
     * @param min The minimum acceptable value for the setting.
     * @param max The maximum acceptable value for the setting.
     * @return The corresponding slider value
     */
    public static final int convertLinearToGamma(int val, int min, int max) {
        return convertLinearToGammaFloat((float) val, (float) min, (float) max);
    }

    /**
     * Version of {@link #convertLinearToGamma} that takes float values.
     * TODO: brightnessfloat merge with above method(?)
     * @param val The brightness setting value.
     * @param min The minimum acceptable value for the setting.
     * @param max The maximum acceptable value for the setting.
     * @return The corresponding slider value
     */
    public static final int convertLinearToGammaFloat(float val, float min, float max) {
        // For some reason, HLG normalizes to the range [0, 12] rather than [0, 1]
        final float normalizedVal = MathUtils.norm(min, max, val) * 12;
        final float ret;
        if (normalizedVal <= 1f) {
            ret = MathUtils.sqrt(normalizedVal) * R;
        } else {
            ret = A * MathUtils.log(normalizedVal - B) + C;
        }

        return Math.round(MathUtils.lerp(GAMMA_SPACE_MIN, GAMMA_SPACE_MAX, ret));
    }
}
   ```

   > 这个类中主要包含了线性值与`GAMMA`值之间的转换算法，以及算法的参数。虽然这个类不能直接使用。不过，可以照葫芦画瓢式的实现一下。
   >
   > 在实现之前简单介绍一下两种转换方式的入参和返回值
   >
   > - `convertGammaToLinear`
   >  - 参数列表：
   >     - `val:int`系统亮度调节拖动条的值
   >     - `min:int` 系统亮度调节拖动条最小值
   >     - `max:int` 系统亮度调节拖动条最大值
   >   - 返回值:
   >     - 目标亮度值
   > - `convertLinearToGamma`
   >   - 参数列表：
   >     - `val:int` 系统屏幕亮度值
   >     - `min:int` 系统屏幕亮度最小值
   >     - `max:int` 系统屏幕亮度最大值
   >   - 返回值
   >     - 系统亮度调节拖动条的值
   > 
   > 写在前面：一般来讲，设置亮度的入参是亮度拖动条的期望值，也就是说，我希望设置亮度为`50%`，但是这个`50%`需要直观表现在的是拖动条上的拖动锚处在中间位置，而非是亮度值折半。那么需要用到的就是`convertGammaToLinear`的算法计算出需要设置的目标亮度值。
   >
   > 获取亮度的入参是系统屏幕亮度，也就是根据当前的屏幕亮度计算出系统亮度拖动条的值（这个值可以以小数或百分比的形式呈现，这也是我们需要得到的数值）

   那么按照上述的算法逻辑，可以封装一个`HLGHelper`类。之所以自己封装，主要是因为`AOSP`中的`BrightnessUtils`类不太好拿来直接用哎，反射也表示它很抱歉；另外就是即便是能有方法调用，方法的传参其实并不合我心意。那么既然给出了算法逻辑，照葫芦画瓢尔。

   ***`HLGHleper`***

   ```java
public class HLGHelper {
	// Hybrid Log Gamma constant values。算法需要使用到的常量参数
    private static final float R = 0.5f;
    private static final float A = 0.17883277f;
    private static final float B = 0.28466892f;
    private static final float C = 0.55991073f;
    
    /**
     * 传入待设置的屏幕亮度期望值(即屏幕亮度拖动条位置)
     * 获取需要设置屏幕亮度的实际值比值
     *
     * @param sliderPer [0, 1] 屏幕亮度期望值(屏幕亮度拖动条的位置)
     * @return [0, 1] 屏幕亮度的实际值
     */
    public static float convertGammaToLinear(
            @FloatRange(from = 0f, to = 1f) float sliderPer) {
        final float ret;
        if (sliderPer <= R) {
            ret = (sliderPer / R) * (sliderPer / R);
        } else {
            ret = (float) Math.exp(((sliderPer - C) / A) + B);
        }
        double finalRet = Math.min(12, Math.max(0, ret));
        return (float) (finalRet / 12);
    }
    
     /**
     * 计算屏幕亮度比值
     * 获取当前屏幕亮度下拖动条位置
     *
     * @param brightnessPer [0, 1]实际亮度比值
     * @return [0, 1] 亮度条比值
     */
    public static float convertLinearToGamma(
            @FloatRange(from = 0f, to = 1f) float brightnessPer) {
        final float normalizedVal = brightnessPer * 12;
        final float ret;
        if (normalizedVal <= 1f) {
            ret = (float) (Math.sqrt(normalizedVal) * R);
        } else {
            ret = (float) (A * Math.log(normalizedVal - B) + C);
        }
        return ret;
    }
}
   ```

   > 不过这是针对`Android P+`的变化，这里我们可以提供一个方法来判定`Android`版本。

   ***`HLGHelper.useHLG()`***

   ```java
/**
 * 是否使用HLG
 * 因为HLG是从Andorid P开始加入的，那么这里用使用版本号做版本划分
 */
public static boolean useHLG() {
    return Build.VERSION.SDK_INT >= Build.VERSION_CODES.P;
}
   ```

   现在对`Brightness`的操作封装为`BrightnessUtils`类；

   那么现在我们获取一下屏幕亮度滑块位置的百分比：

   ***`BrightnessUtils.getBrightnessSliderPercent`***

   ```java
/**
 * 获取屏幕亮度调节值的百分比
 *
 * @return 屏幕亮度拖动条值的百分比
 */
@FloatRange(from = 0f, to = 1f)
public static float getBrightnessSliderPercent() {
    final float brightnessPercent = getBrightnessPercent();

    final float sliderPercent;

    if (HLGHelper.useHLG()) {
        sliderPercent = HLGHelper.convertLinearToGamma(brightnessPercent);
    } else {
        sliderPercent = brightnessPercent;
    }
    return sliderPercent;
}
   ```

   > 这个方法做的事情就是：获取当前屏幕亮度的百分比，如果使用了`HLG`则计算出在`HLG`曲线上的非线性映射位置，获取到屏幕亮度滑块位置的百分比；如果没有使用`HLG`则当前屏幕亮度百分比即屏幕亮度滑块位置。

   ***`BrightnessUtils.setBrightnessPer`***

   ```java
/**
 * 设置屏幕亮度百分比
 *
 * @param targetSliderPer 屏幕亮度滑块位置的期望值
 */
public static void setBrightnessPer(@FloatRange(from = 0f, to = 1f) float targetSliderPer) {
    final float brightnessPer;
    if (HLGHelper.useHLG()) {
        brightnessPer = HLGHelper.convertGammaToLinear(targetSliderPer);
    } else {
        brightnessPer = targetSliderPer;
    }
    int maxBrightness = getMaxBrightness();
    int minBrightness = getMinBrightness();
    final int brightness = (int) (minBrightness + (maxBrightness - minBrightness) * brightnessPer);
    setBrightness(brightness);
}
   ```

   至此，我们就做好了`Andorid P+`有关屏幕亮度和屏幕亮度滑块非线性映射的版本适配。

   到此为止了么？其实并不。

   `emmmm`如果打印输入值和输出值，你会发现，期望结果和最终计算出的结果是有一些差异的。或许并不是因为计算的精度问题，而是在`AOSP`中给出的`Hybrid Log-Gamma`映射的算法参数的问题。值得一提的是，部分手机厂商会对算法参数做优化，采用的

### 2. `HLG`参数适配

值得一提的是，部分手机厂商会对算法参数做优化，比如小米谁谁。所幸！同一套参数在各厂商的手机上表现是类似的。但是使用`Android`原生系统的话，使用的还是原来的一套参数。

这里分享一下优化后的参数列表：

```java
// 适用于Android P+ 部分手机厂商优化的HLG参数
private static final float R1 = 0.2f;
private static final float A1 = 0.314f;
private static final float B1 = 0.06f;
private static final float C1 = 0.221f;
```

> 不过这套参数仅仅在部分厂商的部分`Android P+`机型上验证过，`SO...`

在这里，粗略地根据手机品牌名称来划分使用哪一套参数：

获取手机品牌：

```java
/**
 * 获取手机品牌名称
 */
public static String getBrand(){
    return Build.BRAND;
}
```

我这里将参数封装了一下，当然也可以不必。使用`Set`记录使用优化后参数的`黑名单`

***`HLGHelper$HLGParams`***

```java
public class HLGHelper {
	// Hybrid Log Gamma constant values. 适用于Android P+ 原生系统的HLG参数
    private static final float R0 = 0.5f;
    private static final float A0 = 0.17883277f;
    private static final float B0 = 0.28466892f;
    private static final float C0 = 0.55991073f;

    // 适用于Android P+ 部分手机厂商优化的HLG参数
    private static final float R1 = 0.2f;
    private static final float A1 = 0.314f;
    private static final float B1 = 0.06f;
    private static final float C1 = 0.221f;

    /**
     * 封装HLG参数
     */
    private static class HLGParams {
        float R;
        float A;
        float B;
        float C;
    }
    
	private static HLGParams params;
    
    /**
     * 使用HLG优化参数的手机品牌
     */
    private static Set<String> BRAND_USE_OPTIMIZE_HLG = new HashSet<String>() {{
        add("xiaomi");
        add("Lenovo");
        add("HUAWEI");
        add("OnePlus");
    }};

    /**
     * 延迟实例化`HLGParams`参数
     */
    private static void loadParams() {
        if (BRAND_USE_OPTIMIZE_HLG.contains(getBrand())) {
            params = new HLGParams() {{
                R = R1;
                A = A1;
                B = B1;
                C = C1;
            }};
        } else {
            params = new HLGParams() {{
                R = R0;
                A = A0;
                B = B0;
                C = C0;
            }};
        }
    }
}
```

## 4. 总结

刚开始接手这个需求时候，觉得还是蛮轻松，毕竟直接用官方的`轮子`真心省力。对于权限申请、屏幕亮度百分比的计算、`Android P+`的变化等等也是一路走来遇到并不断填补的坑坑。在这个过程中确实学习到很多。感触最深的就是自己的所陷入的思维误区——理所当然认为亮度条和屏幕亮度就是线性对应的关系。以此来提醒自己在接触新事物的时候尽量保持无知的状态，多问问题并不断求索，禁止犯懒。完结撒盐。

## 5.附录

***`build.gradle`***

```groovy
dependencies {
    // BlankJ
    implementation 'com.blankj:utilcode:1.30.6'
}
```

***`BrightnessDemoApplication`***

```java
public class BrightnessDemoApplication extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        // AndroidManifest中指定Application
        Utils.init(this);
    }
}
```

***`AndroidManifest.xml`***

```xml
<application
	android:name=".BrightnessDemoApplication"
    android:allowBackup="true"
    android:icon="@mipmap/ic_launcher"
    android:label="@string/app_name"
    android:roundIcon="@mipmap/ic_launcher_round"
    android:supportsRtl="true"
    android:theme="@style/Theme.BrightnessDemo">
    <activity android:name=".MainActivity">
        <intent-filter>
            <action android:name="android.intent.action.MAIN" />

            <category android:name="android.intent.category.LAUNCHER" />
        </intent-filter>
    </activity>
</application>
```

### ***`BrightnessUtils`***

```java
public class BrightnessUtils {
    private static Set<String> SHOULD_USE_REFLECT = new HashSet<String>() {{
        add("OnePlus");
    }};

    /**
     * 获取屏幕亮度
     */
    public static int getBrightness() {
        try {
            return Settings.System.getInt(Utils.getApp().getContentResolver(),
                    Settings.System.SCREEN_BRIGHTNESS);
        } catch (Settings.SettingNotFoundException e) {
            e.printStackTrace();
        }
        return 0;
    }

    /**
     * 获取设备屏幕亮度最大值
     * 部分机型获取不到真实的亮度最大值，需要用反射的方式读取(getMaxBrightnessReflect)
     */
    public static int getMaxBrightness() {
        int brightnessSettingMaximumId = Utils.getApp().getResources().getIdentifier("config_screenBrightnessSettingMaximum", "integer", "android");
        int maxBrightness = Utils.getApp().getResources().getInteger(brightnessSettingMaximumId);
        return shouldUseReflect() ? Math.max(maxBrightness, getMaxBrightnessReflect()) : maxBrightness;
    }

    /**
     * 获取设备亮度最大值
     * 部分机型使用getMaxBrightness()得到的最大亮度值有可能不是实际最大亮度值
     * 比如OnePlus机型上的通过getMaxBrightness得到的最大值是255,但是实际亮度值是1023
     */
    public static int getMaxBrightnessReflect() {
        PowerManager powerManager = (PowerManager) Utils.getApp().getSystemService(Context.POWER_SERVICE);
        if (powerManager != null) {
            Field[] fields = powerManager.getClass().getDeclaredFields();
            for (Field field : fields) {
                if (field.getName().equals("BRIGHTNESS_ON")) {
                    field.setAccessible(true);
                    try {
                        return (int) field.get(powerManager);
                    } catch (IllegalAccessException e) {
                        return 0;
                    }
                }
            }
        }
        return 0;
    }

    /**
     * 获取设备屏幕亮度最大值
     */
    public static int getMinBrightness() {
        int brightnessSettingMinimumId = Utils.getApp().getResources().getIdentifier("config_screenBrightnessSettingMinimum", "integer", "android");
        return Utils.getApp().getResources().getInteger(brightnessSettingMinimumId);
    }

    /**
     * 设置屏幕亮度
     *
     * @param brightness 系统屏幕亮度
     */
    public static void setBrightness(int brightness) {
        // 对哦，这个API只能在M及以上的版本使用
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (!PermissionUtils.isGrantedWriteSettings()) {
                PermissionUtils.requestWriteSettings(new PermissionUtils.SimpleCallback() {
                    @Override
                    public void onGranted() {
                        setBrightnessManualMode();
                        Settings.System.putInt(Utils.getApp().getContentResolver(),
                                Settings.System.SCREEN_BRIGHTNESS,
                                brightness);
                    }

                    @Override
                    public void onDenied() {

                    }
                });
            } else {
                setBrightnessManualMode();
                Settings.System.putInt(Utils.getApp().getContentResolver(),
                        Settings.System.SCREEN_BRIGHTNESS,
                        brightness);
            }
        }
    }

    /**
     * 设置屏幕亮度调节模式为手动调节
     */
    private static void setBrightnessManualMode() {
        try {
            int mode = Settings.System.getInt(Utils.getApp().getContentResolver(), Settings.System.SCREEN_BRIGHTNESS_MODE);
            // 如果当前亮度模式是自动调节模式
            if (mode == Settings.System.SCREEN_BRIGHTNESS_MODE_AUTOMATIC) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    if (!PermissionUtils.isGrantedWriteSettings()) {
                        PermissionUtils.requestWriteSettings(new PermissionUtils.SimpleCallback() {
                            @Override
                            public void onGranted() {
                                Settings.System.putInt(Utils.getApp().getContentResolver(),
                                        Settings.System.SCREEN_BRIGHTNESS_MODE,
                                        Settings.System.SCREEN_BRIGHTNESS_MODE_MANUAL);
                            }

                            @Override
                            public void onDenied() {

                            }
                        });
                    } else {
                        Settings.System.putInt(Utils.getApp().getContentResolver(),
                                Settings.System.SCREEN_BRIGHTNESS_MODE,
                                Settings.System.SCREEN_BRIGHTNESS_MODE_MANUAL);
                    }
                }
            }
        } catch (Settings.SettingNotFoundException e) {
            e.printStackTrace();
        }
    }

    /**
     * 获取屏幕亮度比值
     *
     * @return 屏幕亮度比值
     */
    @FloatRange(from = 0, to = 1)
    public static float getBrightnessPercent() {
        int maxBrightness = getMaxBrightness();
        int minBrightness = getMinBrightness();
        int realScreenBrightness = getBrightness();
        float screenBrightnessPer = (float) (realScreenBrightness - minBrightness) / (maxBrightness - minBrightness);
        return Math.min(Math.max(screenBrightnessPer, 0), 1f);
    }

    /**
     * 获取屏幕亮度调节值的百分比
     *
     * @return 屏幕亮度拖动条值的百分比
     */
    @FloatRange(from = 0f, to = 1f)
    public static float getBrightnessSliderPercent() {
        final float brightnessPercent = getBrightnessPercent();

        final float sliderPercent;

        if (HLGHelper.useHLG()) {
            sliderPercent = HLGHelper.convertLinearToGamma(brightnessPercent);
        } else {
            sliderPercent = brightnessPercent;
        }
        // 返回值的粒度为10
        return (Math.round(sliderPercent * 10)) * 10;
    }

    /**
     * 设置屏幕亮度百分比
     *
     * @param targetSliderPer 拖动条位置[0,1]
     */
    public static void setBrightnessPer(@FloatRange(from = 0f, to = 1f) float targetSliderPer) {
        final float brightnessPer;
        if (HLGHelper.useHLG()) {
            brightnessPer = HLGHelper.convertGammaToLinear(targetSliderPer);
        } else {
            brightnessPer = targetSliderPer;
        }
        int maxBrightness = getMaxBrightness();
        int minBrightness = getMinBrightness();
        final int brightness = (int) (minBrightness + (maxBrightness - minBrightness) * brightnessPer);
        setBrightness(brightness);
    }

    /**
     * 是否应该使用反射方式读取屏幕亮度最大值
     */
    private static boolean shouldUseReflect() {
        return SHOULD_USE_REFLECT.contains(getDeviceBrand());
    }

    /**
     * 获取手机厂商名称
     */
    public static String getDeviceBrand() {
        return android.os.Build.BRAND;
    }
}
```

### ***`HLGHelper`***

```java
public class BrightnessUtils {
    private static Set<String> SHOULD_USE_REFLECT = new HashSet<String>() {{
        add("OnePlus");
    }};

    /**
     * 获取屏幕亮度
     */
    public static int getBrightness() {
        try {
            return Settings.System.getInt(Utils.getApp().getContentResolver(),
                    Settings.System.SCREEN_BRIGHTNESS);
        } catch (Settings.SettingNotFoundException e) {
            e.printStackTrace();
        }
        return 0;
    }

    /**
     * 获取设备屏幕亮度最大值
     * 部分机型获取不到真实的亮度最大值，需要用反射的方式读取(getMaxBrightnessReflect)
     */
    public static int getMaxBrightness() {
        int brightnessSettingMaximumId = Utils.getApp().getResources().getIdentifier("config_screenBrightnessSettingMaximum", "integer", "android");
        int maxBrightness = Utils.getApp().getResources().getInteger(brightnessSettingMaximumId);
        return shouldUseReflect() ? Math.max(maxBrightness, getMaxBrightnessReflect()) : maxBrightness;
    }

    /**
     * 获取设备亮度最大值
     * 部分机型使用getMaxBrightness()得到的最大亮度值有可能不是实际最大亮度值
     * 比如OnePlus机型上的通过getMaxBrightness得到的最大值是255,但是实际亮度值是1023
     */
    public static int getMaxBrightnessReflect() {
        PowerManager powerManager = (PowerManager) Utils.getApp().getSystemService(Context.POWER_SERVICE);
        if (powerManager != null) {
            Field[] fields = powerManager.getClass().getDeclaredFields();
            for (Field field : fields) {
                if (field.getName().equals("BRIGHTNESS_ON")) {
                    field.setAccessible(true);
                    try {
                        return (int) field.get(powerManager);
                    } catch (IllegalAccessException e) {
                        return 0;
                    }
                }
            }
        }
        return 0;
    }

    /**
     * 获取设备屏幕亮度最大值
     */
    public static int getMinBrightness() {
        int brightnessSettingMinimumId = Utils.getApp().getResources().getIdentifier("config_screenBrightnessSettingMinimum", "integer", "android");
        return Utils.getApp().getResources().getInteger(brightnessSettingMinimumId);
    }

    /**
     * 设置屏幕亮度
     *
     * @param brightness 系统屏幕亮度
     */
    public static void setBrightness(int brightness) {
        // 对哦，这个API只能在M及以上的版本使用
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (!PermissionUtils.isGrantedWriteSettings()) {
                PermissionUtils.requestWriteSettings(new PermissionUtils.SimpleCallback() {
                    @Override
                    public void onGranted() {
                        setBrightnessManualMode();
                        Settings.System.putInt(Utils.getApp().getContentResolver(),
                                Settings.System.SCREEN_BRIGHTNESS,
                                brightness);
                    }

                    @Override
                    public void onDenied() {

                    }
                });
            } else {
                setBrightnessManualMode();
                Settings.System.putInt(Utils.getApp().getContentResolver(),
                        Settings.System.SCREEN_BRIGHTNESS,
                        brightness);
            }
        }
    }

    /**
     * 设置屏幕亮度调节模式为手动调节
     */
    private static void setBrightnessManualMode() {
        try {
            int mode = Settings.System.getInt(Utils.getApp().getContentResolver(), Settings.System.SCREEN_BRIGHTNESS_MODE);
            // 如果当前亮度模式是自动调节模式
            if (mode == Settings.System.SCREEN_BRIGHTNESS_MODE_AUTOMATIC) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    if (!PermissionUtils.isGrantedWriteSettings()) {
                        PermissionUtils.requestWriteSettings(new PermissionUtils.SimpleCallback() {
                            @Override
                            public void onGranted() {
                                Settings.System.putInt(Utils.getApp().getContentResolver(),
                                        Settings.System.SCREEN_BRIGHTNESS_MODE,
                                        Settings.System.SCREEN_BRIGHTNESS_MODE_MANUAL);
                            }

                            @Override
                            public void onDenied() {

                            }
                        });
                    } else {
                        Settings.System.putInt(Utils.getApp().getContentResolver(),
                                Settings.System.SCREEN_BRIGHTNESS_MODE,
                                Settings.System.SCREEN_BRIGHTNESS_MODE_MANUAL);
                    }
                }
            }
        } catch (Settings.SettingNotFoundException e) {
            e.printStackTrace();
        }
    }

    /**
     * 获取屏幕亮度比值
     *
     * @return 屏幕亮度比值
     */
    @FloatRange(from = 0, to = 1)
    public static float getBrightnessPercent() {
        int maxBrightness = getMaxBrightness();
        int minBrightness = getMinBrightness();
        int realScreenBrightness = getBrightness();
        float screenBrightnessPer = (float) (realScreenBrightness - minBrightness) / (maxBrightness - minBrightness);
        return Math.min(Math.max(screenBrightnessPer, 0), 1f);
    }

    /**
     * 获取屏幕亮度调节值的百分比
     *
     * @return 屏幕亮度拖动条值的百分比
     */
    @FloatRange(from = 0f, to = 1f)
    public static float getBrightnessSliderPercent() {
        final float brightnessPercent = getBrightnessPercent();

        final float sliderPercent;

        if (HLGHelper.useHLG()) {
            sliderPercent = HLGHelper.convertLinearToGamma(brightnessPercent);
        } else {
            sliderPercent = brightnessPercent;
        }
        // 返回值的粒度为10
        return (Math.round(sliderPercent * 10)) * 10;
    }

    /**
     * 设置屏幕亮度百分比
     *
     * @param targetSliderPer 拖动条位置[0,1]
     */
    public static void setBrightnessPer(@FloatRange(from = 0f, to = 1f) float targetSliderPer) {
        final float brightnessPer;
        if (HLGHelper.useHLG()) {
            brightnessPer = HLGHelper.convertGammaToLinear(targetSliderPer);
        } else {
            brightnessPer = targetSliderPer;
        }
        int maxBrightness = getMaxBrightness();
        int minBrightness = getMinBrightness();
        final int brightness = (int) (minBrightness + (maxBrightness - minBrightness) * brightnessPer);
        setBrightness(brightness);
    }

    /**
     * 是否应该使用反射方式读取屏幕亮度最大值
     */
    private static boolean shouldUseReflect() {
        return SHOULD_USE_REFLECT.contains(getDeviceBrand());
    }

    /**
     * 获取手机厂商名称
     */
    public static String getDeviceBrand() {
        return android.os.Build.BRAND;
    }
}
```
