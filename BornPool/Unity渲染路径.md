# 参考

[Unity 渲染路径 2020.3](https://docs.unity3d.com/cn/2020.3/Manual/RenderingPaths.html)

[Unity 渲染管线 2020.3](https://docs.unity3d.com/cn/2020.3/Manual/render-pipelines.html)



# 渲染路径

渲染路径是用于渲染光照和阴影的一系列操作。

渲染路径`(Rendering Path)`决定了光照是如何应用到`Unity Shader`中的。如果要和光源打交道，需要为每个`Pass`指定使用的渲染路径。



> `Unity`支持多种类型的渲染路径
>
> |                                               | `Unity 5.0` 之前 | `Unity 5.0`之后 |
> | --------------------------------------------- | :--------------: | :-------------: |
> | 前向渲染路径`(Forward Rendering Path)`        |        √         |        √        |
> | 延迟渲染路径`(Deferred Rendering Path)`       |        √         |   更新 + 兼容   |
> | 顶点照明渲染路径`(Vertex Lit Rendering Path)` |        √         |        ×        |



大多数情况下， 一个项目只使用一种渲染路径，因此可以为整个项目设置渲染时的渲染路径。

`Unity -> Edit -> Project Settings -> Player -> Other Settings -> Rendering Path` OR `Unity -> Edit -> Project Settings -> Graphics`

![image-20230316103445029](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20230316103445029.png)

此外可以针对每个摄像机重写渲染路径

![image-20230316103642313](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20230316103642313.png)

> 如果运行项目的设备上的 `GPU`不支持所选的渲染路径，则 Unity 将自动使用较低保真度的渲染路径。例如，在无法处理延迟着色的`GPU`上，`Unity`使用前向渲染。
>
> 如`GPU`不支持延迟渲染，那么 Unity 就会使用前向渲染。

完成如上的设置后，就可以在每个`Pass`中使用标签来指定该`Pass`使用的渲染路径，通过设置`Pass`的`LightMode`标签实现，不同类型的渲染路径可能会包含多种标签设置。

>`LightMode` 标签是一个预定义的通道标签，`Unity` 使用它来确定是否在给定帧期间执行该通道，在该帧期间 Unity 何时执行该通道，以及 `Unity`对输出执行哪些操作。
>
>**注意：**`LightMode`标签和`LightMode`枚举无关，后者与光照有关
>
>每个渲染管线都使用 `LightMode` 标签，但预定义的值及其含义各不相同。
>
>在内置渲染管线中，如果不设置 `LightMode` 标签，Unity 会在没有任何光照或阴影的情况下渲染通道；这本质上相当于 `LightMode` 的值为 `Always`。在可编程渲染管线中，您可以使用 `SRPDefaultUnlit` 值来引用没有 `LightMode`标签的通道。
>
>`LightMode`标签也可以用过`C#`脚本使用。
>
>[`Material.SetShaderPassEnabled`](https://docs.unity3d.com/cn/2020.3/ScriptReference/Material.SetShaderPassEnabled.html) 和 [`ShaderTagId`](https://docs.unity3d.com/cn/2020.3/ScriptReference/ShaderTagId.html) 使用 `LightMode` 标签的值来确定 Unity 如何处理给定的通道。

``` csharp
Pass{
    Tags{
        "LightMode" = "ForwardBase"
    }
}
```

>  [内置渲染管线通道标签 2020.3](https://docs.unity3d.com/cn/2020.3/Manual/shader-predefined-pass-tags-built-in.html)
>
>  [通用渲染管线`(URP)`通道标签 10.10.0](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@10.10/manual/urp-shaders/urp-shaderlab-pass-tags.html)



通俗来讲，指定渲染路径是和`Unity`底层渲染引擎的一次重要沟通，相当于协议或约定。随后可以通过`Unity`提供的内置光照变量来访问这些属性。如果没有指定任何渲染路径，那么一些光照变量可能不会被正确赋值，计算出来的效果可能是错误的。

`Light Mode`标记定义了在`Light Pipeline`中`Pass`的职责，在`Built-in Render Pipeline`中，大多数需要和光照交互的着色器都被写成了`Surface Shaders`并处理了所有必要的细节。但是`Built-in Render Pipeline`中自定义着色器需要使用`Light Mode`来指明在`Light Pipeline`中如何考虑`Pass`

下表显示了内置渲染管道中使用的`LightMode`标签与`URP`期望的标签之间的对应关系。和`URP`所期望的标签之间的对应关系。有几个在`URP`中不支持传统的内置渲染管线标签：`PrepassBase`, `PrepassFinal`, `Vertex`, `VertexLMRGBM`, 和 `VertexLM`。同时。在`URP`中还有一些标签，在内置渲染管线中没有对应的标签。



| **`Built-in Render Pipeline`** | Description                                                  | **`URP`**            |
| ------------------------------ | ------------------------------------------------------------ | -------------------- |
| Always                         | Always rendered; no lighting applied                         | -                    |
| ForwardBase                    | Used in Forward rendering; Ambient, main Directional light, vertex/SH lights, and lightmaps applied | UniversalForward     |
| ForwardAdd                     | Used in Forward rendering; Additive per-pixel lights applied, one Pass per light | UniversalForward     |
| Deferred                       | Used in Deferred Shading; renders G-buffer                   | UniversalGBuffer     |
| ShadowCaster                   | Renders object depth into the shadow map or a depth texture  | ShadowCaster         |
| MotionVectors                  | Used to calculate per-object motion vectors                  | MotionVectors        |
|                                | URP uses this tag value in the Forward Rendering Path; the Pass renders object geometry and evaluates all light contributions. | UniversalForwardOnly |
|                                | URP uses this tag value in the 2D Renderer; the Pass renders objects and evaluates 2D light contributions. | Universal            |
|                                | The Pass renders only depth information from the perspective of a Camera into a depth texture. | DepthOnly            |
|                                | This Pass is executed only when baking lightmaps in the Unity Editor; Unity strips this Pass from shaders when building a Player. | Meta                 |
|                                | Use this tag value to draw an extra Pass when rendering objects; it is valid for both the Forward and Deferred Rendering Paths. <br>URP uses this tag value as the default value when a Pass does not have a LightMode tag. | SRPDefaultUnlit      |



## 前向渲染路径

前向渲染路径是`Built-in Render Pipeline`和`URP`的默认渲染路径。是一种通用的渲染路径，限制了可以影响物体像素的实时灯光数量。每个影响物体的灯光都有一个成本。当它们超过一定数量时，灯光将以近似值影响物体（在`URP`中，所有的灯光都是按像素计算的，而且这个限制可以改变）。如果你的项目没有使用大量的实时灯光（移动或`VR`项目），那么这种渲染路径可能是一个很好的选择，因为全屏通过并不是针对场景中的每一个灯光，这对基于`Pixel`的`GPU`来说是很昂贵的。

### 渲染原理

每进行一次完整的前向渲染，需要渲染该对象的渲染图元，并计算两个缓冲区的信息（颜色缓冲区、深度缓冲区）利用深度缓冲区决定一个片元是否可见，如果可见就更新颜色缓冲区中的颜色值。

前向渲染路径的大致过程可以用伪码描述为：

```c#
Pass{
	for (each primitive in this model){
        for(each fragment covered by this primitive){
            if(failed in depth test){
                // 如果没有通过深度测试，说明该片元是不可见的
                discard;
            }else{
                // 如果该片元可见
               	// 就进行光照计算
                float4 color = Shading(materialInfo, pos, normal, lightDir, viewDir);
                //更新帧缓冲
                writeFrameBuffer(fragment, color);
            }
        }
	}
}
```

对于每个逐像素光源，都需要进行一次完整的渲染流程。如果一个物体在多个逐像素光源的影响区域内，那么该物体就需要执行多个`Pass`，每个`Pass`计算一个逐像素光源的光照结果，然后再帧缓冲中把这些光照结果混合起来得到最终的颜色值。

假设场景中有`N`个物体，每个物体受`M`个光源的影响，那么渲染整个场景一共需要`N*M`个`Pass`。如果有大量逐像素光照，那么需要执行的`Pass`数目也会很大，因此，渲染引擎通常会限制每个物体的逐像素光照的数目。



**Built-in Render Pipeline**

> 一个`Pass`不仅仅可以用来是计算逐像素光照，它也可以用来计算逐顶点等其他光照，这取决于光照计算所处的流水线阶段以及计算时使用的数学模型

在`Unity`中，前向渲染路径有3种处理光照（即照亮物体）的方式：**逐顶点处理**，**逐像素处理**，**球谐函数`(Spherical Harmonics, SH)`**处理。决定一个光源使用哪种处理模式取决于它的类型和渲染模式。

在前向渲染中，影响每个对象的一些最亮的光源以完全逐像素光照模式渲染。然后，最多 4 个点光源采用每顶点计算方式。其他光源以球谐函数 (SH) 计算，这种计算方式会快得多，但仅得到近似值。光源是否为每像素光源根据以下原则而定：

- `Render Mode`设置为 **Not Important** 的光源始终为每顶点或 SH 光源。
- 最亮的方向光始终为每像素光源。
- `Render Mode`设置为 **Important** 的光源始终为每像素光源。
- 根据上述规则得到的逐像素光源数量小于`Quality Setting`中的逐像素光源数量`(Pixel Light Count)`，会有更多的光源以逐像素的方式进行渲染。

每个对象的渲染按如下方式进行：

- 基础通道应用一个每像素方向光和所有每顶点/SH 光源。
- 其他每像素光源在额外的通道中渲染（每个光源对应一个通道）。



前向渲染有两种`Pass`，`Base Pass`和`Additional Pass`通常来说，这两种`Pass`进行的标签和渲染设置以及常规光照计算如图所示：

![image-20230317142044265](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20230317142044265.png)

- 除了设置`Pass`标签外，还使用了`#pragma multi_compile_fwdbase`这样的编译指令。虽然`pragma multi_compile_fwdbase`和`#pragma multi_compile_fwdadd`在官方文档中还没有给出相关说明，但实验表明，只有分别为`Base Pass`和`Additional Pass`使用这两个编译指令，我们才可以在相关`Pass`中得到一些正确的光照变量，例如光照衰减值等。
- `Base Pass`旁边的注释给出了`Base Pass`中支持的一些光照特性，例如在`Base Pass`中可以访问光照纹理`(lightmap)`
- `Base Pass`渲染的平行光默认支持阴影（如果开启了光源的阴影功能），而`Additional Pass`中渲染的光源在默认情况下是没有阴影效果的，即便在`Light`组件中设置了有阴影的`Shadow Type`。但是可以在`Additional Pass`中使用`#pragma multi_compile_fwdadd_fullshadows`代替`#pragma multi_compile_fwdadd`编译指令，为点光源和聚光灯开启阴影效果，但是需要`Unity`在内部使用更多的`Shader`变种。
- 环境光和自发光也是在`Base Pass`中计算的。这是因为，对于一个物体来说，环境光和自发光只希望计算一次即可，如果在`Additional Pass`中计算这两种光照，就会造成叠加多次环境光和自发光。
- 在`Additional Pass`的渲染设置中，还开启和设置了混合模式。这是因为，希望每个`Addtional Pass`可以与上一次的光照结果在帧缓存中进行叠加， 从而得到最终的有多个光照的渲染效果。如果没有开启和设置混合模式，那么`Addtional Pass`的渲染结果会覆盖掉之前的渲染结果，看起来就好像物体只受该光源的影响。通常情况下，我们选择混合模式是`Blend One One`。
- 对于前向渲染来说，一个`Unity Shader`通常会定义一个`Base Pass`(`Base Pass` 也可以定义多次，例如需要双面渲染等情况）以及一个`Additional Pass`。一个`Base Pass`金辉执行一次（定义多个`Base Pass`的情况除外）。而一个`Additional Pass`会根据影响该物体的其他逐像素光源的数目被多次调用，即每个逐像素光源会执行一次`Addtional Pass`

> 渲染路径的设置用于告诉`Unity`该`Pass`在前向渲染路径中的位置，然后底层的渲染引擎会进行相关计算并填充一些内置变量(如`_LightColor0`等)。如何利用这些内置变量进行计算，完全取决于开发者。同样也可以在`Addtional Pass`中按照逐顶点的方式进行光照计算，不进行任何逐像素光照计算。



**URP**

在**内置渲染管线**中，前向渲染根据影响对象的光源在一个或多个通道中渲染每个对象。光源本身也可以通过前向渲染进行不同的处理，具体取决于它们的设置和强度。

# 光源类型



# 光照衰减



# 阴影



# `Built-in Render Pipeline`和`URP`区别

### Lighting Mode

- `BRP`默认使用`Gamma`光照模型
- `URP`默认使用`Linear`模型

## Settings

- `BRP`

  - A: `Window -> Rendering -> Lighting`：

    设置光照映射和环境设置，查看实时和烘焙的光照图	

  - B: `Light Inspector`

    `BRP`和`URP`的`Light inspector`有显著的区别

- `URP `

  - `URP Asset Inspector`

    `URP`中的照明很大程度上依赖于在这个面板中选择的设置



