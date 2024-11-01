from django.urls import path

from support import views

app_name = 'support'

urlpatterns = [
    path('create/', views.TicketCreateView.as_view(), name='create_ticket'),
    path('my-tickets/', views.UserTicketListView.as_view(), name='user_ticket_list'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('tickets/<int:pk>/close/', views.TicketCloseView.as_view(), name='ticket_close'),
    path('manage/', views.ManageTicketListView.as_view(), name='manage_ticket_list'),
]