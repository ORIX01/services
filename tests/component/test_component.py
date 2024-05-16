import requests

book_manager_url = 'http://localhost:8000'
get_books_url = f'{book_manager_url}/get_books'
get_book_by_id_url = f'{book_manager_url}/get_book_by_id'
add_book_url = f'{book_manager_url}/add_book'
delete_book_url = f'{book_manager_url}/delete_book'

new_book = {
    "id": 99,
    "title": "War and Peace",
    "author": "Leo Tolstoy",
    "published_date": "2024-04-30T12:00:00",
    "pages": 1225
}

def test_1_add_book():
    res = requests.post(f"{add_book_url}", json=new_book)
    assert res.status_code == 200

def test_2_get_books():
    res = requests.get(f"{get_books_url}").json()

    books = [book for book in res if book['id'] == new_book['id']]
    assert len(books) == 1

def test_3_get_book_by_id():
    res = requests.get(f"{get_book_by_id_url}?book_id={new_book['id']}").json()

    assert res['title'] == new_book['title']
    assert res['author'] == new_book['author']
    assert res['pages'] == new_book['pages']

def test_4_delete_book():
    res = requests.delete(f"{delete_book_url}?book_id={new_book['id']}").json()
    assert res == {"message": "Success"}
