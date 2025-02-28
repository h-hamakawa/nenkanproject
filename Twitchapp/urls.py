from django.urls  import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name='Twitchapp'
urlpatterns=[
    path('',views.IndexView.as_view(), name='index'),
    path('Twitch index/',views.IndexView.as_view(), name='Twitch index'),
    path('profile_done/',views.ProfileSuccessView.as_view(), name='profile_done'),
    path('profile/create/', views.ProfileCreateView.as_view(), name='profile_create'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('post/', views.post_create_view, name='post_create'),
    path('video/<int:pk>/', views.VideoDetailView.as_view(), name='video_detail'),
    path('video/<int:pk>/comment/', views.post_comment, name='post_comment'),
    path('search/', views.UserSearchView.as_view(), name='search'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<int:pk>/follow/', views.FollowToggleView.as_view(), name='follow_toggle'),
    path('contents/', views.ContentListView.as_view(), name='contents'),
   path('contents/', views.ContentListView.as_view(template_name='contents.html'), name='contents'),
      path('contents/<str:game_tag>/', views.ContentListView.as_view(template_name='game_tag_videos.html'), name='game_tag_videos'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)