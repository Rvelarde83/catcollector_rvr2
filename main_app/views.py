from django.shortcuts import render
from django.http import HttpResponse

# Demo Cat Data - Replace with Database

class Cat:
  def __init__(self, name, breed, description, age):
    self.name = name
    self.breed = breed
    self.description = description
    self.age = age

cats = [
  Cat('Lolo', 'tabby', 'foul little demon', 3),
  Cat('Yoda', 'himalayan', 'orange ball of fluff', 15),
  Cat('Kajit', 'black cat', 'the best cat ever that ran away', 4)
]    


# Create your views here.

def home(request):
  return HttpResponse('<h1>Hello World /ᐠ｡‸｡ᐟ\ﾉ</h1>')


def about(request):
  # To send back raw text or an html string use 'HttpResponse'
  # return HttpResponse('About Page')
  # To send back a full template file use 'render'
  return render(request, 'about.html')


def cats_index(request):
  return render(request, 'cats/index.html', {'cats': cats })