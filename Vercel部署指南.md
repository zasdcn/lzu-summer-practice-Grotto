# Vercel 部署详细指南

本指南将详细介绍如何将兰州大学暑期实践宣传平台部署到 Vercel 上。

## ? 前置准备

### 1. 账号准备
- GitHub 账号（用于代码托管）
- Vercel 账号（可以用 GitHub 账号直接登录）

### 2. 本地环境
- Git 已安装
- 项目代码已准备完毕

## ? 详细部署步骤

### 步骤 1：准备项目文件

项目已经包含了以下必要的配置文件：

1. **`vercel.json`** - Vercel 部署配置
2. **`requirements.txt`** - Python 依赖包
3. **`api/index.py`** - Vercel 专用的 Flask 应用入口
4. **`.gitignore`** - Git 忽略文件配置

### 步骤 2：创建 GitHub 仓库

1. **登录 GitHub**
   - 访问 [github.com](https://github.com)
   - 使用您的账号登录

2. **创建新仓库**
   - 点击右上角的 "+" 按钮
   - 选择 "New repository"
   - 仓库名称：`lzu-summer-practice`（或您喜欢的名称）
   - 设置为 Public（公开）
   - 不要勾选 "Initialize this repository with a README"
   - 点击 "Create repository"

### 步骤 3：上传代码到 GitHub

在项目根目录打开命令行，执行以下命令：

```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit: 兰州大学暑期实践宣传平台"

# 添加远程仓库（替换为您的 GitHub 用户名和仓库名）
git remote add origin https://github.com/zasdcn/lzu-summer-practice.git

# 推送代码到 GitHub
git branch -M main
git push -u origin main
```

### 步骤 4：连接 Vercel

1. **访问 Vercel**
   - 打开 [vercel.com](https://vercel.com)
   - 点击 "Sign Up" 或 "Log In"
   - 选择 "Continue with GitHub" 使用 GitHub 账号登录

2. **导入项目**
   - 登录后，点击 "New Project"
   - 在 "Import Git Repository" 部分找到您刚创建的仓库
   - 点击 "Import"

3. **配置项目**
   - **Project Name**: 保持默认或修改为您喜欢的名称
   - **Framework Preset**: 选择 "Other"
   - **Root Directory**: 保持默认（./）
   - **Build and Output Settings**: 保持默认
   - 点击 "Deploy"

### 步骤 5：等待部署完成

1. **部署过程**
   - Vercel 会自动检测 `vercel.json` 配置
   - 安装 Python 依赖
   - 构建应用
   - 部署到全球 CDN

2. **部署状态**
   - 绿色勾号：部署成功
   - 红色叉号：部署失败（查看日志排查问题）

### 步骤 6：访问您的网站

部署成功后，Vercel 会提供：
- **临时域名**: 如 `your-project-name.vercel.app`
- **自定义域名**: 可以在设置中绑定自己的域名

## ? 常见问题解决

### 问题 1：部署失败

**可能原因**：
- Python 版本不兼容
- 依赖包安装失败
- 代码路径错误

**解决方案**：
1. 检查 Vercel 部署日志
2. 确认 `requirements.txt` 中的包版本
3. 检查 `vercel.json` 配置是否正确

### 问题 2：数据库问题

**注意**：Vercel 是无服务器平台，不支持持久化的 SQLite 数据库。

**解决方案**：
1. **开发/演示环境**：使用内存数据库（每次重启会重置）
2. **生产环境**：建议使用云数据库服务：
   - [PlanetScale](https://planetscale.com/)（MySQL）
   - [Supabase](https://supabase.com/)（PostgreSQL）
   - [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

### 问题 3：静态文件访问

**问题**：上传的图片无法显示

**解决方案**：
- 使用云存储服务（如阿里云 OSS、腾讯云 COS）
- 或使用 Vercel 的静态文件托管

## ? 更新部署

当您修改代码后，只需要推送到 GitHub：

```bash
# 添加修改的文件
git add .

# 提交修改
git commit -m "更新功能描述"

# 推送到 GitHub
git push
```

Vercel 会自动检测到代码变更并重新部署。

## ? 监控和分析

Vercel 提供了丰富的监控功能：

1. **访问统计**：查看网站访问量
2. **性能监控**：页面加载速度
3. **错误日志**：运行时错误追踪
4. **部署历史**：查看所有部署记录

## ? 优化建议

### 性能优化
1. **启用缓存**：合理设置静态资源缓存
2. **图片优化**：使用 WebP 格式，压缩图片大小
3. **代码分割**：按需加载 JavaScript

### 安全优化
1. **环境变量**：敏感信息存储在 Vercel 环境变量中
2. **HTTPS**：Vercel 自动提供 SSL 证书
3. **访问控制**：可以设置密码保护或 IP 白名单

## ? 技术支持

如果遇到问题：

1. **查看文档**：[Vercel 官方文档](https://vercel.com/docs)
2. **社区支持**：[Vercel 社区](https://github.com/vercel/vercel/discussions)
3. **联系我们**：项目技术支持邮箱

## ? 部署完成

恭喜！您的兰州大学暑期实践宣传平台已成功部署到 Vercel。

**下一步**：
- 分享您的网站链接
- 开始发布实践内容
- 邀请团队成员使用

---

**注意事项**：
- 免费版 Vercel 有一定的使用限制（带宽、函数执行时间等）
- 如需更高性能，可考虑升级到付费版本
- 定期备份重要数据