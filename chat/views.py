from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from chat.models import *
from django.contrib.auth.models import User

# Create your views here.


def checkonline(request):
    if request.user.is_authenticated:
        return True
    else:
        return False


@login_required
def dm(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads' : threads
    }
    return render(request, 'inbox.html', context)

def sample(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread')
    context = {
        'Threads' : threads
    }
    return render(request, 'messages.html', context)

def newthread(request,id):
    receiver=User.objects.get(id=id)
    sender=User.objects.get(username=request.user)

    check=Thread.objects.filter(first_person=sender,second_person=receiver)
    rev_check=Thread.objects.filter(first_person=receiver,second_person=sender)
    if check or rev_check:
        return redirect(dm)
    else:
        newthread=Thread.objects.get_or_create(first_person=sender,second_person=receiver)   
    return redirect(dm)


# @login_required
# def inbox(request):
#     user = request.user
#     messages = Message.get_message(user=user)
#     active_direct = None
#     directs = None

#     if messages:
#         message = messages[0]
#         active_direct = message['user'].username
#         directs = Message.objects.filter(user=user, recipient=message['user'])
#         directs.update(is_read=True)

#         for message in messages:
#             if message['user'].username == active_direct:
#                 message['unread'] = 0
#     context = {
#         'directs' : directs,
#         'active_direct' : active_direct,
#         'messages' : messages,
#     }

#     return render(request, 'inbox.html', context)


# def Chats(request, username):
#     user = request.user
#     messages = Message.get_message(user=user)
#     active_direct = username
#     directs = Message.objects.filter(user=user, recipient__username=username)
#     directs.update(is_read=True)

#     for message in messages:
#         if message['user'].username == username:
#             message['unread'] = 0
    
#     context = {
#         'directs' : directs,
#         'active_direct' : active_direct,
#         'messages' : messages,
#     }

#     return render(request, 'directs.html', context)

# def SendMessage(request):
#     from_user = request.user
#     to_user_username = request.Post.get('to_user')
#     body = request.Post.get('body')

#     if request.method =="POST":
#         to_user = User.objects.get(username=to_user_username)
#         Message.send_message(from_user, to_user, body)
#         return redirect('inbox')
#     else:
#         pass
        