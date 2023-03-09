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

*/

int main() {

}
