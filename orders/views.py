from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
	response = "Home Page"
	return HttpResponse(response)
