# CCC Group 7 

## Project Structure

### FrontEnd (2C9G)
1. Vue
2. 数据可视化
3. 接口联调

### BackEnd（2C9G)
1. Django(8081)
2. CouchDB相关接口
3. Object Storage接口
4. 数据查询接口
5. 接口联调

### Spider （2C9G)
1. 申请Twitter Developer API
2. 定时运行脚本（30min？）
   1. 抓取数据
   2. 数据预处理
   3. 图片预处理
   4. 图片存到Object Storage（调用后端接口）
   5. twitter内容存到第一级的CouchDB （调用后端接口）

### Machine Learning (2C9G)
1. 选择模型：鉴黄、食物识别
2. 训练模型
3. 定时运行脚本（30min？）
   1. 扫描第一级CouchDB（调用后端接口）
   2. 从后端取图片
   3. 图片分类
   4. 将结果写入第二级CouchDB（调用后端接口）

### Hadoop and Operation 
1. Ansible
2. Docker运行3份CouchDB实例(8081, 8082, 8083)(2C9G + 180G)


   
   
