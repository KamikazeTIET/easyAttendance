from django.contrib import admin
from .models import Student, Date, Attendance, Contact

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'name', 'hostel', 'room_no')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date_display', 'student_roll', 'student_name', 'student_hostel', 'status')
    def date_display(self, obj):
        return str(obj.date.date)
    def student_roll(self, obj):
        return str(obj.student.roll_no)
    def student_name(self, obj):
        return str(obj.student.name)
    def student_hostel(self, obj):
        return str(obj.student.hostel)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')

admin.site.register(Date)

admin.site.site_header = "Hostel Attendance Management System"
admin.site.site_title = "Hostel Attendance Management System"
admin.site.index_title = "Welcome to Hostel Attendance Management System"
