图片内存大小

[Android中一张图片占据的内存大小是如何计算](https://juejin.cn/post/6844903693230276616)



通用计算方法：分辨率 * 像素点内存占用

默认：`ARGB_8888` 4B

资源res/drawable文件中的图片会根据设备dpi缩放



[为何大厂的图片不会OOM？](https://cloud.tencent.com/developer/article/1761686?policyId=1004)

Bitmap内存复用；**在 Android 4.4 版本之前，只能重用相同大小的 Bitmap 内存区域， 4.4 之后你可以重用任何 Bitmap 的内存区域，只要这块内存比将要分配内存的 bitmap 大就可以。**

