from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from listings.models import Listing

@login_required
def start_conversation(request, listing_pk):
    listing = get_object_or_404(Listing, pk=listing_pk)
    donor = listing.donor

    # Check if a conversation already exists between this student and donor about this listing
    conversation, created = Conversation.objects.get_or_create(
        listing=listing,
        student=request.user,
        donor=donor
    )

    return redirect('conversation_detail', conversation_id=conversation.id)

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    if request.user != conversation.student and request.user != conversation.donor:
        return redirect('homepage')  # Restrict access to only the student and donor
    
    if request.method == "POST":
        text = request.POST.get('message')
        if text:
            Message.objects.create(conversation=conversation, sender=request.user, text=text)
    
    messages = conversation.messages.all().order_by('timestamp')
    return render(request, 'messaging/conversation_detail.html', {'conversation': conversation, 'messages': messages})

@login_required
def inbox(request):
    if request.user.is_authenticated:
        # Show conversations for the logged-in user (as either donor or student)
        conversations_as_student = Conversation.objects.filter(student=request.user)
        conversations_as_donor = Conversation.objects.filter(donor=request.user)

        # Combine and sort conversations by creation time (or any other desired criteria)
        conversations = conversations_as_student | conversations_as_donor
        conversations = conversations.order_by('-created_at')

        return render(request, 'messaging/inbox.html', {'conversations': conversations})
    else:
        return redirect('login')  # Redirect to login if the user is not authenticated