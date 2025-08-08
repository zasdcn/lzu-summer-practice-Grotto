# This file is for local development only
# For Vercel deployment, use api/index.py

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'lzu2023summer'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['DATABASE'] = 'data/database.db'

# Initialize database for local development
def init_db():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        c = conn.cursor()
        # Create team members table
        c.execute('''CREATE TABLE IF NOT EXISTS team_members (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     role TEXT NOT NULL,
                     description TEXT NOT NULL,
                     image TEXT)''')
        # Create articles table
        c.execute('''CREATE TABLE IF NOT EXISTS articles (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     content TEXT NOT NULL,
                     publish_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                     images TEXT)''')
        conn.commit()

# Get database connection
def get_db():
    return sqlite3.connect(app.config['DATABASE'])

# Home route
@app.route('/')
def index():
    conn = get_db()
    c = conn.cursor()
    
    # Get team members
    c.execute("SELECT * FROM team_members")
    team_members = c.fetchall()
    
    # Get all articles
    c.execute("SELECT * FROM articles ORDER BY publish_date DESC")
    articles = c.fetchall()
    
    # Create article details dictionary
    articles_details = {}
    for article in articles:
        # Handle date format - SQLite may return string
        publish_date = article[3]
        if publish_date:
            try:
                # Try to parse SQLite date string format
                if isinstance(publish_date, str):
                    # SQLite CURRENT_TIMESTAMP format: 'YYYY-MM-DD HH:MM:SS'
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

# Handle image upload
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png', 'gif']

# Publish article route
@app.route('/publish', methods=['POST'])
def publish_article():
    title = request.form.get('title')
    content = request.form.get('content')
    images = []
    
    # Handle uploaded files
    if 'images' in request.files:
        files = request.files.getlist('images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                images.append(filename)
    
    # Save to database
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO articles (title, content, images) VALUES (?, ?, ?)',
              (title, content, ','.join(images)))
    conn.commit()
    conn.close()
    
    flash('推文发布成功！', 'success')
    return redirect(url_for('index'))

# Delete article route
@app.route('/delete/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    conn = get_db()
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

# Admin route
@app.route('/admin')
def admin():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM team_members')
    team_members = c.fetchall()
    c.execute('SELECT * FROM articles ORDER BY publish_date DESC')
    articles = c.fetchall()
    conn.close()
    
    return render_template('admin.html', team_members=team_members, articles=articles)

if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)
