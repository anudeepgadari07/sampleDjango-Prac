from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
def greet(request):
    return HttpResponse('Hello World')

def sample(request):
    return HttpResponse('Welcome to Django class.')

def sampleInfo(request):
    data = { "name":"Anudeep", "age":"23" }
    return JsonResponse(data) #default safe = True # data = [1,2,3,4,5] 
    # return JsonResponse(data,safe = False) #here safe is used to send data that which are not dict. 

def calculate(request, operation, num1, num2):
    if operation == 'add':
        result = num1 + num2
    elif operation == 'sub':
        result = num1 - num2
    elif operation == 'mul':
        result = num1 * num2
    elif operation == 'div':
        result = num1 / num2 if num2 != 0 else 'Division by zero error!' 
    else:
        return HttpResponse("Invalid operation! Use add, sub, mul, or div.")
        
    return HttpResponse(f"The result of {operation} between {num1} and {num2} is {result}")