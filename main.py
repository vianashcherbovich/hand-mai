from datetime import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    intro = db.Column(db.String(150), nullable=False)
    text = db.Column(db.Text, nullable=False)
    dog = db.Column(db.Text, nullable=False)
    lll = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/d')
def d():
    return render_template('d.html')


@app.route('/r')
def r():
    return render_template('r.html')


@app.route('/s')
def s():
    return render_template('s.html')


@app.route('/e')
def e():
    return render_template('e.html')


@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        dog = request.form['dog']
        lll = request.form['lll']

        # получить запись из БД по указанному id
        article = Article(title=title, intro=intro, text=text, dog=dog, lll=lll)
        db.session.add(article)
        db.session.commit()

        return redirect('/articles')

    else:
        return render_template('create_article.html')


@app.route('/articles')
def articles():
    # взять из БД все статьи и отсортировать их по дате
    art = Article.query.order_by(Article.date.desc()).all()
    return render_template('articles.html', xyz=art)


@app.route('/articles/<int:id>')
def article(id):
    # получить запись из БД по указанному id
    art = Article.query.get(id)
    return render_template('article_detailed.html', abc=art)


@app.route('/articles/<int:id>/delete')
def article_delete(id):
    # получить запись из БД по указанному id
    art = Article.query.get(id)
    db.session.delete(art)
    db.session.commit()
    return redirect('/articles')


@app.route('/articles/<int:id>/update', methods=['POST', 'GET'])
def article_update(id):
    # получить запись из БД по указанному id
    art = Article.query.get(id)
    if request.method == 'POST':
        art.title = request.form['title']
        art.intro = request.form['intro']
        art.text = request.form['text']
        art.dog = request.form['dog']
        art.lll = request.form['lll']
        db.session.commit()

        return redirect('/articles')

    else:
        return render_template('article_update.html', aaa=art)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=0)
