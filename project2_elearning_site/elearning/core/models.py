from django.db import models
from django.contrib.auth.models import User


# Course Models

class Courses(models.Model):
    name = models.CharField(max_length=30, null=True)
    slug = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to = "files/thumbnails")
    date = models.DateTimeField(auto_now_add=True)
    resources = models.FileField(upload_to='files/resources')
    length = models.IntegerField(null=False)


    def __str__(self):
        return self.name


    

class courseProperty(models.Model):
    description = models.CharField(max_length=50, null=False)
    Courses = models.ForeignKey(Courses, null=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Tag(courseProperty):
    pass
    
class Prerequisite(courseProperty):
    pass
    
class Learning(courseProperty):
    pass
   

# viedo Models

class Video(models.Model):

    title  = models.CharField(max_length = 100 , null = False)
    course = models.ForeignKey(Courses , null = False , on_delete=models.CASCADE)
    serial_number = models.IntegerField(null=False)
    video_id = models.CharField(max_length = 100 , null = False)
    is_preview = models.BooleanField(default = False)

    def __str__(self):
        return self.title

class UserCourse(models.Model):
    user = models.ForeignKey(User , null = False , on_delete=models.CASCADE)
    course = models.ForeignKey(Courses , null = False , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.name}'

class Payment(models.Model):
    order_id = models.CharField(max_length = 50 , null = False)
    payment_id = models.CharField(max_length = 50)
    user_course = models.ForeignKey(UserCourse , null = True , blank = True ,  on_delete=models.CASCADE)
    user = models.ForeignKey(User ,  on_delete=models.CASCADE)
    course = models.ForeignKey(Courses , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)