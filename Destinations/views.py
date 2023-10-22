
import secrets, hashlib
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, redirect,reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from Destinations.models import Destination, User, Session



def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(8)
    hash_ = hashlib.sha256(bytes(password + salt, "UTF-8")).hexdigest()

    for _ in range(10):
        hash_ = hashlib.sha256(bytes(hash_, "UTF-8")).hexdigest()

    return hash_, salt

def verify_password(input, password_hash, salt):
    print(salt)
    password, salt = hash_password(input, salt)
    
    return password_hash == password

def sign_up(req): # users/new /users
    if req.method == "POST" and not req.COOKIES.get('session_token'):
        user = User(
            name = req.POST.get("name"),
            email = req.POST.get("email"),
            password_hash = req.POST.get("password")
        )
        try:
            user.checkValidEmail()
            user.checkValidPassword()
            user.password_hash,salt = hash_password(req.POST.get("password"))
            user.password_hash = user.password_hash+ '|'+salt
            user.save()
            session = Session(
                    user = user,
                    token = secrets.token_hex(64)
                )
            session.save()
            
            res = render(req, "core/destinations.html")
            res.set_cookie('session_token',session.token)
            return res
        except ValidationError as e:
            return HttpResponseBadRequest(e.message)
        except IntegrityError:
            return HttpResponseBadRequest("Email is already taken!")
    elif req.COOKIES.get('session_token'):
        return redirect("destinations")
    else:
        return render(req, "core/sign_up.html")
    
def sign_in(req): #sessions/new and sessions #working
    # abc  p@p   esperanza1
    if req.method =="POST" and not req.COOKIES.get('session_token'):
        email = req.POST.get("email")
        password = req.POST.get("password")

        user = User.objects.filter(email=email).first()
        hash_, salt = user.password_hash.split('|')
        if user:
            if verify_password(password, hash_, salt):
                session = Session(
                    user = user,
                    token = secrets.token_hex(64)
                )
                session.save()
                res = render(req, "core/destinations.html")
                res.set_cookie('session_token',session.token)
                return res
            else:
                return HttpResponseNotFound("Invalid Password")
        else:
            return HttpResponseNotFound("Invalid email")
    elif req.COOKIES.get('session_token'):
        token = req.COOKIES.get('session_token')
        try:
            session = Session.objects.get(token=token)
        except Session.DoesNotExist:
            session = None
        if session == None:
            res = render(req, "core/login.html")
            res.delete_cookie('session_token')
            return res
        return redirect("destinations")
    else:
        return render(req, "core/login.html")

def destinations_page(req):#destinations #working
    token = req.COOKIES.get('session_token')
    session = Session.objects.filter(token = token).first()
    if req.method == "POST":
        name = req.POST.get("name")
        review = req.POST.get("review")
        rating = int(req.POST.get("rating"))
        share_publicly = req.POST.get("public")=='on'

        user = session.user
        

        destination = Destination(
            name = name,
            review = review,
            rating = rating,
            share_publicly = share_publicly,
            user = user
        )
        destination.save()
        return redirect("destinations")
    return render(req, "core/destinations.html", {"Destinations": Destination.objects.all(), "Session": session} )

def new_destination(req):#new_destination #working
    return render(req, "core/new_destinations.html")

def update_destination(req, id):#destinations/:id
    token = req.COOKIES.get('session_token')
    session = Session.objects.filter(token = token).first()

    destination = Destination.objects.get(pk=id)
    if destination.user != session.user:
        return HttpResponseNotFound("Destination not found!")
    if req.method == "POST":
        print(req.POST,1)
        destination.name = req.POST.get("name")
        destination.review = req.POST.get("review")
        destination.rating = req.POST.get("rating")
        destination.share_publicly = req.POST.get("public")=='on'
        destination.save()
        url = reverse('destinations')
        return redirect(url)
    return render(req, "core/one_destination.html",{"Destination":destination})

def destroy_destination(req, id):#destinations/id/destroy
    try:
        destination = Destination.objects.get(pk=id)
        destination.delete()
        return redirect('destinations')
    except:
        return HttpResponseNotFound("destination not found!")

def index(req: HttpRequest):
    destinations = Destination.objects.order_by('id')[:5]
    return render(req, "core/index.html", {"Destinations": destinations})

def destroy_session(req):#sessions/destroy #working
    token = req.COOKIES.get('session_token')
    session = Session.objects.filter(token=token).first()

    session.delete()
    return redirect("/")
    