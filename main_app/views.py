from django.shortcuts import render
from .models import Cat
# from django.http import HttpResponse

# Demo Cat Data - Replace with Database

# class Cat:
#   def __init__(self, name, breed, description, age):
#     self.name = name
#     self.breed = breed
#     self.description = description
#     self.age = age

# cats = [
#   Cat('Lolo', 'tabby', 'foul little demon', 3),
#   Cat('Yoda', 'himalayan', 'orange ball of fluff', 15),
#   Cat('Kajit', 'black cat', 'the best cat ever that ran away', 4),
#   Cat('Simone', 'Russian Blue', ' slow cat', 8)
# ]    


# Create your views here.

def home(request):
  # return HttpResponse('<h1>Hello World /ᐠ｡‸｡ᐟ\ﾉ</h1>')
  return render(request, 'home.html')


def about(request):
  # To send back raw text or an html string use 'HttpResponse'
  # return HttpResponse('About Page')
  # To send back a full template file use 'render'
  return render(request, 'about.html')


def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', { 'cats': cats })


def cats_detail(request, cat_id):
  ## Get the the individual cat
  cat = Cat.objects.get(id=cat_id)
  ## render template, pass it the cat
  return render(request, 'cats/detail.html', { 'cat': cat })


  