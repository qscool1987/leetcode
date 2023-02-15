
class Solution {
public:
    /*
        定义 f(i, cnt1, is_limit, is_num) 表示构造从左往右第 i 位及其之后数位中的 1 的个数
        cnt1 表示前面填了多少个 1
        is_limit 表示当前是否受到了 n 的约束。若为真，则第 i 位填入的数字至多为 s[i]，否则可以是 9。如果在受到约束的情况下填了 s[i]，那么后续填入的数字仍会受到 n 的约束
        is_num 表示 i 前面的数位是否填了数字。若为假，则当前位可以跳过（不填数字），或者要填入的数字至少为 1；若为真，则要填入的数字可以从 0开始
    */
    int countDigitOne(int n) {
        auto s = to_string(n);
        int m = s.length(), dp[m][m];
        memset(dp, -1, sizeof(dp));
        function<int(int, int, bool)> f = [&](int i, int cnt1, bool is_limit) -> int {
            if (i == m) return cnt1;
            if (!is_limit && dp[i][cnt1] >= 0) return dp[i][cnt1];
            int res = 0;
            for (int d = 0, up = is_limit ? s[i] - '0' : 9; d <= up; ++d) // 枚举要填入的数字 d
                res += f(i + 1, cnt1 + (d == 1), is_limit && d == up);
            if (!is_limit) dp[i][cnt1] = res;
            return res;
        };
        return f(0, 0, true);
    }
};