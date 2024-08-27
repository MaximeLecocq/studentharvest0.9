from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from listings.models import Listing
from messaging.models import Conversation, Message

User = get_user_model()

class MessagingTestCase(TestCase):

    #the `setUp` method runs before each test case.
    #it sets up the necessary data, including two users (a student and a donor),
    #and a listing created by the donor.
    def setUp(self):
        #create two users: a student and a donor
        self.student = User.objects.create_user(username='student_user', email='student@example.com', password='password123', role='student')
        self.donor = User.objects.create_user(username='donor_user', email='donor@example.com', password='password123', role='donor')

        #create a listing by the donor
        self.listing = Listing.objects.create(title='Test Listing', description='Test description', donor=self.donor)

    def test_start_conversation(self):
        #log in as a student
        self.client.login(username='student_user', password='password123')

        #simulate starting a conversation for the listing
        response = self.client.get(reverse('start_conversation', args=[self.listing.pk]))

        #check if the conversation was created
        conversation = Conversation.objects.filter(student=self.student, donor=self.donor, listing=self.listing).first()
        self.assertIsNotNone(conversation)
        
        #check if the redirection to the conversation detail page works
        self.assertRedirects(response, reverse('conversation_detail', args=[conversation.id]))

    
    def test_send_message(self):
        #log in as a student
        self.client.login(username='student_user', password='password123')

        #create a conversation manually
        conversation = Conversation.objects.create(student=self.student, donor=self.donor, listing=self.listing)

        #send a message via POST
        response = self.client.post(reverse('conversation_detail', args=[conversation.id]), {
            'text': 'Hello, I am interested in your listing!'
        })

        #check if the message was created
        message = Message.objects.filter(conversation=conversation, sender=self.student, text='Hello, I am interested in your listing!').first()
        self.assertIsNotNone(message)

        #check if the page redirects back to the conversation detail view
        self.assertRedirects(response, reverse('conversation_detail', args=[conversation.id]))

    def test_conversation_permission(self):
        #create a conversation manually
        conversation = Conversation.objects.create(student=self.student, donor=self.donor, listing=self.listing)

        #log in as another user (unauthorized user)
        unauthorized_user = User.objects.create_user(username='other_user', email='other@example.com', password='password123')
        self.client.login(username='other_user', password='password123')

        #attempt to view the conversation
        response = self.client.get(reverse('conversation_detail', args=[conversation.id]))

        #check that the unauthorized user is not allowed to view the conversation
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('inbox'))