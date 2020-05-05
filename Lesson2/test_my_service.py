#!/usr/bin/python3
#-*- encoding=utf8 -*-

import requests
from requests.auth import HTTPBasicAuth
import pytest


#uses for positive authorization
user = 'admin'
password = 'admin'

#uses for checking negative scenarios
wrong_user = ''
wrong_pass = ''

@pytest.fixture
def auth_cookie():
    #Getting authorization cookie function

    url = 'http://127.0.0.1:8080/login'
    result = requests.get(url, auth=HTTPBasicAuth(user, password))
    data = result.json()

    yield data['auth_cookie']

def test_check_login():                                             #test 1
    """Log in to the service and get the auth cookie"""

    url='http://127.0.0.1:8080/login'
    result=requests.get(url,auth=HTTPBasicAuth(user,password))
    data = result.json()


    """Status code must be 200 and auth cookie has uuid4 format"""

    assert result.status_code == 200, "Error status code"
    assert 'auth_cookie' in data , "Auth cookie missing in data"
    assert data['auth_cookie'] > '' ,"Auth cookie has empty value"

def test_wrong_user_wrong_pass():                                   #test 2(negative scenario)
    """Try to log in to service with invalid user"""
    url = 'http://127.0.0.1:8080/login'
    result = requests.get(url, auth = HTTPBasicAuth(wrong_user,password))

    assert result.status_code == 401,"Error status code!"
    assert result.status_code != 200 , "Auth protection is missing!"


    """Try to log in to service with invalid password"""
    url1 = 'http://127.0.0.1:8080/login'
    result1 = requests.get(url1, auth=HTTPBasicAuth(user, wrong_pass))

    assert result1.status_code == 401,"Error status code!"
    assert result1.status_code != 200, "Auth protection is missing!"


def test_check_list_of_books(auth_cookie):        #test3
    """Get list of books"""

    url = 'http://127.0.0.1:8080/books'
    result = requests.get(url, cookies={'auth_cookie': auth_cookie})


    """Verify status code"""
    assert result.status_code == 200,"Book list is not available"


def test_add_book(auth_cookie):                                      #test4

    """Add new book"""
    url = 'http://127.0.0.1:8080/addbook'
    result = requests.post(url, cookies={'auth_cookie': auth_cookie}, data ={'title': "Test 4!",
                                                                             'author': 'Me'})

    assert result.status_code == 200,"Adding book function is not available"

    url1 = 'http://127.0.0.1:8080/books'
    result1 = requests.get(url1, cookies={'auth_cookie': auth_cookie})
    data = result1.json()

    """Checking if book list is not empty"""

    assert data != {},"Book list is empty"

def test_book_uid (auth_cookie):                                     #Test 5
    """This test is checking the right form of the unique book id after the new book has been added"""

    url = 'http://127.0.0.1:8080/addbook' #Add new book
    result = requests.post(url, cookies={'auth_cookie': auth_cookie}, data={'title': "Test 5!",
                                                                        'author': 'Me'})
    data = result.json()
    uid= data.get('uid')

    """Verify right format of received book id """

    assert '-' in uid,"Wrong book id format!"
    assert len(uid) == 36 ,"Wrong book id format!"

def test_getting_book_info(auth_cookie) :                             #Test 6

    """This test is checking correct display of information on the book profile"""

    url = 'http://127.0.0.1:8080/addbook' #Add new book
    result = requests.post(url, cookies={'auth_cookie': auth_cookie}, data={'title': "Test 6!",
                                                                            'author': 'Me'})
    data = result.json()
    uid = data.get('uid') #Get book unique id

    bookURL = 'http://127.0.0.1:8080/books/' + uid #The profile of created book
    result1 = requests.get(bookURL, cookies={'auth_cookie': auth_cookie})

    data1 = result.json()

    """Verify info on the book profile"""

    assert result1.status_code == 200,"Book profile is not working!"
    assert data1 != {},"Information on the book profile is missing!"

def test_delete_book (auth_cookie) :                                 #Test 7

    """This test is checking delete book function """

    url = 'http://127.0.0.1:8080/addbook'            #Add new book
    result = requests.post(url, cookies={'auth_cookie': auth_cookie}, data={'title': "Test 7!",
                                                                            'author': 'Me'})
    data = result.json()
    uid = data.get('uid')                            #Get book unique id

    bookURL = 'http://127.0.0.1:8080/books/' + uid # Send delete request
    result2 = requests.delete(bookURL,cookies={'auth_cookie': auth_cookie})
    data2=result2.json()

    """Check if the delete request was sent correctly and the book info is missing"""

    assert data2 == {},"Book information wasn't deleted!"
    assert result2.status_code == 200,"Delete request failed!"

    booklistURL = 'http://127.0.0.1:8080/books' #Get list of books
    resdata = requests.get(booklistURL, cookies={'auth_cookie': auth_cookie})

    listdata = resdata.json()


    """Deleted book mustn't be in the book list"""

    assert "Test 7!" not in listdata,"Deleted book is in book list!"

def test_main_page(auth_cookie):                                     #Test 8

    """Check main page of service"""

    url = 'http://127.0.0.1:8080/'#Send get request
    result = requests.get(url, cookies={'auth_cookie': auth_cookie})
    data=result.text


    """Check status code and page text """

    assert 'Hello World!' in data,"The text on the main page is missing"
    assert result.status_code == 200,"The main page failed!"

def test_book_info_update(auth_cookie):                             #Test 9

    """This test is checking book info update function"""

    add_book_url = 'http://127.0.0.1:8080/addbook' #Add new book
    result = requests.post(add_book_url, cookies={'auth_cookie': auth_cookie}, data={'title': "Test 9!",
                                                                            'author': 'Me'})
    data = result.json()
    uid = data.get('uid')            #Get book unique id

    updated_title = 'Test 9!UPDATED' #Updated title info
    updated_author = 'UPDATED'       #Updated author info

    book_update_url = 'http://127.0.0.1:8080/books/' + uid # Send put request
    result3 = requests.put(book_update_url, cookies={'auth_cookie': auth_cookie}, data={'title': updated_title,
                                                                            'author': updated_author})
    book_update_data = result3.json()
    new_title = book_update_data.get('title')    #Get new title
    new_author = book_update_data.get ('author') #Get new author

    """Check if book info was updated correctly """

    assert result.status_code == 200,"The put request failed!"
    assert new_title =='Test 9!UPDATED',"The title info wasn't updated!"
    assert new_author =='UPDATED',"The author info wasn't update!"

def test_try_usage_of_service_without_authorization(auth_cookie):               #Test 10(negative scenario)

    """In this test we try to use service functionality without getting auth cookie  """

    """Try to open book list entering empty pass and user name"""
    url = 'http://127.0.0.1:8080/books'
    result = requests.get(url,auth = HTTPBasicAuth(wrong_user,wrong_pass))

    assert result.status_code != 200,"Book list doesn't use auth cookie protection!"

    """ Try to add new book without using auth cookie"""
    url1 = 'http://127.0.0.1:8080/addbook'
    result1 = requests.post(url1, data={'title': "Test 10!",'author': 'Me'})

    assert result1.status_code != 200,"Add book function doesn't use auth cookie protection!"

    """Try to get book information without using auth cookie"""

    url2 = 'http://127.0.0.1:8080/addbook'              #Add new book
    result2 = requests.post(url2, cookies={'auth_cookie': auth_cookie}, data={'title': "Test 10!",
                                                                            'author': 'Me'})
    data2 = result2.json()
    uid = data2.get('uid')

    bookURL = 'http://127.0.0.1:8080/books/' + uid      #Open book URL
    result3 = requests.get(bookURL)                     #Get book information

    assert result3.status_code != 200,"Book profile doesn't use auth cookie protection!"

    """Try to delete book without using auth cookie"""

    url3 = 'http://127.0.0.1:8080/addbook'             #Add new book
    result4 = requests.post(url3, cookies={'auth_cookie': auth_cookie}, data={'title': "Test 10.2!",
                                                                            'author': 'Me'})
    data4 = result4.json()
    uid4 = data4.get('uid')

    bookURL = 'http://127.0.0.1:8080/books/' + uid4   #Open book URL
    result5 = requests.delete(bookURL)                #Try to delete book

    result6 = requests.get(bookURL,cookies={'auth_cookie': auth_cookie}) #Get book info
    data6 =result6.json()
    title6 = data6.get('title')                       #Get book title info

    assert result5.status_code != 200,"Delete function doesn't use auth cookie protection!"
    assert "Test 10.2!" in title6 ,"Delete function doesn't use auth cookie protection!"

    """Try to update book info without using auth cookie"""

    url7 = 'http://127.0.0.1:8080/addbook'     #Add new book
    result7 = requests.post(url7, cookies={'auth_cookie': auth_cookie}, data={'title': "Test 10.7!",
                                                                              'author': 'Me'})
    data7 = result7.json()
    uid7 = data7.get('uid')                    #Get book unique id

    bookURL7 = 'http://127.0.0.1:8080/books/' + uid7
    result8 = requests.put(bookURL7,data={'title':'qwerty','author': 'qwerty'}) #Try to update book info

    result9 = requests.get(bookURL7, cookies={'auth_cookie': auth_cookie}) #Get book info
    data9 = result9.json()

    title10 = data9.get('title')              #Get book title

    assert result8.status_code != 200,"Information update function doesn't use auth cookie protection! "
    assert "Test 10.7!" in title10 ,"Information update function doesn't use auth cookie protection! "
    assert 'qwerty' not in title10,"Information update function doesn't use auth cookie protection! "




























