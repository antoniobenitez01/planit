from django.shortcuts import render
from django.http import HttpResponse

def login_page(request):
    return render(request, 'login.html')

def main_page(request):
    return render(request, 'main.html')
