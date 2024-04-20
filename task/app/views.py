from django.shortcuts import render,redirect
from .forms import CreateUserForm,LoginForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import os
import docx

# Create your views here.
@login_required(login_url="login")
def homepage(request):
    if request.method == "POST":
        uploaded_file = request.FILES["file"]
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        filename = os.path.join(settings.MEDIA_ROOT,uploaded_file.name)
        extracted_text = extract_doc_text(filename)
        context = {"file":extracted_text}
        return render(request,"app/homepage.html",context)
    return render(request,"app/homepage.html")


def extract_doc_text(filename):
    try:
        # Open the DOC file
        doc = docx.Document(filename)

        # Extract text from all paragraphs
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)

        # Combine extracted text into a single string
        extracted_text = '\n'.join(full_text)
        return extracted_text
    except docx.exceptions.DocxError:
        # Handle potential errors (e.g., corrupted file)
        return "Error: Unable to extract text from DOC file."

@login_required(login_url="login")
def showRes(request):
    return render(request,"app/showRes.html")

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        
    context = {"registerForm":form}
    
    return render(request,"app/register.html",context=context)

def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request,data = request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request,username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect("home")
    context = {'loginF':form}
    return render(request,"app/login.html",context)

    

def logout(request):
    auth.logout(request)
    return redirect("home")
