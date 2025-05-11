# Flask web应用程序，使用使用SSM框架Flask+Mybatis。

智能教学系统，调用dify的工作流实现教师出作业和批改作业

作业只涉及编程题

实现多个教师用户登录，存储教师的出题记录和批改记录


管理端：1.添加、修改学生、老师信息

2.添加、修改课程

教师端：1.出题情况概览；

2.查看教授课程，每个课程的出题记录；（未给出界面示例和实现思路）

3.查看每个课程选修的学生，每个学生的批改记录。（未给出界面示例和实现思路）

4.出题（以下为出题流程示例）

学生端：1.查看历史和当前作业，进行答题、批改。查看个人批改记录（只有一个界面，以下为界面示例）

## 教师端

首页实现出题情况概览（示例界面展示不具体，具体。。。

![image-20250506193919644](https://raw.githubusercontent.com/zus12873/typora_images/main/image-20250506193919644.png)

1. 作业设置。根据科目章节题型生成作业

题型默认编程题，不能选择


![image-20250506193928363](https://raw.githubusercontent.com/zus12873/typora_images/main/image-20250506193928363.png)

![image-20250506193937195](https://raw.githubusercontent.com/zus12873/typora_images/main/image-20250506193937195.png)

下拉框查看该老师教授课程

![截屏2025-04-16 下午3.04.49](https://raw.githubusercontent.com/zus12873/typora_images/main/clip_image008.jpg)

2. 作业题目筛选。对生成的习题进行题目筛选和题目修改，生成完整题目

![截屏2025-04-18 下午7.54.24](https://raw.githubusercontent.com/zus12873/typora_images/main/clip_image010.jpg)单次作业有多个题，可能要改表

 

![image-20250506193959349](https://raw.githubusercontent.com/zus12873/typora_images/main/image-20250506193959349.png)

![截屏2025-04-16 下午3.05.50](https://raw.githubusercontent.com/zus12873/typora_images/main/clip_image014.jpg)

3. 题目评判标准设置。设置评判标准，发布作业。

![image-20250506194020719](https://raw.githubusercontent.com/zus12873/typora_images/main/image-20250506194020719.png)

## 学生端

![image-20250506194029785](https://raw.githubusercontent.com/zus12873/typora_images/main/image-20250506194029785.png)

“左侧”是历史和当前作业。

“顶部数字123”代表一次作业里面有几个题，动态显示，每次作业题目数量不一样，学生看到题目数量随老师出题数量变化。

“1.题干。。。。”代表题目。

学生在“答题区”输入代码，也可以从IDE复制粘贴代码

点击“提交/完成”按钮，对单个题目进行保存和批改。点击按钮后获取题干的信息，学生答案，这道题的评分标准。将这三个参数给dify工作流。返回批改结果。

将批改结果显示于此。

 