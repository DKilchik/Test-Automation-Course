#!/usr/bin/python3
# -*- encoding=utf8 -*-
import pytest
from utils import add_book
from utils import get_all_books
from utils import get_book
from utils import update_book
from utils import delete_book
from utils import validate_uuid4
from utils import main_page
from utils import auth
from utils import auth_check
from utils import delete_book_twice
from utils import update_deleted_book
from utils import get_book_status_code





def test_main_page_without_cookies():
    """Make simple get request to API service(without getting cookies),verify that server is working"""

    response = main_page()

    assert response.status_code == 200, "Rest API Service doesn't response!Check if it was hosted correctly"
    assert 'Hello World' in response.text

def test_main_page_with_cookies():
    """Make get request to API service main URL after getting auth cookies"""

    cookie_data = auth()
    response = main_page(cookie_data)

    assert response.status_code == 200, "Starting page crashes if user has auth cookie"
    assert 'Hello World' in response.text

def test_auth_positive_scenario():
    """Check getting auth cookie after entering valid username and password"""

    cookie_data = auth()

    assert len(cookie_data) > 0, "Auth  cookies are missing!"
    assert len(cookie_data['my_cookie']) != 0, 'Value of cookie is missing in the dictionary!'
    assert 'my_cookie' in cookie_data.keys(), 'Key is missing in the dictionary!'

def test_validate_uuid4():
    """Check format of auth cookies. """

    cookie_data = auth()
    uuid_string = cookie_data['my_cookie']
    response = validate_uuid4(uuid_string)


    assert response, "Service uses incorrect format of auth cookie !"
    assert cookie_data['my_cookie'].count('-') == 4,"Service uses incorrect format of auth cookie !"
    assert len(cookie_data['my_cookie']) > 0, "Service uses incorrect format of auth cookie ! "

@pytest.mark.parametrize('user', ['', 'test', u'тест'.encode('utf8'),'"','longuser'*15,'!@#$%&*()_',
                                                                          'CaPS', u'測試'.encode('utf8')])
@pytest.mark.parametrize('password', ['', 'test', u'тест'.encode('utf8'), '"', 'longpass'*15,
                                                            '!@#$%^&*()', 'CaPS', u'測試'.encode('utf8')])
def test_auth_negative_scenario(user, password):
    """This function test responses of API login method after entering invalid login values"""

    response = auth_check(user, password)


    assert response == 401 ,"Incorrect working of Authorisation method!!!"
    assert 400 <= response < 500, "Server had't processed input auth values!"
    assert response != 200, "Authorisation by invalid login values!"

def test_create_1_book():
    """This function check if created book was added to book list"""

    book = {'title': '1 Created book', 'author': 'One author'}
    new_book = add_book(book)

    all_books = get_all_books()

    assert new_book in all_books
    assert len(all_books) >= 1

def test_create_some_books():
    """This function verify that all of created books was added to book list"""

    book1 = {'title': 'First created book', 'author': 'First author'}
    new_book1 = add_book(book1)

    book2 = {'title': 'Second created book', 'author': 'Second author'}
    new_book2 = add_book(book2)

    all_books = get_all_books()

    assert new_book1 and new_book2 in all_books
    assert len(all_books) >= 2

@pytest.mark.parametrize('title', ['', 'Test', u'Tест', '@#%$^', 'long title'*10, u'測試'])
@pytest.mark.parametrize('author', ['', 'Teodor Drayzer', u'Пушкин', '@#$%#', 'long author'*10, u'測試'])
def test_create_new_book(title, author):
    """ Check 'create book' method with different values of
        Title and Author.
    """

    book = {'title': title, 'author': author}
    new_book = add_book(book)

    all_books = get_all_books()

    assert new_book in all_books
    assert len(all_books) > 0


def test_books_with_similar_title():
    """This test check Api behavior after creating more than one book with identical title """

    """Create some books with identical title"""
    first_book = add_book({'title': 'The same title', 'author': 'Some author 1'})
    first_book_id = first_book['id']
    second_book = add_book({'title': 'The same title', 'author': 'Some author 2'})
    second_book_id = second_book['id']

    """Get list of books"""
    all_books = get_all_books()

    assert first_book in all_books
    assert second_book in all_books

    """Get info of created books"""
    first_book_info = get_book(first_book_id)
    second_book_info = get_book(second_book_id)

    assert first_book_info != second_book_info
    assert first_book_id != second_book_id
    assert first_book['author'] == 'Some author 1'
    assert second_book['author'] == 'Some author 2'

def test_books_with_similar_author():
    """This test check API behavior after creating more than one book with identical author """

    """Create some books with identical author"""
    first_book = add_book({'title': 'Title 1', 'author': 'The same author'})
    first_book_id = first_book['id']
    second_book = add_book({'title': 'Title 2', 'author': 'The same author'})
    second_book_id = second_book['id']

    """Get list of books"""
    all_books = get_all_books()

    assert first_book in all_books
    assert second_book in all_books

    """Get info of created books"""
    first_book_info = get_book(first_book_id)
    second_book_info = get_book(second_book_id)

    assert first_book_info != second_book_info
    assert first_book_id != second_book_id
    assert first_book['title'] == 'Title 1'
    assert second_book['title'] == 'Title 2'

def test_book_list():
    """In this test we create some books and after that check if they will appear in book list """

    new_book = add_book({'title': 'Silent Hill', 'author': 'Heranuka'})
    another_new_book = add_book({'title': 'Silent Hill 2', 'author': "Heranuka po Royal'u"})

    book_list = get_all_books()

    assert new_book in book_list
    assert another_new_book in book_list
    assert len(book_list) >= 2


@pytest.mark.parametrize('sort', ['by_title', ''])
def test_sorting(sort):
    """This test is checking get_book_list method after passing sort parameter"""


    """Create some books with different titles"""
    new_book1 = add_book({'title': '1', 'author': 'Someone'})
    new_book2 = add_book({'title': 'B', 'author': 'Someone'})
    new_book3 = add_book({'title': '2', 'author': 'Someone'})
    new_book4 = add_book({'title': 'A', 'author': 'Someone'})
    new_book5 = add_book({'title': u'д', 'author': 'Someone'})
    new_book6 = add_book({'title': u'Nǐ hǎo!', 'author': 'Someone'})
    new_book7 = add_book({'title': u'г', 'author': 'Someone'})

    """Get list of books,pass to get_all_books sort parameter"""

    params = {'sort': sort}
    book_list = get_all_books(params=params)

    """Get indexes of created books in the list"""
    b1_index, b2_index, b3_index, b4_index, b5_index, b6_index, b7_index = book_list.index(new_book1),\
                                                                           book_list.index(new_book2),\
                                                                           book_list.index(new_book3),\
                                                                           book_list.index(new_book4),\
                                                                           book_list.index(new_book5),\
                                                                           book_list.index(new_book6),\
                                                                           book_list.index(new_book7)

    sort_type = sort
    if sort_type == '':
        assert b1_index < b2_index < b3_index < b4_index < b5_index < b6_index < b7_index, "Error in default sort!"
    else:
        assert b1_index < b3_index < b4_index < b2_index, "Error in sort by title !"
        assert b6_index < b7_index < b5_index, "Error in sort by title !"
        assert b1_index < b3_index < b4_index < b2_index < b6_index < b7_index < b5_index, "Error in sort by title!"


def test_sort_identical_title():
    """This test is checking API behavior when there are some identical title in the list
    and the list need to be sorted"""

    """Create some books with identical title"""
    new_book = add_book({'title': 'Identical title', 'author': 'Some author'})
    new_book2 = add_book({'title': 'Identical title', 'author': 'Some author'})

    """Get sorted list bo books"""
    params = {'sort': 'by_title'}
    book_list = get_all_books(params=params)

    assert book_list.index(new_book) < book_list.index(new_book2), 'Incorrect sorting if there are ' \
                                                                   'some identical titles!'

@pytest.mark.parametrize('limit', ['1', '10', '100'])
def test_limits(limit):
    """This test is checking get_book_list method after passing limit parameter"""

    """Create one more book than indicated in the limit """
    if int(limit) > 0:
        for l in range(int(limit)+1):
            new_book = add_book({'title': 'The Dark Tower ' + str(l), 'author': 'Stephen King'})

        """Get list of books with limit parameter"""
        params = {'limit': limit}
        book_list = get_all_books(params=params)

        """Check if numbers of books in the list corresponds to the limit"""
        assert len(book_list) == int(limit), "Wrong limit parameter's working!"

    else:
        assert 1 > 2, "Wrong value of limit!In positive scenario limit have to be more than 0"

@pytest.mark.parametrize('sort', ['by_title', ''])
@pytest.mark.parametrize('limit', ['1', '10', '100'])
def test_sorting_with_limits(sort, limit):
    """Comprehensive verification of sorting and limits"""

    """Create some books(number == limit) """
    new_book = add_book({'title': ' ', 'author': ' '})
    last_created_book = 1 #Костыль
    for l in range(int(limit) - 1):
         last_created_book = add_book({'title': ' ' + str(l), 'author': 'Stephen King'})

    params = {'limit': limit, 'sort': sort}
    book_list = get_all_books(params)

    if last_created_book in book_list:
        assert len(book_list) == int(limit)
        assert book_list.index(new_book) < book_list.index(last_created_book)

    else:
        assert len(book_list) == int(limit)

def test_delete_one_book():
    """This test check API delete method"""

    """Create a book"""
    new_book = add_book({'title': 'Deleted book', 'author': 'Deleted author'})
    book_id = new_book['id']

    """Get list of books"""
    all_books = get_all_books()
    list_number = len(all_books)

    """Check if created book was added to book list correctly.If it wasn't print error exception"""
    if new_book in all_books:
        # Delete created book
        delete_book(book_id)
        all_books = get_all_books()
        updated_list_number = len(all_books)

        assert new_book not in all_books, "The book wasn't deleted.Incorrect work of DELETE method!"
        assert (list_number - 1) == updated_list_number
        # Get book info by book id.
        book_info = get_book(new_book)
        assert len(book_info) == 0, "Book info wasn't deleted.Incorrect work of DELETE method!"

    else:
        assert 1 == 0, "The book wasn't created correctly. Check add_book method!!!"


def test_delete_one_of_two_books():
    """In this test we create two books with the same title and author.After that  delete one of them and
    will check that delete method work correctly"""

    """Create some books with identical authors and titles"""
    first_book = add_book({'title': 'Foundation', 'author': 'Isaac Asimov'})
    first_book_id = first_book['id']
    second_book = add_book({'title': 'Foundation', 'author': 'Isaac Asimov'})
    second_book_id = second_book['id']

    """Get list of books"""
    all_books = get_all_books()

    """Check if created books were added to book list correctly.If they weren't print error exception"""
    if first_book and second_book in all_books:
        # Delete first created book
        delete_book(first_book_id)
        all_books = get_all_books()

        #Check that was deleted only one book of two that were created.
        assert first_book not in all_books, "The book wasn't deleted.Incorrect work of DELETE method!"
        assert second_book in all_books, "Two books were deleted instead of one!Incorrect work of DELETE method! "

        # Get book info by book id.
        first_book_info = get_book(first_book_id)
        second_book_info = get_book(second_book_id)

        #Check that info of first book was deleted and info of second one wasn't spoiled
        assert len(first_book_info) == 0, "Book info wasn't deleted.Incorrect work of DELETE method!"
        assert len(second_book_info) > 0, "Two books were deleted instead of one!Incorrect work of DELETE method! "
        assert second_book['author'] == 'Isaac Asimov'
        assert second_book['title'] == 'Foundation'
        assert second_book['id'].count('-') == 4

    else:
        assert 1 == 0, "The books weren't created correctly. Check add_book method!!!"

def test_delete_one_book_twice():
    """This test delete created book twice"""

    new_book = add_book({'title': 'Foundation', 'author': 'Isaac Asimov'})
    new_book_id = new_book['id']

    response = delete_book_twice(new_book_id)

    assert len(response) > 0
    assert new_book_id in response
    assert 'deleted' in response


@pytest.mark.parametrize('book_id', ['', ' ', '1', u'Пушкин', '@#$%#', 'text', u'測試', 'long text'*100])
def test_delete_invalid_id(book_id):
    """This test enter different invalid values to Delete method and check API behavior"""

    text = delete_book(book_id)

    assert text == None, "API Delete method process invalid input values!"


@pytest.mark.parametrize('title', ['', 'test',u'тест', '@#%$^', 'long title'*10])
@pytest.mark.parametrize('author', ['', 'Teodor Drayzer', u'Пушкин', '@#$%#', 'long author'*10])
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


def test_update_same_title():
    """This test check API behavior if we'll try to rename 2 books and give them the same title/author """

    """Create 2 new books"""
    book1 = add_book({'title': '', 'author': ''})
    book1_id = book1['id']
    book2 = add_book({'title': '', 'author': ''})
    book2_id = book2['id']


    """Update created books and give them identical titles and author"""
    update_book(book1_id, {'title': 'Test title', 'author': 'test author'})
    update_book(book2_id, {'title': 'Test title', 'author': 'test author'})

    """ Get info about this book: """
    book1_info = get_book(book1_id)
    book2_info = get_book(book2_id)

    """ Verify that changes were applied correctly: """

    assert book1_info['title'] == book2_info['title'] == 'Test title', "Error in update function!"
    assert book1_info['author'] == book2_info['author'] == 'test author', "Error in update function!"

def test_update_deleted_book():
    """This test checks API behavior after updating deleted book"""

    """Create new book"""
    new_book = add_book({'title': 'Some book', 'author': 'author'})
    book_id = new_book['id']

    """Delete created book"""
    delete_book(book_id)

    """Try to update created book"""
    response = update_deleted_book(book_id, {'title': 'updated title', 'author': 'updated author'})

    assert response == 404, "Update function work with incorrect input values!"

def test_nonexistent_book():
    """This test checks API behavior after update function get nonexistent(invalid) book id"""

    """Get some invalid format id"""
    book_id = 1

    """Try to update nonexistent book"""
    response = update_deleted_book(book_id, {'title': 'updated title', 'author': 'updated author'})

    assert response == 404, "Update function work with incorrect input values!"


def test_book_info():
    """In this test we get existing book and check all parameters of book info"""

    """Create new book"""
    new_book = add_book({'title': 'New book', 'author': 'New author'})
    book_id = new_book['id']

    """Get book info"""

    book_info = get_book(book_id)

    assert book_info['title'] == 'New book', "Error! get_book function works incorrect"
    assert book_info['author'] == 'New author', "Error! get_book function works incorrect"

def test_deleted_book_info():
    """This test checks API behavior after requesting deleted book info"""
    pass

    """Create new book"""
    new_book = add_book({'title': 'Pytest tutorial', 'author': 'QA'})
    book_id = new_book['id']

    """Delete created book"""
    delete_book(book_id)

    """Get book info"""
    info = get_book(book_id)
    status_code = get_book_status_code(book_id)


    assert len(info) == 0
    assert status_code == 200, "Wrong request status code in getting deleted book info"


@pytest.mark.parametrize('book_id', [' ', '1',u'тест', '@#%$^', 'longtitle'*10, 'test'])
def test_get_book_invalid_id(book_id):
    """This test checks API behavior after get_book request by invalid id  """

    info = get_book(book_id)
    status_code = get_book_status_code(book_id)

    assert len(info) == 0
    assert status_code == 200

@pytest.mark.parametrize('title', ['', 'test',u'тест', '@#%$^', 'longtitle'*10])
@pytest.mark.parametrize('author', ['', 'Teodor Drayzer', u'Пушкин', '@#$%#', 'longauthor'*10])
def test_book_info_different_options(title, author):
    """This test checks get_book request with different book info parameters"""

    """Create new book"""
    new_book = add_book({'title': title, 'author': author})
    book_id = new_book['id']

    """Get created book info and verify request status code"""
    book_info = get_book(book_id)
    status_code = get_book_status_code(book_id)

    assert book_info['title'] == title, "Incorrect work of get_book function !"
    assert book_info['author'] == author, "Incorrect work of get_book function !"
    assert status_code == 200, "Wrong get_book request status code!"































































