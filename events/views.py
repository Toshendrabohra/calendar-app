from django.shortcuts import render
from django.http import HttpResponse
from google_auth_oauthlib.flow import Flow
from django.shortcuts import redirect
from googleapiclient.discovery import build
import datetime

flow =Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=[
            "https://www.googleapis.com/auth/calendar.events.readonly"
        ]
    )

flow.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect/'

def Index(request):
    return render(request,'home.html')


def GoogleCalendarInitView(request):
    """This view will start the first step of the OAuth.\n It will prompt user for credentials""" 
    authorization_url, _ = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    return redirect(authorization_url)


def GoogleCalendarRedirectView(request):
    temp_var = request.build_absolute_uri()
    if "http:" in temp_var:
        temp_var = "https:" + temp_var[5:]  
    try :
        flow.fetch_token(authorization_response=temp_var)
        credentials = flow.credentials

        service = build('calendar', 'v3', credentials=credentials)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=100, singleEvents=True,
                                                orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return  HttpResponse('<h1>No Event Found</h1>')

        context = {
            'events':events
        }
        return render(request, "events.html", context)
    except :
        return HttpResponse('<h1>Error in request grant</h1>')

        