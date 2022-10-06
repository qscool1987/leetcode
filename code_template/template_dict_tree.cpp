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
    字典树
    1.一般的，字符串数组，涉及前后缀查询的问题适合用字典树
    2.一般的，题目要求按字典序排序适合用字典树
    3.特殊的，可以按正整数二进制位构建字典树，解决位操作相关问题
*/

struct WordTree {
    WordTree(){};
    unordered_map<char, WordTree*> childs;
    string name;
};

// 全局变量，字典数根节点
WordTree tree; 

// 插入单词
void addWord(string& s) {
    WordTree* p = &tree;
    int i = 0; 
    while(i < s.length()) {
        if (p->childs.find(s[i]) == p->childs.end()) {
            p->childs[s[i]] = new WordTree();
        }
        p = p->childs[s[i]];
        ++i;
    }
    p->name = s;
}

// 查找单词
bool search(string& s) {
    WordTree* p = &tree;
    int i = 0; 
    while(i < s.length()) {
        if (p->childs.find(s[i]) == p->childs.end()) {
            return false;
        }
        p = p->childs[s[i]];
        ++i;
    }
    return true;
}

