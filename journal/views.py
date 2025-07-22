from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import MoodEntry
from .forms import MoodEntryForm
import matplotlib.pyplot as plt
import os
import io
import base64

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard(request):
    entries = MoodEntry.objects.filter(user=request.user).order_by('-date')[:7]
    moods = [e.mood for e in entries][::-1]
    dates = [e.date.strftime("%b %d") for e in entries][::-1]

    plt.figure(figsize=(5, 3))
    plt.plot(dates, moods, marker='o')
    plt.title("Mood Over Time")
    plt.ylim(0, 10)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    return render(request, 'journal/dashboard.html', {'entries': entries, 'chart': chart})

@login_required
def add_entry(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('dashboard')
    else:
        form = MoodEntryForm()
    return render(request, 'journal/add_entry.html', {'form': form})
