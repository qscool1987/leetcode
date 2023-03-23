
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

    */
    int countSpecialNumbers(int n) {
        auto s = to_string(n);
        int m = s.length(), dp[m][1 << 10]; //最多10位
        memset(dp, -1, sizeof(dp));

        /*
        返回：i开始填数字，i前面数字的集合是mask，能构造出来的特殊数字数量
        is_limit 前面0...i-1是否填了n对应位上的数，是则 当前位最大只能为s[i]，否则可到9
        is_num 0...i-1 位是否有填数字，有则为true，那么当前位可以从0开始，否则可以跳过，或者从1开始填数字
        状态：i, mask, is_limit, is_num的组合
        */
        function<int(int, int, bool, bool)> f = [&](int i, int mask, bool is_limit, bool is_num) -> int {
            if (i == m) return is_num;
            if (!is_limit && is_num && dp[i][mask] >= 0) return dp[i][mask]; //这里只是记录不受is_limit, is_num约束的i,mask的组合，
            int res = 0;
            if (!is_num) res = f(i + 1, mask, false, false); // 可以跳过当前数位
            for (int d = 1 - is_num, up = is_limit ? s[i] - '0' : 9; d <= up; ++d) // 枚举要填入的数字 d
                if ((mask >> d & 1) == 0) // d 不在 mask 中
                    res += f(i + 1, mask | (1 << d), is_limit && d == up, true);
            if (!is_limit && is_num) dp[i][mask] = res; //存储不受is_limit, is_num约束下的方案数
            return res;
        };
        return f(0, 0, true, false); 
    }
};