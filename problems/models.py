from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Signup(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    contact = models.CharField(max_length=11)
    area = models.CharField(max_length=30)
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class problem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploadingdate = models.DateTimeField(auto_now=True)
    area = models.CharField(max_length=30)
    field = models.CharField(max_length=30)
    problemfile = models.FileField(null=True)
    filetype = models.CharField(max_length=30)
    description = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=15)


    def __str__(self):
        return self.field


class solve(models.Model):
    problem = models.ForeignKey(problem, on_delete=models.CASCADE)
    solution = models.TextField()
    solver = models.ForeignKey(Signup, on_delete=models.CASCADE)

    def __str__(self):
        return self.problem.field
