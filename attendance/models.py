from django.db import models

# Create your models here.

class Student(models.Model):
    roll_no = models.IntegerField(primary_key = True, unique = True)
    name = models.CharField(max_length = 80)
    email = models.EmailField(max_length=100)
    parent_email = models.EmailField(max_length=100)
    hostel = models.CharField(max_length = 5)
    room_no = models.CharField(max_length = 7)
    image = models.ImageField(upload_to='attendance/static/attendance/images')
    
    def __str__(self) -> str:
        return str(self.roll_no)

class Date(models.Model):
    date = models.DateField(blank = True, auto_now = True)

    def __str__(self) -> str:
        return str(self.date)

class Attendance(models.Model):
    date = models.ForeignKey(Date, on_delete = models.CASCADE)
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    status = models.CharField(max_length = 1)

    def __str__(self) -> str:
        return f"{self.student.roll_no} {self.date.date}"

class Contact(models.Model):
    name = models.CharField(max_length = 80)
    email = models.CharField(max_length = 100)
    query = models.CharField(max_length = 300)

    def __str__(self) -> str:
        return str(self.id)