from abc import abstractmethod
from django.contrib.auth import logout
from django.core.checks.messages import Error
from django.shortcuts import redirect, render
from .models import Courses, Payment, UserCourse, Video
from django.http import HttpResponse
from .forms import Registration_form, Login_form
from django.views import View
from elearning.settings import *
from django.contrib.auth.decorators import login_required
from time import time
import razorpay
from django.views.decorators.csrf import  csrf_exempt
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


def home(request):
    courses_list = Courses.objects.all()
    return render(request, 'home.html', {'courses':courses_list}) 


def course_slug(request, slug):
    course = Courses.objects.get(slug = slug)
    serial_number = request.GET.get('lecture')
    videos = course.video_set.all().order_by('serial_number')

    

    if not serial_number:
        serial_number = 1
    video = Video.objects.get(serial_number=serial_number, course=course)

    if video.is_preview is False:
        if request.user.is_authenticated is False :
            return redirect('login')

        else:
            userCourse = None
            user = request.user
            try:
                userCourse = UserCourse.objects.get(course=course, user=user)
                print(userCourse)
            except:
                if userCourse is None:
                    return redirect('checkoutpage', slug = course.slug)

    
   


    context = {
        'videos':videos,
        'video':video,
        'course':course,
        'slug':slug
    }
    return render(request, template_name = 'course_page.html', context = context)


class signupView(View):

    def get(self, request):
        form = Registration_form()
        context = {
            'form':form
        }
        return render(request, 'signup.html', context)

    def post(self, request):
        form = Registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')

        return render(request, 'signup.html', {'form':form})


class loginView(View):
    def get(self, request):
        form = Login_form()
        context = {
            'form':form
        }

        return render(request, 'login.html', context)
    
    def post(self, request):
        form = Login_form(request=request, data=request.POST)
        if form.is_valid():
            return redirect('homepage')
        return render(request, 'login.html', {'form':form})


def signout(request):
    logout(request)
    return redirect('homepage')


def checkout(request, slug):
    course = Courses.objects.get(slug = slug)
    user = request.user
    if not request.user.is_authenticated:
        return redirect('login')
    action = request.GET.get('action')
    order = None
    payment = None
    user_course = None
    error = None
    if action == 'create_payment':

        try:
            user_course = UserCourse.objects.get(user = user, course=course )
            print(user_course)
            error = 'Course Already purchase'
            # return HttpResponse('<Script>alert("Course Already purchase")</script>')
        except:       
            amount = (course.price - (course.price * course.discount * 0.01)) * 100
            currency = 'INR'
            receipt = f"vaibhav-{int(time())}"
            notes = {
                "email" : user.email,
                "name" : f'{user.first_name} {user.last_name}'
            }

            order = client.order.create(data = {
                'amount':amount,
                'currency':currency,
                'receipt':receipt,
                'notes':notes,

            })

            payment = Payment()
            payment.user = user
            payment.course = course
            payment.order_id = order.get('id')
            payment.save()



        
    context = {
        'course':course,
        'order':order,
        'payment':payment,
        'user': user,
        'error':error
    }

    return render(request, 'checkout.html', context)

@csrf_exempt
def verify_payment(request):    
    if request.method == 'POST':
        data = request.POST
        print(data)
        context = {}
        try:
            client.utility.verify_payment_signature(data)
            
            razorpay_payment_id = data['razorpay_payment_id']
            razorpay_order_id = data['razorpay_order_id']
            razorpay_signature = data['razorpay_signature']

            payment = Payment.objects.get(order_id = razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True

            user_course = UserCourse(user = payment.user, course = payment.course)
            user_course.save()


            payment.user_course = user_course
            payment.save()



           
            return render(request, 'my_courses.html', context)
        except:
            return HttpResponse('Payment Failed')


@login_required(login_url='login')
def mycourses(request):
    user = request.user
    user_course =   UserCourse.objects.filter(user = user)

    context = {
        "user_course":user_course
    }

    return render(request, 'my_courses.html', context)