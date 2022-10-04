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
    该题解法来源于 @灵茶山艾府 leetcode 个人主页 https://leetcode.cn/u/endlesscheng/
    定义 f[i]f[i] 表示删除后缀 s[i:]s[i:] 所需的最大操作数。
    根据题意，我们可以枚举删除字母的长度 jj，如果 s[i:i+j] = s[i+j:i+2j]s[i:i+j]=s[i+j:i+2j]，那么可以删除，
    此时有转移 f[i] = f[i+j] + 1f[i]=f[i+j]+1。如果不存在两个子串相等的情况，则 f[i] = 1f[i]=1。f[i]f[i] 取所有情况的最大值。
    倒着计算 f[i]f[i]，答案为 f[0]f[0]。
    最后，我们需要快速判断两个子串是否相同。这可以用 O(n^2)的 DP 预处理出来，具体见代码。
    来源 作者：endlesscheng
    链接：https://leetcode.cn/problems/maximum-deletions-on-a-string/solution/xian-xing-dppythonjavacgo-by-endlesschen-gpx9/
    来源：力扣（LeetCode）
    著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
*/

class Solution {
public:

    int deleteString(string s) {
        int n = s.length();
        if (equal(s.begin() + 1, s.end(), s.begin())) // 特判全部相同的情况
            return n;
        int lcp[n + 1][n + 1]; // lcp[i][j] 表示 s[i:] 和 s[j:] 的最长公共前缀
        memset(lcp, 0, sizeof(lcp));
        for (int i = n - 1; i >= 0; --i) // 这个知识点如果不知道估计这题悬了
            for (int j = n - 1; j > i; --j)
                if (s[i] == s[j])
                    lcp[i][j] = lcp[i + 1][j + 1] + 1;
        int f[n];
        memset(f, 0, sizeof(f));
        for (int i = n - 1; i >= 0; --i) {
            for (int j = 1; i + j * 2 <= n; ++j) // 长度为1 ... (n-i)/2
                if (lcp[i][i + j] >= j) // 说明 s[i:i+j] == s[i+j:i+j*2]
                    f[i] = max(f[i], f[i + j]);
            ++f[i];
        }
        return f[0];
    }
};

int main(int argc, const char * argv[]) {
    string s = "aaaaaab";
    Solution so;
    cout << so.deleteString(s) << endl;
    return 0;
}