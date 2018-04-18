from django.db import models

import json
import urllib.request
from django.shortcuts import render

def get_spreadsheet():
    with urllib.request.urlopen("https://sheets.googleapis.com/v4/spreadsheets/1gp7_DzmgDvQaqu35X7n3TtF1em4NhRGWdajdv8TYTv4/values/DO_NOT_EDIT?majorDimension=ROWS&key=AIzaSyCqgfQaLDbWRWxMKZi4o4OZtX-TG4ZRpws") as url:
        spreadsheet = json.loads(url.read().decode())
        return(spreadsheet['values'])

def employee_information(request, all_employees):
    employee = {'employee_id': request.GET.get('q'),'valid_id': False}
    for row in all_employees:
        if row[0] == employee['employee_id']:
            employee['valid_id'] = True
            employee['employee_name'] = row[1]
            employee['employee_number'] = row[2]
            employee['employee_info'] = row[:-1]
    return employee

def all_events(spreadsheet):
    data = {
        'days': list(map(lambda date : date.split(' ')[0], spreadsheet[0][5:-1])),
        'months': list(map(lambda date : date.split(' ')[1], spreadsheet[0][5:-1])),
        'event_titles': spreadsheet[1][5:-1],
        'event_doors': spreadsheet[2][5:-1]
    }
    events = [list(a) for a in zip(
        data['days'],
        data['months'],
        data['event_titles'],
        data['event_doors'])]
    return events