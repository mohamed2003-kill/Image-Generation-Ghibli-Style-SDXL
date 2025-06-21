from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse, HttpResponse

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not username or not email or not password1 or not password2:
            messages.error(request, 'All fields are required.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        else:
            try:
                user = CustomUser.objects.create_user(username=username, email=email, password=password1)
                login(request, user)
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'Username already exists.')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required(login_url='login')
def chat_view(request):
    return render(request, 'chat.html')
import json
@login_required(login_url='login')
def generate_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        data = json.loads(request.body)
        prompt = data['prompt']
        print("here is the prompt :",prompt)
        print("here is the request parameters :",request.body)
        if not prompt:
            return JsonResponse({'status': 'error', 'message': 'No prompt provided'}, status=400)
        # Forward the request to the Flask backend
        response = requests.post('https://78ac-34-124-253-83.ngrok-free.app/generate', json={'prompt': prompt})
        return JsonResponse(response.json(), status=response.status_code)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)

@login_required(login_url='login')
def progress_view(request):
    # Forward the request to the Flask backend
    response = requests.get('https://78ac-34-124-253-83.ngrok-free.app/progress')
    if response.headers.get('Content-Type') == 'image/png':
        # Return the image directly
        return HttpResponse(response.content, content_type='image/png')
    return JsonResponse(response.json())
