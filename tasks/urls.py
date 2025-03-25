from django.urls import path
from . import views
urlpatterns = [
  path('create_task', views.create_task, name='assign_task'),
  path('assign_task', views.assign_task, name='assign_task'),
  path('get_tasks', views.get_tasks, name='get_tasks'),
  path('get_assigned_tasks',views.get_assigned_tasks, name='get_assigned_tasks'),
  path('get_assigned_tasks/<str:status>',views.get_tasks_assigned_status, name='get_pending_tasks_assigned_by_admin'),
  path('get_assigned_task_by_userid/<int:user_id>',views.get_tasks_assigned_by_userid, name='get_tasks_assigned_by_userid'),
]