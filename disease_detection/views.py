import base64
from .ml.predict import predict_disease
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'signup.html')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def detect(request):
    if request.method == 'POST':
        image = None
        try:
            # 📁 File upload
            if request.FILES.get('image'):
                image = request.FILES['image']
            # 📸 Camera capture (base64)
            elif request.POST.get('captured_image'):
                format, imgstr = request.POST['captured_image'].split(';base64,')
                ext = format.split('/')[-1]
                image = ContentFile(base64.b64decode(imgstr), name='captured.' + ext)
            # ❌ No image provided
            if image is None:
                return render(request, 'detect.html', {'error': 'No image provided'})
            # 🔥 ML Prediction
            result, confidence, prevention = predict_disease(image)
            print("Prediction:", result, confidence)
            # 💾 Store in session
            request.session['result'] = result
            request.session['confidence'] = confidence
            request.session['prevention'] = prevention
            return redirect('result')
        except Exception as e:
            print("Error:", e)
            return render(request, 'detect.html', {'error': 'Error processing image'})
    return render(request, 'detect.html')

@login_required
def result(request):
    result = request.session.get('result')
    confidence = request.session.get('confidence')
    prevention = request.session.get('prevention')
    print("Session result:", result, confidence)
    return render(request, 'result.html', {
        'result': result,
        'confidence': confidence,
        'prevention':prevention
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')