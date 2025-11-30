对于收集到的trace文件(**.html)，可以通过perfetto页面打开；直接打开可能回因为日志文件过大导致页面崩溃；文件导入到perfetto页面后会生成一系列数据表，可以通过PerfettoSQL跟踪分析；

Perfetto 的设计初衷是作为 Android 操作系统和 Chrome 浏览器的默认追踪系统。因此，Perfetto 官方支持以下数据的收集、分析和可视化：

- **Android 上的系统跟踪功能**可用于调试 Android 平台和 Android 应用的功能和性能问题，并找出其根本原因。Perfetto 适用于调试启动缓慢、丢帧（卡顿）、动画故障、内存不足导致的应用终止、应用无响应 (ANR) 以及常见的错误行为等。
- **Android 上的 Java 堆转储和本机堆配置文件**分别用于在 Android 平台和 Android 应用中调试和查找导致 Java/Kotlin 代码和 C++ 代码中内存使用量过高的根本原因。
- **Android 上的 Callstack 采样配置文件**用于调试 Android 平台和 Android 应用中 C++/Java/Kotlin 代码的高 CPU 使用率并找出根本原因。
- **Chrome 浏览器可追溯到**浏览器、V8、Blink 以及高级用例中的网站本身的调试和根本原因问题。



- Tracing(跟踪)
  - 涉及收集有关系统执行的极其详细的数据；跟踪信息包含足够的细节，足以完整地重建事件的时间线；
- Logging 日志记录
  - 和Logging相比，Tracing更像是一种结构化的记录
- Metrics 指标
  - 示例：`CPU使用率`, `内存使用率`, `网络带宽`。相比于指标，Tracing在生产环境中是比较重量级；
- Profiling 分析
  - 涉及对程序对资源的使用情况进行采样。单个连续的记录会话；内存分析用于了解程序的哪些部分在堆上分配内存；常见的分析类型：`CPU分析`和`内存分析`





# 使用方式

## 1. 将trace文件导入perfetto Trace Viewer页面

Perfetto 所有轨迹分析的核心都是**轨迹处理器 (Trace Processor)**，这是一个 C++ 库，可以解决这种复杂性。它承担了解析、构建和查询轨迹数据的重任。

跟踪处理器负责：

- **解析跟踪**：提取各种跟踪格式，包括 Perfetto、ftrace 和 Chrome JSON。
- **结构化数据**：将原始跟踪数据转化为结构化格式。
- **公开查询接口**：提供PerfettoSQL接口用于查询结构化数据。
- **捆绑标准库**：包括用于开箱即用分析的 PerfettoSQL 标准库。

## 2. 从轨迹可视化UI界面 + PerfettoSQL来跟踪分析

**跟踪处理器抽象出底层跟踪格式并通过PerfettoSQL**公开数据，PerfettoSQL 是一种 SQL 方言，允许您像查询数据库一样查询跟踪的内容。

[Perfetto SQL](https://perfetto.dev/docs/analysis/perfetto-sql-getting-started)

[PerfettoSQL Prelude 表结构](https://perfetto.dev/docs/analysis/sql-tables)



> 这块文档更新了。。。之前的建表语句找不到了

![b27324b7bc8d50502a8955e74a6c23b1](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/b27324b7bc8d50502a8955e74a6c23b1.png)

建表

```sql
DROP VIEW IF EXISTS slice_with_utid;
CREATE VIEW slice_with_utid AS
SELECT
  ts,
  dur,
  slice.name as slice_name,
  slice.id as slice_id, utid,
  thread.name as thread_name
FROM slice
JOIN thread_track ON thread_track.id = slice.track_id
JOIN thread USING (utid);

DROP TABLE IF EXISTS slice_thread_state_breakdown;
CREATE VIRTUAL TABLE slice_thread_state_breakdown
USING SPAN_LEFT_JOIN(
  slice_with_utid PARTITIONED utid,
  thread_state PARTITIONED utid
);
```

![image-20250703120716383](https://raw.githubusercontent.com/RabbitFeng/TyporaPic/master/images/image-20250703120716383.png)