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
        本题关键在于求lcp
        1. lcp[n+1][n+1] n=4000，开辟1600+万个整数的数组没问题，极限为4900*4900的数组 大概110M
        2. 从后向前处理，简化逻辑
    */
    int deleteString(string& s) {
        int n = s.length();
        if (equal(s.begin() + 1, s.end(), s.begin())) // 特判全部相同的情况
            return n;
        int lcp[n + 1][n + 1]; // lcp[i][j] 表示 s[i:] 和 s[j:] 的最长公共前缀
        memset(lcp, 0, sizeof(lcp));
        for (int i = n - 1; i >= 0; --i)
            for (int j = n - 1; j > i; --j)
                if (s[i] == s[j])
                    lcp[i][j] = lcp[i + 1][j + 1] + 1;
        int f[n];
        memset(f, 0, sizeof(f));
        for (int i = n - 1; i >= 0; --i) { //从后往前计算
            for (int j = 1; i + j * 2 <= n; ++j) //枚举长度
                if (lcp[i][i + j] >= j) // 说明 s[i:i+j] == s[i+j:i+j*2]
                    f[i] = max(f[i], f[i + j]);
            ++f[i];
        }
        return f[0];
    }
};