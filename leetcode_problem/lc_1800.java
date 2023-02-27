package DailyCode;


/**
 * @author xiaohua
 * @create 2022-09-30 23:15
 */
public class lc_1800 {

    //子数组要求连续
    //子序列子串不要求连续
    public int maxAscendingSum(int[] nums) {

        if (nums == null || nums.length < 1) {
            return 0;
        }
//        一次遍历，并判断是否升序，每一组升序子数组加一块
//        然后与初始的答案比较，对于这种题别忘了，最后一种情况可能会漏掉
//        在return处补一个 比较
        int ans = 0;
        int count = nums[0];
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] > nums[i - 1]) {
                count += nums[i];
            } else {
                ans = Math.max(ans, count);
                count = nums[i];
            }
        }
        return Math.max(ans,count);
    }

}
