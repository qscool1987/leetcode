package DailyCode;


/**
 *
 * 测评链接：https://leetcode.cn/problems/number-of-students-unable-to-eat-lunch/
 * @author xiaohua
 * @create 2022-10-19 23:57
 */
public class lc_1700 {


    /**
     *
     * @param students 学生数组
     * @param sandwiches 三明治数组
     * @return 没有午餐的学生
     *
     *
     * 输入：students = [1,1,1,0,0,1], sandwiches = [1,0,0,0,1,1]
     * 输出：3
     *
     * 本题说了，如果不喜欢当前三明治，让后排，所以我们完全可以利用一个变量记录
     * 学生的数量
     * 因此 喜欢1号三明治的学生 定为s1 喜欢零号  定为 s0
     * 然后开始判断当前的三明治有没有人要，例如 sandwiches 索引在0位置
     * 正好学生索引0位置喜欢，那么直接拿走，如果说
     * 索引0位置的学生不喜欢，往后排，就判断下一个
     * 这种情况如果还是1则继续重复上述过程，要是0呢，那么就拿走
     * 所以if   （else if  ） else 结构第一个可以判当前是不是s0 第二个可以判当前是不是
     * s1，另外要满足，s0 学生要的时候  s0学生是存在的，s1同理
     * 如果上面判断都不满足，说明 当前为这个午餐所有人都不喜欢
     * 那么 s0或者s1有一个必为零，
     * 剩下的都是没有饭的学生，为了省掉判断，采用了s0+s1 进行返回
     */
    public int countStudents(int[] students, int[] sandwiches) {
        int s1 = 0;
        for(int i = 0;i<students.length;i++){
            s1+=students[i];
        }
        int s0 = students.length-s1;
        for(int i = 0;i<students.length;i++){
            if(sandwiches[i]==0&&s0>0){
                s0--;
            }else if(sandwiches[i]==1&&s1>0){
                s1--;
            }else{
                break;
            }
        }
        return s1+s0;

    }

}
