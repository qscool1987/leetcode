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

class Solution {
public:
    /*
        本题关键在于：
        1.预处理，方便O(1)时间获取s[i-j]是否为回文串
        2.dp定义，f[i]表示s[0...i]中长度>=k的回文串有多少个， f[i]单调增,基于单调性，只需要找到第一个f[j]即可退出
    */
    int maxPalindromes(string s, int k) {
        int n = s.length();
        int dp[2001][2001] = {0}; //预处理dp[i][j]表示s[i...j]是否为回文串 O(n^2)
        for(int i = n-1; i >= 0; --i) {
            for(int j = i;j < n; ++j) {
                if (i == j) {
                    dp[i][j] = 1;
                } else {
                    if (j == i+1) {
                        if (s[i] == s[j]) {
                            dp[i][j] = 1;
                        }
                    } else {
                        if (s[i] == s[j]) {
                            dp[i][j] = dp[i+1][j-1];
                        }
                    }
                }
            }
        }
        vector<int> f(2001); //f[i]表示s[0...i]中长度>=k的回文串有多少个， f[i]单调增
        f[k-1] = dp[0][k-1]; //初始化
        for(int i = k; i < n; ++i) { //直接从下标k开始即可
            f[i] = dp[0][i]; //初始化
            for(int j = i-k; j >= 0; --j) { //从后向前截取1个长度>=k的串,因为f[i] 是单调递增的，所以只需要找到第一个dp[j+1][i]=1即可
                if(dp[j+1][i]) {
                    f[i] = max(f[i], f[j] + 1);
                    break;
                }
            }
            f[i] = max(f[i], f[i-1]);
        }
        return f[n-1];
    }
};