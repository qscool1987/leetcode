#include <iostream>
#include <vector>
#include <stack>
#include <queue>
#include <algorithm>
#include <list>
#include <map>
#include <unordered_map>
#include <set>
#include <unordered_set>
#include <cmath>
using namespace std;


//二进制拆分
void binary_split(int n, vector<int>& out) {
    int i = 0;
    while(n > 0) {
        if (n&1) out.push_back(1 << i);
        n >>= 1;
        ++i;
    }
}
/*
本模版归纳背包问题，主要是
1. 01背包
2. 完全背包
3. 多重背包
只有题目能够转化为以下问题模式就能够使用背包模版
问题：有N件物品和一个容量为V的背包。第i件物品的容量是c[i]，价值是w[i]。求解将哪些物品装入背包可使价值总和最大。

01 背包的限制：每件物品只有一件
状态定义：f[i][j] 表示考虑前 0--i 种物品所装容量为j的情况下的最大价值
转移方程：
f[i][j] = max(f[i-1][j], f[i-1][j-c[i]] + w[i])   
其中，
f[i-1][j] 为不选第二种物品
f[i-1][j-c[i]] + w[i] 选择第i中物品 
状态数量为 NV, 状态转移过程为O(1), 总时间复杂度为O(NV)
for i = 1--N:
    for j = 0--V:
        f[i][j] = max(f[i-1][j], f[i-1][j-c[i]] + w[i])
优化：
1. 因为f[i][j] 只和 f[i-1]有关，可以用滚动数组优化空间 
2. 降低维度, 用一维数组存储dp值，需要调整j的遍历顺序，需要确保 f[j] 计算依赖的 f[j-c[i]]是 i-1时计算的结果
如果不更改便利循序，那么计算f[j-c[i]]就是 i时计算的结果，这个显然不正确
for i = 1--N:
    for j = V--0: 注意便利顺序
        f[j] = max(f[j], f[j-c[i]] + w[i])


完全背包限制：每件物品有无数件
状态定义同01背包 f[i][j] 表示考虑前 0--i 种物品所装容量为j的情况下的最大价值
转移方程：
f[i][j] = max(f[i-1][j], f[i-1][j-c[i]] + w[i], f[i-1][j-2*c[i]] + 2 * w[i], ..., f[i-1][j-k*c[i]] + k * w[i])
其中 k <= V / c[i]
由于 状态计算需要O(k),总时间复杂度为O(NVK)
优化：
for i = 1--N:
    for j = 0--V:
        f[i][j]=max{f[i-1][j],f[i][j-c[i]]+w[i]}
降低维度:
for i = 1--N:
    for j = 0--V: 注意和01背包的区别，在考虑“加选一件第i种物品”这种策略时，正需要一个可能已选入第i种物品的子结果f[i][j-c[i]]，所以就可以并且必须采用j=0..V的顺序循环
        f[j] = max(f[j], f[j-c[i]] + w[i])


多重背包限制：每件物品数量有限，第i件物品数量为n[i]
思路：可以将物品i数量按2进制拆分，转换成 log(n[i]) 个数量不同的物品，其容量和价值分别为
m1*c[i], m1*w[i]
m2*c[i], m2*w[i]
...
mk*c[i], mk*w[i]
n[i] = sum(m1,m2,m3,...,mk)
然后按01背包求解
时间复杂度为 O(V*NlogN)
*/


int main()
{
    return 0;
}