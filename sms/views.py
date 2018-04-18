from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from twilio.twiml.messaging_response import MessagingResponse
from search.views import get_spreadsheet, all_events
from django.shortcuts import render
from urllib.request import urlopen
import os

def find_employee(phone_number):
    spreadsheet = get_spreadsheet()
    employee_name = ''
    for row in spreadsheet:
        if row[2] == phone_number:
            employee_name = row[1]
            employee_dates = row[5:-1]
    events = all_events(spreadsheet)
    data = [list(a) for a in zip(events,employee_dates)]
    print(data)
    return [employee_name, data]

@csrf_exempt
def sms_response(request):

    #fix arrive by
    resp = MessagingResponse()
    phone_number = request.POST.get('From', '')[2:]
    body = int(request.POST.get('Body', ''))
    data = find_employee(phone_number)[1]
    name = find_employee(phone_number)[0]
    print(data)
    mystr = '----- \n \nHello, ' + name.split(' ')[0] + '!\n \n'
    for i in range(body):
        mystr += (
        "Date: " +
        data[i][0][0] +
        ' ' + data[i][0][1] + '\n' +
        "Event: " +
        data[i][0][2] + '\n' +
        "Arrive By: " +
        data[i][0][3] + '\n' +
        '\n' + data[0][1]
        )
    print(mystr)
    msg = resp.message(mystr)
    return HttpResponse(str(resp))