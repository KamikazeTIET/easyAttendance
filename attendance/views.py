from django.contrib import messages
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from .camera import VideoCamera
from .models import Attendance, Contact, Student, Date
import csv
import cv2
import numpy as np
import face_recognition
import os
import datetime

# Create your views here.


def index(request):
    return render(request, 'attendance/index.html')

@login_required(login_url="/login")
def mark(request):
    return render(request, 'attendance/mark.html')

@login_required(login_url="/login")
def manualMark(request):
    if request.method=="POST":
        roll_no = request.POST['roll_no']
        status = request.POST['status']
        try:
            student = Student.objects.get(roll_no=roll_no)
        except Student.DoesNotExist:
            messages.error(request, "Invalid Roll Number")
            return redirect("/mark-manual")
        try:
            date = Date.objects.get(date=datetime.date.today())
        except Date.DoesNotExist:
            addDate()
            date = Date.objects.get(date=datetime.date.today())
        student.attendance_set.get(date=date).status = status
        messages.error(request, "Attendance marked succesfully")
        return redirect("/mark-manual")
    return render(request, 'attendance/manual_mark.html')

def view(request):
    try:
        date = Date.objects.get(date=datetime.date.today())
    except Date.DoesNotExist:
        addDate()
        date = Date.objects.get(date=datetime.date.today())
    passStd = date.attendance_set.filter(status='P')
    abstStd = date.attendance_set.filter(status='A')
    context = {
        'present': passStd,
        'absent': abstStd
    }
    return render(request, 'attendance/view.html', context=context)

@login_required(login_url="/login")
def hostelDashboard(request):
    return render(request, "attendance/hostel_authority_dashboard.html")

def sendMails(request):
    try:
        date = Date.objects.get(date=datetime.date.today())
    except Date.DoesNotExist:
        return
    students = date.attendance_set.filter(status='A')
    receivers = []
    for student in students:
        receivers.append(student.student.parent_email)
    message = ('Your ward absent', f"Your ward was absent from hostel on {date.date} night", 'askandola07@gmail.com', receivers)
    send_mass_mail((message, ))
    messages.success(request, "Mails sent successfully")
    return redirect('/')

def login_view(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            messages.warning(request, "Invalid username or password")
            return redirect('/login')
        login(request, user)
        if 'next' in  request.POST:
            return redirect(request.POST["next"])
        return redirect("/hostel-dashboard")
    return render(request, "attendance/login_page.html")

def logout_view(request):
    if request.user.is_anonymous:
        return redirect("/")
    logout(request)
    return redirect("/")

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        query = request.POST['message']
        entry = Contact(name=name, email=email, query=query)
        entry.save()
        messages.success(request, "Thankyou for contacting us.")
    return redirect('/')

@login_required(login_url='/login')
def export_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers = {'Content-Disposition': 'attachment; filename="record.csv"'}
    )
    writer = csv.writer(response)
    dates = Date.objects.all()
    columns = ['Sr. No.', 'Student Roll Number', 'Student Name', 'Student Hostel', 'Student Room No.']
    for date in dates:
        columns.append(str(date.date))
    writer.writerow(columns)
    students = Student.objects.all()
    count = 0
    for student in students:
        count += 1
        row = [str(count), str(student.roll_no), student.name, student.hostel, student.room_no]
        for attendance in student.attendance_set.all():
            row.append(attendance.status)
        writer.writerow(row)
    return response

def addDate():
    date = Date()
    date.save()
    students = Student.objects.all()
    for student in students:
        entry = Attendance(student=student, date=date, status='A')
        entry.save()

def markAttendance(roll_no):
    try:
        date = Date.objects.get(date=datetime.date.today())
    except Date.DoesNotExist:
        addDate()
        date = Date.objects.get(date=datetime.date.today())
    try:
        student = Student.objects.get(roll_no=roll_no)
    except Student.DoesNotExist:
        return
    attendance = Attendance.objects.get(student=student, date=date)
    attendance.status = 'P'
    attendance.save()

def gen(camera):
    images = []
    RollNo = []
    # myList = os.listdir(path)
    myList = []
    students = Student.objects.all()
    for student in students:
        myList.append(os.path.relpath(student.image.path))
        RollNo.append(str(student.roll_no))
    print(myList)
    for cl in myList:
        ImgRn = cv2.imread(cl)
        
        images.append(ImgRn)
        # RollNo.append(os.path.splitext(cl)[0])
    print(RollNo)

    def findEncodings(images):
        EList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            EList.append(encode)
        return EList
    
    EListKnown = findEncodings(images)
    print('Encoding Complete')

    while True:
        img = camera.get_frame()

        if img is None:
            print("Null Object")
            break

        imgFinal = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgFinal = cv2.cvtColor(imgFinal, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgFinal)
        encodesCurFrame = face_recognition.face_encodings(imgFinal, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(EListKnown, encodeFace)
            faceDis = face_recognition.face_distance(EListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                RNo = RollNo[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, RNo, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (127, 0, 255), 2)
                markAttendance(int(RNo))

        # frame_flip = cv2.flip(img, 1)
        _, frame = cv2.imencode('.jpg', img)
        frame = frame.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def videoStream(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                    content_type='multipart/x-mixed-replace; boundary=frame')