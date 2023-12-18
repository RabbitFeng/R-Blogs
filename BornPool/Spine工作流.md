Spine 

## Spine 工作流

[在Unity中导入Spine资产](http://zh.esotericsoftware.com/spine-unity#%E5%9C%A8Unity%E4%B8%AD%E5%AF%BC%E5%85%A5Spine-%E8%B5%84%E4%BA%A7)

[`Spine`常见导入问题解答](https://www.bilibili.com/video/BV1BD4y1Y7By/?vd_source=4b7c5084536409a397ad3a0b8670be11)

`Spine`提供了两种`texture`导出的基本工作流。两种工作流的`Texture`打包器导出和`Texture & Material`导入设置不同。

1. `Premultiplied alpha`默认设置，在`Gamma`色彩空间中进行`premultiplied`

   ![image-20230524111745708](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230524111745708.png)

2. `Straight alpha`

   ![image-20230524111928307](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230524111928307.png)

`Spine` `Texture`打包器默认设置使用`Premultiply alpha`，运行时的所有`Spine`着色器也都默认使用`Premultiply alpha`工作流。

某些情况下可能需要使用`straight alpha`工作流

- 使用了线性色彩空间，必须使用`straight alpha`

- 想要使用非`Spine`着色器时

  一般的着色器默认用于`straight alpha`的`texture`，这将导致图像附近周围出现错误的黑色边框

切换到`straight alpha`工作流时，确保对所有`texture`和`materials`进行如上配置。可以通过`Project Settings - Player - Other Settings - Color Space`来检查或者修改当前的颜色空间。

![](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230524112415878.png)

### [SkeletonGraphic组件](http://zh.esotericsoftware.com/spine-unity#SkeletonGraphic组件)

`SkeletonGraphic` 组件是三种在Unity中使用Spine skeleton的方式之一. 它们是: [SkeletonAnimation](http://zh.esotericsoftware.com/spine-unity#SkeletonAnimation组件), [SkeletonMecanim](http://zh.esotericsoftware.com/spine-unity#SkeletonMecanim组件) 和 [SkeletonGraphic (UI)](http://zh.esotericsoftware.com/spine-unity#SkeletonGraphic组件).

`SkeletonGraphic` 组件是 [`SkeletonAnimation`](http://zh.esotericsoftware.com/spine-unity#SkeletonAnimation组件)组件的平替, 它使用Unity的UI系统进行布局、渲染和遮罩交互.与 [`SkeletonAnimation`](http://zh.esotericsoftware.com/spine-unity#SkeletonAnimation组件) 组件一样, 你可以将Spine skeleton添加到`GameObject`中, 将其制成动画, 响应动画事件等等.

#### [为何要使用这一UI组件](http://zh.esotericsoftware.com/spine-unity#为何要使用这一UI组件)

Unity UI(`UnityEngine.UI`)使用 `Canvas` 和 `CanvasRenderers` 系统来分类和管理其可渲染对象.内置的可渲染的UI组件——如 `Text`, `Image`, 和 `RawImage` ——都依赖于`CanvasRenderer`来正常工作.将 `MeshRenderers` (如默认的Cube对象)或 `SpriteRenderers` (如Sprite)等对象置入UI, Unity将不会在 `Canvas` 中渲染它们`SkeletonAnimation`使用的是 `MeshRenderers` , 因此行为方式也是一样的.因此, spine-unity运行时提供了 `SkeletonAnimation` 的平替组件 `SkeletonGraphic`, 它是使用 `CanvasRenderers` 组件进行渲染的 `UnityEngine.UI.MaskableGraphic` 的子类.

#### [重要须知-Material](http://zh.esotericsoftware.com/spine-unity#重要须知-Material)

只能在 `SkeletonGraphic` 组件上使用与 `CanvasRenderer` 兼容的特殊着色器的material, 例如默认的 `Spine/SkeletonGraphic*` 着色器. 不要在 `SkeletonGraphic` 组件上使用如 `Spine/Skeleton` 的URP、LWRP或常规着色器. 没有肉眼可见的视觉错误并不意味着该着色器可以与 `SkeletonGraphic` 一起正常工作. 我们已知这种的情况: 它在移动设备上的渲染不正确, 然而在Unity编辑器中的渲染却没有任何问题. 和其他UI组件一样, `SkeletonGraphic` 使用 `CanvasRenderer` 而非 `MeshRenderer`, 后者使用了一条不同的渲染管线.

当把 `SkeletonDataAsset` 实例化为 `SkeletonGraphic`时, 在 `SpineAtlasAsset` 处指定的常规material将被忽略, 只使用其texture. 你可以使用[`SkeletonGraphicCustomMaterials`](http://zh.esotericsoftware.com/spine-unity#SkeletonGraphicCustomMaterials)组件来覆盖 `SkeletonGraphic`组件的materials.



![image-20230524113503145](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230524113503145.png)

### Spine `SkeletonGraphic`遮罩

和`UGUI`遮罩一样的实现方式即可，给`Image`挂上`Mask`组件即可

![image-20230524142442752](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230524142442752.png)



## Spine SkeletonGraphic源码

> 场景：`Spine`中的插槽`slot`有可能混用了多种混合模式`正常`，`相加`，`相乘`，`滤色`，但是在使用过程中其实并没有用到导入资源时生成的材质球，担心并不能很好的处理混用混合模式。
>
> 结论：生成的Material事实上在代码流程中需要用到，尽管代码仅通过这个Material取他的纹理`mainTexure`，所以生成的`Material`尽管没有直接使用到，仍然不能删除，否则会因为找不到材质和纹理导致渲染出白块。

![image-20230530174952309](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230530174952309.png)

> 合并部分网格，然后创建`Canvas`组件分批渲染。

![image-20230530174544161](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230530174544161.png)

这里只会取用`SubMesh`材质球中的`Texture`，最后`setMaterial`会使用在`Skeleton Graphic`组件上选定的唯一一个材质球(或者`customMaterialOverride`中复写的材质)。

![image-20230530174649047](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230530174649047.png)

渲染结果能够呈现出混合模式（改用Gamma颜色空间会更明显），那么和选用材质球的顶点数据有关。

![image-20230530191217194](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230530191217194.png)



仍然会从`Mesh Renderer`

```
 protected void UpdateMeshMultipleCanvasRenderers(SkeletonRendererInstruction currentInstructions,
            bool keepRendererCount)
```



参考`MeshGenerator.cs`文件中的region

`MeshsGenerator.AddSubesh()`



![image-20230530193418476](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230530193418476.png)



![image-20230530193523276](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230530193523276.png)



![image-20230530193937256](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230530193937256.png)



从结果来看，Spine以`Straight alpha`导出资源图片本身是没有问题的。认为`Spine`的混合是基于`Gamma`工作流，而在`Unity`重新构建时会导致在`Linear`工作流中混合导致出现这样的问题。



## Spine 4.0 工作流 与 `SkeletonGraphic`组件

[Spine-runtimes ChangeLog](https://github.com/EsotericSoftware/spine-runtimes/blob/4.0/CHANGELOG.md)

> `SkelotonGraphic`、`Blend Mode`、`Color Space`相关：
>
> - **Linear color space:** Previously Slot colors were not displayed the same in Unity as in the Spine Editor (when configured to display as `Linear` color space in Spine Editor Settings). This is now fixed at all shaders, including URP and LWRP shaders.
> - Added `SkeletonGraphicCustomMaterials` component, providing functionality to override materials and textures of a `SkeletonGraphic`, similar to `SkeletonRendererCustomMaterials`. Note: overriding materials or textures per slot is not provided due to structural limitations.
> - Additive Slots have always been lit before they were written to the target buffer. Now all lit shaders provide an additional parameter `Light Affects Additive` which defaults to `false`, as it is the more intuitive default value. You can enable the old behaviour by setting this parameter to `true`.
> - Added **native support for slot blend modes** `Additive`, `Multiply` and `Screen` with automatic assignment at newly imported skeleton assets. `BlendModeMaterialAssets` are now obsolete and replaced by the native properties at `SkeletonDataAsset`. The `SkeletonDataAsset` Inspector provides a new `Blend Modes - Upgrade` button to upgrade an obsolete `BlendModeMaterialAsset` to the native blend modes properties. This upgrade will be performed automatically on imported and re-imported assets.
> - `SkeletonGraphic` now **supports all Slot blend modes** when `Advanced - Multiple Canvas Renderers` is enabled in the Inspector. The `SkeletonGraphic` Inspector now provides a `Blend Mode Materials` section where you can assign `SkeletonGraphic` materials for each blend mode, or use the new default materials. New `SkeletonGraphic` shaders and materials have been added for each blend mode. The `BlendModes.unity` example scene has been extended to demonstrate this new feature. For detailed information see the [`SkeletonGraphic documentation page`](http://esotericsoftware.com/spine-unity#Parameters).

> `Unity`项目使用`Linear`颜色空间。对于`Spine`资源中，使用了`相加`或者其他混合模式的插槽在`Unity`中呈现的效果会有比较大的差异。
>
> ![image-20230531192928347](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230531192928347.png)
>
> 这种差异最主要的原因是`Spine`和`Unity`颜色空间差异。`Spine`默认使用`Gamma`颜色空间；`Unity`当前配置的是`Gamma`颜色空间。
>
> `Spine`资源导出和`Unity`资源导入工作流需要做相应的调整。

### Shader

复写`Spine-SkeletonGraphic-Additive.shader`，在`Linear`颜色空间中修改最终输出的`Color`到`Gamma`空间，但是不清楚会不会有未知的风险。

```shaderLab
// This is a premultiply-alpha adaptation of the built-in Unity shader "UI/Default" in Unity 5.6.2 to allow Unity UI stencil masking.

Shader "Spine/SkeletonGraphic Additive"
{
    Properties
    {
        [PerRendererData] _MainTex ("Sprite Texture", 2D) = "white" {}
        [Toggle(_STRAIGHT_ALPHA_INPUT)] _StraightAlphaInput("Straight Alpha Texture", Int) = 0
        [Toggle(_CANVAS_GROUP_COMPATIBLE)] _CanvasGroupCompatible("CanvasGroup Compatible", Int) = 1
        _Color ("Tint", Color) = (1,1,1,1)

        [HideInInspector][Enum(UnityEngine.Rendering.CompareFunction)] _StencilComp ("Stencil Comparison", Float) = 8
        [HideInInspector] _Stencil ("Stencil ID", Float) = 0
        [HideInInspector][Enum(UnityEngine.Rendering.StencilOp)] _StencilOp ("Stencil Operation", Float) = 0
        [HideInInspector] _StencilWriteMask ("Stencil Write Mask", Float) = 255
        [HideInInspector] _StencilReadMask ("Stencil Read Mask", Float) = 255

        [HideInInspector] _ColorMask ("Color Mask", Float) = 15

        [Toggle(UNITY_UI_ALPHACLIP)] _UseUIAlphaClip ("Use Alpha Clip", Float) = 0

        // Outline properties are drawn via custom editor.
        [HideInInspector] _OutlineWidth("Outline Width", Range(0,8)) = 3.0
        [HideInInspector] _OutlineColor("Outline Color", Color) = (1,1,0,1)
        [HideInInspector] _OutlineReferenceTexWidth("Reference Texture Width", Int) = 1024
        [HideInInspector] _ThresholdEnd("Outline Threshold", Range(0,1)) = 0.25
        [HideInInspector] _OutlineSmoothness("Outline Smoothness", Range(0,1)) = 1.0
        [HideInInspector][MaterialToggle(_USE8NEIGHBOURHOOD_ON)] _Use8Neighbourhood("Sample 8 Neighbours", Float) = 1
        [HideInInspector] _OutlineMipLevel("Outline Mip Level", Range(0,3)) = 0
    }

    SubShader
    {
        Tags
        {
            "Queue"="Transparent"
            "IgnoreProjector"="True"
            "RenderType"="Transparent"
            "PreviewType"="Plane"
            "CanUseSpriteAtlas"="True"
        }

        Stencil
        {
            Ref [_Stencil]
            Comp [_StencilComp]
            Pass [_StencilOp]
            ReadMask [_StencilReadMask]
            WriteMask [_StencilWriteMask]
        }

        Cull Off
        Lighting Off
        ZWrite Off
        ZTest [unity_GUIZTestMode]
        Fog
        {
            Mode Off
        }
        Blend One One
        ColorMask [_ColorMask]

        Pass
        {
            Name "Normal"

            CGPROGRAM
            #pragma shader_feature _ _STRAIGHT_ALPHA_INPUT
            #pragma shader_feature _ _CANVAS_GROUP_COMPATIBLE
            #pragma vertex vert
            #pragma fragment frag
            #pragma target 2.0

            // #include "CGIncludes/Spine-SkeletonGraphic-NormalPass.cginc"

            #include "UnityCG.cginc"
            #include "UnityUI.cginc"
            #include "Assets/Spine/Runtime/spine-unity/Shaders/CGIncludes/Spine-Common.cginc"

            #pragma multi_compile __ UNITY_UI_ALPHACLIP

            struct VertexInput
            {
                float4 vertex : POSITION;
                float4 color : COLOR;
                float2 texcoord : TEXCOORD0;
                UNITY_VERTEX_INPUT_INSTANCE_ID
            };

            struct VertexOutput
            {
                float4 vertex : SV_POSITION;
                fixed4 color : COLOR;
                half2 texcoord : TEXCOORD0;
                float4 worldPosition : TEXCOORD1;
                UNITY_VERTEX_OUTPUT_STEREO
            };

            fixed4 _Color;
            fixed4 _TextureSampleAdd;
            float4 _ClipRect;

            VertexOutput vert(VertexInput IN)
            {
                VertexOutput OUT;

                UNITY_SETUP_INSTANCE_ID(IN);
                UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(OUT);

                OUT.worldPosition = IN.vertex;
                OUT.vertex = UnityObjectToClipPos(OUT.worldPosition);
                OUT.texcoord = IN.texcoord;

                #ifdef UNITY_HALF_TEXEL_OFFSET
	                OUT.vertex.xy += (_ScreenParams.zw-1.0) * float2(-1,1);
                #endif

                #ifdef _CANVAS_GROUP_COMPATIBLE
	                half4 vertexColor = IN.color;
	                // CanvasGroup alpha sets vertex color alpha, but does not premultiply it to rgb components.
	                vertexColor.rgb *= vertexColor.a;
	                // Unfortunately we cannot perform the TargetToGamma and PMAGammaToTarget transformations,
	                // as these would be wrong with modified alpha.
                #else
                    // Note: CanvasRenderer performs a GammaToTargetSpace conversion on vertex color already, however incorrectly assuming straight alpha color.
                    float4 vertexColor = PMAGammaToTargetSpace(half4(TargetToGammaSpace(IN.color.rgb), IN.color.a));
                #endif
                    OUT.color = vertexColor * float4(_Color.rgb * _Color.a, _Color.a);
                    // Combine a PMA version of _Color with vertexColor.
                return OUT;
            }

            sampler2D _MainTex;

            fixed4 frag(VertexOutput IN) : SV_Target
            {
                half4 texColor = tex2D(_MainTex, IN.texcoord);

                #if defined(_STRAIGHT_ALPHA_INPUT)
	                texColor.rgb *= texColor.a;
                #endif

                half4 color = (texColor + _TextureSampleAdd) * IN.color;
                color *= UnityGet2DClipping(IN.worldPosition.xy, _ClipRect);

                #ifdef UNITY_UI_ALPHACLIP
	                clip (color.a - 0.001);
                #endif
                
                color.rgb = LinearToGammaSpace(color.rgb);// 转到Gamma空间
                return color;
            }
            ENDCG
        }
    }
    CustomEditor "SpineShaderWithOutlineGUI"
}
```



## Unity 在线性空间和`Gamma`空间中混合颜色有差别

在`MeshRenderder`和`CanvasRenderder`中同时存在

紫色块设置为`Blend One Zero`，色值`(162,145,242)`

黑色块设置为`Blend One Zero`，色值`(0,0,0)`



灰色块设置为`Blend One One`，色值`(140,140,140)`

![image-20230601153055320](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230601153055320.png)



紫色块设置为`Blend One Zero`，色值`(162,145,242)`

黑色块设置为`Blend One Zero`，色值`(0,0,0)`

灰色块设置为`Blend One One`，色值`(140,140,140)`

![image-20230601155245060](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230601155245060.png)

`Gamma`空间最终呈现的效果和设置值是一致的，而`Linear空间



## Unity处理`Linear`和`Gamma`转换的算法

[sRGB Approximations for HLSL 2012.8.6](http://chilliant.blogspot.com/2012/08/srgb-approximations-for-hlsl.html?m=1)

`UnityCG.cginc`文件里定义了`Linear`和`Gamma`转换算法的精确版本，实际使用时会使用它的近似版本。

`UnityCG.cginc`文件在项目中可以直接引用，通过使用它的方法，能在编辑器打开该文件；但是有可能没办法在编辑器中直接通过搜索定位到文件位置，因为该文件并不存放在项目中，它一般被存放在当前`Unity`版本文件目录中

![image-20230601174521834](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230601174521834.png)

`sRGB`色彩空间是非线性的，`RGB`转换到线性空间以及从线性空间转到`sRGB`色彩空间"官方提供"的转换版本是：

```c
// sRGB to Linear
if (C_srgb <= 0.04045)
    C_lin = C_srgb / 12.92;
else
    C_lin = pow((C_srgb + 0.055) / 1.055, 2.4);

// Linear to sRGB
  if (C_lin <= 0.0031308)
    C_srgb = C_lin * 12.92;
  else
    C_srgb = 1.055 * pow(C_lin, 1.0 / 2.4) - 0.055;

```

通常采用近似计算公式$$C_lin_1 = pow(C_srgb, 2.2);$$ 但是这样的曲线拟合十分不准确

```c
// Gamma转Linear，精确计算
inline float GammaToLinearSpaceExact (float value)
{
    if (value <= 0.04045F)
        return value / 12.92F;
    else if (value < 1.0F)
        return pow((value + 0.055F)/1.055F, 2.4F);
    else
        return pow(value, 2.2F);
}

// Gamma转Linear空间，采用近似计算
inline half3 GammaToLinearSpace (half3 sRGB)
{
    // Approximate version from http://chilliant.blogspot.com.au/2012/08/srgb-approximations-for-hlsl.html?m=1
    return sRGB * (sRGB * (sRGB * 0.305306011h + 0.682171111h) + 0.012522878h);

    // Precise version, useful for debugging.
    //return half3(GammaToLinearSpaceExact(sRGB.r), GammaToLinearSpaceExact(sRGB.g), GammaToLinearSpaceExact(sRGB.b));
}

// Linear转Gamma，精确计算
inline float LinearToGammaSpaceExact (float value)
{
    if (value <= 0.0F)
        return 0.0F;
    else if (value <= 0.0031308F)
        return 12.92F * value;
    else if (value < 1.0F)
        return 1.055F * pow(value, 0.4166667F) - 0.055F;
    else
        return pow(value, 0.45454545F);
}

// Linear转Gamma，采用近乎完美拟合的近似计算
inline half3 LinearToGammaSpace (half3 linRGB)
{
    linRGB = max(linRGB, half3(0.h, 0.h, 0.h));
    // An almost-perfect approximation from http://chilliant.blogspot.com.au/2012/08/srgb-approximations-for-hlsl.html?m=1
    return max(1.055h * pow(linRGB, 0.416666667h) - 0.055h, 0.h);

    // Exact version, useful for debugging.
    //return half3(LinearToGammaSpaceExact(linRGB.r), LinearToGammaSpaceExact(linRGB.g), LinearToGammaSpaceExact(linRGB.b));
}
```



折中的方式（不行）

- 以`Gamma`空间导出

- `Unity`不要对资产勾选`sRGB`，`Shader`中统一处理

  在`Spine-SkeletonGraphic-NormalPass.cginc`中将输出的颜色转到`Linear`空间。

  ![image-20230601180457067](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230601180457067.png)





## 线性颜色空间和 HDR

使用 HDR 时，渲染在线性空间中执行到浮点缓冲区。这些缓冲区具有足够的精度，无论何时访问缓冲区，都不需要转换到伽马空间或从伽马空间转换。这意味着，在线性模式下渲染时，您使用的帧缓冲区会将颜色存储在线性空间中。因此，**所有混合效果和后处理效果均在线性空间中隐式执行。当写入最终后备缓冲区时，将应用伽马校正**。

## 线性颜色空间和非 HDR

启用线性颜色空间但未启用 HDR 时，将使用一种特殊的帧缓冲类型，它支持 sRGB 读取和 sRGB 写入（读取时从伽马转换为线性，而写入时从线性转换为伽马）。**当此帧缓冲区用于混合，或将其绑定为纹理时，值在使用前将转换为线性空间。写入这些缓冲区时，所写入的值将从线性空间转换为伽马空间**。如果在线性模式和非 HDR 模式下进行渲染，则所有后处理效果都会创建其源缓冲区和目标缓冲区并启用 sRGB 读写权限，以便在线性空间中进行后处理和后处理混合。



`Linear`和`Gamma`空间颜色混合结果问题

在`Unity` `Linear Color Space`下最终呈现的结果：

- `非HDR`：用于混合或者绑定纹理，使用前转换为线性空间，`Shader`拿到的颜色是经过`GammaToLinearSpace`后的颜色；输出时使用`LinearToGammaSpace`相当于做了两次转换。

  渲染图片本身没有问题，因为做了两次转换，最终呈现的结果一致。但是如果需要做颜色混合，哪怕在`Shader`中执行混合，在`Unity`中呈现的混合结果和在`PS`等美工软件(使用`Gamma`颜色空间)中所呈现的效果会有区别。

- `HDR`：作为线性颜色读取和写入。最终会执行一次`LinearToGammaSpace`的伽马矫正。

![image-20230602101427502](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230602101427502.png)

而在`Gamma Color Space`下，`HDR`和非`HDR`都会呈现`(140,140,140,255)`的结果。

也就是说，在`Linear Color Space`下，`Shader`中首先将`非HDR`其视为`sRGB`颜色，读取时将其从`Gamma`空间转换到了线性空间；而`HDR`颜色没有做转换，当作线性空间颜色直接处理。

如果材质属性中，不使用`Color`类型，而是使用`Vector`类型，那么颜色输入时不会做`Gamma`移除，最后呈现的颜色是`(195,195,195,255)`



也就是说，`Spine`插槽(`Slot`)所使用的相加混合模式，在`Unity` `Linear Color Space`中运作，最终`源缓冲区`和`目标缓冲区`会转到线性空间中去混合，这样会得到和在`Gamma`空间混合不一致的结果，导致呈现的效果暗部细节过多，亮部呈现的不完整，混合后的色值偏低。

> `Linear -> Gamma` 变亮，色值变大
>
> `Gamma -> Linear` 变暗，色值变小



脚本验证：

脚本流程和实际的混合结果时一致的。这里的`Color`相关`API`拿到的`RGB`值是没有所谓的转换过程的，所以可以直接使用。

![image-20230602105938034](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230602105938034.png)



![image-20230602105915726](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230602105915726.png)



`Unity`项目设置中选用`Linear Color Space`，有关`UI`的渲染后处理为`Gamma`，相关的输入也不可以移除伽马矫正



1. `Unity` `Linear Color Space` 处理混合模式(如`线性减淡`)和从设计软件处理所呈现的效果是不同的。会将缓冲区颜色转到线性空间混合，然后执行一次伽马矫正转换到伽马空间。这样会导致最终混合的结果，暗部细节增多，亮部缺失。对一些使用相加模式的光效来说影响很大
2. 针对`Spine`的`Skeleton Graphic`在`UGUI`上的渲染有一种折中的错误解决方案。(仅能保证混合的两种颜色只有一种是在伽马空间下的颜色，对于`线性减淡`效果有修复作用，其他效果不行)





## `Spine - Unity`流程

1. 修改`Spine-SkeletonGraphic-Additive.shader`代码，输出颜色转到`Gamma`颜色空间，目的是为了多一次伽马矫正，将“错误”的颜色输出，在和缓冲区颜色混合时保证由`Additive`着色器输出的颜色是`Gamma`空间颜色，但是因为缓冲区的颜色在混合时仍然会进行一次`伽马矫正移除`，所以缓冲区颜色还是在线性空间下来混合的。这样的修复方式是错误的，但对于`Additive`混合来说，是一个次优解。
2. 另外，需要做变体收集。项目`Shader`中使用的`shader_feature`在打包时会丢失变体，导致效果失真，可以使用`multi_compile`来暂时延缓问题，会带来负面影响，需要及时输出变体收集方案。

### Spine 流程

`Spine`资源制作流程不必改动，仅需要调整导出时的纹理打包设置

***纹理图集 - 打包设置 - 输出*** 勾选**溢出(bleed)**

![image-20230531200818686](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230531200818686.png)

![image-20230531193839413](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230531193839413.png)

***资源检查***

勾选了**`预乘Alpha(Premultiply Alpha,pma)`**导出的资源文件**`***.atlas.txt`**中存在`pma:true`的文本；而勾选了**`溢出(bleed)`**导出的资源中不会存在该文本。

![image-20230605170742260](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230605170742260.png)

![image-20230605170849248](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230605170849248.png)

### `Unity`流程

>  流程1.2.在配置好`Spine` ``Altas Texture Settings`预设后，这两项会默认勾选；生成的材质球也会使用勾选了`Stragith Alpha Texture`的材质球（使用的`Shader`是`Skeleton PMA Multiply`，不必抠字眼）
>
> 不过当前已有的资源需要更新才能重新生成对应配置好的资源。

![image-20230605200731687](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230605200731687.png)

#### 1. Texture 启用 `sRGB (Color Texture)` 和 `Alpha Is Transparency`(配置完预设不必处理)

![image-20230531201552118](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230531201552118.png)

#### 2. Material 参数中启用 `Straight Alpha Texture`（配置完预设不必处理）

![image-20230531201138661](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230531201138661.png)

#### 3. `SkeletonGraphic`组件的使用

为`SkeletonGraphic`组件指定`SkeletonData Asset`，材质球默认选用`SkeletonGraphicDefault`，保证该材质球启用了`Straight Alpha Texture`。

![image-20230531202342464](C:/Users/Nox123/AppData/Roaming/Typora/typora-user-images/image-20230531202342464.png)

如果该`SkeletonData Asset`混用了插槽混合模式(和对应的美术确定是否在`Spine`中使用了多种插槽混合模式)，需要在`Advanced`中开启`Multiple CanvasRenders`。点击`Assign Default`分配默认混合模式材质球。

**注意：**需要关闭`Pma Vertex Colors`以启用`Additive Material`。

![image-20230605173400546](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230605173400546.png)

![image-20230531202549883](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230531202549883.png)

### 其他

推测打包后部分特效有可能视觉效果和编辑器中运行的效果有差异，是因为着色器变体在打包时有丢失的可能。目前有临时修复手段，后续会跟进着色器变体收集和自动化策略。

已有`Spine`资源需要按照给定的规范重新导入导出。



有关`Spine Runtime`中的材质球材质属性目前已经更新了`SkeletonGraphic`相关的一版，尚不完善。后续会跟进处理。

有关局内使用到的`Spine`资源有同样的规范问题，尚未处理。在配置好预设之后以同样的方式更新资源即可，材质编辑器界面按照默认配置即可，一般不需要手动处理。



![image-20230605194804798](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230605194804798.png)





###  对于Spine 4.0+ 版本在Unity线性颜色空间Addtive混合模式呈现结果和实际效果有出入的问题

`Unity`线性颜色空间对于`sRGB`颜色混合得到的结果和在`Gamma`颜色空间混合得到的结果是不一致的，主要是因为在混合缓冲区颜色时，线性颜色空间需要将缓冲区的颜色转到线性空间去混合，然后写入缓冲区时添加伽马矫正。对于`Additive`混合模式来说，在结果上会得到比`Gamma`颜色空间中混合模式偏小的颜色值。

- 修改`Spine/SkeletonGraphic Additive`着色器，着色器输出的结果中添加一个伽马矫正操作

  ![image-20230606151120865](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230606151120865.png)

  实际上这是错误的修复方式

**着色器帧缓冲提取**

仅仅在部分平台上支持

输出合并阶段仅仅意味着高度可配置，但是大概并不能通过编程实现

- 构建测试环境？？

  `Unity`环境

- 添加导入器检查



结果对照

![image-20230607105225943](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230607105225943.png)





# 背景

由于`Unity`游戏工程选用了`Linear`颜色空间



# 方案

## 1. 修改`Unity`游戏工程**颜色空间**为`Gamma`

- 需要预估并承担修改颜色空间带来的风险

> 前期技术选型选用`Linear`颜色空间的必要性。有什么需要考量的因素么



## 2. 美术环境设置为`Linear`

> `Spine 4.0`开始支持线性。但是对于半透明的混合还是会有问题
>
> [渲染管线](https://github.com/EsotericSoftware/spine-runtimes/blob/4.0/CHANGELOG.md)
>
> ![image-20230711103527244](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230711103527244.png)
>
> ![image-20230711142625967](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230711142625967.png)
>
> ![image-20230711143146561](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230711143146561.png)

![image-20230711113127089](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230711113127089.png)





> Unity Version: `2020.3.39f1`
>
> Unity Color Space: `Linear`
>
> Spine Version: `4.0.64`
>
> Spine-Unity Runtime Version: `spine-unity-4.0-2022-09-26.unitypackage`
>
> Spine Color Space: Gamma

我们的团队遇到了一个颜色空间相关的问题。

当我们团队的美术师尝试在Spine中使用插槽混合模式（例如`Addtive`），或者使用半透明图片资源制作一些`UI`特效时。它在`Spine`中的表现效果会和在`Unity`中表现效果有些差异。我们确定这是由于我们在Unity中使用的Linear Color Space所导致的问题，因为当我们尝试把Color Space转为Gamma时能获得一致的视觉表现。另外，我也尝试在Unity中创建了一些场景，在这些场景中，我尝试使用`Shader`的`Blend`来实现`Addtive`混合模式。

在这个示例场景中，我使用了一张颜色值为(128,128,128,255)的纯色图片，如你所见，我对两个游戏物体使用了同样的材质，这个材质的混合模式我在Shader中定义为了`Blend One One`以实现`Additive`的混合模式。当我改变颜色空间时，它的颜色混合结果有了不一致的表现。

![image-20230711113127089](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230711113127089.png)

事实上，我了解这是因为颜色空间的不一致所带来的必然结果。不过我们的团队希望能够以比较小的代价兼容Unity和美术之间的工作流差异，并向Spine团队寻求帮助和解决方案。

目前我们尝试了一种"错误"的解决办法(但是在某些场景下，这种方式能带来不错的效果)。我们采用的方式是修改Spine-Unity Runtime中的Shader代码，以错误的方式来处理`Additive`着色器的片元着色器返回值。例如，我们修改了`Spine/SkeletonGraphic Additive`，使最终得到的颜色做一次`TargetToGammaSpace`的操作。

![image-20230724200125681](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230724200125681.png)

这种方式肯定是错误的，但是在算法上他确实会使得最终的混合结果向我们所期待的结果靠拢，下面是我们在项目中调试后所得到的效果

![image-20230607105225943](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230607105225943.png)

所以我们的诉求是希望能够在Linear颜色空间下得到和Spine中一致的视觉效果。很遗憾我们的技术总监表明Unity的颜色空间不可以轻易修改，所以我们只能使用这种笨拙的方式来处理问题。很希望能够得到Spine团队的帮助和建议，期待您的回复。





Our team has encountered a color space related issue.

When the artists in our team try to create some `UI` effects using slot blending modes (e.g. `Addtive`) in Spine, or using semi-transparent image resources. It would behave a bit differently in `Spine` than in `Unity`. We've determined that this is due to the Linear Color Space we're using in Unity, as we get consistent visual performance when trying to convert Color Space to Gamma. Additionally, I also tried to create some scenes in Unity where I tried to use `Shader`'s `Blend` to implement the `Addtive` blend mode.

In this sample scene I used a solid color image with color values (128,128,128,255) and as you can see I used the same material for both game objects, the blend mode of this material I defined in the Shader as `Blend One One` to implement the `Additive` blend mode. When I change the color space, it has an inconsistent color mixing result.







In fact, I understand that this is an inevitable result of inconsistencies in the color space. However, our team wanted to be compatible with the workflow differences between Unity and the art at a relatively small cost and looked to the Spine team for help and a solution.

So far we've tried a "buggy" solution (but in some scenarios it works well). The way we did it was to modify the shader code in the Spine-Unity Runtime to handle the slice shader return values of the `Additive` shader in a wrong way. For example, we modified the `Spine/SkeletonGraphic Additive` so that the final color obtained does a `TargetToGammaSpace` operation.





感谢您的回复，我们团队仔细阅读相关文档，也注意到Spine编辑器从4.0版本开始支持了对于线性颜色空间的预览，并尝试了将Spine预览修改到线性颜色空间。事实上，这种方式解决了我们关于Unity和Spine视觉效果不一致的问题，也能够帮助美术师在Spine资源制作的流程中预览到它在Unity项目中的视觉表现。

但是我们的美术团队习惯使用Gamma的工作流来输出美术资源，所以我们使用的图片资源几乎都是符合`sRGB`标准的图片，这在Gamma颜色空间下表现很好，但是切换到线性空间后表现很糟糕。如下图所示：

![image-20230725134355211](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230725134355211.png)

我们认为如果能使用线性图片资源而不是sRGB图片或许能解决这个问题，遗憾的是我们的美术团队并不适应线性空间的工作流。于是我们尝试将sRGB的资源图片在`PhotoShop`或者其他图片处理软件中转为线性图片。这样的处理方式得到的图片尽管看起来一团糟，但是我将它导入Unity项目中并正确配置Texture后它的表现却出乎意料的好。我也将这张处理过的图片在Spine中替换原有的图片资源，并期待能够解决我们所遇到的全部问题。但结果令人惋惜，它在Spine的预览里并没有按照预想的那般有很好的视觉表现。等等，我好像遗漏了些什么内容，我会次尝试去验证这种做法到底是不是有效。

我们不是很清楚其他团队有没有遇到这种因为颜色空间所导致的工作流冲突，并期望能够得到一些建议和帮助。





Thanks for your reply, our team read the documentation carefully and noticed that the Spine editor supports previewing in linear color space since version 4.0, and tried to modify the Spine preview to linear color space. In fact, this approach solved our problem about the inconsistency between Unity and Spine visuals, and also helped artists to preview the visual performance of Spine resources in Unity projects during the production process.

However, our art team is used to using Gamma's workflow to output art resources, so almost all of the image resources we use are `sRGB` compliant images, which performs well in Gamma color space, but performs poorly when switching to linear space. This is shown in the image below:

![image-20230725134355211](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230725134355211.png)

We thought we might be able to solve this problem if we could use linear image resources instead of sRGB images, unfortunately our art team is not adapted to the linear color space workflow. So we tried to convert the sRGB resource images to Linear images in `PhotoShop` or other image processing software. The resulting image looked like a mess, but when I imported it into the Unity project and configured the `Texture` correctly, it performed surprisingly well. I also took this processed image and replaced the original image resource in Spine, expecting it to solve all the problems we were having. Sadly, it didn't work as well as expected in the Spine preview. Wait, I think I'm missing something, I'll try again to see if this works.

We're not sure if other teams are experiencing this kind of workflow conflict due to color space, and look forward to some advice and help.





感谢您的回复和建议，我会告知我的同事们并继续收集一些问题和做法。另外很抱歉我在描述问题时使用了不准确的术语。

正如您所说的那样。我是从一篇博客中看到一种处理图片的方式：在PhotoShop中修改图片为每通道32bit，然后使用灰度系数混合RGB颜色。尽管我不清楚它的原理。可正如我之前提到的，我遗漏了一些东西。我尝试查询之前的工作记录，发现其实它并没有表现得很理想，条带也并没有消失。

我们也意识到以每通道16或32位通道保存图像资源是一种不可取的方式。仅仅修改Shader也并不能解决问题。正如你所说的，我们得出的结论和您所说的基本一致——在Gamma颜色空间混合结果看起来很好，切换到Linear颜色空间就是会存在差异，这种情况几乎不可避免。

我们也了解到一种代价极高的方法。在Unity中将所有UI层的图片取消勾选`sRGB (Color Texture)`，这样会渲染出错误的颜色。然后通过屏幕后处理操作将这次的错误做法补偿，最后渲染出来的结果看起来会像是在Gamma颜色空间中所表现的那样。我们预估这种操作会带来一些性能上的消耗以及其他未知的风险，所以目前并没有采用。



另外感谢您的建议，我们会尝试继续做一些努力。

![image-20230725214948938](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/main/images/image-20230725214948938.png)





Thank you for your reply and I apologize for using inaccurate terminology when describing the problem.

As you said. I was reading from a blog post about a way to process images: modifying them in PhotoShop to 32bit per channel, and then mixing the RGB colors using grayscale coefficients. Although I'm not sure how it works. But as I mentioned before, I'm missing something. I tried to look up the log of my previous work and realized that it didn't actually behave optimally and the bands didn't disappear.

We also realized that saving image resources at 16 or 32 bit channels per channel was an undesirable way to go. Simply modifying the Shader didn't solve the problem either. We came to the same conclusion as you said - Looks good with gamma-space blending, then not so good with linear-space blending, which is almost inevitable.

We have also learned of an extremely costly approach. Uncheck `sRGB (Color Texture)` for all UI layer images in Unity, which will render the wrong colors. This error is then compensated for by a screen post-processing operation, and the final rendered result will look like it was represented in Gamma color space. We anticipate some performance hit and other unknown risks associated with this operation, so it is not currently used.

We get the visual effect we want in the Game view, even though it's what should have been rendered in the Scene view.



很高兴得到您的及时指点！

我们最终还是希望能在Unity项目和美术师保持工作流一致。我们的技术总监已经尝试采纳您的建议，将Unity颜色空间切换到Gamma。我们不确定这种修改方式会不会因为版本迭代而存在风险，不够目前来看，它在我们的游戏里表现良好。

至于我之前所提到的那篇博客，很遗憾它已经被我丢进了垃圾桶。不过我在Adobe Support Community中看到了关于[**Creating Linear Color space**]([](https://community.adobe.com/t5/photoshop-ecosystem-discussions/creating-linear-color-space/td-p/10465287))的建议。它提到了在线性空间中创建文档相关的操作。



Glad to have your prompt guidance!

We ultimately want to keep the workflow consistent across Unity projects and artists. Our technical director has tried to take your suggestion and switch the Unity color space to Gamma, and we're not sure if this modification is risky due to version iteration, but so far it's working well in our game.

As for the blog I mentioned earlier, unfortunately it's in the trash. I did however see something in the Adobe Support Community about [**Creating Linear Color space**](https://community.adobe.com/t5/photoshop-ecosystem-discussions/ creating-linear-color-space/td-p/10465287) suggestion. It mentions operations related to creating documents in linear space.





## [Make spine animation plays in editor mode](https://zh.esotericsoftware.com/forum/d/11084-play-an-animation-on-editor-mode/18)

```c#
using System;
using System.Linq;
using Spine.Unity;
using UnityEditor;
using UnityEngine;

namespace Spine
{
    public enum SpineAnimationType
    {
        None = 0,
        SkeletonAnimation = 10,
        SkeletonGraphic = 20,
    }

    [ExecuteInEditMode]
    public class SpineAnimationController : MonoBehaviour
    {
        [SerializeField] private SkeletonAnimation skeletonAnimation;
        [SerializeField] private SkeletonGraphic skeletonGraphic;

        [SerializeField] private int indexAnim = 0;
        [SerializeField] private string animationName = "idle";
        [SerializeField] private bool loop = false;
        [SerializeField] private SpineAnimationType type = SpineAnimationType.SkeletonAnimation;
        [SerializeField] private float timeScale = 1f;

        public SkeletonAnimation SkeletonAnimationHolder =>
            skeletonAnimation ?? gameObject.GetComponent<SkeletonAnimation>();

        public SkeletonGraphic SkeletonGraphicHolder =>
            skeletonGraphic ?? gameObject.GetComponent<SkeletonGraphic>();
    }

    /// <summary>
    /// Mask Spine animation play in editor mode.
    /// </summary>
    [CustomEditor(typeof(SpineAnimationController))]
    // [CanEditMultipleObjects]
    public class SpineAnimationControllerEditor : Editor
    {
        internal static class Styles
        {
            public static readonly GUIContent TypePop = new GUIContent("Type");

            public static readonly GUIContent LoopLabel = new GUIContent("Loop",
                "Whether or not .AnimationName should loop. This only applies to the initial animation specified in the inspector, or any subsequent Animations played through .AnimationName. Animations set through state.SetAnimation are unaffected.");

            public static readonly GUIContent AlwaysPlayLabel = new GUIContent("Always Play");

            public static readonly GUIContent TimeScaleLabel = new GUIContent("Time Scale",
                "The rate at which animations progress over time. 1 means normal speed. 0.5 means 50% speed.");

            public static readonly GUIContent AnimationNameLabel = new GUIContent("Animation Name",
                "The rate at which animations progress over time. 1 means normal speed. 0.5 means 50% speed.");

            public static readonly GUIContent AnimationEmptyLabel = new GUIContent("Animation is empty!");

            public static readonly GUIContent ResumtButton = new GUIContent("Resume");

            public static readonly GUIContent PauseButton = new GUIContent("Pause");

            public static readonly GUIContent RestartButton = new GUIContent("Restart");
        }


        private SpineAnimationController Script => target as SpineAnimationController;

        private SkeletonAnimation SkeletonAnimationHolder => Script.SkeletonAnimationHolder;

        private SkeletonGraphic SkeletonGraphicHolder => Script.SkeletonGraphicHolder;

        // private int indexAnim = 0;
        //
        // string animationName = "idle";

        SerializedProperty indexAnim;
        SerializedProperty animationName;
        SerializedProperty loop;
        SerializedProperty type;
        SerializedProperty timeScale;

        SpineAnimationType Type
        {
            set { type.intValue = (int)value; }
            get { return (SpineAnimationType)type.intValue; }
        }

        private void OnEnable()
        {
            indexAnim = serializedObject.FindProperty("indexAnim");
            animationName = serializedObject.FindProperty("animationName");
            loop = serializedObject.FindProperty("loop");
            type = serializedObject.FindProperty("type");
            timeScale = serializedObject.FindProperty("timeScale");
        }

        public override void OnInspectorGUI()
        {
            if (Type == SpineAnimationType.None)
            {
                if (SkeletonAnimationHolder != null)
                {
                    Type = SpineAnimationType.SkeletonAnimation;
                }
                else if (SkeletonGraphicHolder != null)
                {
                    Type = SpineAnimationType.SkeletonGraphic;
                }
            }

            // Type
            Type = (SpineAnimationType)EditorGUILayout.EnumPopup(Styles.TypePop, Type);
            EditorGUILayout.Space(10);

            // Get animation name array from skeletonDataAsset
            var animationItems = GetAnimationItems();
            var animationValid = (animationItems != null && animationItems.Length > 0);
            if (!animationValid)
            {
                EditorGUILayout.LabelField(Styles.AnimationEmptyLabel);
                EditorGUILayout.Space(10);
            }

            // Inspector UI
            using (new EditorGUI.DisabledScope(!animationValid))
            {
                EditorGUI.BeginChangeCheck();
                indexAnim.intValue =
                    EditorGUILayout.Popup(Styles.AnimationNameLabel, indexAnim.intValue, animationItems);
                if (animationValid)
                    animationName.stringValue = animationItems[indexAnim.intValue];
                if (EditorGUI.EndChangeCheck())
                {
                    RestartAnim();
                }

                timeScale.floatValue = EditorGUILayout.Slider(Styles.TimeScaleLabel, timeScale.floatValue, -2, 2);

                EditorGUI.BeginChangeCheck();
                loop.boolValue = EditorGUILayout.Toggle(Styles.LoopLabel, loop.boolValue);
                EditorGUILayout.Space(10);
                if (EditorGUI.EndChangeCheck())
                {
                    ResumeAnim();
                }

                EditorGUILayout.BeginHorizontal();
                if (GUILayout.Button(Styles.ResumtButton))
                    ResumeAnim();

                if (GUILayout.Button(Styles.RestartButton))
                    RestartAnim();

                if (GUILayout.Button(Styles.PauseButton))
                    PauseAnim();
                EditorGUILayout.EndHorizontal();
            }

            serializedObject.ApplyModifiedProperties();
        }

        #region Animation

        public string[] GetAnimationItems()
        {
            if (Type == SpineAnimationType.SkeletonAnimation)
            {
                return Script.SkeletonAnimationHolder?.skeletonDataAsset.GetSkeletonData(false).Animations
                    .Items.ToList().ConvertAll(input => input.Name).ToArray() ?? new string[0];
            }
            else if (Type == SpineAnimationType.SkeletonGraphic)
            {
                return Script.SkeletonGraphicHolder?.skeletonDataAsset.GetSkeletonData(false).Animations
                    .Items.ToList().ConvertAll(input => input.Name).ToArray() ?? new string[0];
            }

            return new string[0];
        }

        private TrackEntry _trackEntry;
        private float _timeCount;

        public void ResumeAnim()
        {
            EditorApplication.update -= UpdateSpine;
            EditorApplication.update += UpdateSpine;

            if (Type == SpineAnimationType.SkeletonAnimation)
            {
                SkeletonAnimationHolder?.Skeleton.SetToSetupPose();
                SkeletonAnimationHolder?.AnimationState.ClearTracks();

                SkeletonAnimationHolder?.gameObject.SetActive(true);
                _trackEntry =
                    SkeletonAnimationHolder?.AnimationState.SetAnimation(0, animationName.stringValue, loop.boolValue);
            }
            else if (Type == SpineAnimationType.SkeletonGraphic)
            {
                SkeletonGraphicHolder?.Skeleton.SetToSetupPose();
                SkeletonGraphicHolder?.AnimationState.ClearTracks();

                SkeletonGraphicHolder?.gameObject.SetActive(true);
                _trackEntry =
                    SkeletonGraphicHolder?.AnimationState.SetAnimation(0, animationName.stringValue, loop.boolValue);
            }
        }

        public void PauseAnim()
        {
            EditorApplication.update -= UpdateSpine;
        }

        public void RestartAnim()
        {
            _timeCount = 0f;
            ResumeAnim();
        }

        public void UpdateSpine()
        {
            _timeCount += Time.deltaTime * timeScale.floatValue;

            if (_trackEntry != null)
            {
                _trackEntry.TrackTime = _timeCount;
            }

            if (Type == SpineAnimationType.SkeletonAnimation)
            {
                SkeletonAnimationHolder?.Update(_timeCount);
                SkeletonAnimationHolder?.Skeleton.Update(_timeCount);
                SkeletonAnimationHolder?.LateUpdate();
            }
            else if (Type == SpineAnimationType.SkeletonGraphic)
            {
                SkeletonGraphicHolder?.Update(_timeCount);
                SkeletonGraphicHolder?.Skeleton.Update(_timeCount);
                SkeletonGraphicHolder?.LateUpdate();
            }
        }

        private void OnDestroy()
        {
            EditorApplication.update -= UpdateSpine;
        }

        #endregion
    }
}
```





