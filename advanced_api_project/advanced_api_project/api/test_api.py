from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book, Author

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test admin user
        self.user = User.objects.create_user(username='testuser', password='testpass', is_staff=True)
        
        # Create a test author
        self.author = Author.objects.create(name="Test Author")
        
        # Create a test book
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            publication_year=2021
        )
        
        # Log in the test user
        self.client.login(username='testuser', password='testpass')
        
    def test_create_book(self):
        url = reverse('book_list_create_api')
        data = {
            "title": "New Book",
            "author": self.author.id,
            "publication_year": 2022
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(id=2).title, 'New Book')

    def test_update_book(self):
        url = reverse('book_detail_update_delete_api', args=[self.book.id])
        new_author = Author.objects.create(name="Updated Author")
        data = {
            "title": "Updated Book",
            "author": new_author.id,
            "publication_year": 2023
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
        self.assertEqual(self.book.author.name, 'Updated Author')

    def test_delete_book(self):
        url = reverse('book_detail_update_delete_api', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_list_books(self):
        url = reverse('book_list_create_api')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_book(self):
        url = reverse('book_detail_update_delete_api', args=[self.book.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

    def test_permissions(self):
        self.client.logout()
        url = reverse('book_list_create_api')
        data = {
            "title": "Unauthorized Book",
            "author": self.author.id,
            "publication_year": 2024
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)