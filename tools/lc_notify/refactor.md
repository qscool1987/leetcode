# 重构计划
1.将app.py的接口抽象为service，理由：mvc原则，app.py制作为控制器转发请求，具体执行交给具体service类

2.改为多线程处理用户数据，理由：除了目标系统的pk类型目标涉及到两个人，每个人的信息统计和计算都独立