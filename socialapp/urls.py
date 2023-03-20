from django.urls import path, include
from rest_framework import routers
from .views import TagList, PostList, PostDetail, LikeCreate, LikeList

router = routers.DefaultRouter()
router.register(r'tags', TagList)
router.register(r'likes', LikeList)

urlpatterns = [
    path('', PostList.as_view(), name='post-list'),
    path('<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('like/', LikeCreate.as_view(), name='like-create'),
    path('', include(router.urls)),
]
