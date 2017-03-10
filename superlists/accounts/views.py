from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages, auth
from accounts.models import Token
from django.core.urlresolvers import reverse
import sys

# Create your views here.
def send_login_email(request):
	email = request.POST['email']
	token = Token.objects.create(email=email)
	url = request.build_absolute_uri(
		reverse('login') + '?token={uid}'.format(uid=str(token.uid))
	)
	message_body = 'Use this link to log in:\n\b{url}'.format(url=url)
	send_mail(
		'Your login link for Superlists',
		message_body,
		'noreply@Superlists',
		[email]
		)
	messages.success(
		request,
		"Check your email, we've sent you a link you can use to log in."
	)
	return redirect('/')

def login(request):
	user = auth.authenticate(uid=request.GET.get('token'))
	if user:
		auth.login(request, user)
	return redirect('/')