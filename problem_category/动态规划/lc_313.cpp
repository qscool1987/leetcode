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

/*
超级丑数 是一个正整数，并满足其所有质因数都出现在质数数组 primes 中。
给你一个整数 n 和一个整数数组 primes ，返回第 n 个 超级丑数 。
题目数据保证第 n 个 超级丑数 在 32-bit 带符号整数范围内。

输入：n = 12, primes = [2,7,13,19]
输出：32 
解释：给定长度为 4 的质数数组 primes = [2,7,13,19]，前 12 个超级丑数序列为：[1,2,4,7,8,13,14,16,19,26,28,32] 。

输入：n = 1, primes = [2,3,5]
输出：1
解释：1 不含质因数，因此它的所有质因数都在质数数组 primes = [2,3,5] 中。
*/

class Solution {
public:
    int nthSuperUglyNumber(int n, vector<int>& primes) {
        int m = primes.size();
        vector<int> f(m, 1);
        vector<long long> dp(n+1);
        dp[1] = 1;
        for(int i = 2; i <= n; ++i) {
            long long min_v = INT_MAX;
            for(int j = 0; j < m; ++j) { //寻找下一个丑数
                if (min_v > dp[f[j]] * primes[j]) {
                    min_v = dp[f[j]] * primes[j];
                }
            }
            dp[i] = min_v;
            for(int j = 0; j < m; ++j) { //将对应位置前移，准备后续的查找，假如不迁移，将会导致找的丑数比之前找到的还要小
                if (dp[f[j]] * primes[j] == min_v) ++f[j];
            }
            
        }
        return  dp[n];
        
    }
};