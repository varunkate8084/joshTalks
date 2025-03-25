from django.db import models
from authentication.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    title = models.CharField(max_length=255)  
    description = models.TextField(blank=True, null=True) 
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")  
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")  
    due_date = models.DateTimeField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.title} - {self.assigned_to.username}"



class TaskAssign(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_assignments")
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_assigned")
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_received")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} - {self.assigned_by.username} -> {self.assigned_to.username}"
    
    
    
    