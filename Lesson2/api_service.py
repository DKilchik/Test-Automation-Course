#!/usr/bin/python3
#-*- encoding=utf8 -*-

from uuid import uuid4
import flask
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth
from flask import make_response

app=Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
basic_auth = BasicAuth(app)

BOOKS = []
SESSIONS = []


@app.route('/',methods=['GET'])
def main_page():
    return 'Hello World!'

def verify_cookie(request):
    """This function verifies cookie."""

    cookie = request.cookies.get('auth_cookie')




    return cookie in SESSIONS

@app.route('/login',methods=['GET'])
@basic_auth.required
def get_auth():
    """This function verifies user and password and creates
       new cookie if user and password are correct"""

    cookie = str(uuid4())
    SESSIONS.append(cookie)
    result=make_response(flask.jsonify({'auth_cookie':cookie}))
    result.set_cookie('auth_cookie',cookie)

    return result

@app.route('/books',methods =['GET'])
def get_list_of_books():
    """Thist function returns the list of books"""

    global BOOKS

    if verify_cookie(request):
        sort_filter = request.args.get('sort','')
        list_limit = int(request.args.get('limit',-1))

        result = BOOKS

        if sort_filter == 'by_title':
            result= sorted(result,key=lambda x: x['title'])

        if list_limit > 0:
            result =result[:list_limit]

        return flask.jsonify(BOOKS)

    raise Exception('Check auth function!!!')


@app.route('/addbook', methods = ['POST'])
def add_book():
    """This funtion adds new book in the list."""

    global BOOKS

    if verify_cookie(request):
        book_uid = str(uuid4())
        title = request.values.get('title','')
        author = request.values.get('author','No Name')

        new_book = { 'uid': book_uid, 'title': title, 'author': author}

        BOOKS.append(new_book)
        print("Added new book!")

        return flask.jsonify(new_book)


    raise Exception('Check auth function!!!')


@app.route('/books/<book_uid>', methods=['GET'])
def get_book(book_uid):
    # This function returns one book from the list.

    if verify_cookie(request):
        result = {}

        for book in BOOKS:
            if book['uid'] == book_uid:
                result = book

        return flask.jsonify(result)


@app.route('/books/<book_uid>',methods = ['DELETE'])
def delete_book(book_uid):
    # This function deletes book from the list.

    global BOOKS

    if verify_cookie(request):
        result = {}

        #Create new list of book and skip one book
        #whith specified id:
        new_book = [b for b in BOOKS if b['uid'] != book_uid]

        BOOKS = new_book

        return flask.jsonify(result)

@app.route('/books/<book_uid>', methods=['PUT'])
def update_book(book_uid):
    """ This function updates information about some book. """

    if verify_cookie(request):

        for i, book in enumerate(BOOKS):
            # Find the book with this ID:
            if book['uid'] == book_uid:
                book['title'] = request.values.get('title', book['title'])
                book['author'] = request.values.get('author', book['author'])

                # Update information about this book:
                BOOKS[i] = book

                return flask.jsonify(book)

    raise Exception('Check auth function!!!')


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080)