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
 leetcode https://leetcode.cn/problems/subdomain-visit-count/
 思路：模拟题，按照题目要求做题即可
 */

class Solution {
public:
    vector<string> subdomainVisits(vector<string>& cpdomains) {
        unordered_map<string, int> mp;
        for(auto& s : cpdomains) {
            int n = s.length();
            int i = 0;
            // 1.截取频次
            while(s[i] != ' ') ++i;
            string pv = s.substr(0, i);
            int cnt = atoi(pv.c_str());
            int j = n - 1;
            // 2.由后向前遍历依次截取域名
            while(j > i) {
                while(j > i && s[j] != '.') --j;
                string d = s.substr(j+1, n-j-1);
                mp[d] += cnt;
                --j;
            }
        }
        vector<string> ans;
        for(auto& it : mp) {
            ans.push_back(to_string(it.second) + " " + it.first);
        }
        return ans;
    }
};