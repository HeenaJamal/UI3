from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, FileUploadForm
from .models import User, UploadedFile
from django.db import connection
import csv
from .forms import FileUploadForm



def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/message.html', {'message': 'Signup Successful'})
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email, password=password)
                return render(request, 'users/message.html', {'message': 'Login Successful'})
            except User.DoesNotExist:
                return render(request, 'users/message.html', {'message': 'Invalid Credentials'})
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})



def upload_file_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            table_name = uploaded_file.table_name

            # Parse the uploaded CSV file
            file_path = uploaded_file.file.path
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  # Get the header row
                rows = list(reader)  # Get the data rows

            # Dynamically create the table with headers as columns
            with connection.cursor() as cursor:
                # Construct the SQL for table creation
                create_table_query = f"""
                    CREATE TABLE `{table_name}` (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        {", ".join([f"`{col}` TEXT" for col in headers])}
                    )
                """
                cursor.execute(create_table_query)

                # Insert the rows into the table
                for row in rows:
                    placeholders = ", ".join(["%s"] * len(headers))
                    insert_query = f"""
                        INSERT INTO `{table_name}` ({", ".join([f"`{col}`" for col in headers])})
                        VALUES ({placeholders})
                    """
                    cursor.execute(insert_query, row)

            return render(request, 'users/message.html', {
                'message': f'File uploaded successfully. Data stored in table: {table_name}'
            })
    else:
        form = FileUploadForm()
    return render(request, 'users/upload.html', {'form': form})

