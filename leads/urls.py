from django.urls import path
from.views import  lead_create, lead_detail, lead_list,lead_update,lead_delete,LeadListView,LeadDetailView,LeadCreateView,LeadUpdateView,LeadDeleteView,CategoryList

app_name="leads"
urlpatterns=[
path('',LeadListView.as_view(),name="lead_list"),
path('<int:pk>/',LeadDetailView.as_view(),name="lead_detail"),
path('create/',LeadCreateView.as_view(),name="lead_create"),
path('<int:pk>/update',LeadUpdateView.as_view(),name="lead_update"),
path('<int:pk>/delete',LeadDeleteView.as_view(),name="lead_delete"),
path('categories/',CategoryList.as_view(),name="categories"),









]