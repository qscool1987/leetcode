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

vector<int> c;
int n;

int lowbit(int x) {
    // x 的二进制中，最低位的 1 以及后面所有 0 组成的数。
    // lowbit(0b01011000) == 0b00001000
    //          ~~~~^~~~
    // lowbit(0b01110010) == 0b00000010
    //          ~~~~~~^~
    return x & -x;
}

int getsum(int x) {  // a[1]..a[x]的和 下标从1开始
    int ans = 0;
    while (x > 0) {
        ans = ans + c[x];
        x = x - lowbit(x);
    }
    return ans;
}

void add(int x, int k) {
  while (x <= n) {  // 不能越界
    c[x] = c[x] + k;
    x = x + lowbit(x);
  }
}

//建树
void buildtree(vector<int>& nums) {
    n = nums.size() + 1;
    c.resize(n, 0);
    for(int i = 0; i < nums.size(); ++i) {
        add(i+1, nums[i]);
    }
}