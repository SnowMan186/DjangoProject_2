from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from .models import Message, Recipient
from .forms import MessageForm


@login_required
@permission_required('mailings.view_all', raise_exception=True)
def dashboard(request):
    return render(request, 'dashboard.html')

def home(request):
    return render(request, 'home.html')

def messages(request):
    messages = Message.objects.all()
    return render(request, 'messages.html', {'messages': messages})

def add_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('messages')
    else:
        form = MessageForm()
    return render(request, 'add_message.html', {'form': form})

def edit_message(request, id):
    message = Message.objects.get(pk=id)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('messages')
    else:
        form = MessageForm(instance=message)
    return render(request, 'edit_message.html', {'form': form})

def delete_message(request, id):
    message = Message.objects.get(pk=id)
    message.delete()
    return redirect('messages')

def recipients(request):
    recipients = Recipient.objects.all()
    return render(request, 'recipients.html', {'recipients': recipients})