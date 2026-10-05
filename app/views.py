from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth import logout 
from django.contrib.auth.hashers import make_password, check_password 
from app.models import Disorders 
import pandas as pd 
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import accuracy_score

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmPassword')
        contact = request.POST.get('contact')
        address = request.POST.get('address')

        if password == confirmpassword:
            if Disorders.objects.filter(email=email).exists():
                messages.error(request, f"This Email ID Already Exists, Try Another")
                return redirect('register')
            else:
                hash_password = make_password(password)
                queryset  = Disorders(name=name, email=email, password=hash_password, contact=contact, address=address)
                queryset.save()
                messages.success(request, f"User Register Successfully, Thank You")
                return redirect('login')
        else:
            messages.error(request, f"Password and Confirm Password do not match, Try Again")
            return redirect('register')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = Disorders.objects.filter(email=email).first()
        if user:
            if check_password(password, user.password):
                messages.success(request, f"User Login Successfully")
                return redirect('home')
            else:
                messages.error(request, f"Invalid Password, Try Again")
                return redirect('login')
        else: 
            messages.error(request, f"User Not Found, Please Register")
            return redirect('login')
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def view_dataset(request):
    df = pd.read_csv('app/Final_dataset.csv')
    column = df.head(200).to_html()
    return render(request, 'view_dataset.html', {'col':column})


df = pd.read_csv('app/Final_dataset.csv')
x = df.drop('Class', axis=1) 
y = df['Class']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


def prediction(request):
    msg = None
    if request.method == 'POST':
        num1 = request.POST.get('num1')
        num2 = request.POST.get('num2')
        num3 = request.POST.get('num3')
        num4 = request.POST.get('num4')
        num5 = request.POST.get('num5')
        num6 = request.POST.get('num6')
        num7 = request.POST.get('num7')
        num8 = request.POST.get('num8')
        num9 = request.POST.get('num9')
        num10 = request.POST.get('num10')
        num11 = request.POST.get('num11')
        num12 = request.POST.get('num12')
        num13 = request.POST.get('num13')
        num14 = request.POST.get('num14')
        num15 = request.POST.get('num15') 

        input = [[num1, num2, num3, num4, num5, num6, num7, num8, num9, num10, num11, num12, num13, num14, num15]]

        rf = RandomForestClassifier()
        rf.fit(x_train, y_train)
        predict = rf.predict(input)

        if predict == 0:
            msg = "Prediction of Psychiatric Disorders is Addictive disorder"
        elif predict == 1:
            msg = "Prediction of Psychiatric Disorders is Anxiety disorder"
        elif predict == 2:
            msg = "Prediction of Psychiatric Disorders is Healthy control"
        elif predict == 3:
            msg = "Prediction of Psychiatric Disorders is Mood disorder"
        elif predict == 4:
            msg = "Prediction of Psychiatric Disorders is Obsessive compulsive disorder"
        elif predict == 5:
            msg = "Prediction of Psychiatric Disorders is Schizophrenia"
        elif predict == 6:
            msg = "Prediction of Psychiatric Disorders is Trauma and stress related disorder"
            
        return render(request, 'prediction.html', {'msg': msg})

    return render(request, 'prediction.html')

def view_logout(request):
    logout(request)
    messages.success(request, f"User Logout Successfully")
    return redirect('login')
