#!/usr/bin/python3
# -*- encoding=utf8 -*-

import pytest

from utils import add_book
from utils import get_all_books
from utils import get_book
from utils import update_book
from utils import delete_book
from utils import validate_uuid4


@pytest.mark.parametrize('title', ['', 'test', u'тест', '@#%$^', 'long title' * 10])
@pytest.mark.parametrize('author', ['', 'Teodor Drayzer', u'Пушкин', '@#$%#', 'long author' * 10])
def test_create_new_book(title, author):
    """ Check 'create book' method with different values of
        Title and Author.
    """

    book = {'title': title, 'author': author}
    new_book = add_book(book)

    all_books = get_all_books()

    assert new_book in all_books
    assert len(all_books) > 0


def test_get_list_of_books():
    """ Check that 'get books' method returns correct list of books. """

    # Create two books, just to make sure books will be correctly
    # added to the list:
    add_book({'title': '', 'author': ''})
    add_book({'title': '1', 'author': '2'})

    # Get list of all books:
    all_books = get_all_books()

    # Check that every book in the list has all required attributes:
    for book in all_books:
        assert 'title' in book
        assert 'author' in book
        assert validate_uuid4(book['id'])

    # Make sure that the list has at least 2 books:
    assert len(all_books) >= 2


@pytest.mark.parametrize('title', ['', 'test', u'тест', '@#%$^', 'long title' * 10])
@pytest.mark.parametrize('author', ['', 'Teodor Drayzer', u'Пушкин', '@#$%#', 'long author' * 10])
def test_update_book(title, author):
    # Create new book:
    new_book = add_book({'title': '', 'author': ''})
    book_id = new_book['id']

    # Update book attributes:
    update_book(book_id, {'title': title, 'author': author})

    # Get info about this book:
    book = get_book(book_id)

    # Verify that changes were applied correctly:
    assert book['title'] == title
    assert book['author'] == author


def test_delete_book():
    # Create new book
    new_book = add_book({'title': 'Book to be deleted', 'author': 'Test Author'})
    book_id = new_book['id']

    # Get list of books
    all_books = get_all_books()

    # Check adding new book to book list.
    if new_book in all_books:
        # If book was added to list :1.Get number of books in list.
        number_of_books = len(all_books)

        # 2.Delete created book.
        delete_book(book_id)

        # 3.Check if the book was deleted and the list of books was reduced by 1 element
        all_books = get_all_books()
        updated_number_of_books = len(all_books)
        assert new_book not in all_books
        assert number_of_books > updated_number_of_books

    else:
        print('Test Error!!!The book was not created at the beginning of the test case')
