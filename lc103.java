package DailyCode.Dailycode11;

import com.xiaohua.TreeNode;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;

/**
 * @author xiaohua
 * @create 2022-11-02 9:20
 */
public class lc103 {


    //本题采用层序遍历的思路
    public List<List<Integer>> zigzagLevelOrder(TreeNode root) {
        List<List<Integer>> ans = new ArrayList<>();
        if(root==null){
            return ans;
        }
        //申请双端队列
        ArrayDeque<TreeNode> deque = new ArrayDeque<>();
        TreeNode cur = root;
        //先将首节点加入队列
        deque.addLast(cur);
        while (!deque.isEmpty()){
            //奇数层遍历
            int size = deque.size();
            ArrayList<Integer> list =new ArrayList<>();
            //利用队列中等size 一批一批搞
            while (size-->0){
                //奇数点 从头开始取
                TreeNode node = deque.pollFirst();
                list.add(node.val);
                //要照顾偶数层逆序所以从双端队列的最后插入
                if (node.left!=null) {
                    deque.addLast(node.left);
                }
                if (node.right!=null) {
                    deque.addLast(node.right);
                }
            }
            ans.add(list);
            size = deque.size();
            list= new ArrayList<>();
            //偶数层遍历
            while (size-->0){
                //偶数点从尾部开始取
                TreeNode node = deque.pollLast();
                list.add(node.val);
                //照顾奇数层的顺序遍历所以从头插入，不过要先加right再加
                //left 才能保证奇数层的顺序
                if (node.right!=null){
                    deque.addFirst(node.right);
                }
                if (node.left!=null){
                    deque.addFirst(node.left);
                }
            }
            //有可能出现只有奇数层的情况，那么第二个while不一定进去
            //利用size来判空
            if (list.size()!=0){
                ans.add(list);
            }
        }
        return ans;
    }

}
