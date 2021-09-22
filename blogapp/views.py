from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from .forms import CustomUserCreationForm
from .models import Post_Blog,Comment_Section
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy,reverse

# Create your views here.
def home(request):
	count = User.objects.count()
	return render(request,'home.html',{'count':count})

def signup(request):
	if request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = CustomUserCreationForm()
	return render(request,'registration/signup.html',{'form':form})

def Display(request):
	if request.user.is_authenticated:
		current_user_id= request.user.id
		data = Post_Blog.objects.all()
		return render(request,'registration/display.html',{'data':data})

def Add(request):
	print('Hii')
	if request.method=="POST":
		form = AddForm(request.POST,request.FILES)
		if form.is_valid():
			Title = form.cleaned_data['title']
			Content = form.cleaned_data['content']
			Status = form.cleaned_data['status']
			Image = form.cleaned_data['img']
            
			obj = Post_Blog(title=Title,content=Content,img = Image,status=Status,author_id=request.user.id)
			obj.save()
			data = Post_Blog.objects.all()
			return render(request,'registration/display.html',{'data':data})
	form = AddForm()
	return render(request,'registration/add.html',{'form':form})

def Delete(request,id):
	data = Post_Blog.objects.get(id=id)
	data.delete()
	obj = Post_Blog.objects.all()
	#return render(request,'registration/myposts.html',{'obj':obj})
	return HttpResponseRedirect(reverse('myposts'))

def MyPosts(request):
	if request.user.is_authenticated:
		data = Post_Blog.objects.filter(author_id=request.user.id)
		return render(request,'registration/myposts.html',{'data':data})
def PostDetail(request,id):
	global flag
	flag = id
	data = Post_Blog.objects.get(id=id)
	author_data = User.objects.get(id=data.author_id)
	is_liked=False
	if data.likes.filter(id=request.user.id).exists():
		is_liked=True
	total=data.total_likes()
	print(data.img.url)
	return render(request,'registration/postdetail.html',{'data':data,'author_data':author_data,'is_liked':is_liked,'total':total})
def like_post(request,id):
	post = Post_Blog.objects.get(id=id)
	is_liked=False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		is_liked=False
	else:
		post.likes.add(request.user)
		is_liked=True	
	return HttpResponseRedirect(reverse('post_detail',args=[str(id)]))
def Comment(request):
	print(flag)
	commentperpost = Comment_Section.objects.filter(post_id=flag) 
	data = Post_Blog.objects.get(id=flag)
	author_data = User.objects.get(id=data.author_id)
	if request.method=="POST":
		comment = request.POST['comment']
		print(flag)
		user = User.objects.get(id = request.user.id)
		obj = Comment_Section(content=comment,user=user,post_id=flag)
		obj.save()
		commentperpost = Comment_Section.objects.filter(post_id=flag)
		return render(request,'registration/postdetail.html',{'data':data,'author_data':author_data,'commentperpost':commentperpost})
	return render(request,'registration/postdetail.html',{'data':data,'author_data':author_data,'commentperpost':commentperpost})

def Edit(request,id):
	return HttpResponseRedirect(reverse('myposts'))
