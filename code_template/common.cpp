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
质数筛选
先预处理，后续直接判断 x 是否为质数
*/

vector<bool> prim(1000010, true);
const int N = 1000000;
int init = [](int n){
    for(int i = 2; i <= n; i++) {
        if(prim[i]) {
            for(int j = i * 2; j <= n; j += i) prim[j] = false;
        }
    }
    return 0;
}(N);


/*
质因素分解
将整数 num 分解质因素
*/
void div_num_into_prime(int num, vector<int>& out) {
    for (int i = 2; i <= num / i; i++) {
        while (num != i) {
            if (num % i == 0) {
                out.push_back(i);
                num = num / i;
            } else break;
        }
    }
    if (num != 1) {
        out.push_back(num);
    }
}

/*
数组的排列
1.数组无重复元素
2.数组有重复元素
*/
void arr_permutation1(vector<int>& nums, int cur, vector<vector<int>>& out) {
    if (cur == nums.size()) {
        out.push_back(nums);
        return;
    }
    for(int i = cur; i < nums.size(); ++i) {
        swap(nums[i], nums[cur]);
        arr_permutation1(nums, cur+1, out);
        swap(nums[i], nums[cur]);
    }
}


/*要求nums为有序数组*/
void arr_permutation2(vector<int>& nums, vector<bool>& use, vector<int>& tmp, vector<vector<int>>& out) {
    if (tmp.size() == nums.size()) {
        out.push_back(tmp);
        return;
    }
    for(int i = 0; i < nums.size(); ++i) {
        if (use[i] || (i > 0 && nums[i-1] == nums[i] && !use[i-1])) continue;
        use[i] = true;
        tmp.push_back(nums[i]);
        arr_permutation2(nums, use, tmp, out);
        tmp.pop_back();
        use[i] = false;
    }
}

/*
数组的子集 包含重复元素
需要先对nums进行排序
*/
void arrSubSet(vector<int>& nums, int start, vector<int>& temp, vector<vector<int>>& ans) {
    ans.push_back(temp);
    for (int i = start; i < nums.size(); i++) {//注意i的起始值
        //和上个数字相等就跳过
        if (i > start && nums[i] == nums[i - 1]) { // 比如1 2 2 4  当i = 2时, 后面的组合已经包含在了 i=1的结果里 2 ,2 4 包含在了2, 2 2, 2 4, 2 2 4中
            continue;
        }
        temp.push_back(nums[i]);
        arrSubSet(nums, i + 1, temp, ans);
        temp.pop_back();
    }
}

vector<vector<int>> arrSubSet2(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    int n = nums.size();
    vector<vector<int>> ans;
    for (int mask = 0; mask < (1 << n); ++mask) {
        vector<int> t;
        bool flag = true;
        for (int i = 0; i < n; ++i) {
            if (mask & (1 << i)) { //使用了第i个元素 1 2 2 3  i = 2的组合会包含在 i=1的组合中
                if (i > 0 && (mask >> (i - 1) & 1) == 0 && nums[i] == nums[i - 1]) {
                    flag = false;
                    break;
                }
                t.push_back(nums[i]);
            }
        }
        if (flag) {
            ans.emplace_back(move(t));
        }
    }
    return ans;
}

/*
字符串相乘 leetcode-43
string s1 * s2
*/
string big_integer_mul(string& s1, string& s2) {
    if (s1 == "0" || s2 == "0") return "0";
    vector<int> f(s1.length() + s2.length(), 0);
    for(int i = s1.length()-1; i >= 0; --i) {
        for(int j = s2.length()-1; j >= 0; --j) {
            f[i+j+1] += (s1[i]-'0') * (s2[j] - '0');
        }
    }
    int c = 0;
    for(int i = f.size()-1; i >= 0; --i) {
        int t = f[i] + c;
        f[i] = t % 10;
        c = t / 10;
    }
    string ans;
    for(int i = 0; i < f.size(); ++i) {
        if (ans.empty() && f[i] == 0) continue;
        ans.push_back(f[i] + '0');
    }
    return ans;
}

/*
最大子数组和,并返回起始和终止位置下标
*/
int maxSubArray(vector<int>& nums) {
    int pre = nums[0];
    int ans = nums[0];
    int _s = 0, _e = 0;
    int s = 0, e = 0;
    for(int i = 1; i < nums.size(); ++i) {
        if (pre >= 0) {
            pre += nums[i];
            e++;
        } else {
            pre = nums[i];
            s = i;
            e = i;
        }
        if (ans < pre) {
            ans = pre;
            _s = s;
            _e = e;
        }
    }
    return ans;
}

/*
前缀和 f[i+1] - f[j] [j, i]之间的和
后缀和 f[i] - f[j+1] [i, j]之间的和
*/

void preArray(vector<int>& nums, vector<int>& pre) {
    pre.resize(nums.size() + 1);
    for(int i = 1; i <= nums.size(); ++i) {
        pre[i] = pre[i-1] + nums[i-1];
    }
}

void postArray(vector<int>& nums, vector<int>& post) {
    post.resize(nums.size() + 1);
    for(int i = nums.size()-1; i >= 0; --i) {
        post[i] += post[i+1] + nums[i];
    }
}

/*
最大递增子序列 nums[i] < nums[i+1]
如果要求 nums[i] <= nums[i+1] 则将 lower_bound 改成 upper_bound
*/
int maxSubArraySet(vector<int>& nums) {
    int n = nums.size();
    if (n <= 1) return n;
    vector<int> ans;
    int sz = 0;
    for(int i = 0; i < n; ++i) {
        if (ans.empty() || ans.back() < nums[i]) { // ans.back() <= nums[i]
            ans.push_back(nums[i]);
            ++sz;
        } else {
            // 
            int idx = lower_bound(ans.begin(), ans.begin() + sz, nums[i]) - ans.begin(); //lower_bound -> upper_bound
            ans[idx] = nums[i];
        }
    }
    return sz;
}

/*
删除倒数第k个节点
假如节点个数为n
1 2 3 4 5
先让一个指针走k步
然后第二个指针从开始和第一个指针一起走
第一个指针走到结尾后，第二个指针指节点就是要删除的节点
*/


/*
前缀比较优化
可以用一个diff变量来记录前缀整体的不同
if p not in mp2:
    ++diff
mp2[p] = cnt
if mp2[p] == mp1[p]:
    --diff
if diff == 0: 说明此时前缀整体相同
*/

/*
Problem Statement
You are given an integer 
K greater than or equal to 
2.
Find the minimum positive integer 
N such that 
N! is a multiple of 
K.

Here, 
N! denotes the factorial of 
N. Under the Constraints of this problem, we can prove that such an 
N always exists.

Constraints
2≤K≤10 
12
 
K is an integer.
*/
long long findMinN(long long k) {
	long long p,a,n,x,ans=1;
	for(p=2;(p*p)<=k;p++){
		a=0;
		while(k%p==0)k /= p, a++;     //质因数分解， 质数为p，个数为a
		n=0;
		while(a > 0){    //判断n要到多少才能满足n!中有a个p
			n += p;
			x = n;
			while(x % p == 0) {
                x /= p;
                a--;
            }
		}
		ans=max(ans,n);
	}
	ans=max(ans,k);
	return ans;
}



int main() {
    
    return 0;
}