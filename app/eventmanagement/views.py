from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Event
from datetime import datetime, timezone


@login_required
def home(request):

    try:
        users_event = Event.objects.filter(user__username=request.user.username).all()
        print(users_event)
    except:
        return render(request, 'eventmanagement/error.html', {
            'error': {
                'code': 500,
                'message': 'Internal server error, please try again later',
                'redirect': 'home',
                'destination': 'home'
            }
        })
    return render(request, 'eventmanagement/home.html')
    

    
def event_serializer(Events):

    now = datetime.now().replace(tzinfo=timezone.utc)
    events = []

    for event in Events:
        events.append({
            'id': event.id,
            'title': event.title,
            'start': event.start,
            'end': event.end,
            'description': event.description,
            'status': 'completed' if event.end < now else 'active'
        })

    return events
    

@login_required
def get_user_events(request):
    
    events = Event.objects.filter(user__username=request.user.username).all()
    events_serialized = event_serializer(events)

    return JsonResponse(events_serialized, safe=False)


def validateInputs(inputs):

    for input in inputs:

        input = input.strip()
        if len(input) == 0:
            return True
    
    return False



@login_required
def createEvent(request):

    user = request.user

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start')
        end_date = request.POST.get('end')
        start_time = request.POST.get('startTime')
        end_time = request.POST.get('endTime')

        hasError = validateInputs([title, description, start_date, start_time, end_date, end_time])

        if hasError:
            return render(request, 'eventmanagement/error.html', {
                'error': {
                    'code': 400,
                    'message': 'Could not create event, please make sure you input all the fields',
                    'redirect': 'home',
                    'destination': 'home'
                }
            })

        # check and serialize the inputs

        start = start_date + 'T' + start_time
        end = end_date + 'T' + end_time

        start = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
        end = datetime.fromisoformat(end).replace(tzinfo=timezone.utc)

        try:
            event = Event.objects.create(
                title=title,
                description=description,
                start=start,
                end=end,
                user=user
            )
        except Exception as e:
            return render(request, 'eventmanagement/error.html', {
                'error': {
                    'code': 500,
                    'message': e.message,
                    'redirect': 'home',
                    'destination': 'home'
                }
            })

        return redirect('home')



@login_required
def user_dashboard(request):

    user = request.user

    try:
        events = Event.objects.filter(user=user).all()
    except Exception as e:
        return render(request, 'eventmanagement/error.html', {
                'error': {
                    'code': 500,
                    'message': e.message,
                    'redirect': 'home',
                    'destination': 'home'
                }
            })
    events_serailized = event_serializer(events)

    now = datetime.now().replace(tzinfo=timezone.utc)

    upcoming_events = []
    ongoing_events = []
    completed_events = []

    for event in events_serailized:

        if event['end'] < now:
            completed_events.append(event)
        elif event['start'] > now:
            upcoming_events.append(event)
        elif event['start'] <= now and event['end'] > now:
            ongoing_events.append(event)


    return render(request, 'eventmanagement/dashboard.html', {
        'events': events_serailized,
        'completed_events': completed_events,
        'upcoming_events': upcoming_events,
        'ongoing_events': ongoing_events
    })
    


def event_page(request, event_id):

    user = request.user

    event = Event.objects.get(id=event_id)
    if event.user == user:

        if request.method == 'POST':

            title = request.POST.get('title')
            description = request.POST.get('description')
            start_date = request.POST.get('start')
            end_date = request.POST.get('end')
            start_time = request.POST.get('startTime')
            end_time = request.POST.get('endTime')

            if start_date and start_time:
                start = start_date + 'T' + start_time
                start = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
                event.start = start

            if end_date and end_time:
                end = end_date + 'T' + end_time
                end = datetime.fromisoformat(end).replace(tzinfo=timezone.utc)
                event.end = end

            if title:
                event.title = title

            if description:
                event.description = description

            try:
                event.save()
            except Exception as e:
                return render(request, 'eventmanagement/error.html', {
                    'error': {
                        'code': 500,
                        'message': e.message,
                        'redirect': 'home',
                        'destination': 'home'
                    }
                })
            return redirect('home')

        elif request.method == 'GET':    
            return render(request, 'eventmanagement/editevent.html', {
                'event': event
            })
            
        elif request.method == 'DELETE':
            event.delete()
            return JsonResponse({
                'status': 'success'
            })
            
    else:
        return render(request, 'eventmanagement/error.html', {
                'error': {
                    'code': 403,
                    'message': 'you do not have the access to edit this event.',
                    'redirect': 'home',
                    'destination': 'home'
                }
            })