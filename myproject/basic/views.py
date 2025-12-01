from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt
from basic.models import students,users,movieData
# from django.http import QueryDict
from django.contrib.auth.hashers import make_password,check_password
import jwt
from django.conf import settings
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo

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


@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # print(data)
        insert = users.objects.create(
            username = data.get("username"),
            email = data.get("email"),
            password = make_password(data.get("password"))
        )
        return JsonResponse({"data":"successfully created"},status = 200)


    elif request.method == "GET":
        try:
            data = json.loads(request.body)
            # print(data)
            if "id" in data:
                ref_id = data.get("id")
                specific_record = users.objects.filter(id = ref_id).values().first() #gets specific record from id
                return JsonResponse({"status":"OK","record":specific_record},status = 200)
        except Exception as e:
            print(e)
            return JsonResponse({"error":"not found"},status = 400)

    elif request.method == "PUT":
        data = json.loads(request.body)
        ref_id = data.get("id")
        # print(ref_id)
        try:
            if not ref_id:
                return JsonResponse({"message":"Id is required for an update"},status = 200)
            try:
                user = users.objects.get(id=ref_id)
            except Exception as e:
                print("error",e)
                return JsonResponse({"error": "Record not found"}, status=400)
            try:
                user.username = data.get("username",user.username)
                user.email = data.get("email",user.email)
                user.password = make_password(data.get("password",user.password))
                user.save()
                return JsonResponse({"status":"updated",f"updated values":data},status = 200)
            except Exception as e:
                return JsonResponse({"status":"failed to update"},status = 400)
            

        except Exception as e:
            return JsonResponse({"error":f"user not found {ref_id}"},status = 200)



    elif request.method == "DELETE":
        data = json.loads(request.body)
        ref_id = data.get("id")
        get_deleted_data = users.objects.filter(id = ref_id).values().first()
        to_delete = users.objects.get(id = ref_id)
        to_delete.delete()
        return JsonResponse({"status":"success","deleted data":get_deleted_data},status = 200)

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # print(data)
        username = data.get("username")
        password = data.get("password")
        try:
            user = users.objects.get(username=username)
            issued_time=datetime.now(ZoneInfo("Asia/Kolkata"))
            expired_time=issued_time+timedelta(minutes=25)
            if check_password(password,user.password):
                # token = "a json web token"
                payload = {"username":username,"email":user.email,"exp":expired_time}
                token = jwt.encode(payload,settings.SECRET_KEY,algorithm='HS256')
                return JsonResponse({"status":"logged in successfully","token":token,"issued_at":issued_time,"expired at":expired_time,"expiring in":int((expired_time-issued_time).total_seconds()/60)},status = 200)
            else:
                return JsonResponse({"status":"make sure your password is correct"},status = 400)
        except Exception as e:
            print("error",e)
            return JsonResponse({"status":"user not found"},status = 400)




@csrf_exempt
def movieDatainfo(request):
    if request.method == "GET":
        try:
            movie_id = request.GET.get("id")  # read from URL query params
            rating = request.GET.get("Rating")
            budget = request.GET.get("Budget")
            if movie_id:   # if id is passed
                record = movieData.objects.filter(id=movie_id).values().first()
                if record:
                    return JsonResponse({"status": "OK", "record": record}, status=200)
                else:
                    return JsonResponse({"status": "NOT FOUND", "message": "Invalid ID"}, status=404)
            elif rating:
                rating = float(rating)
                record = list(movieData.objects.filter(Rating__gt=rating).values())
                # print(record)
                return JsonResponse({"status":"success",f"Rating grater than {rating}":record},status = 200)
            elif budget:
                budget = int(budget[:-2])
                record = movieData.objects.all().values()
                records = []
                # print(budget)
                for item in record:
                    db_budget = item["Budget"]
                    db_budget = int(db_budget[:-2])
                    if db_budget > budget:
                        records.append(item)
                return JsonResponse({"status":"success",f"budget grater than {budget}cr":records},status = 200)
            else:
            # return all records
                all_data = list(movieData.objects.values())
                return JsonResponse({"status": "OK", "data": all_data}, status=200)

        except Exception as e:
            print("error", e)
            return JsonResponse({"error": "Failed"}, status=400)
        
        
    
    
    elif request.method == "POST":
        try:
            # data = json.loads(request.body)
            data = request.POST
            infodata = movieData.objects.create(
                MovieName = data.get("MovieName"),
                ReleaseDate = data.get("ReleaseDate"),
                Budget = data.get("Budget"),
                Rating = data.get("Rating")
            )
            return JsonResponse({"status": "success", "id": infodata.id}, status=201)
        except Exception as e:
            print("error",e)
            return JsonResponse({"error":"faild to post data"},status = 400)

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            # data = request.POST
            # data = QueryDict(request.body)

            movie_id = data.get("id")

            if not movie_id:
                return JsonResponse({"error": "ID is required for update"}, status=400)

            try:
                movie = movieData.objects.get(id=movie_id)
            except movieData.DoesNotExist:
                return JsonResponse({"error": "Record not found"}, status=404)

        # Update fields only if provided
            movie.MovieName = data.get("MovieName", movie.MovieName)
            movie.ReleaseDate = data.get("ReleaseDate", movie.ReleaseDate)
            movie.Budget = data.get("Budget", movie.Budget)
            movie.Rating = data.get("Rating", movie.Rating)
        
            movie.save()

            return JsonResponse({"status": "updated", "id": movie.id}, status=200)

        except Exception as e:
            print("PUT error:", e)
            return JsonResponse({"error": "Failed to update"}, status=400)

    elif request.method == "DELETE":
        try:
            data = json.loads(request.body)
            ref_id = data.get("id")
            get_deleted_data = movieData.objects.filter(id = ref_id).values().first()
            to_delete = movieData.objects.get(id = ref_id)
            to_delete.delete()
            return JsonResponse({"status":"deleted data successfully","deleted data":get_deleted_data},status = 200)
        except Exception as e:
            return JsonResponse({"error":"failed to delete data"},status = 400)

    
    


