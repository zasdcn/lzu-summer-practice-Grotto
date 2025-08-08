from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime
import tempfile

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'lzu2023summer'
app.config['UPLOAD_FOLDER'] = '/tmp/images'
app.config['DATABASE'] = '/tmp/database.db'

# Initialize database
def init_db():
    db_path = app.config['DATABASE']
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
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

# Format date helper function
def format_date(date_str):
    try:
        if isinstance(date_str, str):
            # Try to parse different date formats
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%Y��%m��%d��')
                except ValueError:
                    continue
            return date_str  # Return original string if parsing fails
        elif hasattr(date_str, 'strftime'):
            return date_str.strftime('%Y��%m��%d��')
        else:
            return str(date_str)
    except Exception:
        return 'δ֪����'

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
            flash('���ķ����ɹ���', 'success')
        except Exception as e:
            print(f"Publishing article error: {e}")
            flash('����ʧ�ܣ������ԣ�', 'error')
    else:
        flash('����д������Ϣ��', 'error')
    
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
            return jsonify({'success': True, 'message': '����ɾ���ɹ�'})
        else:
            conn.close()
            return jsonify({'success': False, 'message': '���Ĳ�����'}), 404
            
    except Exception as e:
        print(f"Delete article error: {e}")
        return jsonify({'success': False, 'message': 'ɾ��ʧ�ܣ�������'}), 500

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

if __name__ == '__main__':
    app.run(debug=True)