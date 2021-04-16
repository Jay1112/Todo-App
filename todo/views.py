from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import sys 
from  .forms import TaskForm
from .models import Task

def home(request):
	form = TaskForm()
	tasks = Task.objects.filter(user=request.user)
	if not request.user.is_authenticated:
		return redirect("/login/")
	if request.method == "POST":
		form = TaskForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			return redirect("/")
	context = {"form":form,"tasks":tasks}
	return render(request,"todo/home.html",context)

def edit(request,id):
	instance = Task.objects.get(id=id)
	form = TaskForm(instance=instance)
	context = {"id":id,"form":form}

	if request.method == "POST":
		form = TaskForm(request.POST,instance=instance)

		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			return redirect("/")

	return render(request,"todo/edit.html",context)

def delete(request,id):
	instance = Task.objects.get(id=id)

	if request.method == "POST":
		instance = Task.objects.filter(id=id).delete()
		return redirect("/")

	context = {"id":id,"task":instance}
	return render(request,"todo/delete.html",context)

