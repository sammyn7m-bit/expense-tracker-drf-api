from django.shortcuts import render
from .models import Expense, Category
from .serializers import ExpenseSerializer, CategorySerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


#view all the categories
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# create a category
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# Create and view the expenses
class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user = self.request.user).order_by("-date", "created_at")

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


# update/delete an expense
class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user = self.request.user)

