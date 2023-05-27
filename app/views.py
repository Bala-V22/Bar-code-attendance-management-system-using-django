from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import studends, Detected,staff
from .forms import studentForm,ManualForm,StaffForm
import cv2
import pickle
# import face_recognition
import datetime
from cachetools import TTLCache
import datetime 
from django.shortcuts import render, HttpResponse
import random
from barcode import EAN13
from barcode.writer import ImageWriter
from barcode.base import Barcode
import numpy as np
import cv2 as cv
from multiprocessing.pool import ThreadPool
from collections import deque
import dbr
from dbr import *
import time
import cv2
from pyzbar import pyzbar
from django.shortcuts import  render, redirect
from .forms import studentForm,StaffForm
from django.contrib.auth import login, authenticate #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import pymysql
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def main():
    # global code
    code=[]
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        try:
            if code[0] != None:
                camera.release()
                cv2.destroyAllWindows()
        except:
            pass 

        try:  
            barcodes = pyzbar.decode(frame)

            for barcode in barcodes:
                barcode_text = barcode.data.decode('utf-8')
                code.append(barcode_text)
                print(barcode_text)
            # frame = read_barcodes(frame)
            # print(text)
            cv2.imshow('Barcode reader', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        except:
            pass    

    camera.release()
    cv2.destroyAllWindows()
    return code


def create(name):
    Barcode.default_writer_options['write_text'] = False
    
    number = str(random.randint(100000000000,999999999999))    

    my_code = EAN13(number, writer=ImageWriter())
    numbers = "{}.{}".format(number, name)
    my_code.save("bar/"+numbers)
    return numbers

def send_mail_barcode(path):
    from_addr="pythonfabhost2021@gmail.com"
    SMTP_PASSWORD = 'frqrvtpbohkqfoxk'
    to_addr="pythonfabhost2022@gmail.com"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Your attendence barcode"
    # msg['From'] = from_addr
    # msg['To'] = to_addr

    text = MIMEText('<img src="cid:image1">', 'html')
    msg.attach(text)

    image = MIMEImage(open(path, 'rb').read())

    # Define the image's ID as referenced in the HTML body above
    image.add_header('Content-ID', '<image1>')
    msg.attach(image)
    server = smtplib.SMTP('smtp.gmail.com', 25)
    server.connect("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.login(from_addr, SMTP_PASSWORD)
    server.sendmail(from_addr, student_mail, msg.as_string())
    server.quit()

import json
times = 0
def register(request):
    global times
    print('Register Page Opened!')
    times += 1
    current_url = request.path
    print(current_url)
    print(0)
    if request.path == '/register/signup/':
        report_loc = '../signup/'
    else: report_loc = 'signup/'
    return render(request, 'register.html', {'loc':report_loc,'error': ''})
    
def signup(request):
    pass


def loged_page(request):
    pass
    return render(request, 'login.html')

def signin(request):
    pass




cache = TTLCache(maxsize=20, ttl=60)
def mail(mail):
    import smtplib
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("pythonfabhost2021@gmail.com", "ynjohoeoaupmrtaf")
    message = "absent"
    s.sendmail("pythonfabhost2021@gmail.com", mail, message)
    s.quit()

def identify1(id,path):
    
    timestamp = str(datetime.datetime.now(tz=timezone.utc))

    now = datetime.datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)  
    print(id, timestamp)
    cache[id] = 'detected'
    path = "bar/{}.png".format(path)
    if current_time <= '18:40:00':
        try:
            emp = studends.objects.get(id=id)
            print(emp)
            emp.detected_set.create(time_stamp=timestamp, photo=path)
        except Exception as e:
            print(e)  

def manual_attent(frame, name):
    if name in cache:
        return
    timestamp = str(datetime.datetime.now(tz=timezone.utc))
        
    print(name, timestamp)
    cache[name] = 'detected'
    path = "C:/Users/PYTHONFABHOST/Downloads/Face_recognition-master/Face_recognition-master/media//{}.jpg".format(name)
    write_path = path
    print(name)
    # cv2.imwrite(write_path, frame)
    emp = studends.objects.get(name=name)
    print(emp)
    try:
        emp = studends.objects.get(name=name)
        print("hello",emp)
        emp.detected_set.create(time_stamp=timestamp, photo=path)
    except:           
        pass


def index(request):
    return render(request, 'app/index.html')

def about(request):
    return render(request, 'app/about.html')

def admin(request):
    return render(request, 'app/admin.html')


def video_stream(request):
    pass
    return HttpResponseRedirect(reverse('index'))


def add_photos(request):
    print(studends.objects.all())
    emp_list = studends.objects.all()
    print(emp_list)
    return render(request, 'app/add_photos.html', {'emp_list': emp_list})


def create_barcode(request, emp_id):
    # cam = cv2.VideoCapture(0)
    # emp = get_object_or_404(studends, id=emp_id)
    # click(emp.name, emp.id, cam)
    path=create(emp_id)
    # camera.release()
    cv.destroyAllWindows()
    full_path='bar/{}.png'.format(path)
    send_mail_barcode(full_path)

    return HttpResponseRedirect(reverse('index'))


def log(request):
    # trainer()
    return render(request,'login.html')


def absent(request):
    

    if request.method == 'GET':
        date_formatted = datetime.datetime.today().date()
        date = request.GET.get('search_box', None)
        if date is not None:
            date_formatted = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        det_list = Detected.objects.filter(time_stamp__date=date_formatted).order_by('time_stamp').reverse()
        # det_list = Detected.objects.all()
        # print(det_list)
        nm=[]
        for det in det_list:
            nm.append(det.emp_id)
        print(nm)
            
        # ex=Employee.objects.get(id='1')
        ex=studends.objects.all()
        # # ex1=[]
        # # for det1 in ex:
        # #     ex1.append(det1.emp_id)
        # # print(nm)
        not_attent=[]
        for n in ex:
            if n not in nm:
                not_attent.append(n)

        print('n',not_attent)

        print(list(ex))
        # mail()
        all_mail=[]
        for i in not_attent:
            all_mail.append(i.email)
        print(all_mail)
        if request.method == 'GET':
            data1 = request.GET.get('all mail', None)
            if(data1 == 'all_mail'):
                for i in all_mail:
                    mail(i)


        

    # det_list = Detected.objects.all().order_by('time_stamp').reverse()
    return render(request, 'app/absent.html', {'det_list': not_attent, 'date': date_formatted,'all_mail':all_mail})


def send_mail(request):
    if request.method == 'GET':
        send = request.GET.get('send mail', None)
        mail(send)
    return HttpResponseRedirect(reverse('index'))


def detected(request):
    if request.method == 'GET':
        date_formatted = datetime.datetime.today().date()
        date = request.GET.get('search_box', None)
        if date is not None:
            date_formatted = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        det_list = Detected.objects.filter(time_stamp__date=date_formatted).order_by('time_stamp').reverse()
        # det_list = Detected.objects.all()
        # print(det_list)
        nm=[]
        for det in det_list:
            nm.append(det.emp_id)
        print(nm)
            
        # ex=Employee.objects.get(id='1')
        ex=studends.objects.all()
        # # ex1=[]
        # # for det1 in ex:
        # #     ex1.append(det1.emp_id)
        # # print(nm)
        not_attent=[]
        for n in ex:
            if n not in nm:
                not_attent.append(n)

        print('n',not_attent)

        print(list(ex))
        

    # det_list = Detected.objects.all().order_by('time_stamp').reverse()
    return render(request, 'app/detected.html', {'det_list': det_list, 'date': date_formatted})



def identify(request):
    # video_capture = cv2.VideoCapture(0)
    # identify_faces(video_capture)
    import glob
    import os
    code=main()
    img_path=glob.glob("bar/*")
    print(img_path)
    head, tail = os.path.split(str(img_path))
    tail=tail.split('.')
    first=[]
    second=[]
    for i in img_path:
        head, tail = os.path.split(str(i))
        tail=tail.split('.')
        first.append(tail[0])
        second.append(tail[1])
    print('The first name  '+ str (first))
    print('The second name  '+ str (second))   
    codes=str(code[0])
    codes=codes[0:12] 
    print(codes[0:12])
    # print(codes,first)
    if codes in first:
        print('Enter in attendence')
        ID=first.index(codes)
        path='{}.{}'.format(first[ID],second[ID])
        print(ID)
        student_id=(second[ID])
        identify1(student_id,path)
    else:
        print('First step is not completed')    
    print (tail)

    return HttpResponseRedirect(reverse('index'))

def add(name):
    print(studends.objects.all())
    emp_list = studends.objects.filter(name=name)
    print(emp_list)
    return emp_list

def add_s(name):
    print(staff.objects.all())
    emp_list = staff.objects.filter(name=name)
    print(emp_list)
    return emp_list    


def login(request):
    while True:                                                 
        if request.method == "POST":
            print('Enter in the post method---------------------------------------')
            id = request.POST['id']
            mail = request.POST['email']
            con=pymysql.connect(db='barcode',host='localhost',user='root',password='jillabala',autocommit=True)
            cur =con.cursor()
            get=[]


            cur.execute("SELECT * FROM student WHERE id ='"+ id +"'")
            results = cur.fetchall()
            print(results)
            print('Enter in the Student database---------------------------------------')

            if len(results)==0:
                cur.execute("SELECT * FROM staff WHERE id ='"+ id +"'")
                results = cur.fetchall()
                print(results) 
                print('Enter in the Staff database---------------------------------------')
                get.append('staff')
            else:
                get.append('student')


            if get[0]=='student':
                print('Opening student---------------------------------------')
                return render(request,'app/student.html')
            elif get[0]=='staff':
                print('Opening Staff---------------------------------------')
                return render(request, 'app/staff.html')
            else:
                return render(request, 'login.html')
        return render(request, 'app/index.html')
        
def com(request):
    return render(request, 'app/complain.html')

def stu_back(request):
    return render(request, 'app/student.html')

def add_emp(request):
    return render(request, 'app/reg.html')


def add_staff(request):
    if request.method == "POST":
        form = StaffForm(request.POST)
        print(form)
        if form.is_valid():
            emp = form.save()
            if form.is_valid():
                id = request.POST['id']
                name = request.POST['name']
                mail = request.POST['email']
                con=pymysql.connect(db='barcode',host='localhost',user='root',password='jillabala',autocommit=True)
                cur =con.cursor()

                while True:
                    cur.execute("SELECT * FROM staff WHERE ID ='"+ id +"'")
                    results = cur.fetchall()
                    print(results)
                    break
                if len(results)==0:
                    sql="INSERT INTO staff(ID,name,mail) VALUES(%s,%s,%s)"
                    val=(id,name,mail)
                    cur.execute(sql,val)
            print(emp)
            # post.author = request.user
            # post.published_date = timezone.now()
            # post.save()
            emp_list=add_s(emp)
            return render(request, 'login.html', {'emp_list': emp_list})
            # return HttpResponseRedirect(reverse('add'))
    else:
        form = StaffForm()
    return render(request, 'app/add_staff.html', {'form': form})


def add_stu(request):
    if request.method == "POST":
        form = studentForm(request.POST)
        print(form)
        if form.is_valid():
            emp = form.save()
            if form.is_valid():
                id = request.POST['id']
                name = request.POST['name']
                global student_mail
                mail = request.POST['email']
                student_mail=mail
                con=pymysql.connect(db='barcode',host='localhost',user='root',password='jillabala',autocommit=True)
                cur =con.cursor()
                                   
                while True:
                    cur.execute("SELECT * FROM student WHERE ID ='"+ id +"'")
                    results = cur.fetchall()
                    print(results)
                    break
                if len(results)==0:
                    sql="INSERT INTO student(ID,name,mail) VALUES(%s,%s,%s)"
                    val=(id,name,mail)
                    cur.execute(sql,val)
            print(emp)
            # post.author = request.user
            # post.published_date = timezone.now()
            # post.save()
            emp_list=add(emp)
            return render(request, 'app/add_photos.html', {'emp_list': emp_list})
            # return HttpResponseRedirect(reverse('add'))
    else:
        form = studentForm()
    return render(request, 'app/add_emp.html', {'form': form})    


def add_attent(request):
    # if request.method == "POST":
    #     form = ManualForm(request.POST)
    #     print(form)
    #     if form.is_valid():
    #         emp = form.save()
    #         # post.author = request.user
    #         # post.published_date = timezone.now()
    #         # post.save()
    #         return HttpResponseRedirect(reverse('index'))
    # else:
    #     form = ManualForm()
    import datetime
    date_formatted = datetime.datetime.today().date()
    date = request.GET.get('search_box', None)
    if date is not None:
        date_formatted = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    det_list = Detected.objects.filter(time_stamp__date=date_formatted).order_by('time_stamp').reverse()
    # query="SELECT * FROM dt_table WHERE date BETWEEN date('now') AND date('now','3 day')"
    # date_1 = datetime.datetime.strptime(datetime.datetime.now(), "%m/%d/%y")
    from datetime import  timedelta
    end_date = Detected.objects.filter(time_stamp__gte = datetime.datetime.now() - timedelta(days=3)) 
    # dt=Detected.objects.filter(time_stamp__gte=date_1 ,time_stamp__lte=end_date )
    # print('e',end_date)
    
        # det_list = Detected.objects.all()
        # print(det_list)
    nm=[]
    for det in det_list:
        nm.append(det.emp_id)
    print(nm)
            
        # ex=Employee.objects.get(id='1')
    ex=studends.objects.all()
        # # ex1=[]
        # # for det1 in ex:
        # #     ex1.append(det1.emp_id)
        # # print(nm)
    not_attent=[]
    for n in ex:
        if n not in nm:
            not_attent.append(n)
    for n in ex:
        if n not in end_date:
            print(n)

    print('n',not_attent)

    print(list(ex))
        # mail()
    all_mail=[]
    for i in not_attent:
        all_mail.append(i.name)
    print(all_mail)
    if request.method == 'GET':
        data1 = request.GET.get('send mail', None)
        frame=None
        if data1:
            manual_attent(frame, data1)
        
    # return render(request, 'app/add_attent.html', {'form': form})
    return render(request, 'app/add_attent.html', {'det_list': not_attent, 'date': date_formatted,'all_mail':all_mail})

def threedays_absent(request):
        from datetime import  timedelta
        det_list = Detected.objects.filter(time_stamp__gte = datetime.datetime.now() - timedelta(days=3)) 
        nm=[]
        for det in det_list:
            nm.append(det.emp_id)
        print(nm)
        ex=studends.objects.all()
        not_attent=[]
        for n in ex:
            if n not in nm:
                not_attent.append(n)

        print('n',not_attent)

        print(list(ex))
        # mail()
        all_mail=[]
        for i in not_attent:
            all_mail.append(i.email)
        print(all_mail)
        if request.method == 'GET':
            data1 = request.GET.get('all mail', None)
            if(data1 == 'all_mail'):
                for i in all_mail:
                    mail(i)


        

        return render(request, 'app/three.html', {'det_list': not_attent, 'all_mail':all_mail})




