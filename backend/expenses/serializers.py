from rest_framework import serializers

from .models import Expense, Category


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
             "id","title", "amount", "category", "description", "date",
             "created_at",
          ]
        read_only_fields =[  "id", "created_at"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =[ "id", "name", "description",]
        read_only_fields = ["id"]
