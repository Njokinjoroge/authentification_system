
from django.db import models
from users.models import User

class Role(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class BusinessElement(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class AccessRoleRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE)
    can_read = models.BooleanField(default=False)
    can_write = models.BooleanField(default=False)
