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

struct Tire {
    Tire():val(0) {
        childs.resize(2);
    }
    vector<Tire*> childs;
    int val;
};

int N = 20; //二进制位的数量
Tire root;

void addNumber(int x) {
    Tire* cur = &root;
    for(int i = N; i >= 0; --i) {
        int t = ((x >> i) & 1);
        if (cur->childs[t] == nullptr) {
            cur->childs[t] = new Tire();
        }
        cur = cur->childs[t];
    }
    cur->val = x;
}

bool searchNumber(int x) {
    Tire* cur = &root;
    for(int i = N; i >= 0; --i) {
        int t = ((x >> i) & 1);
        if (cur->childs[t] == nullptr) {
            return false;
        }
        cur = cur->childs[t];
    }
    return cur->val == x;
}

