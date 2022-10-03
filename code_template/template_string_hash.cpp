//
//  main.cpp
//  cppcode
//
//  Created by 默认 on 2022/9/6.
//

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
 简介：字符串滚动hash
 参数1：待求hash的字符串
 参数2：按长度k求hash，依次求[0,k-1],[1,k],[2,k+1],...,[n-k, n-1]
 参数3：计算hash时用的质数，一般指定为31
 参数4：mod用于对hash值求模，避免整形越界
 参数5：base用于计算下一个hash值，一般的base = pow(prim, k)
 返回值：返回 n-k+1 个hash值
 */

vector<int> getKStringHash(string& s, int k, int  prim, long long mod, long long  base) {
    long long  h = 0;
    vector<int> ans(s.length() - k + 1);
    // 先计算第一个hash值
    for(int i = 0; i < k; ++i) {
        h = h * prim + s[i];
        h %= mod;
    }
    int j = 0;
    ans[j++] = h;
    for(int i = k; i < s.length(); ++i) {
        // 滚动计算hash
        // 特别注意 - 操作可能导致结果为负数，需要+mod保证取值为正
        h = (h * prim % mod - s[i-k] * base % mod + mod) % mod + s[i];
        h %= mod;
        ans[j++] = h;
    }
    return ans;
}

int main() {
    string s = "aaaaaabbbbbaaaaaaaaab";
    vector<long long> bases(11);
    int prim = 31;
    long long  mod = 1e9+7;
    long long pre = 1;
    for(int i = 1; i < 10; ++i) {
        pre *= prim;
        pre %= mod;
        bases[i] = pre;
    }
    int k = 7;
    auto ans = getKStringHash(s, k, prim, mod, bases[k]);
    for(auto x : ans) {
        cout << x << ", ";
    }
    cout << endl;
    return 0;
}
