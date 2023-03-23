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
lcp 最长公共前缀
*/
vector<vector<int>>  longestPrefix(string& s) {
    int n = s.length();
    vector<vector<int>> f(n+1, vector<int>(n+1,0));
    for (int i = n - 1; i >= 0; --i) // 这个知识点如果不知道估计这题悬了
        for (int j = n - 1; j > i; --j)
            if (s[i] == s[j])
                f[i][j] = f[i + 1][j + 1] + 1;
    return f;
}

/*
lcs 最长公共子序列, 并返回子序列字符串
*/
string lcs(string& s1, string& s2) {
    int m = s1.length(), n = s2.length();
    vector<vector<int>> f(m+1, vector<int>(n+1));
    for(int i = 1; i <= m; ++i) {
        for(int j = 1; j <= n; ++j) {
            if (s1[i-1] == s2[j-1]) {
                f[i][j] = f[i-1][j-1] + 1;
            } else {
                f[i][j] = max(f[i-1][j], f[i][j-1]);
            }
        }
    }
    if (f[m][n] == 0) return "";
    string ans;
    for(int i = m, j = n; i >= 1 && j >= 1;) {
        if(s1[i-1] == s2[j-1]) {
            ans.push_back(s1[i-1]);
            --i;
            --j;
        } else {
            if (f[i][j] == f[i-1][j]) {
                --i;
            } else {
                --j;
            }
        }
    }
    reverse(ans.begin(), ans.end());
    return ans;
}

/*
最长回文子串
*/
string longestPalindrome(string& s) {
    int n = s.length();
    vector<vector<int>> f(n, vector<int>(n,0));
    for(int i = n-1; i >= 0; --i) {
        for(int j = i; j < n; ++j) {
            if (i == j || (j == i+1 && s[i] == s[j])) {
                f[i][j] = true;
                continue;
            }
            if (s[i] == s[j]) f[i][j] = f[i+1][j-1];
        }
    }
    int ans = 0;
    int l=-1, r=-1;
    for(int i = 0; i < n; ++i) {
        for(int j = i; j < n; ++j) {
            if (f[i][j] && j-i+1 > ans) {
                l = i;
                r = j;
                ans = j-i+1;
            }
        }
    }
    return s.substr(l, r-l+1);
}

/*
最长回文子序列
*/
int longestPalindromeSubseq(string s) {
    int n = s.length();
    vector<vector<int>> f(n, vector<int>(n,1));
    for(int i = n-1; i >= 0; --i) {
        for(int j = i+1; j < n; ++j) {
            if (s[i] == s[j]) {
                if (j == i+1) f[i][j] = 2;
                else f[i][j] = f[i+1][j-1] + 2;
            } else {
                f[i][j] = max(f[i+1][j], f[i][j-1]);
            }
        }
    }
    return f[0][n-1];
}


int main() {

}
