from django.urls import path
from .views import ExpenseListCreateView, ExpenseDetailView, CategoryListCreateView,CategoryDetailView

urlpatterns =[
    path("", ExpenseListCreateView.as_view(), name = "expense-list-create"),
    path("<int:pk>/", ExpenseDetailView.as_view(), name = 'expense-detail'),

    path("categories/",CategoryListCreateView.as_view(),name="category-list-create",),
    path("categories/<int:pk>/", CategoryDetailView.as_view(),name="category-detail",),
]
