from django.urls import re_path

from rent import views

app_name = 'rent'

urlpatterns = [
    re_path(r'^my-rentals/$', views.RentalUserListView.as_view(), name='rental_user_list'),
    re_path(r'^all/$', views.RentalManagerListView.as_view(), name='rental_manager_list'),
    #
    re_path(r'^create/(?P<model_id>\d+)$', views.RentalCreateView.as_view(), name='rental_create'),
    re_path(r'^cancel/(?P<pk>\d+)/$', views.RentalCancelView.as_view(), name='rental_cancel'),
    re_path(r'^finish/(?P<pk>\d+)/$', views.RentalFinishView.as_view(), name='rental_finish'),
    re_path(r'^detail/(?P<pk>\d+)/$', views.RentalDetailView.as_view(), name='rental_detail'),
]