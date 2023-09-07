from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.forms import AuthenticationForm
# import view sets from the REST framework
from rest_framework import viewsets

# import the TodoSerializer from the serializer file
from .serializers import *

# import the Todo model from the models file
from .models import *

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .forms import NewUserForm

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

# Email AUTH
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.http import HttpResponse

# create a class for the Todo model viewsets
class MagnoliaCakesAndCupcakesView(viewsets.ModelViewSet):

	# create a serializer class and
	# assign it to the TodoSerializer class
	serializer_class = MagnoliaCakesAndCupcakesSerializer

	# define a variable and populate it
	# with the Todo list objects
	queryset = MagnoliaCakesAndCupcakes.objects.all()

@api_view(['POST'])
@permission_classes([AllowAny]) ###### Add this to allow users to access despite not being logged in
def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.data)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return activateEmail(request, user, form.cleaned_data.get('email'))
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny]) ###### Add this to allow users to access despite not being logged in
def activateEmail(request, user, to_email):
    test_email_server_connectivity()
    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    try:
        if email.send():
            return Response({'message': 'User registered successfully. Please complete verification by clicking the link sent to your email.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Problem sending confirmation email. Please contact an administrator.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        print(error)
        return Response({'message': 'Problem sending confirmation email. Please contact an administrator.'}, status=status.HTTP_400_BAD_REQUEST)
    

import smtplib
def test_email_server_connectivity():
    try:
        # Establish a connection to the email server
        server = smtplib.SMTP('smtp.gmail.com', 2525)

        # Identify yourself to the email server (optional)
        server.ehlo()

        # If using a secure connection (e.g., SMTP over SSL/TLS), uncomment the following line and provide the necessary parameters
        server.starttls()

        # Login to the email server (if required) with your credentials
        server.login('noreply.magnoliacakes@gmail.com', 'mtzndgodvtfuyfwd')

        # Close the connection
        server.quit()

        print("Email server connectivity test successful.")
    except Exception as e:
        print(f"Email server connectivity test failed. Error: {str(e)}")





@permission_classes([AllowAny]) ###### Add this to allow users to access despite not being logged in
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        # return Response({'message': 'Thank you for your email confirmation. Now you can login your account.'}, status=status.HTTP_202_ACCEPTED)
    
    return HttpResponse('Activation link is invalid!')
    # return Response({'message': 'Activation link is invalid!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny]) ###### Add this to allow users to access despite not being logged in
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request._request, data=request.data)
        print("form ", form.error_messages)
        
        if form.is_valid():
            username = request.data.get('username') 
            password = request.data.get('password')
            
            user = authenticate(request._request, username=username, password=password)
            if user is not None:
                django_login(request._request, user)  # Use django_login instead of login
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Login failed', 'error_messages': 'user does not exist'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'Login failed', 'error_messages': form.error_messages}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)

     def post(self, request):          
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([AllowAny]) ###### Add this to allow users to access despite not being logged in
def terms_and_conditions(request):
    if request.method == 'GET':
        terms = TermsAndConditions.objects.first()
        serializer = TermsAndConditionsSerializer(terms)
        return Response(serializer.data)

    elif request.method == 'PUT':
        terms = TermsAndConditions.objects.first()
        serializer = TermsAndConditionsSerializer(terms, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Terms & Conditions updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)