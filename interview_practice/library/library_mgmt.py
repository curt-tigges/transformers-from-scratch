from dataclasses import dataclass, asdict, replace
from typing import List, Optional

@dataclass
class Book():
    book_id: int
    title: str
    author: str
    isbn: str
    publication_year: int
    available: Optional[bool] = True

@dataclass
class User():
    user_id: int
    name: str
    email: str
    is_staff: Optional[bool] = False


class LibraryManagementSystem():
    def __init__(self):
        self.books = {}
        self.users = {}
        self.memberships = {}
        self.rentals = {}

    def add_book(self, book_id: int, title: str, author: str, isbn: str, publication_year: int) -> None:
        self.books[book_id] = Book(book_id, title, author, isbn, publication_year)

    def get_book(self, book_id: int) -> Book:
        return self.books[book_id]
    
    def add_user(self, user_id, name, email, is_staff=False) -> None:
        self.users[user_id] = User(user_id, name, email, is_staff)

    def get_user(self, user_id: int) -> User:
        return self.users[user_id]
    
    def display_book_info(self, book_id: int) -> None:
        book = self.books[book_id]

        print(f"Title: {book.title}\nAuthor: {book.author}\nISBN: {book.isbn}\nPublication Year: {book.publication_year}\nAvailable: {'Yes' if book.available else 'No'}\n")

