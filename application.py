from flask import Flask
application = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

@app.route('/')
def index():
    return "Hello There"

@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for books in books:
        book_data = {'name': books.book_name, 'description': books.author}
        book_data['id'] = books.id
        book_data['book_name'] = books.book_name
        book_data['author'] = books.author
        book_data['publisher'] = books.publisher
        output.append(book_data)

    return {'books': [{ 'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher } for book in books]}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    publisher = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<Book {self.book_name} by {self.author}>"
    
@app.route('/books/<int:id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonfy({'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher})

@app.route('/books', methods=['POST'])
def add_book():
    book_data = request.get_json()
    new_book = Book(
        book_name=book_data['book_name'],
        author=book_data['author'],
        publisher=book_data['publisher']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully!'}), 201
from flask import request, jsonify

if __name__ == '__main__':
    app.run(debug=True)
    