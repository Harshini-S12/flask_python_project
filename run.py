from datetime import datetime

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.update(
    SECRET_KEY='topsecert',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:pgadmin@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)

app.app_context().push()


@app.route('/index')
@app.route('/')
def helloflask():
    return 'Hello Flask! '


@app.route('/new/')
def query_string(greeting='hello'):
    q_val = request.args.get('greeting', greeting)
    return '<h1> the greeting is {0},</h1>'.format(q_val)


@app.route('/user')
@app.route('/user/<name>')
def n_query_string(name='mina'):
    return '<h1> Hi There : {0} </h1>'.format(name)


# strings
@app.route('/text/<string:name>')
def w_string(name):
    return '<h1> String : ' + name + '</h1>'


# numbers
@app.route('/no/<int:n>')
def w_n(n):
    return '<h1> no is : ' + str(n) + '</h1>'


# numbers
@app.route('/add/<int:n1>/<int:n2>')
def add(n1, n2):
    return '<h1> the sum of the nos are {}'.format(n1 + n2) + '</h1>'


@app.route('/mul/<float:m1>/<float:m2>')
def mul(m1, m2):
    return '<h1> Product is {}'.format(m1 * m2) + '</h1>'


@app.route('/temp')
def using_templates():
    return render_template('hello.html')


@app.route('/watch')
def top_movies():
    movies_list = ['abc', 'xyx', 'wwww', 'heellooo', 'byyyee']
    return render_template('movies.html', movies=movies_list, name='Harshini')


@app.route('/tables')
def movies_plus():
    movies_dict = {'abc': 02.30,
                   'xyx': 04.20,
                   'wwww': 50.20,
                   'heellooo': 01.00,
                   'byyyee': 02.00}
    return render_template('table_data.html', movies=movies_dict, name='Yamini')


@app.route('/filter')
def filter_data():
    movies_dict = {'abc': 02.30,
                   'xyx': 04.20,
                   'wwww': 50.20,
                   'heellooo': 01.00,
                   'byyyee': 02.00}
    return render_template('filter_data.html', movies=movies_dict, name=None, flim='a carol')


class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'The Publisher is {}'.format(self.name)


#BOOKS TABLE
class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # ESTABLISH RELATIONSHIP
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):

        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
