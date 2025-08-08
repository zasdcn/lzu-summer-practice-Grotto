from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'lzu2023summer'
app.config['UPLOAD_FOLDER'] = '../static/images'
app.config['DATABASE'] = '../data/database.db'

# 初始化数据库
def init_db():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'database.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
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

# 格式化日期的辅助函数
def format_date(date_str):
    try:
        if isinstance(date_str, str):
            # 尝试解析不同的日期格式
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%Y年%m月%d日')
                except ValueError:
                    continue
            return date_str  # 如果无法解析，返回原字符串
        elif hasattr(date_str, 'strftime'):
            return date_str.strftime('%Y年%m月%d日')
        else:
            return str(date_str)
    except Exception:
        return '未知日期'

@app.route('/')
def index():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'database.db')
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM articles ORDER BY id DESC')
        articles = c.fetchall()
        conn.close()
        
        # 处理日期格式
        articles_details = {}
        for article in articles:
            article_id = f'article_{article[0]}'
            articles_details[article_id] = {
                'date': format_date(article[3]),
                'title': article[1],
                'content': article[2]
            }
        
        return render_template('index.html', articles=articles, articles_details=articles_details)
    except Exception as e:
        print(f"数据库错误: {e}")
        return render_template('index.html', articles=[], articles_details={})

@app.route('/publish', methods=['POST'])
def publish():
    title = request.form.get('title')
    content = request.form.get('content')
    
    if title and content:
        db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'database.db')
        
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute('INSERT INTO articles (title, content, publish_date) VALUES (?, ?, ?)',
                     (title, content, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            conn.close()
            flash('推文发布成功！', 'success')
        except Exception as e:
            print(f"发布推文时出错: {e}")
            flash('发布失败，请重试！', 'error')
    else:
        flash('请填写完整信息！', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'database.db')
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # 检查推文是否存在
        c.execute('SELECT * FROM articles WHERE id = ?', (article_id,))
        article = c.fetchone()
        
        if article:
            # 删除推文
            c.execute('DELETE FROM articles WHERE id = ?', (article_id,))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': '推文删除成功'})
        else:
            conn.close()
            return jsonify({'success': False, 'message': '推文不存在'}), 404
            
    except Exception as e:
        print(f"删除推文时出错: {e}")
        return jsonify({'success': False, 'message': '删除失败，请重试'}), 500

@app.route('/admin')
def admin():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'database.db')
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM articles ORDER BY id DESC')
        articles = c.fetchall()
        conn.close()
        return render_template('admin.html', articles=articles)
    except Exception as e:
        print(f"管理页面错误: {e}")
        return render_template('admin.html', articles=[])

# 初始化数据库
init_db()

# Vercel需要的应用实例
app = app