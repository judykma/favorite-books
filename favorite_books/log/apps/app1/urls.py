from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^books$', views.books),
	url(r'^clear$', views.clear),
	url(r'^add$', views.add),
	url(r'^favor/(?P<number>\d+)$', views.favor),
	url(r'^books/(?P<number>\d+)$', views.info),
	url(r'^unfavor/(?P<number>\d+)$', views.unfavor),
	url(r'^delete/(?P<number>\d+)$', views.delete),
	url(r'^update/(?P<number>\d+)$', views.update),
	url(r'^edit/(?P<number>\d+)$', views.edit)

]