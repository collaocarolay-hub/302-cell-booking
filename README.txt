
302细胞房预约系统（云端版）

部署方式：

方案1：Render
1. 注册 https://render.com
2. 新建 Web Service
3. 上传整个文件夹
4. Build Command:
   pip install -r requirements.txt

5. Start Command:
   python app.py

部署完成后会生成公网网址。

手机打开网址即可使用。

功能：
- 云端共享数据库
- 周期预约查看
- 同设备时间冲突自动禁止
- 手机访问
- 不需要实验室电脑开机

下一步可以增加：
- 微信登录
- 管理员权限
- 培训资格控制
- 值日提醒
- 预约统计
