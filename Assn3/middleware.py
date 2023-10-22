from django.shortcuts import render, redirect

from Destinations.models import Session
from django.http import HttpResponseRedirect, HttpResponse

def session_middleware(next):

    no_login = ["/", "/sessions", "/users/new", "/favicon.ico", "/sessions/new", "/users"]
    
    def middleware(req):
        token = req.COOKIES.get('session_token')
        session = None
        if token:
            try:
                session = Session.objects.get(token=token)
            except Session.DoesNotExist:
                session = None
        
        if req.path not in no_login and session is None:
            return HttpResponseRedirect("/sessions/new")
        
        if session:
            req.user = session.user
        res = next(req)
        return res
    
    return middleware    