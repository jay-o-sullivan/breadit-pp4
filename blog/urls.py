# blog urls
from django.urls import path
from . import views
from .views import post_upvote, post_downvote
urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('profile/', views.profile, name='profile'),
    path('create_post/', views.create_post, name='create_post'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('<slug:slug>/upvote/', post_upvote, name='post_upvote'),
    path('<slug:slug>/downvote/', post_downvote, name='post_downvote'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    
]
