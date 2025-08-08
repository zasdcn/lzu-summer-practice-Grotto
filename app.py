from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'lzu2023summer'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['DATABASE'] = 'data/database.db'

# 初始化数据库
def init_db():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        c = conn.cursor()
        # 创建团队表
        c.execute('''CREATE TABLE IF NOT EXISTS team_members (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     role TEXT NOT NULL,
                     description TEXT NOT NULL,
                     image TEXT)''')
        # 创建推文表
        c.execute('''CREATE TABLE IF NOT EXISTS articles (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     content TEXT NOT NULL,
                     publish_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                     images TEXT)''')
        conn.commit()

# 获取数据库连接
def get_db():
    return sqlite3.connect(app.config['DATABASE'])

# 首页路由
@app.route('/')
def index():
    conn = get_db()
    c = conn.cursor()
    
    # 获取团队成员
    c.execute("SELECT * FROM team_members")
    team_members = c.fetchall()
    
    # 获取所有推文
    c.execute("SELECT * FROM articles ORDER BY publish_date DESC")
    articles = c.fetchall()
    
    # 创建推文详情字典
    articles_details = {}
    for article in articles:
        # 处理日期格式 - SQLite返回的可能是字符串
        publish_date = article[3]
        if publish_date:
            try:
                # 尝试解析SQLite的日期字符串格式
                if isinstance(publish_date, str):
                    # SQLite CURRENT_TIMESTAMP格式: 'YYYY-MM-DD HH:MM:SS'
                    date_obj = datetime.strptime(publish_date, '%Y-%m-%d %H:%M:%S')
                    formatted_date = date_obj.strftime('%Y年%m月%d日')
                else:
                    formatted_date = publish_date.strftime('%Y年%m月%d日')
            except (ValueError, AttributeError):
                formatted_date = '未知日期'
        else:
            formatted_date = '未知日期'
            
        articles_details[f'article_{article[0]}'] = {
            'title': article[1],
            'date': formatted_date,
            'content': f'<h3>{article[1]}</h3><p><strong>发布时间：</strong>{formatted_date}</p><div>{article[2]}</div>'
        }
    
    conn.close()
    
    return render_template('index.html', team_members=team_members, articles=articles, articles_details=articles_details)

# 处理图片上传
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png', 'gif']

# 发布推文路由
@app.route('/publish', methods=['POST'])
def publish_article():
    title = request.form.get('title')
    content = request.form.get('content')
    images = []
    
    # 处理上传的文件
    if 'images' in request.files:
        files = request.files.getlist('images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                images.append(filename)
    
    # 保存到数据库
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO articles (title, content, images) VALUES (?, ?, ?)",
              (title, content, ','.join(images)))
    conn.commit()
    conn.close()
    
    flash('推文发布成功！', 'success')
    return redirect(url_for('index'))

# 删除推文路由
@app.route('/delete/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    try:
        conn = get_db()
        c = conn.cursor()
        
        # 首先检查推文是否存在
        c.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        article = c.fetchone()
        
        if not article:
            conn.close()
            return jsonify({'error': '推文不存在'}), 404
        
        # 删除推文
        c.execute("DELETE FROM articles WHERE id = ?", (article_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': '推文删除成功'}), 200
        
    except Exception as e:
        return jsonify({'error': '删除失败'}), 500

# 管理后台路由
@app.route('/admin')
def admin():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM articles ORDER BY publish_date DESC")
    articles = c.fetchall()
    conn.close()
    return render_template('admin.html', articles=articles)

if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    init_db()
    # 修改为可以被外部访问
    # host='0.0.0.0' 允许所有IP访问
    # port=5000 可以修改为其他端口
    app.run(debug=False, host='0.0.0.0', port=5000)
