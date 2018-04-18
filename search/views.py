# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def index(request, pk=None, *args, **kwargs):
    employee = employee_information(request, get_spreadsheet())
    if employee['valid_id'] == False:
        return render(request, "view.html", {'valid_id': False})
    employee_stuff = employee['employee_info'][5:]
    events = all_events(get_spreadsheet())
    for i, event in enumerate(events):
        event.append(employee_stuff[i])
    context = {
        'valid_id': employee['valid_id'],
        'name': employee['employee_name'].split(' ')[0],
        'events': events
    }
    return render(request, "view.html", context)

def events_view(request, pk=None, *args, **kwargs):
    events = all_events(get_spreadsheet())
    context = {
        'events': events
    }
    return render(request, "events.html", context)

def events_detail_view(request, pk=None, *args, **kwargs):
    spreadsheet = get_spreadsheet()
    date = request.path[-6:-1]
    events = all_events(spreadsheet)
    workers = []
    date_index = 0
    for i, event in enumerate(events):
        if (event[0] + event[1]) == (date[:3] + date[3:]):
            date_index = i + 4
    for employee in spreadsheet[4:]:
        if employee[date_index] and employee[date_index] != 'RO':
            workers.append([employee[1],employee[date_index]])
    event = events[date_index - 4]
    employee_count = len(workers)
    context = {
        'event': event,
        'events': workers,
        'employee_count': employee_count
    }
    return render(request, "event_details.html", context)