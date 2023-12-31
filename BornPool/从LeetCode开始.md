# 动态规划算法

## 知识点吧



###  [70. 爬楼梯](https://leetcode.cn/problems/climbing-stairs/description/?envType=study-plan-v2&envId=dynamic-programming)  [^Easy]

> 假设你正在爬楼梯。需要 `n` 阶你才能到达楼顶。
>
> 每次你可以爬 `1` 或 `2` 个台阶。你有多少种不同的方法可以爬到楼顶呢？
>
> **示例 1：**
>
> ```
> 输入：n = 2
> 输出：2
> 解释：有两种方法可以爬到楼顶。
> 1. 1 阶 + 1 阶
> 2. 2 阶
> ```
>
> **示例 2：**
>
> ```
> 输入：n = 3
> 输出：3
> 解释：有三种方法可以爬到楼顶。
> 1. 1 阶 + 1 阶 + 1 阶
> 2. 1 阶 + 2 阶
> 3. 2 阶 + 1 阶
> ```
>
> **提示：**
>
> - `1 <= n <= 45`

这是一道比较经典的动态规划题目。

#### 方法1：动态规划

$ f(x)$ 表示爬到第$x$级台阶的方案数。考虑最后一步爬到第$x$级台阶是爬了一级台阶或者两级台阶，所以可以得到一般情况下的状态转移方程：

​		$$ f(x) = f(x-1) + f(x-2):for (x > 2)$$

然后去讨论它的边界条件。从第0级开始，爬到第1级共有1种方案，爬到第2级共有2种方案。爬到第3级共有3种方案... 枚举以验证状态转移方程的正确性。

 ```java
 class Solution {
     public int climbStairs(int n) {
         // 这里插入一个额外的约定，就是从第0阶开始爬，爬到第0阶的方案数约定为1。这样能不必考虑状态转移方程在有效数字中的边界条件。写出更加简洁的代码
         int[] temp = new int[]{0,0,1};
         for(int i = 1; i <= n; i++){
             temp[0] = temp[1];
             temp[1] = temp[2];
             temp[2] = temp[0] + temp[1];
         }
         return temp[2];
     }
 }
 ```

- 时间复杂度: $O(n)$
- 空间复杂度: $O(1)$

#### 方法2：矩阵快速幂

#### 方法3：通项公式

### [746. 使用最小花费爬楼梯](https://leetcode.cn/problems/min-cost-climbing-stairs/)  [^Easy]

>给你一个整数数组 `cost` ，其中 `cost[i]` 是从楼梯第 `i` 个台阶向上爬需要支付的费用。一旦你支付此费用，即可选择向上爬一个或者两个台阶。
>
>你可以选择从下标为 `0` 或下标为 `1` 的台阶开始爬楼梯。
>
>请你计算并返回达到楼梯顶部的最低花费。
>
> 
>
>**示例 1：**
>
>```
>输入：cost = [10,15,20]
>输出：15
>解释：你将从下标为 1 的台阶开始。
>- 支付 15 ，向上爬两个台阶，到达楼梯顶部。
>总花费为 15 。
>```
>
>**示例 2：**
>
>```
>输入：cost = [1,100,1,1,1,100,1,1,100,1]
>输出：6
>解释：你将从下标为 0 的台阶开始。
>- 支付 1 ，向上爬两个台阶，到达下标为 2 的台阶。
>- 支付 1 ，向上爬两个台阶，到达下标为 4 的台阶。
>- 支付 1 ，向上爬两个台阶，到达下标为 6 的台阶。
>- 支付 1 ，向上爬一个台阶，到达下标为 7 的台阶。
>- 支付 1 ，向上爬两个台阶，到达下标为 9 的台阶。
>- 支付 1 ，向上爬一个台阶，到达楼梯顶部。
>总花费为 6 。
>```
>
>**提示：**
>
>- `2 <= cost.length <= 1000`
>- `0 <= cost[i] <= 999`

和 `70.`类似的解法。约定$f(x)$是爬到第$x$级楼梯的最小花费。状态转移方程：

​				$$f(x) = min(f(x-1),f(x-2)) + cost[x];x>= 2 \\ f(x) = cost[x]; x = 0 , 1 $$

```java
class Solution {
    public int minCostClimbingStairs(int[] cost) {
        int a = cost[0]; // x - 2 最小花费. 从0开始
        int b = cost[1]; // x - 1 最小花费. 从1开始
        int t = 0; // x 层最小花费
        for(int i = 2; i < cost.length; i++){
            t = Math.min(a,b) + cost[i];
            a = b;
            b = t;
        }
        return Math.min(a,b);
    }
}
```

### [198. 打家劫舍](https://leetcode.cn/problems/house-robber/)

> 你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，**如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警**。
>
> 给定一个代表每个房屋存放金额的非负整数数组，计算你 **不触动警报装置的情况下** ，一夜之内能够偷窃到的最高金额。
>
>  
>
> **示例 1：**
>
> ```
> 输入：[1,2,3,1]
> 输出：4
> 解释：偷窃 1 号房屋 (金额 = 1) ，然后偷窃 3 号房屋 (金额 = 3)。
>      偷窃到的最高金额 = 1 + 3 = 4 。
> ```
>
> **示例 2：**
>
> ```
> 输入：[2,7,9,3,1]
> 输出：12
> 解释：偷窃 1 号房屋 (金额 = 2), 偷窃 3 号房屋 (金额 = 9)，接着偷窃 5 号房屋 (金额 = 1)。
>      偷窃到的最高金额 = 2 + 9 + 1 = 12 。
> ```
>
>  
>
> **提示：**
>
> - `1 <= nums.length <= 100`
> - `0 <= nums[i] <= 400`

约定$f(a,b)$表示偷窃区间$[a , b]$ 房间的最高金额，其中，$ 0 <= a <= b $。f(n)表示偷第`n`间房间所得

假设我们始终从房间下标对应的较小值开始偷，那么对于 $f(0, n)$来说，直观上，我们得到状态转移方程

$$ f(a,b) = max(f(a+1,b), f(a+2, b) + f(a,a)); $$

考虑边界条件，

- 当 $b-a = 0$时，$f(a,b) = f(a)$
- 当$b-a = 1$时，$f(a,b)= max(f(a), f(b))$
- 当$b-a >1$时，$f(a,b) = max(f(a + 1, b), f(a+2,b) + f(a))$

那么归纳一下

$$f(0,5) = max(f(1,5), f(2,5) + f(0)) \\ f(1,5) = max(f(2,5), f(3,5) + f(1)) \\ f(2,5) = max(f(3,5) ,f(4,5) + f(2))\\ f(3,5) = max(f(4,5), f(5,5) + f(3))\\ f(4,5) = max(f(4), f(5))$$

优化一下

约定$f(n)$是偷前 `n+1`房间的最高金额，

f(n) =max (f(n - 1) , f(n -2) + r[n]).

边界

n = 0 时，result = 0

n = 1 时，result = r[0]
