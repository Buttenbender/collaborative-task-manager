from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timezone
import json

def get_calendar_service(calendar_token: str):
    token_data = json.loads(calendar_token)
    credentials = Credentials(
        token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=token_data.get("client_id"),
        client_secret=token_data.get("client_secret")
    )
    return build("calendar", "v3", credentials=credentials)

def create_calendar_event(calendar_token: str, title: str, due_date: datetime) -> str:
    service = get_calendar_service(calendar_token)
    event = {
        "summary": title,
        "start": {
            "dateTime": due_date.isoformat(),
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": due_date.isoformat(),
            "timeZone": "UTC"
        }
    }
    created_event = service.events().insert(calendarId="primary", body=event).execute()
    return created_event.get("id")

def delete_calendar_event(calendar_token: str, event_id: str) -> None:
    service = get_calendar_service(calendar_token)
    service.events().delete(calendarId="primary", eventId=event_id).execute()