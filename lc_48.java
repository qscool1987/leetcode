package DailyCode;

/**
 * @author xiaohua
 * @create 2022-10-21 11:11
 */
public class lc_48 {

    /**
     * 思想  一圈一圈的转，不要整个一起转，会很麻烦
     * @param matrix
     */
    public void rotate(int[][] matrix) {
        //只用旋转正方形边长的一半次数就好
        for (int i = 0; i < matrix.length/2; i++) {
            process(i,matrix.length-1-i,matrix);
        }
    }
    /**
     *
     * @param left  正方形的左顶点的横坐标
     * @param right 正方形的右顶点的纵坐标
     * @param matrix 旋转的矩阵
     */
    public void process(int left ,int right ,int[][] matrix){
        //当只有一个数或者越界直接退出
        if (left>=right){
            return;
        }
        //记录左顶点，然后逆时针替换
        for (int i = 0; i < right; i++) {
            int tem = matrix[left][left+i];
            matrix[left][left+i]=matrix[right-i][left];
            matrix[right-i][left] = matrix[right][right-i];
            matrix[right][right-i]=matrix[right][left+i];
            matrix[right][left+i]=tem;

        }
    }

}
