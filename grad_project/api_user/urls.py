from django.urls import path
from . import views

app_name = 'api_user'
urlpatterns = [
    path('', views.UserView.as_view()), #User에 관한 API를 처리하는 view로 Request를 넘김
    #path('<int:id>', views.UserView.as_view()), #User pk id가 전달되는 경우
    path('<str:model>', views.UserView.as_view()),  # User pk id가 전달되는 경우
    #path(r'^<int:id>/$', views.UserView.as_view()),
]
