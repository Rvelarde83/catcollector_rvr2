from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from .forms import FeedingForm
from .models import Cat, Toy, Photo
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = "rv-collector"


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
    return render(request, 'cats/index.html', {'cats': cats})


def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    # Get the toys the cat doesn't have
    toys_cat_doesnt_have = Toy.objects.exclude(
        id__in=cat.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', {
        'cat': cat, 'feeding_form': feeding_form,
        # Add the toys to be displayed
        'toys': toys_cat_doesnt_have
    })


def add_feeding(request, cat_id):
    # create the ModelForm using the data in request.POST
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the cat_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('detail', cat_id=cat_id)


def add_photo(request, cat_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension also
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, cat_id=cat_id)
            photo.save()
        except:
            print('An error occurred')
    return redirect('detail', cat_id=cat_id)


def assoc_toy(request, cat_id, toy_id):
    # Note that you can pass a toy's id instead of the whole object
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)


def rm_cat_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('detail', cat_id=cat_id)


class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    success_url = '/cats/'


class CatUpdate(UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']


class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'


class ToyList(ListView):
    model = Toy


class ToyDetail(DetailView):
    model = Toy


class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'


class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']


class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'
