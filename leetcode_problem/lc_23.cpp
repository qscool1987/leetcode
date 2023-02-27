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
 leetcode https://leetcode.cn/problems/merge-k-sorted-lists/
 思路：链表的多路归并
 采用小顶堆，依次弹出，弹出堆顶元素压入下一个节点
 */

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

class Solution {
public:
    // 自定义比较函数对象
    struct Compair {
        bool operator ()(ListNode* a, ListNode* b) {
            return a->val > b->val;
        }
    };
    
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        priority_queue<ListNode*, vector<ListNode*>, Compair> pq; // 小顶堆
        ListNode nd;
        // 先将每条链表的头节点入堆
        for (int i = 0; i < lists.size(); ++i) {
            if(lists[i] != nullptr) // 注意头节点为空的情况
                pq.push(lists[i]);
        }
        ListNode* pre = &nd; // 利用头节点减少复杂判断
        while (!pq.empty()) {
            auto cur = pq.top(); // 弹出堆顶
            pq.pop();
            pre->next = cur;
            pre = pre->next;
            if (cur->next != nullptr) { // 如果下一个不为空则压入堆
                pq.push(cur->next);
            }
        }
        return nd.next;
    }
};

int main(int argc, const char * argv[]) {
    Solution so;
    
    return 0;
}