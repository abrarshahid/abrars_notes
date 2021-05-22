from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="BlogHome" ),
    path('suggest-post/',views.suggestpost,name="SuggestPost" ),
    path('search/',views.search,name="search" ),
    path('signup/',views.handleSignup,name="signup" ),
    path('login/',views.handleLogin,name="login" ),
    path('logout/',views.handleLogout,name="logout" ),
    path('blogpost/<str:slug>',views.blogpost,name="blogPost" ),
    path('postComment',views.postComment,name="postComment"),
    path('postLike',views.postLike,name="postLike"),
    path('removeLike',views.removeLike,name="removeLike")
]