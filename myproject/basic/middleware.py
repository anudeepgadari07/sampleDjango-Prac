from django.http import JsonResponse
import re
import json
from django.http import HttpResponse
from basic.models import users
import jwt
from django.conf import settings





class basicMiddleware():
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        
        if(request.path == "/student/"):
            print(request.method,"method")
        response = self.get_response(request)
        return response

class sscMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if(request.path in ["job1/","job2/"]):
            ssc_result=request.GET.get("ssc")
            # print(ssc_result,'hello')
            if(ssc_result !='True'):
                return  JsonResponse({"error":"u should qualify atleast ssc for applying this job"},status=400)
        return self.get_response(request)

 
class medicalMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if(request.path == "job1/"):
            medical_fit_result=request.GET.get("medically_fit")
            if(medical_fit_result !='True'):
                return JsonResponse({"error":"you are not medically fit to apply for this job role"},status=400)
        return self.get_response(request)
 
class AgeMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if (request.path in ["job1/","job2/"]):
            Age_checker=int(request.GET.get("age",17))
            if(Age_checker >25 and Age_checker<18):
                return JsonResponse({"error":"age must be in b/w 18 and 25"},status=400)
        return self.get_response(request)


class usernameMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self,request):
        # response=self.get_response
        if (request.path == "/signup/") and (request.method == "POST"):
            data = json.loads(request.body)
            username = data.get("username")
            #checks username
            if not username:
                return JsonResponse({"error":"username is required"},status = 400)

            if len(username)<3 or len(username)>20:
                return JsonResponse({"error":"username should contain atleast 3 characters to 20 characters"},status = 400)

            if username[0] in "._" or username[-1] in "._":
                return JsonResponse({"error":"username should not start or end with . or _"},status = 400)

            if not re.match(r"^[a-zA-Z0-9._]+$",username):
                return JsonResponse({"error":"username should contain letters,numbers,dot,underscore"},status = 400)

            if ".." in username or "__" in username:
                return JsonResponse({"error":"cannot have .. or __"},status = 400)

        return self.get_response(request)



#mot empty
#basic eamil pattern
# email alredy exists 
class emailMiddleWare:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self,request):
        if(request.path == "/signup/") and (request.method == "POST"):
            try:
                data = json.loads(request.body)
                email = data.get("email")
                if not email:
                    return JsonResponse({"error":"email is required"},status = 400)

                if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                    return JsonResponse({"error":"should match the email pattern."},status = 400)

                try:
                    if users.objects.filter(email=email).exists():
                        return JsonResponse({"error": "email already exists"},status=400)
                except Exception as e:
                    print(e)
                    return JsonResponse({"error":"error"},status = 400)
            except Exception as e:
                print("error",e)
        return self.get_response(request)


class passwordMiddleWare:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self,request):
        if (request.path == "/signup/") and (request.method == "POST"):
            data = json.loads(request.body)
            password = data.get("password")

            if not password:
                return JsonResponse({"error": "password is required"}, status=400)

            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

            if not re.match(pattern, password):
                return JsonResponse({"error": "Password must contain at least 8 characters, "
                                        "one uppercase letter, one lowercase letter, "
                                        "one number, and one special character (@$!%*?&)"},status=400)
        return self.get_response(request)



class movieMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self,request):
        if request.path == "/movieData/":
            # print("movie api called")
            incoming_data = request.POST
            # print("incoming data",incoming_data)
        return self.get_response(request)


class authenticate_middleware():
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if request.path=="/getData/":
            token=request.headers.get("Authorization")
            print(token,"token") #prints bearer <token>
            if not token:
                return JsonResponse({"error":"Authorization token missing"},status=401) 
            token_value=token.split(" ")[1]
            print(token_value,"token_value") 
            try:
                decoded_data=jwt.decode(token_value,settings.SECRET_KEY,algorithms=["HS256"])
                print(decoded_data,"decoded_data")               
                request.token_data=decoded_data               
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error":"token has expired, please login again"},status=401) 
            except jwt.exceptions.InvalidSignatureError:
                return JsonResponse({"error":"invalid token signature"},status=401)    

        return self.get_response(request)