### Mod网址：

[模组检索](https://www.mcmod.cn/modlist.html)
[模组](https://www.minecraftmods.com/category/new-content/)
[CurseForge](https://www.curseforge.com/minecraft/mc-mods)

### MineCraft版本：

[苦力怕论坛](https://klpbbs.com/)

`Java Edition`

`Bedrock Edition`



### Add-on

[基岩版安装教学](https://forum.gamer.com.tw/C.php?bsn=18673&snA=185713)

[Getting Started with Add-on ...](https://learn.microsoft.com/en-us/minecraft/creator/documents/gettingstarted)

[Minecraft Add-Ons for Bedrock Versions FAQ](https://help.minecraft.net/hc/en-us/articles/4409140076813-Minecraft-Add-Ons-for-Bedrock-Versions-FAQ)


Add-on

由两部分组成：`行为包`+`资源包`

MC支持的文件格式
`.mcaddon`： 包含行为包和资源包
`.mcpack` ：仅包含行为包或资源包其中一种
`.mcworld`： 地图资源包

> 和Java版本不同，Add-on的模组非单一档案，而是以资料夹的形式存在
>
> 如果下载的档案只有资源包，功能和Java版一样，只用来修改材质或者使用光影


Addon档案下载来之后，通常会有两种情况:
- 档案名后缀是`.mcpack`或者`.mcaddon`，`.mcworld`  Android 手机可以直接通过使用其他应用打开
- 档案名后缀为`.zip` 通常使用手动安装
	- 压缩文件解压后一般会产生两个文件夹，对应的两个文件夹直接移动到MC游戏目录的指定资源保护或行为包文件夹中
	- 有可能是类似`.mcaddon.zip`这种有可能通过删除`.zip`文件来转为使用第一种方式直接打开
	- 或者可以直接修改后缀为`.mcaddon`来使用第一种方式打开


### 安装方式

**手动安装**

Add-on手动安装很简单，就是将压缩文件解压缩，将解压缩后的文件移动到指定文件夹即可。
默认安装路径: /Android/data/com.mojang.minecraftpe/games/com.mojang/
或者/Android/data/com.mojang.minecraftpe/files/games/com.mojiang/
> p.s. 安装游戏后，如果尚未创建  files文件目录有可能是空的

![[Pasted image 20221019115405.png]]

指定文件夹下 有:[resource_packs] 和 [behavior_packs]文件夹

根目录和每个minecraftWorlds存档里都会有这两个文件夹

![[Pasted image 20221019134229.png]]


![[Pasted image 20221019163503.png]]


竞品日志：
```txt
2022-10-19 20:47:23.875 1404-4127/? I/ActivityManager: START u0 {act=android.intent.action.VIEW dat=content://com.es.file.explorer.manager.files/storage/emulated/0/add_on/物品高亮显示.mcaddon typ=*/* flg=0x10000000 cmp=com.mojang.minecraftpe/.MainActivity} from uid 11813


2022-10-19 20:47:24.376 10176-10235/? D/AppsFlyer: attribute: path = /storage/emulated/0/add_on/物品高亮显示.mcaddon

2022-10-19 20:47:24.376 10176-10235/? D/AppsFlyer: attribute: link = content://com.es.file.explorer.manager.files/storage/emulated/0/add_on/%E7%89%A9%E5%93%81%E9%AB%98%E4%BA%AE%E6%98%BE%E7%A4%BA.mcaddon

```
NoxFiles
```txt
2022-10-19 20:49:05.721 1404-2472/? I/ActivityManager: START u0 {act=android.intent.action.EDIT dat=content://com.noxgroup.file.manager.utilcode.fileprovider/external_path/add_on/物品高亮显示.mcaddon typ=*/* flg=0x3 cmp=com.mojang.minecraftpe/.MainActivity} from uid 11814

```

```java
  String packageName = "com.mojang.minecraftpe";  
            String className = "com.mojang.minecraftpe.MainActivity";  
            if (FileUtils.isMcAddonFile(file)) {  
                Log.d("ZFLog", "ComnUtil.realOpenFile: 打开MC文件 ACTION_OPEN_DOCUMENT");  
  
                intent.setClassName(packageName, className);  
                intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);  //！！！！！！！！！！！！！！！
  
                // COPY  
  
                Uri uri = UriUtils.file2Uri(file);  
  
                if (uri == null) {  
                    return;  
                }  
                Log.d("ZFLog", "ComnUtil.realOpenFile: uri = " + uri);  
  
                com.blankj.utilcode.util.Utils.getApp().grantUriPermission(packageName, uri, Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);  
                intent.setDataAndType(uri,type);  
  
                if (Utils.isIntentAvailable(context, intent)) {  
//                    context.startActivity(Intent.createChooser(intent, context.getString(R.string.choice_application)));  
                    context.startActivity(intent);  
                } else {  
                    ToastUtils.showShort(R.string.toast_no_application);  
                }  
                return;
```


1. 自动安装

MC支持的文件格式
- `.mcaddon`： 包含行为包和资源包
- `.mcpack` ：仅包含行为包或资源包其中一种
- `.mcworld`： 地图资源包
使用`MC`应用直接打开对应的文件等待导入完成即可。



优化

1. 文件匹配方式最好改为仅后缀。可以二次处理文件名


Android 10+ /Android/data 访问权限

竞品：

![[Pasted image 20221021112428.png]]

通过查询文案找到指定代码：

`DocumentTreeAuthHelper`
回调方法中：
`C10587e.mo4708a`

```java

   public void mo4708a() {
  
            DocumentRWUtil.C10313b m6511i;
  
            String format;
  
            Intent intent = new Intent("android.intent.action.OPEN_DOCUMENT_TREE");
  
            boolean m11756C1 = PathUtils.m11756C1(this.f42603c);
  
            if (m11756C1 && Build.VERSION.SDK_INT < 29) {
  
                intent.putExtra("android.content.extra.SHOW_ADVANCED", true);
  
            } else {
  
                PathUtils.C9648g m11697R0 = PathUtils.m11697R0(this.f42603c);
  
                int i = this.f42604d;
  
                String str = "primary%3A";
  
                DocumentFile documentFile = null;
  
                if (i == RsDecisionListener.C9586f.f36198l) {
  
                    if (m11756C1 && Build.VERSION.SDK_INT >= 30 && m11697R0 != null) {
  
                        str = m11697R0.f36657e + "%3A";
  
                    }
  
                    format = String.format("content://com.android.externalstorage.documents/tree/%s/document/%s", str + "Android%2Fdata", str);
  
                } else if (i == RsDecisionListener.C9586f.f36199m) {
  
                    if (m11756C1 && Build.VERSION.SDK_INT >= 30 && m11697R0 != null) {
  
                        str = m11697R0.f36657e + "%3A";
  
                    }
  
                    format = String.format("content://com.android.externalstorage.documents/tree/%s/document/%s", str + "Android%2Fobb", str);
  
                } else if (i == RsDecisionListener.C9586f.f36200n) {
  
                    if (m11697R0 != null) {
  
                        String str2 = m11697R0.f36657e + "%3A";
  
                        format = String.format("content://com.android.externalstorage.documents/tree/%s/document/%s", str2, str2);
  
                    }
  
                    format = null;
  
                } else {
  
                    if (DocumentRWUtil.m6511i(this.f42603c) != null) {
  
                        String str3 = m6511i.f40929b + "%3A";
  
                        format = String.format("content://com.android.externalstorage.documents/tree/%s/document/%s", str3, str3);
  
                    }
  
                    format = null;
  
                }
  
                if (format != null) {
  
                    documentFile = DocumentFile.m44427a(App.m28805w(), Uri.parse(format));
  
                }
  
                intent.setFlags(CipherSuite.TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA256);
  
                if (Build.VERSION.SDK_INT >= 26 && documentFile != null) {
  
                    intent.putExtra("android.provider.extra.INITIAL_URI", documentFile.mo44426b());
  
                }
  
            }
  
            m4709b(intent);
  
        }
```


`RestictRUtil`
`DocumentRWUtil`

### Android 11+ 版本 `/Android/data`目录相关访问

[Google Developer 应用数据和文件-保存到共享的存储空间-文档和其他文件](https://developer.android.com/training/data-storage/shared/documents-files#document-tree-access-restrictions)

[开发者访问安卓11 /android/data的方法](https://www.zhihu.com/question/420023759)