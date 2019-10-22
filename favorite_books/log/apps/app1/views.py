from django.shortcuts import render, redirect
import bcrypt
from .models import *
from django.contrib import messages
from django.db.models import Count

def index(request):
	return render(request, 'app1/index.html')

def register(request):
	errors = User.objects.basic_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		if request.method == "POST":
			password = request.POST['password']
			pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

			user = User.objects.create(first=request.POST['first'], last=request.POST['last'], email=request.POST['email'], password=pw_hash)
			request.session['userid'] = user.id
			messages.success(request, "Successfully logged in")
			return redirect('/books')

def login(request):

	if request.method == "POST":
		email = User.objects.filter(email=request.POST['l_email'])
		if email:
			user = email[0]
			if bcrypt.checkpw(request.POST['l_password'].encode(), user.password.encode()):
				request.session['userid'] = user.id

				return redirect('/books')
			else: 
				messages.error(request, "Incorrect password")
				return redirect('/')
		else:
			messages.error(request, "User does not exist")
			return redirect('/')

def books(request):
	if 'userid' not in request.session:
		return redirect('/')
	else:
		num = request.session['userid']
		context = {
			"user" : User.objects.get(id=num),
			"books" : Book.objects.all(),
			# "posters" : User.objects.all()
		}
		return render (request, 'app1/books.html', context)

def add(request):
	errors = Book.objects.basic_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/books')
	else:
		num = request.session['userid']
		user = User.objects.get(id=num)
		if request.method == "POST":
			book = Book.objects.create(title=request.POST['title'], desc=request.POST['desc'], user=user)
			Favorite.objects.create(favorite=True, user=user, book=book)
		return redirect('/books')

def clear(request):
	request.session.clear()
	return redirect('/')

def favor(request, number):
	if request.method == "POST":
		num = request.session['userid']
		user = User.objects.get(id=num)
		book = Book.objects.get(id=number)
		Favorite.objects.create(favorite=True, user=user, book=book)
	return redirect(f'/books/{number}')

def unfavor(request, number):
	num = request.session['userid']
	user = User.objects.get(id=num)
	book = Book.objects.get(id=number)
	number = number
	favorite = Favorite.objects.get(book=book, user=user)
	if request.method == "POST":
		favorite.delete()
		return redirect(f'/books/{number}')

def info(request, number):
	num = request.session['userid']
	user = User.objects.get(id=num)
	book = Book.objects.get(id=number)
	favorites = Favorite.objects.filter(book=book)
	favorite = Favorite.objects.filter(book=book, user=user).count()
	context = {
		'book': book,
		'user': user,
		'favorites': favorites,
		'favor' : favorite
	}
	return render(request, 'app1/info.html', context)

def delete(request, number):
	num = request.session['userid']
	user = User.objects.get(id=num)
	book = Book.objects.get(id=number)
	if request.method == "POST":
		book.delete()
		return redirect('/books')

def update(request, number):
	
	book = Book.objects.get(id=number)
	context = {
		
		'book': book
	}
	return render(request, 'app1/update.html', context)

def edit(request, number):
	num = request.session['userid']
	user = User.objects.get(id=num)
	book = Book.objects.get(id=number)
	if request.method == "POST":
		book.title = request.POST['title']
		book.desc = request.POST['desc']
		book.save()
		return redirect('/books')