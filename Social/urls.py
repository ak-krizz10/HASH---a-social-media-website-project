from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.webpage,name='frontpage'),
    
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('createprofile', views.createProfile, name='createprofile'),
    
    path('feed', views.feed, name='feed'),
    path('Thoughtsfeed', views.tweetfeed, name='tweetfeed'),
    path('search', views.search, name='search'),
    path('notifications', views.notifications, name='notifications'),
    # path('screentime',views.screen_time_view,name='screentime'),
    
    path('newpost',views.NewPost,name='newpost'), 
    path('newtweet', views.createtweet, name='newtweet'),
    
    path('@<username>', views.profile, name='profilee'),
    path('@<username>/saved', views.profile, name='savedd'),
    path('@<username>/thoughts', views.profile, name='thoughts'),
    path('@<username>/screentime', views.profile, name='screentime'),
    path('editprofile', views.editProfile, name='editprofile'),
    path('<int:id>/<int:status>', views.followuser, name='follownow'),
    
    path('@<username>/<slug:slug>/', views.PostDetail, name='post-details'),
    path('#tag/<slug:tag_slug>', views.tags, name='tags'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('fetch_post_comments/<int:post_id>/', views.fetch_post_comments, name='fetch_post_comments'),
    path('like', views.like, name='like'),
    path('<int:post_id>/saved', views.saved, name='saved'),
    
    path('tweet-details/<int:id>/', views.TweetDetail, name='tweet-details'),
    path('liketweet', views.liketweet, name='liketweet'),
    
    #Reset password
    path('reset_password',auth_views.PasswordResetView.as_view(template_name="reset_pass.html"),name="reset_password"),
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name="reset_pass_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name="reset_pass_confirm.html"),name="password_reset_confirm"),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name="reset_pass_done.html"),name="password_reset_complete"),
   
    
    path('password_change', views.password_change, name='password_change'),
    
    # path('tweetopen/<int:id>',views.tweet_replies,name="twt_open"),   
    # path('newtweet',views.createtweet),
    # path('edittweet/<int:id>',views.edittweet,name="twt_edit"),
    # path('deletetweet/<int:id>',views.deletetweet,name="twt_del"), 
    
    # path('profile', views.profile, name='profile'),
    # path('my_profile', views.my_profile, name='my_profile'),
    # path('<username>/follow/<option>', views.follow, name='follow'),
    # path('usertweets',views.userprofile),
     
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

