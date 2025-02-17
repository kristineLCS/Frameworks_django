from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Inbox
from .forms import InboxForm

@login_required
def inbox(request):
    inbox = Inbox.objects.filter(receiver=request.user, is_archived=False).order_by('-timestamp')
    return render(request, 'message/inbox.html', {'inbox': inbox})

@login_required
def sent_messages(request):
    inbox = Inbox.objects.filter(sender=request.user).order_by('-timestamp')
    return render(request, 'message/message_sent.html', {'inbox': inbox})

@login_required
def message_detail(request, inbox_id):
    inbox = get_object_or_404(Inbox, id=inbox_id, receiver=request.user)
    inbox.is_read = True  # Mark as read
    inbox.save()
    return render(request, 'message/message_details.html', {'inbox': inbox})

@login_required
def send_message(request):
    if request.method == "POST":
        form = InboxForm(request.POST)
        if form.is_valid():
            inbox = form.save(commit=False)
            inbox.sender = request.user  # Ensure sender is assigned
            if 'receiver' in form.cleaned_data:
                inbox.receiver = form.cleaned_data['receiver']  # Assign receiver
            inbox.save()
            return redirect('inbox')
    else:
        form = InboxForm()
    
    return render(request, 'message/send_message.html', {'form': form})

@login_required
def archived_messages(request):
    archived_msgs = Inbox.objects.filter(receiver=request.user, is_archived=True)
    return render(request, 'message/archived_messages.html', {'archived_msgs': archived_msgs})


@login_required
def archive_inbox(request, inbox_id):
    inbox = get_object_or_404(Inbox, id=inbox_id, receiver=request.user)
    inbox.is_archived = True
    inbox.save()
    return redirect('archived_messages')
