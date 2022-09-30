//
//  main.cpp
//  cppcode
//
//  Created by 默认 on 2022/9/6.
//

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
 leetcode https://leetcode.cn/problems/zero-matrix-lcci/
 思路：用第一行和第一列分别存储需要被置零的列号和行号
 例如，matrix[i][j] = 0 则将matrx[i][0] 和matrix[0][j]置为0
 特别注意，因为第一行和第一列用于记录特殊信息，所以需要用额外的变量用来
    记录第一行和第一列是否需要被置零
 */

void setZeroes(vector<vector<int>>& matrix) {
    if (matrix.size() == 0) return;
    int m = matrix.size(), n = matrix[0].size();
    bool r_flag = false, c_flag = false; //变量用于记录第一行第一列是否要被置零
    for(int i = 0; i < m; ++i) {
        for(int j = 0; j < n; ++j) {
            if (matrix[i][j] == 0) {
                matrix[i][0] = 0;
                matrix[0][j] = 0;
                if (j == 0) c_flag = true;
                if (i == 0) r_flag = true;
            }
        }
    }
    // 特别注意，先不处理第一行第一列
    for(int i = 1; i < m; ++i) {
        if (matrix[i][0] == 0) {
            for(int j = 0;j < n; ++j) {
                matrix[i][j] = 0;
            }
        }
    }
    for(int i = 1; i < n; ++i) {
        if (matrix[0][i] == 0) {
            for(int j = 0; j < m; ++j) {
                matrix[j][i] = 0;
            }
        }
    }
    // 处理第一行和第一列
    if (r_flag) {
        for(int i = 0; i < n; ++i) {
            matrix[0][i] = 0;
        }
    }
    if (c_flag) {
        for(int i = 0; i < m; ++i) {
            matrix[i][0] = 0;
        }
    }
}

int main(int argc, const char * argv[]) {
    vector<vector<int>> matrix = {{0,1,2,0},{3,4,5,2},{1,3,1,5}};
    setZeroes(matrix);
    for(auto& v : matrix) {
        for(auto x : v) {
            cout << x << " ";
        }
        cout << endl;
    }
    return 0;
}
