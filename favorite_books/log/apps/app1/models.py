from __future__ import unicode_literals
from django.db import models
import re




class UserManager(models.Manager):
	def basic_validator(self, data):
		errors = {}
		if len(data['first']) < 2:
			errors['first'] = "Get yourself a longer name"
		if len(data['last']) < 2:
			errors['last'] = "Your name is not long enough"
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		if not EMAIL_REGEX.match(data['email']):
			errors['email'] = "Invalid email address!"
		if User.objects.filter(email=data['email']):
			errors['email'] = "That email is already in use"
		if len(data['password']) < 8:
			errors['password'] = "Passwords must be at least 8 characters long"
		if data['confirm'] != data['password']:
			errors['confirm'] = "Your passwords do not match"
		return errors


class User(models.Model):
	first = models.CharField(max_length=30)
	last = models.CharField(max_length=30)
	email = models.CharField(max_length=40)
	password = models.CharField(max_length=40)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class BookManager(models.Manager):
	def basic_validator(self, dat):
		errors = {}
		if len(dat['title']) < 2:
			errors['title'] = "A title is required"
		if len(dat['desc']) < 5:
			errors['desc'] = "If this is one of your favorite books then you should be able to give a short description"
		return errors

class Book(models.Model):
	title = models.CharField(max_length=155)
	desc = models.TextField()
	user = models.ForeignKey(User, related_name="books")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = BookManager()

class Favorite(models.Model):
	favorite = models.BooleanField()
	user = models.ForeignKey(User, related_name="favorites")
	book = models.ForeignKey(Book, related_name="favorites")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)