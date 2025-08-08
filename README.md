# 暑期实践宣传平台

一个用于暑期实践活动宣传的推文发布网站，支持发布推文、点赞、分享等功能。

## 功能特点

- ? **推文发布**: 支持发布最多280字符的推文内容
- ? **作者署名**: 每条推文都有作者信息
- ?? **互动功能**: 支持点赞和分享推文
- ? **数据统计**: 管理后台提供推文数据统计
- ? **数据持久化**: 推文数据保存在JSON文件中
- ? **响应式设计**: 支持手机和电脑访问

## 技术栈

- **后端**: Flask (Python)
- **前端**: HTML5, CSS3, JavaScript, Bootstrap 5
- **数据存储**: JSON文件
- **图标**: Font Awesome

## 安装和运行

### 1. 激活虚拟环境

```bash
# Windows
weather_analysis_env\Scripts\activate

# 或者使用PowerShell
weather_analysis_env\Scripts\Activate.ps1
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行应用

```bash
python app.py
```

### 4. 访问网站

- 主页: http://localhost:5000
- 管理后台: http://localhost:5000/admin

## 项目结构

```
summer/
├── app.py                 # Flask应用主文件
├── requirements.txt       # Python依赖列表
├── README.md             # 项目说明文档
├── tweets_data.json      # 推文数据文件（运行后自动生成）
└── templates/            # HTML模板目录
    ├── index.html        # 主页模板
    └── admin.html        # 管理后台模板
```

## API接口

### 获取所有推文
- **GET** `/api/tweets`
- 返回所有推文的JSON数组

### 发布新推文
- **POST** `/api/tweets`
- 请求体: `{"author": "作者名", "content": "推文内容"}`

### 点赞推文
- **POST** `/api/tweets/{tweet_id}/like`
- 增加指定推文的点赞数

### 分享推文
- **POST** `/api/tweets/{tweet_id}/share`
- 增加指定推文的分享数

### 删除推文
- **DELETE** `/api/tweets/{tweet_id}`
- 删除指定的推文

## 使用说明

### 发布推文
1. 在主页填写作者姓名和推文内容
2. 推文内容最多280字符
3. 点击"发布推文"按钮

### 互动功能
- 点击??按钮为推文点赞
- 点击?按钮分享推文

### 管理功能
- 访问 `/admin` 查看所有推文和统计数据
- 可以删除不当推文
- 查看总推文数、点赞数、分享数统计

## 注意事项

- 推文数据保存在 `tweets_data.json` 文件中
- 首次运行时会自动创建数据文件
- 建议定期备份数据文件
- 生产环境部署时请修改Flask的debug模式

## 自定义配置

可以在 `app.py` 中修改以下配置：
- 服务器端口（默认5000）
- 推文字符限制（默认280）
- 数据文件路径

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！