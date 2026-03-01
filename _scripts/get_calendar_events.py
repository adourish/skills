#!/usr/bin/env python3
"""
Helper function to get Google Calendar events
"""

from datetime import datetime, timedelta, timezone

def get_calendar_events(calendar_service, days=7):
    """Get calendar events for today and next N days"""
    if not calendar_service:
        return []
    
    try:
        now = datetime.now(timezone.utc)
        time_min = now.isoformat()
        time_max = (now + timedelta(days=days)).isoformat()
        
        events_result = calendar_service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            maxResults=50,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        calendar_items = []
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'No title')
            
            # Parse start time
            if 'T' in start:
                event_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
            else:
                event_time = datetime.fromisoformat(start + 'T00:00:00+00:00')
            
            # Determine if event is today or soon
            days_until = (event_time.date() - now.date()).days
            
            if days_until == 0:
                priority = 'high'
                due_str = 'today'
            elif days_until <= 2:
                priority = 'high'
                due_str = event_time.strftime('%Y-%m-%d')
            else:
                priority = 'normal'
                due_str = event_time.strftime('%Y-%m-%d')
            
            calendar_items.append({
                'title': f"📅 {summary}",
                'source': 'Google Calendar',
                'due': due_str,
                'priority': priority,
                'time': event_time.strftime('%I:%M %p') if 'T' in start else 'All day',
                'id': event['id']
            })
        
        return calendar_items
        
    except Exception as e:
        print(f"⚠️  Error fetching calendar events: {e}")
        return []
