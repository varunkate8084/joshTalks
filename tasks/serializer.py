from rest_framework import serializers
from .models import Task,TaskAssign

class TaskSerializer(serializers.ModelSerializer):
    admin_email = serializers.CharField(source='admin_id.email',read_only=True)
    admin_username = serializers.CharField(source='admin_id.username',read_only=True)
  
    class Meta:
      model = Task
      fields = ['title','description','admin_email','status','priority','due_date','admin_username']


# from rest_framework import serializers
# from .models import TaskAssign

class TaskAssignSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task_id.title', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    assigned_to_email = serializers.CharField(source='assigned_to.email', read_only=True)
    assigned_by_username = serializers.CharField(source='assigned_by.username', read_only=True)
    assigned_by_email = serializers.CharField(source='assigned_by.email', read_only=True)
    class Meta:
        model = TaskAssign
        fields = ['id', 'task_id', 'task_title',"status",'assigned_to','assigned_to_username','assigned_to_email','assigned_by_username','assigned_by_email','assigned_by','created_at']
