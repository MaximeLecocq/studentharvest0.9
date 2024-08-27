from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Conversation, Message
from listings.models import Listing
from django.db.models import OuterRef, Subquery, Q

#this view allows a logged-in user to start a conversation with a listing donor.
#it retrieves or creates a conversation between the student and the donor for the specified listing.
@login_required
def start_conversation(request, listing_pk):
    #get the current user (student)
    user = request.user
    listing = get_object_or_404(Listing, pk=listing_pk)
    donor = listing.donor

    #create or retrieve a conversation between the student (user) and the donor for this listing
    conversation, created = Conversation.objects.get_or_create(
        student=user,
        donor=donor,
        listing=listing
    )

    return redirect('conversation_detail', conversation_id=conversation.id)

#this view shows the details of a specific conversation and allows users to send messages within that conversation.
@login_required
def conversation_detail(request, conversation_id):
    #retrieve the specific conversation using its ID
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    #ensure the user is part of the conversation
    if request.user not in [conversation.student, conversation.donor]:
        messages.error(request, "You are not allowed to view this conversation.")
        return redirect('inbox')
    
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                text=text
            )
        return redirect('conversation_detail', conversation_id=conversation.id)
    
    return render(request, 'messaging/conversation_detail.html', {'conversation': conversation})

#this view shows the inbox of the logged-in user, displaying all their conversations ordered by the latest message time.
@login_required
def inbox(request):
    user = request.user
    conversations = Conversation.objects.filter(
        Q(donor=user) | Q(student=user)
    ).annotate(
        latest_message_time=Subquery(
            Message.objects.filter(conversation=OuterRef('pk')).order_by('-timestamp').values('timestamp')[:1]
        )
    ).order_by('-latest_message_time') #order conversations by the latest message time (descending)


    return render(request, 'messaging/inbox.html', {'conversations': conversations})