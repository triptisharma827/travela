from django.db import connection, connections
from django.http import JsonResponse
from django.shortcuts import redirect, render
import datetime

import requests
import jwt
import uuid
import os
from django.shortcuts import render


from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGODB_URI"))
db = client['vercelmongodb']

# Create your views here.
# flag for the challenge crack the cookie
flag="FLAG1_und6i1bkal3n"

def home(request):
    access_token = request.COOKIES.get('access_token')
    if access_token:
        # isValid = match_access_token(access_token)
        payload = verify_access_token(access_token)
        print("found the user_id",payload['user_id'])
        if payload['user_id'] == 'eva chapman':
            return render(request, 'secret.html', {'flag':flag})
    
    return render(request, 'index.html')

def authenticate_and_redirect(email, password):
    access_token = generate_access_token(email)
    response = None

    with connection.cursor() as cursor:
        # revoke all Permission from user Alex
        cursor.execute(f"REVOKE ALL ON ALL TABLES IN SCHEMA public FROM Alex;")

        # grant only read permission to Alex
        cursor.execute(f"GRANT SELECT ON ALL TABLES IN SCHEMA public TO Alex;")

    # Redirect users based on their credentials
    if email == 'eva chapman' and password == '1po%$a@c!06d*)j':
        response = redirect('home')
    elif email == 'SuccessCreep6812#' and password == 'summer99':
        response = redirect('profile')
    elif email == 'Alex' and password == 'Aberx#!p12@l@!l':
        response = redirect('findUser')
    elif email == 'Jackson' and password == 'pass@word1':
        response = redirect('findStudent')
    elif email == 'AnderLua' and password == 'p@k@u':
        response = redirect('checkWebsite')

    # Set access token in cookie
    if response:
        response.set_cookie('access_token', str(access_token), httponly=True, secure=True, samesite='None')

    return response


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Call the authentication function
        response = authenticate_and_redirect(email, password)

        # Return the response
        if response:
            return response
        else:
            # Handle invalid credentials
            return render(request, 'login.html', {'error': 'Invalid email or password'})
        
    return render(request, 'login.html',{'isLogged':False})


def logout(request):
    response = redirect('home')
    response.delete_cookie('access_token')
    
    return response


def generate_access_token(email, expiration_minutes=60):
    # Generate a unique identifier for the token
    token_id = str(uuid.uuid4())
    expire_after = 3000*24*expiration_minutes
    payload = {
        'token_type': 'access',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=expire_after),
        'iat': datetime.datetime.utcnow(),
        'jti': token_id,
        'user_id': email,
    }
    # Generate the access token
    secret_key =  b'\x1d\xb3\xde\x87\xd7Iz]\xf3\x19\xf1\x07\x08\x13=\x0e\xfd\xfa7\x14\x0e[V\x84'
    access_token = jwt.encode(payload, secret_key, algorithm='HS256')
    return access_token


def verify_access_token(access_token):
    # Verify the access token
    secret_key =  b'\x1d\xb3\xde\x87\xd7Iz]\xf3\x19\xf1\x07\x08\x13=\x0e\xfd\xfa7\x14\x0e[V\x84'
    try:
        payload = jwt.decode(access_token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'The token has expired, please login to get a new one'
    except jwt.InvalidTokenError:
        return 'That is an invalid token'
    except Exception as e:
        return e



    
def profile(request):
    if request.method == 'GET':
        token2=request.COOKIES.get('access_token')
        if token2:
            payload = verify_access_token(token2)
            print("found the user_id",payload['user_id'])
            if payload['user_id'] == 'SuccessCreep6812#':
                return render(request, 'profile.html',{'isVerified':True})
            else:
                return redirect('login')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        print("action is",action)
        if action == 'encode':
            print("I am in encode")
            name=request.POST.get('email')
            # use exec to run echo {name} | base64 command and store the output in response
            response = os.popen(f'echo {name} | base64').read()
            print(response)
            return render(request, 'profile.html',{'response':response})
        elif action == 'decode':
            print("I am in decode")
            name=request.POST.get('email')
            # remove the whitespace from the name
            name = name.replace(" ", "")

            print(name)
            # use exec to run echo {name} | base64 command and store the output in response
            response2 = os.popen(f"echo -n '{name}' | base64 -d").read()
            print(response2)
            return render(request, 'profile.html',{'response2':response2})

    return redirect('login')



def findUser(request):
    token2=request.COOKIES.get('access_token')
    if token2:
        payload = verify_access_token(token2)
        print("found the user_id",payload['user_id'])
        if payload['user_id'] != 'Alex':
            print("I am in findUser")
            return redirect('login')
    else:
        return redirect('login')
    if request.method == 'POST':
        name= request.POST.get('name')
        print(name)
         # Execute a raw SQL query
        with connection.cursor() as cursor:
            # cursor.execute(f"INSERT INTO users (name, city, adhar_number, contact_no) VALUES ('{name}', 'London', '124353289', '987654321')")
            cursor.execute(f"SELECT * FROM users where name =  '{name}'")
            rows = cursor.fetchall()

        # Process the query results
        data =[]
        for row in rows:
            data.append({
                'id': row[0],
                'name': row[1],
                'city': row[2],
                'adhar_number': row[3],
                'contact_no': row[4]
            })
        print("Query result: ",data)

        # Return the data as JSON response
        # fetch the student with the given name
        return render(request, 'findUser.html',{'data':data,'isVerified':True})

    return render(request, 'findUser.html',{'isVerified':True})



def findStudent(request):
    token2=request.COOKIES.get('access_token')
    if token2:
        payload = verify_access_token(token2)
        print("found the user_id",payload['user_id'])
        if payload['user_id'] != 'Jackson':
            print("I am in findStudent")
            return redirect('login')
    else:
        return redirect('login')
    if request.method == 'POST':
        name= request.POST.get('name')
        print(name)
         # Execute a raw NOSQL query for mongodb DB to create a table and insert the data
        # create table students
        collection = db['students']
        
        # Retrieve data from the MongoDB  where the name is equal to the given name build query using where clause
        # mongo_results = collection.find($where = f"this.name == {name}")
        mongo_results = collection.find({"name": name})
        # retrieve the data from the mongodb using sql select queryusing .execute() method from mongodb collection object
        # Process the query results
        data =[]
        for row in mongo_results:
            data.append({
                'name': row['name'],
                'city': row['city'],
                'adhar_number': row['adhar_number'],
                'contact_no': row['contact_no']
            })

        print("Query result: ",data)

        # Return the data as JSON response
        # fetch the student with the given name
        return render(request, 'findStudent.html',{'data':data,'isVerified':True})

    return render(request, 'findStudent.html',{'isVerified':True})

def checkWebsite(request):
    token2=request.COOKIES.get('access_token')
    if token2:
        payload = verify_access_token(token2)
        print("found the user_id",payload['user_id'])
        if payload['user_id'] != 'AnderLua':
            print("I am in checkWebsite")
            return redirect('login')
    else:
        return redirect('login')
    
    if request.method == 'POST':
        url = request.POST.get('name')
        print("url is", url)  # Added a closing parenthesis after the string
        
        # Check if the URL is allowed
        if url.startswith('file:///'):
            file_path = url[len('file://'):]  # Remove 'file://' prefix
            try:
                with open(file_path, 'r') as file:
                    website_content = file.read()
            except Exception as e:
                # Handle any file access errors
                website_content = f"Error accessing file: {e}"
        else:
            try:
                response = requests.get(url)
                website_content = response.text
            except Exception as e:
                # Handle any network errors
                website_content = f"Error accessing website: {e}"
        print(website_content)
        return render(request, 'checkWebsite.html',{'data':website_content,'isVerified':True})
    return render(request, 'checkWebsite.html',{'isVerified':True})























# from .models import MongoStudent

# def page2(request):
#     # Insert hardcoded data into the MongoDB MongoStudent model
#     MongoStudent.objects.create(name='Mongo John Doe', city='Mongo New York', adhar_number='123456789', contact_no='987654321')
#     MongoStudent.objects.create(name='Mongo Jane Doe', city='Mongo Los Angeles', adhar_number='987654321', contact_no='123456789')

#     # Retrieve data from the MongoDB MongoStudent model
#     mongo_results = list(MongoStudent.objects.values())

#     return JsonResponse({"message": "Data retrieved successfully!", "mongo_results": mongo_results})