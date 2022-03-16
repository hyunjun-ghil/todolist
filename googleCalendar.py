from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    result = []
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)


        # Call the Calendar API
        curTime = datetime.datetime.now()
        now = datetime.datetime(curTime.year, curTime.month, curTime.day, 0, 0, 0, 100000, tzinfo=None).isoformat() + 'Z'
        now2 = datetime.datetime(curTime.year, curTime.month, curTime.day, 23, 59, 59, 100000, tzinfo=None).isoformat() + 'Z'
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              timeMax=now2, maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            data = []
            data.append(start[11:16])
            data.append(event['summary'])
            if 'location' in event:
                data.append(event['location'])
            else:
                data.append('')
            data.append(event['id'])
            result.append(data)

    except HttpError as error:
        print('An error occurred: %s' % error)

    return result

def save(date, time, subject, location):
    """Shows basic usage of the Google Calendar API.
     Prints the start and name of the next 10 events on the user's calendar.
     """
    result = []
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        now = datetime.datetime(date.year(), date.month(), date.day(), time.hour(), time.minute(), time.second()).isoformat()
        addOneHour = datetime.datetime(date.year(), date.month(), date.day(), time.hour()+1, time.minute(), time.second()).isoformat()

        print(now)
        print(addOneHour)
        ev = {
            'summary': subject,
            'location': location,
            'description': '',
            'start': {
                'dateTime': now,
                'timeZone': 'Asia/Seoul',
            },
            'end': {
                'dateTime': addOneHour,
                'timeZone': 'Asia/Seoul',
            },
            'attendees': [
            ],
            'reminders': {
                'useDefault': True,
            },
        }
        print(ev)
        event = service.events().insert(calendarId='primary', body=ev).execute()

    except HttpError as error:
        print('An error occurred: %s' % error)

    print(event)

def delete(id):
    """Shows basic usage of the Google Calendar API.
     Prints the start and name of the next 10 events on the user's calendar.
     """
    result = []
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        service.events().delete(calendarId='primary', eventId=id).execute()

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()