from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('profile-update/<int:id>', views.update_user_profile, name='profile_update'),
    path('add-profile',views.create_profile,name='add_profile' ),
    path('view-profile',views.view_user_profile, name="view-user-profile"),
    path('user-fileupload', views.user_file_upload, name='user-file-upload'),
    path('posts', views.view_posts, name='view-posts'),
    path('comment/<int:id>', views.user_comment, name='comment'),
    path('more-about-post/<int:id>',views.more_about_post, name='more-post-info')
]