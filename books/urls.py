from django.urls import path, include
from books.views import BooksViewSet, RequestViewSet, IssueViewSet, ReturnViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'books', BooksViewSet)
router.register(r'requests', RequestViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'returns', ReturnViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
