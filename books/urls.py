from django.urls import path, include
from books.views import BooksViewSet, RequestViewSet, TicketViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'books', BooksViewSet)
router.register(r'requests', RequestViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
