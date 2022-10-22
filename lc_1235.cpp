class SegmentTree {
public:
    // tree的节点总数
    static const int N = 5e5;
    
    // 标记节点是否已被使用
    static const int INF = INT_MAX;
    
    struct Node {
        Node():l(INF),r(INF),val(-1){}
        int l, r;
        long long val; //区间[l,r]的最大值
    };
    Node tree[N];
    
    /*
     功能：向线段树中插入单点
     参数1：cur一般为1，表示根索引
     参数2，3：[l, r]表示该节点代表的范围
     参数4：待插入的值的索引
     参数5: 待插入的值
     返回值：无
     */
    void insert(int cur, int l, int r, int index, int val) {
        auto& nd = tree[cur];
        // nd.l == INF 动态开点
        if (nd.l == INF) {
            nd.l = l;
            nd.r = r;
        }
//        nd.val = max(nd.val, val);
        if (val > nd.val) nd.val = val;
        if (index == l && index == r) {
            return;
        }
        int m = l + (r - l) / 2;
        if (index <= m) {
            insert(cur << 1, l, m, index, val);
        } else {
            insert(cur << 1 | 1, m + 1, r, index, val);
        }
    }
    
    /*
     功能：查询[i, j]范围内的元素的最大值
     参数1：cur一般为1，表示根索引
     参数2，3：[l, r]表示该节点代表的范围
     参数4，5：[i, j]待查询的范围
     返回值：long long
     */
    long long search(int cur, int l, int r, int i, int j) {
        auto& nd = tree[cur];
        if (nd.l == INF) return 0;
        if (i <= l && j >= r) return nd.val;
        int m = l + (r - l) / 2;
        if (j <= m) {
            return search(cur << 1, l, m, i, j);
        } else if (i > m) {
            return search(cur << 1 | 1, m + 1, r, i, j);
        } else {
            return max(search(cur << 1, l, m, i, m),
                       search(cur << 1 | 1, m + 1, r, m + 1, j));
        }
    }
};
class Solution {
public:
    struct item {
        item() {}
        item(int i, int j, int k): st(i), et(j), p(k) {}
        int st;
        int et;
        int p;
    };
    // 二分查找, 招
    int upper_bound(vector<item>& arr, int j, int k) {
        int i = 0;
        int index = -1;
        while (i <= j) {
            int m = i + (j - i) / 2;
            if (arr[m].et > k) {
                j = m - 1;
            } else {
                index = m;
                i = m + 1;
            }
        }
        return index;
    }

    int jobScheduling(vector<int>& startTime, vector<int>& endTime, vector<int>& profit) {
        int n = startTime.size();
        vector<item> arr;
        for(int i = 0; i < n; ++i) {
            arr.push_back(item(startTime[i], endTime[i], profit[i]));
        }
        sort(arr.begin(), arr.end(), [](const item& a, const item& b) {
            return a.et < b.et;
        });
        // dp[i] 表示以arr[i]结尾的 最大收益
        // dp[i] = max(dp[k] + arr[i].p) (k = 0...i-1) 
        // 如果遍历，则时间复杂度为N^2, 但是dp[i] 只与 dp[0]...dp[i-1] 之间的最大值相关，所以
        // 动态维护区间[0, i-1]的最大值即可 (这是典型的线段树应用)
        vector<long long> dp(n, 0);
        SegmentTree tree;
        // cout << "fuck" << endl;
        for(int i = 0; i < arr.size(); ++i) {
            int index = upper_bound(arr, i-1, arr[i].st);
            if (index == -1) dp[i] = arr[i].p;
            else {
                dp[i] = tree.search(1, 0, n-1, 0, index) + arr[i].p;
            }
            tree.insert(1, 0, n-1, i, dp[i]);
        }
        return tree.search(1, 0, n-1, 0, n-1);
    }
};