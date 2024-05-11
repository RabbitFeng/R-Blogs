[Python3.12 Tutorial](https://docs.python.org/zh-cn/3/tutorial/index.html)

[Python 魔法函数](https://zhuanlan.zhihu.com/p/344951719)

[Python标准库](https://docs.python.org/zh-cn/3.7/library/index.html)

[定义函数](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#defining-functions)



[Python输出颜色](https://blog.csdn.net/weixin_45694843/article/details/124222543)

[Python输出颜色](https://www.cnblogs.com/huchong/p/7516712.html)

# 1. 基础

## Python

- 解释型语言，不需要编译和链接
- 简洁易读
  - 高级数据类型允许在单一语句中表述复杂操作
  - 使用缩进而不是括号实现代码分组
  - 无需预声明变量或参数

## 传入参数

解释器可以读取命令行参数，把脚本名和其他参数转化成字符串列表存到`sys` 模块的`argv`变量里。

*`demo1-1`*

```python
import sys

if __name__ == "__main__":
    for i in range(len(sys.argv)):
        print(f"{i}:{sys.argv[i]}")

---terminal
(.venv) dongzf@DongZFdeMacBook-Pro controlflow % python3 __init__.py a b c
0:__init__.py
1:a
2:b
3:c
(.venv) dongzf@DongZFdeMacBook-Pro controlflow % 
```

**`argv`是一个列表类型，可被篡改**

*`demo1-2`*

```python
import sys

if __name__ == "__main__":
    sys.argv[0] = 'hahahahaha'
    for i in range(len(sys.argv)):
        print(f"{i}:{sys.argv[i]}")
        
---terminal
(.venv) dongzf@DongZFdeMacBook-Pro controlflow % python3 __init__.py a b c
0:hahahahaha
1:a
2:b
3:c
(.venv) dongzf@DongZFdeMacBook-Pro controlflow % 
```

`if`语句并非必要

*`demo1-3`*

```python
import sys

for i in range(len(sys.argv)):
    print(f"{i}:{sys.argv[i]}")
    
---terminal
(.venv) dongzf@DongZFdeMacBook-Pro controlflow % python3 __init__.py a b c
0:__init__.py
1:a
2:b
3:c
(.venv) dongzf@DongZFdeMacBook-Pro controlflow % 
```

## 解释器运行环境

默认情况下，Python 源码文件的编码是 UTF-8

> 这种编码支持世界上大多数语言的字符，可以用于字符串字面值、变量、函数名及注释 —— 尽管标准库只用常规的 ASCII 字符作为变量名或函数名，可移植代码都应遵守此约定。要正确显示这些字符，编辑器必须能识别 UTF-8 编码，而且必须使用支持文件中所有字符的字体。

# 2. 基础类型&数据结构

> [Python 数据结构](https://docs.python.org/zh-cn/3/tutorial/datastructures.html)

## 2.1 元组 & 序列

## 





# 标准库

[标准库 time](https://docs.python.org/zh-cn/3.7/library/time.html)



Dic迭代器：

```python
# YalogType对应的匹配字符串
MATCH_DIC = {
    YalogType.OSF: '"type":"osf","ext":{"fid":"',
    YalogType.CF: '"type":"cf","ext":{"fid":"'
}

for i, e in enumerate(MATCH_DIC.items()):
    print(f'{i}:{e}')
# 0:(<YalogType.OSF: ('osf',)>, '"type":"osf","ext":{"fid":"')
# 1:(<YalogType.CF: 2>, '"type":"cf","ext":{"fid":"')

for i, e in enumerate(MATCH_DIC):
    print(f'{i}:{e}')
# 0:YalogType.OSF
# 1:YalogType.CF

for i, e in enumerate(MATCH_DIC.keys()):
    print(f'{i}:{e}')
# 0:YalogType.OSF
# 1:YalogType.CF

print('\nenumerate(MATCH_DIC.values()) ==>')
for i, e in enumerate(MATCH_DIC.values()):
    print(f'{i}:{e}')
# 0:"type":"osf","ext":{"fid":"
# 1:"type":"cf","ext":{"fid":"

print('\nenumerate(MATCH_DIC.items()) ==>')
for k, v in MATCH_DIC.items():
    print(f'{k}:{v}')
# YalogType.OSF:"type":"osf","ext":{"fid":"
# YalogType.CF:"type":"cf","ext":{"fid":"
```

















