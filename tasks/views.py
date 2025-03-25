from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from authentication.models import User
from .models import Task, TaskAssign
from rest_framework.decorators import api_view
from .serializer import TaskSerializer,TaskAssignSerializer
import logging
logging.basicConfig(filename='error.log',level=logging.ERROR)


# Create Task
@csrf_exempt
@api_view(['POST'])
def create_task(request):
        try:
            print("Type:::",type(request.user.id))
            data = json.loads(request.body)
            title = data.get("title")
            description = data.get("description", "")
            priority = data.get("priority", "medium")
            due_date = data.get("due_date", None)

            # Check if the user is an admin
            if not request.user.is_superuser:
              return JsonResponse({"status": "failed", "error": "Only admins can assign tasks"}, status=403)

            try:
              admin = User.objects.get(id=request.user.id)
            except User.DoesNotExist:
              return JsonResponse({"status": "failed", "error": "Admin with this token not found"}, status=404)
            # Create the task
            task = Task.objects.create(
                title=title,
                description=description,
                admin_id = admin,
                priority=priority,
                due_date=due_date
            )

            return JsonResponse({
                "status": "success",
                "message": "Task assigned successfully",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "admin_id": task.admin_id.username,
                    "priority": task.priority,
                    "due_date": task.due_date,
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"status": "failed", "error": "Invalid JSON"}, status=400)


# Assign Task
@csrf_exempt
@api_view(['POST'])
def assign_task(request):
    try:
      # Check if the user is an admin
      if not request.user.is_superuser:
        return JsonResponse({"status": "failed", "error": "Only admins can assign tasks"}, status=403)
      # Get the task id and the user id
      data = json.loads(request.body)
      task_id = data.get("task_id")
      assigned_by_id = request.user.id
      assigned_to_id = data.get("assigned_to")
      try:
        task = Task.objects.get(id=task_id)
      except Task.DoesNotExist:
        return JsonResponse({"status": "failed", "error": "Task with this id not found"}, status=404)
      try:
        assigned_to = User.objects.get(id=assigned_to_id)
      except User.DoesNotExist:
        return JsonResponse({"status": "failed", "error": "User with this id not found"}, status=404)
      try:
        assigned_by = User.objects.get(id=assigned_by_id)
      except User.DoesNotExist:
        return JsonResponse({"status": "failed", "error": "User with this username not found"}, status=404)
      
      # Check if the task is already assigned to this user or not
      if TaskAssign.objects.filter(task_id=task, assigned_to=assigned_to).exists():
        return JsonResponse({
            "status": "failed",
            "error": "This task is already assigned to this user"
        }, status=400)
      # Query to assign a task
      task_assign = TaskAssign.objects.create(
        task_id=task,
        assigned_by=assigned_by,
        assigned_to=assigned_to
      )
      return JsonResponse({"status": "success","message": "Task assigned successfully",
        "task": {
          "id": task.id,
          "title": task.title,
          "assigned_by": task.admin_id.email,
          "assigned_to": task_assign.assigned_to.email,
          "priority": task.priority,
          "due_date": task.due_date,
          "status": task_assign.status,
        }
      }, status=201)
        
    except Exception as e:
        return JsonResponse({"status": "failed to assign task", "error": str(e)}, status=400)


#get all task created by an admin
@csrf_exempt
@api_view(['GET'])
def get_tasks(request):
    try:
      # Check if the user is an admin
      if not request.user.is_superuser:
        return JsonResponse({"status": "failed", "error": "Only admins can assign tasks"}, status=403)
      # Get the task id and the user id
      try:
        task = Task.objects.filter(admin_id=request.user.id)
        task_data =  TaskSerializer(task,many=True).data
      except Task.DoesNotExist:
        return JsonResponse({"status": "failed", "error": "Task with this id not found"}, status=404)
      return JsonResponse({"status": "success","message": "Task Get successfully","task": task_data}, status=200)
    except Exception as e:
        return JsonResponse({"status": "failed to fetch tasks", "error": str(e)}, status=400)
          

#get all task assigned to an user
@api_view(['GET'])
def get_assigned_tasks(request):
    try:
      if not request.user.is_superuser:
        return JsonResponse({"status": "failed", "error": "You are not to perform this operation"}, status=400)
      tasks = TaskAssign.objects.filter(assigned_by_id=request.user.id).select_related("task_id", "assigned_to")
      task_data = TaskAssignSerializer(tasks, many=True).data
      return JsonResponse({"status": "success", "message": "Task Get successfully", "task": task_data}, status=200)
    except Exception as e:
      return JsonResponse({"status": "failed to fetch tasks", "error": str(e)}, status=400)



@api_view(['GET'])
def get_tasks_assigned_status(request,status:str):
    try:
      if not request.user.is_superuser:
        return JsonResponse({"status": "failed", "error": "You are not to perform this operation"}, status=400)
      tasks = TaskAssign.objects.filter(assigned_by_id=request.user.id,status=status).select_related("task_id", "assigned_to")
      task_data = TaskAssignSerializer(tasks, many=True).data
      return JsonResponse({"status": "success", "message": "Task Get successfully", "task": task_data}, status=200)
    except Exception as e:
      return JsonResponse({"status": "failed to fetch tasks", "error": str(e)}, status=400)
        

@api_view(['GET'])
def get_tasks_assigned_by_userid(request,user_id:int):
    try:
      if not request.user.is_superuser:
        return JsonResponse({"status": "failed", "error": "You are not to perform this operation"}, status=400)
      tasks = TaskAssign.objects.filter(assigned_by_id=request.user.id,assigned_to_id=user_id).select_related("task_id", "assigned_to")
      task_data = TaskAssignSerializer(tasks, many=True).data
      return JsonResponse({"status": "success", "message": "Task Get successfully", "task": task_data}, status=200)
    except Exception as e:
      return JsonResponse({"status": "failed to fetch tasks", "error": str(e)}, status=400)