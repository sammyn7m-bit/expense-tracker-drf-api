from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import User
from expenses.models import Expense, Category


class ExpenseAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="sammy",
            email="sammy@example.com",
            password="Testpass123"
        )

        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(
            name="Food",
            description="Food and meals"
        )

        self.expense = Expense.objects.create(
            user=self.user,
            title="Lunch",
            amount="250.00",
            category=self.category,
            description="Lunch at school",
            date=date(2026, 9, 16)
        )

    def test_list_expenses(self):
        url = reverse("expense-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_expense(self):
        url = reverse("expense-list-create")

        data = {
            "title": "Transport",
            "amount": "100.00",
            "category": self.category.id,
            "description": "Bus fare",
            "date": "2026-09-17"
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(Expense.objects.count(), 2)
        self.assertEqual(response.data["title"], "Transport")

    def test_retrieve_expense(self):
        url = reverse(
            "expense-detail",
            kwargs={"pk": self.expense.id}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Lunch")

    def test_update_expense(self):
        url = reverse(
            "expense-detail",
            kwargs={"pk": self.expense.id}
        )

        data = {
            "amount": "300.00",
            "description": "Lunch and a drink"
        }

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], "300.00")

    def test_delete_expense(self):
        url = reverse(
            "expense-detail",
            kwargs={"pk": self.expense.id}
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(Expense.objects.count(), 0)

    def test_user_cannot_access_another_users_expense(self):
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="Testpass123"
        )

        other_expense = Expense.objects.create(
            user=other_user,
            title="Private Expense",
            amount="500.00",
            category=self.category,
            date=date(2026, 9, 17)
        )

        url = reverse(
            "expense-detail",
            kwargs={"pk": other_expense.id}
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_unauthenticated_user_cannot_access_expenses(self):
        self.client.force_authenticate(user=None)

        url = reverse("expense-list-create")
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class CategoryAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="categoryuser",
            email="category@example.com",
            password="Testpass123"
        )

        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(
            name="Food",
            description="Food and meals"
        )

    def test_list_categories(self):
        url = reverse("category-list-create")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data), 1)

    def test_create_category(self):
        url = reverse("category-list-create")

        data = {
            "name": "Transport",
            "description": "Transport expenses"
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(Category.objects.count(), 2)

    def test_retrieve_category(self):
        url = reverse(
            "category-detail",
            kwargs={"pk": self.category.id}
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(response.data["name"], "Food")

    def test_update_category(self):
        url = reverse(
            "category-detail",
            kwargs={"pk": self.category.id}
        )

        data = {
            "name": "Groceries"
        }

        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(response.data["name"], "Groceries")

    def test_delete_category(self):
        url = reverse(
            "category-detail",
            kwargs={"pk": self.category.id}
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(Category.objects.count(), 0)
