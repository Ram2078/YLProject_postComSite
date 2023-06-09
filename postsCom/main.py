from flask import Flask, render_template, request, redirect, url_for
from essential_generators import DocumentGenerator
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def close_db_connection(conn):
    conn.close()


def init_db():
    conn = get_db_connection()
    conn.execute(
        'CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT '
        'NULL, content TEXT NOT NULL, pic_path TEXT NOT NULL, random_comment TEXT NOT NULL)')
    conn.close()


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def get_post(post_id):
    global pid
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    pid = post['id']
    conn.close()
    return render_template('post.html', post=post)


@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        pic_url = request.form['pic_url']
        random_comment = DocumentGenerator().sentence()

        conn = get_db_connection()

        conn.execute(
            'INSERT INTO posts (title, content, pic_path, random_comment) VALUES (?, ?, ?, ?)',
            (title, content, pic_url, random_comment))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_post.html')


if __name__ == '__main__':
    pid = 1
    init_db()
    app.run()
