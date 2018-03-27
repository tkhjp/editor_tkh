from django.urls import path
from django.conf.urls import url, include


from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('<int:question_upload_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_upload_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_upload_id>/edit_answer/', views.edit_answer, name='edit'),
]