from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

all_books = []

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

db.create_all()

@app.route('/')
def home():
    return render_template("index.html", book_list=Books.query.all())


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template("add.html")
    else:
        new_book = Books(title=request.form["name"], author=request.form["author"], rating=request.form["rating"])
        db.session.add(new_book)
        db.session.commit()
        return redirect('/')


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        book_id = id
        book = Books.query.filter_by(id=book_id).first()
        book_name = book.title
        current_rating = book.rating
        return render_template('edit_rating.html', book_name=book_name, current_rating=current_rating, id=book_id)
    else:
        book_id = id
        book_to_update = Books.query.filter_by(id=book_id).first()
        book_to_update.rating = request.form["new_rating"]
        db.session.commit()
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=8000)

