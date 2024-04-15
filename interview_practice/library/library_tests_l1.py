import unittest
from library_mgmt import LibraryManagementSystem

class TestLibraryManagementSystemLevel1(unittest.TestCase):
    def setUp(self):
        self.lms = LibraryManagementSystem()

    def test_add_book(self):
        self.lms.add_book(1, "Book 1", "Author 1", "ISBN1", 2021)
        book = self.lms.get_book(1)
        self.assertEqual(book.title, "Book 1")
        self.assertEqual(book.author, "Author 1")
        self.assertEqual(book.isbn, "ISBN1")
        self.assertEqual(book.publication_year, 2021)
        self.assertTrue(book.available)

    def test_add_user(self):
        self.lms.add_user(1, "User 1", "user1@example.com")
        user = self.lms.get_user(1)
        self.assertEqual(user.name, "User 1")
        self.assertEqual(user.email, "user1@example.com")
        self.assertFalse(user.is_staff)

    def test_add_staff_user(self):
        self.lms.add_user(2, "Staff User", "staff@example.com", is_staff=True)
        user = self.lms.get_user(2)
        self.assertEqual(user.name, "Staff User")
        self.assertEqual(user.email, "staff@example.com")
        self.assertTrue(user.is_staff)

    # def test_display_book_info(self):
    #     self.lms.add_book(2, "Book 2", "Author 2", "ISBN2", 2022)
    #     expected_output = "Title: Book 2\nAuthor: Author 2\nISBN: ISBN2\nPublication Year: 2022\nAvailable: Yes\n"
    #     with self.assertLogs() as logs:
    #         self.lms.display_book_info(2)
    #     self.assertEqual(logs.output, [f"INFO:root:{expected_output}"])

if __name__ == '__main__':
    unittest.main()