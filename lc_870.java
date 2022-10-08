public int[] advantageCount(int[] nums1, int[] nums2) {
        int n = nums1.length;
        int[] visited = new int[n]; //记录是否被使用过
        Arrays.sort(nums1);
        int[] ans = new int[n];
        for (int i = 0; i < n; i++) {
            int target = nums2[i];
            int l = 0;
            int r = n;
            int mid;
            while (l < r) {   //二分查找获得最接近target且大于target的数
                mid = l + (r - l) / 2;
                if (nums1[mid] > target) {
                    r = mid;
                } else {
                    l = mid + 1;
                }
            }
            while (visited[l % n] == 1) {  //如果该数使用了就往后取数，如果没有了就从0位开始取最小的数
                l++;
            }
            ans[i] = nums1[l % n];
            visited[l % n] = 1;
        }
        return ans;
}
