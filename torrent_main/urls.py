from django.urls import path

from torrent_main import views

urlpatterns = [
    # home/
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('torrent/<slug:slug>/', views.TorrentDetailView.as_view(), name='torrent_detail'),
    path('download/<slug:slug>/', views.download_torrent, name='download_torrent'),
    path('create-torrent/', views.TorrentCreation.as_view(), name='create_torrent'),
    path('filter/', views.filter, name='filter'),
]
