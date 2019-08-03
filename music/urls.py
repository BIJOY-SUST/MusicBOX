from django.urls import path,re_path
from music import views as user_view
from django.conf import  settings
from django.contrib.auth import views as auth_views


app_name = 'music'

urlpatterns = [

    path('testing/',user_view.testing,name='testing'),
    path('testing2/',user_view.testing2,name='testing2'),
    path('testing3/',user_view.testing3,name='testing3'),

    path('', user_view.index, name='index'),
    path('register/', user_view.register, name='register'),
    # account confirmations
    # path('activate/<uid>/<token>/', views.activate,name='activate'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',user_view.activate,name='activate'),

    path('login_user/', user_view.login_user, name='login_user'),
    path('logout_user/', user_view.logout_user, name='logout_user'),


    path('feed/', user_view.feed, name='feed'),
    path('<int:album_id>/p_album', user_view.p_album, name='p_album'),

    path('index2/', user_view.index2, name='index2'),
    path('<int:album_id>/detail_public', user_view.detail_public, name='detail_public'),

    path('<int:album_id>/', user_view.detail, name='detail'),
    path('<int:song_id>/favorite/', user_view.favorite, name='favorite'),
    re_path(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', user_view.songs, name='songs'),
    # path('songs/<char:filter_by>/', views.songs, name='songs'),
    path('create_album/', user_view.create_album, name='create_album'),
    path('<int:album_id>/create_song/', user_view.create_song, name='create_song'),


    path('<int:album_id>/delete_song/<int:song_id>/', user_view.delete_song, name='delete_song'),
    path('<int:album_id>/favorite_album/', user_view.favorite_album, name='favorite_album'),
    path('<int:album_id>/delete_album/', user_view.delete_album, name='delete_album'),

    path('<int:album_id>/delete_palbum/', user_view.delete_palbum, name='delete_palbum'),




]