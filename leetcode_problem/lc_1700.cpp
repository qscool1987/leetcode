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
    思路：采用队列模拟，当队列top和sandwiches[i]相等时移动i
    复杂度O(N^2)
    特别注意退出条件，当队列遍历一遍后都没有和sandwiches[i]相等的值则退出
*/

class Solution {
public:
    int countStudents(vector<int>& students, vector<int>& sandwiches) {
        queue<int> que;
        for(auto x : students) que.push(x);
        for(int i = 0; i < sandwiches.size(); ++i) {
            int sz = que.size(); // 用来控制队列刚好遍历一遍
            while(sz > 0 && que.front() != sandwiches[i]) {
                que.push(que.front());
                que.pop();
                --sz;
            }
            if (sz <= 0) return que.size();
            que.pop();
        }
        return 0;
    }
};

int main(int argc, const char * argv[]) {
    vector<int> students = {1,1,1,0,0,1};
    vector<int> sandwiches = {1,0,0,0,1,1};
    Solution so;
    cout << so.countStudents(students, sandwiches) << endl;
    return 0;
}
