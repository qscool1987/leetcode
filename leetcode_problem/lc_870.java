//
//  main.java
//  javacode
//
//  Created by Ruinenstadt9029 on 2022/10/8.
//
/*
链接：https://leetcode.cn/problems/advantage-shuffle/submissions/
思路：如果两个数组都是升序那么就简单了。
技巧：对nums2的下标按nums2的值进行升序排序，这样可以保证nums2中数字位置不变，得到一个nums2按升序排序的下标。
时间复杂度：稳定在 2nlogn+n
 */
import java.util.Arrays;
import java.util.Comparator;

public class AdvantageCount {
    public int[] advantageCount(int[] nums1, int[] nums2) {
        int n = nums1.length;
        Arrays.sort(nums1);
        Integer[] idx = new Integer[n];  //记录nums2的下标
        for(int i = 0;i<n;i++) idx[i] = i;
        Arrays.sort(idx, Comparator.comparingInt(i -> nums2[i]));//按照nums2升序对下标进行排序
        int l = 0,r = n-1;
        for(int x:nums1){
            if(x>nums2[idx[l]]) nums2[idx[l++]] = x;
            else nums2[idx[r--]] = x;
        }
        return nums2;
    }
}
