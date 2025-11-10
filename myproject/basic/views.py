from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from basic.models import students  # Model imported

def greet(request):
    return HttpResponse('Hello World')

def sample(request):
    return HttpResponse('Welcome to Django class.')

def sampleInfo(request):
    data = {"name": "Anudeep", "age": "23"}
    return JsonResponse(data)

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

# ✅ Test DB connection
def connect(request):
    try:
        with connection.cursor() as c:
            c.execute("select 1")
        return JsonResponse({"status": "ok", "db": "connected"})
    except Exception as e:
        return JsonResponse({"status": "error", "db": str(e)})

# ✅ Create Student API (Fixed)
@csrf_exempt
def addStudent(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            name  = data.get('Name')
            age   = data.get('Age')
            email = data.get('Email')

            # ✅ Validation to avoid NULL errors
            if not name or not age or not email:
                return JsonResponse({"error": "All fields are required (Name, Age, Email)"}, status=400)

            student = students.objects.create(
                Name=name,
                Age=age,
                Email=email,
            )

            return JsonResponse({"status": "success", "id": student.id}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Use POST Method only"}, status=405)


# post name
# post type
# post description
# post date