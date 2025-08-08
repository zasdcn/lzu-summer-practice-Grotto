from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
template_dir = os.path.join(project_root, 'templates')
static_dir = os.path.join(project_root, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'lzu2023summer'
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['DATABASE'] = '/tmp/database.db'

# Initialize database
def init_db():
    db_path = app.config['DATABASE']
    
    # Check if database already exists to avoid reinitializing
    if os.path.exists(db_path):
        return
        
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            # Create team members table
            c.execute('''CREATE TABLE IF NOT EXISTS team_members (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         role TEXT NOT NULL,
                         bio TEXT,
                         image_path TEXT
                     )''')
            
            # Create articles table
            c.execute('''CREATE TABLE IF NOT EXISTS articles (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         title TEXT NOT NULL,
                         content TEXT NOT NULL,
                         publish_date TEXT NOT NULL
                     )''')
             
            conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")

# Format date helper function
def format_date(date_str):
    try:
        if isinstance(date_str, str):
            # Try to parse different date formats
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%Y年%m月%d日')
                except ValueError:
                    continue
            return date_str  # Return original string if parsing fails
        elif hasattr(date_str, 'strftime'):
            return date_str.strftime('%Y年%m月%d日')
        else:
            return str(date_str)
    except Exception:
        return '未知日期'

@app.route('/')
def index():
    db_path = app.config['DATABASE']
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM articles ORDER BY id DESC')
        articles = c.fetchall()
        conn.close()
        
        # Format article details
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
        print(f"Database error: {e}")
        return render_template('index.html', articles=[], articles_details={})

@app.route('/publish', methods=['POST'])
def publish():
    title = request.form.get('title')
    content = request.form.get('content')
    
    if title and content:
        db_path = app.config['DATABASE']
        
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute('INSERT INTO articles (title, content, publish_date) VALUES (?, ?, ?)',
                     (title, content, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            conn.close()
            flash('推文发布成功！', 'success')
        except Exception as e:
            print(f"Publishing article error: {e}")
            flash('发布失败，请重试！', 'error')
    else:
        flash('请填写完整信息！', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    db_path = app.config['DATABASE']
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Check if article exists
        c.execute('SELECT * FROM articles WHERE id = ?', (article_id,))
        article = c.fetchone()
        
        if article:
            # Delete article
            c.execute('DELETE FROM articles WHERE id = ?', (article_id,))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': '推文删除成功'})
        else:
            conn.close()
            return jsonify({'success': False, 'message': '推文不存在'}), 404
            
    except Exception as e:
        print(f"Delete article error: {e}")
        return jsonify({'success': False, 'message': '删除失败，请重试'}), 500

@app.route('/admin')
def admin():
    db_path = app.config['DATABASE']
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM team_members')
        team_members = c.fetchall()
        c.execute('SELECT * FROM articles ORDER BY id DESC')
        articles = c.fetchall()
        conn.close()
        
        return render_template('admin.html', team_members=team_members, articles=articles)
    except Exception as e:
        print(f"Database error: {e}")
        return render_template('admin.html', team_members=[], articles=[])

# Initialize database
init_db()

# For Vercel deployment - export the app
app = app

if __name__ == '__main__':
    app.run(debug=True)
