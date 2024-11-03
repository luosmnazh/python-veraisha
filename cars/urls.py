from django.urls import re_path

from cars import views

app_name = 'cars'

urlpatterns = [
    re_path(r'^$', views.IndexPageView.as_view(), name='index'),
    re_path(r'^cars/filter/$', views.filter_cars, name='filter_cars'),
    re_path(r'^cars/create/$', views.CarCreateView.as_view(), name='create_car'),
    re_path(r'^cars/model/(?P<model_id>\d+)/$', views.CarListView.as_view(), name='car_list_manager'),
    re_path(r'^cars/$', views.CarModelListView.as_view(), name='car_models'),
    #
    re_path(r'^car/(?P<pk>\d+)/maintenance/add/$', views.CarMaintenanceCreateView.as_view(), name='maintenance_add'),
    re_path(r'^car/(?P<pk>\d+)/maintenances/$', views.CarMaintenancesView.as_view(), name='car_maintenance'),
    re_path(r'^car/(?P<pk>\d+)/delete/$', views.CarDeleteView.as_view(), name='car_delete'),
    re_path(r'^car/(?P<pk>\d+)/edit/$', views.CarUpdateView.as_view(), name='car_update'),
    #
    re_path(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
]
