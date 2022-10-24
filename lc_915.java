package DailyCode;

/**
 * 测评链接：https://leetcode.cn/problems/partition-array-into-disjoint-intervals/
 * @author xiaohua
 * @create 2022-10-24 1:22
 */
public class lc_915 {

    /**
     *
     * 两次遍历：记录以i位置为划分的left最大值位置，记录以i位置为划分的right最小值位置
     * 题目不是要求左边的最大值要小于等于right的最小值嘛？
     * 所以 第一次 左边的最大值小于等于右边的最小值就是答案，但是要加一返回；
     * 最后return 返回是为了防止遍历结束，仍未找到，那么答案一定在N（数组长度）-2（数组的位置）处；
     */
    public int partitionDisjoint1(int[] nums) {

        int N = nums.length;
        int[] leftMax = new int[N];
        int[] rightMin = new int[N];

        int max = Integer.MIN_VALUE;
        for (int i = 0; i < N; i++) {
            if (max<nums[i]){
                leftMax[i] = nums[i];
                max = nums[i];
            }else {
                leftMax[i]=max;
            }
        }
        int min = Integer.MAX_VALUE;
        for (int i = N-1; i >=0 ; i--) {
            if (nums[i]<min){
                rightMin[i] = nums[i];
                min = nums[i];
            }else {
                rightMin[i] = min;
            }
        }
        for (int i = 0; i < N; i++) {
            if (leftMax[i]<=rightMin[i]){
                return i+1;
            }
        }
        return N-2;

    }

    /**
     *
     * 参考评论区fibonacciWH题解
     * 题目不是说，要左边的区域小于等于右边的区域嘛？而且要left尽量小
     * 那么 题目就可以简化为 左边的区域小于右边的区域，等于的情况要舍弃（根据题目规则）
     * 考虑，以i位置为划分位置，如果左边区域的大于i位置的元素，那么符合条件
     * leftmax更新为当前区域的最大值，每次以i为right区域的最小值
     * 一遍模拟后，即可找出   当前ans位置包括ans位置的元素的最大值都是小于right区域的最小值
     *
     */
    public int partitionDisjoint(int[] nums) {

        int max = nums[0];
        int leftMax = nums[0];
        int ans = 0;
        for (int i = 0; i < nums.length; i++) {
            max = Math.max(max,nums[i]);
            if (nums[i]<leftMax){
                leftMax = max;
                ans = i;
            }
        }
        return ans+1;
    }

}
