from django.shortcuts import render
from RestrauntApp.models import Restraunt
from django.contrib.auth import login,logout,authenticate
# Create your views here.
def home(request):
    return render(request,'home/index.html')

def handle_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            
    return render(request,'home/login.html')

def restraunt_register(request):
    submit = False
    if request.method == "POST":
        restraunt_name = request.POST['restraunt_name']
        owner_name = request.POST['owner_name']
        contact_no = request.POST['contact_no']
        fssai = request.POST['fssai']
        opening_timing = request.POST['open_time']
        closing_timing = request.POST['close_time']
        food_type = request.POST['food_type']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        address_line_3 = request.POST['address_line_3']
        state = request.POST['state']
        city = request.POST['city']
        zip_code = request.POST['zip_code']
        new_restraunt_request = Restraunt.objects.create(
            name = restraunt_name,
            contact_no = contact_no,
            address_line_1 = address_line_1,
            address_line_2 = address_line_2,
            address_line_3 = address_line_3,
            state = state,
            city = city,
            zip_code = zip_code,
            closing_timing = closing_timing,
            opening_timing = opening_timing,
            food_type = food_type,
            fssai_no = fssai,
            owner_name = owner_name,
        )
        new_restraunt_request.save()
        submit = True
    context = {
        'submit':submit
    }
    
    return render(request,'home/restraunt_register.html',context)