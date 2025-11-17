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

#  Test DB connection
def connect(request):
    try:
        with connection.cursor() as c:
            c.execute("select 1")
        return JsonResponse({"status": "ok", "db": "connected"})
    except Exception as e:
        return JsonResponse({"status": "error", "db": str(e)})

# Create Student API 
@csrf_exempt
def addStudent(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name  = data.get('Name')
            age   = data.get('Age')
            email = data.get('Email')

            #  Validation to avoid NULL errors
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


    elif request.method == "GET":
        try:
            data = json.loads(request.body)
            if "id" in data:
                ref_id = data.get("id")#getting id
                specific_record = students.objects.filter(id = ref_id).values().first()
                return JsonResponse({"status":"OK","record":specific_record},status = 200)
            elif "min_age" in data:
                min_age = data.get("min_age")#getting age
                under_age = list(students.objects.filter(Age__gte = min_age).values())
                return JsonResponse({"status":"ok","under_age":under_age},status = 200)
            elif "max_age" in data:
                max_age = data.get("max_age")#grtting age from body
                max_ages = list(students.objects.filter(Age__lte = max_age).values())
                return JsonResponse({"status":"OK","max_age":max_ages},status = 200) 

        except Exception as e:
            print("error",e)

        
        try:
            getDetails = list(students.objects.values())
            # print(getDetails)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        return JsonResponse({"status":"OK","Data":getDetails},status = 200)




    elif request.method == "PUT":
        data = json.loads(request.body)
        ref_id = data.get("id")#getting id
        new_email = data.get("Email") #gettting email
        existingStudent = students.objects.get(id = ref_id)
        existingStudent.Email = new_email#updating data
        existingStudent.save()
        updatedData = students.objects.filter(id = ref_id).values().first()
        print(updatedData)
        return JsonResponse({"status":"data Updated successfully","updated data":updatedData},status = 200)

    elif request.method == "DELETE":
        data = json.loads(request.body)
        ref_id = data.get("id")#getting id
        get_deleted_data = students.objects.filter(id = ref_id).values().first()
        to_delete = students.objects.get(id = ref_id)
        to_delete.delete()
        return JsonResponse({"status":"deleted data successfully","deleted data":get_deleted_data},status = 200)

    return JsonResponse({"error": "Use POST Method only"}, status=405)        


def job1(request):
    return JsonResponse({"message":"you haave successfully applied for job1."},status=200)

def job2(request):
    return JsonResponse({"message":"you have successfully applied for job2."})