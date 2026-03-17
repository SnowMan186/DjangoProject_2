from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page

from .form import MailingForm, MessageForm, RecipientForm
from .models import Message, Recipient


@login_required
@permission_required("mailings.view_all", raise_exception=True)
def dashboard(request):
    return render(request, "dashboard.html")


@cache_page(60 * 15)
def home(request):
    return render(request, "home.html")


def messages(request):
    messages = Message.objects.all()
    return render(request, "messages.html", {"messages": messages})


def add_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("messages")
    else:
        form = MessageForm()
    return render(request, "add_message.html", {"form": form})


def edit_message(request, id):
    message = Message.objects.get(pk=id)
    if request.method == "POST":
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect("messages")
    else:
        form = MessageForm(instance=message)
    return render(request, "edit_message.html", {"form": form})


def delete_message(request, id):
    message = Message.objects.get(pk=id)
    message.delete()
    return redirect("messages")


@login_required
def recipients(request):
    recipients = Recipient.objects.filter(owner=request.user)
    return render(request, "recipients.html", {"recipients": recipients})


@login_required
def add_recipient(request):
    if request.method == "POST":
        form = RecipientForm(request.POST)
        if form.is_valid():
            recipient = form.save(commit=False)
            recipient.owner = request.user
            recipient.save()
            return redirect("recipients")
    else:
        form = RecipientForm()
    return render(request, "add_recipient.html", {"form": form})


@login_required
def add_mailing(request):
    if request.method == "POST":
        form = MailingForm(request.POST)
        if form.is_valid():
            mailing = form.save(commit=False)
            mailing.owner = request.user
            mailing.save()
            return redirect("mailings")
    else:
        form = MailingForm()
    return render(request, "add_mailing.html", {"form": form})


@login_required
def launch_mailing(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    if mailing.status == "created":
        mailing.status = "started"
        mailing.save()
        send_message.delay(mailing.pk)
    return redirect("mailings")
