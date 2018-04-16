# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

import json
import urllib.request
from pprint import pprint

def all_data():
    with urllib.request.urlopen("https://sheets.googleapis.com/v4/spreadsheets/1gp7_DzmgDvQaqu35X7n3TtF1em4NhRGWdajdv8TYTv4/values/DO_NOT_EDIT?majorDimension=ROWS&key=AIzaSyCqgfQaLDbWRWxMKZi4o4OZtX-TG4ZRpws") as url:
        return json.loads(url.read().decode())

def employee_information(request, all_employees):
    employee = {'employee_id': request.GET.get('q'),'valid_id': False}
    for row in all_employees:
        if row[0] == employee['employee_id']:
            employee['valid_id'] = True
            employee['employee_name'] = row[1]
            employee['employee_info'] = row[:-1]
    return employee

def event_information(all_employees):
    events = {
        'days': [],
        'months': [],
        'event_titles': all_employees[1][4:-1],
        'event_doors': all_employees[2][4:-1],
        'employee_dates': all_employees[4:]
    }
    for dates in all_employees[0][4:-1]:
        split_date = dates.split(' ')
        events['days'].append(split_date[0])
        events['months'].append(split_date[1])
    return events

def index(request, pk=None, *args, **kwargs):
    spreadsheet = all_data()
    all_employees = spreadsheet['values']
    employee = employee_information(request, all_employees)
    if employee['valid_id'] == False:
        return render(request, "view.html", {'valid_id': False})
    events = event_information(all_employees)
    zipped = list(map(list,zip(
        events['days'],
        events['months'],
        events['event_titles'],
        events['event_doors'],
        employee['employee_info'][4:]
        )))
    context = {
        'valid_id': employee['valid_id'],
        'name': employee['employee_name'].split(' ')[0],
        'events': zipped
    }
    return render(request, "view.html", context)

def events_view(request, pk=None, *args, **kwargs):
    spreadsheet = all_data()
    all_employees = spreadsheet['values']
    events = event_information(all_employees)
    zipped = list(map(list,zip(
        events['days'],
        events['months'],
        events['event_titles'],
        events['event_doors'],
    )))
    context = {
        'events': zipped
    }
    return render(request, "events.html", context)

def events_detail_view(request, pk=None, *args, **kwargs):
    myslug = request.path[-6:-1]
    spreadsheet = all_data()
    all_employees = spreadsheet['values']
    date = myslug
    events = event_information(all_employees)
    zipped = list(map(list,zip(
        events['days'],
        events['months'],
        events['event_titles'],
        events['event_doors'],
    )))
    workers = []
    date_index = 0
    for i, event in enumerate(zipped):
        if (event[0] + event[1]) == (date[:3] + date[3:]):
            date_index = i + 4
    for employee in all_employees[4:]:
        if employee[date_index] and employee[date_index] != 'RO':
            workers.append([employee[1],employee[date_index]])
    event = zipped[date_index - 4]
    employee_count = len(workers)
    context = {
        'event': event,
        'events': workers,
        'employee_count': employee_count
    }
    return render(request, "event_details.html", context)