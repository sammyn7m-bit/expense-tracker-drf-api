from django.shortcuts import render
from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user = self.request.user).order_by("-date", "created_at")

    def perform_create(self, serializer):
        serializer.save(user = swlf.request.user)
