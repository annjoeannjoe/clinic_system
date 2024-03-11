from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import Patient, Property, Medication, MedicationOrder, OrderItem
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import datetime, date
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator

# Create your views here.



def users(request):
    return HttpResponse("Hello World")

def login(request):
        if request.method == 'POST':
            email = request.POST['email'].lower()
            password = request.POST['password']

            try:
                user = User.objects.get(email=email)

            except User.DoesNotExist:
                messages.error(request,"Account with this email does not exist.")
                return render(request, 'login.html')

            if check_password(password, user.password):
                auth.login(request,user)
                return redirect('homepage')
            else:
                messages.error(request, 'Incorrect password. Please try again.')
                return render(request, 'login.html')
        
        return render(request,'login.html')


def homepage(request):
    patients = Patient.objects.filter(deleted=False).order_by('created_at')

    allergies = Property.objects.all()
    
    # Create paginator
    paginator = Paginator(patients,10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    max_pages = paginator.num_pages
    current_page = page.number
    page_range = range(max(1, current_page - 2), min(max_pages, current_page + 2) + 1)

    context={
        'patients': page,
        'allergies': allergies,
        'page_range': page_range
    }

    return render(request,'homepage.html', context)

def check_duplicate_nric(request):
    if request.method == "POST":
        nric_passport = request.POST.get('nric_passport', None)
        if nric_passport:
            if Patient.objects.filter(nric_passport=nric_passport).exists():
                return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})

def addPatient(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        nric_passport = request.POST['nric_passport']
        dob_str = request.POST['dobInput']
        age = request.POST['ageInput']
        allergies_ids = request.POST.getlist('allergies')

        # Convert dob_str to a date object
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

        if fullname and nric_passport and dob and age:
            
            # Perform age calculation
            #today = date.today()
            #calculated_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            
            # Convert age to an integer
            age = int(age)
            
            patient = Patient(
                fullname=fullname,
                nric_passport=nric_passport,
                dob=dob,
                age=age
            )
            patient.save()

            # Add allergies for patient
            for allergy_id in allergies_ids:
                allergy = Property.objects.get(pk=allergy_id)
                patient.allergies.add(allergy)

            messages.success(request, 'The new patient has been successfully added.')
            return redirect('homepage')
    return render(request, "homepage.html")

def editPatient(request,pk):
    patient = get_object_or_404(Patient,pk=pk)

    if request.method == "POST":
        patient.fullname = request.POST['fullname']
        patient.nric_passport = request.POST['nric_passport']
        patient.dob_str = request.POST['dobInput']
        patient.age = request.POST['ageInput']

        patient.save()

        # Update patient allergies
        allergies_selected = request.POST.getlist("allergies")
        patient.allergies.clear() # Clear existing allergies
        for allergy_id in allergies_selected:
            allergy = Property.objects.get(id=allergy_id)
            patient.allergies.add(allergy)

        messages.success(request, 'The change(s) made has been successfully saved.')
        return HttpResponseRedirect(reverse('homepage'))
    
    return render(request, 'homepage.html')

def deletePatient(request,pk):
    patient = get_object_or_404(Patient, id=pk)

    patient.soft_delete()

    return redirect('homepage')


def deletedRecordsArchive(request):
    patients = Patient.objects.filter(deleted=True).order_by('created_at')
    allergies = Property.objects.all()

    # Create paginator
    paginator = Paginator(patients,10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    max_pages = paginator.num_pages
    current_page = page.number
    page_range = range(max(1, current_page - 2), min(max_pages, current_page + 2) + 1)

    context={
        'patients': patients,
        'page_range': page_range,
        'allergies': allergies
    }

    return render(request,'deletedRecordsArchive.html',context)

def medicationOrder(request):
    patients = Patient.objects.filter(deleted=False).order_by('created_at')
    medications = Medication.objects.all()
    medication_orders = MedicationOrder.objects.all()
    order_items = OrderItem.objects.all()

    # Create paginator
    paginator = Paginator(medication_orders,10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    max_pages = paginator.num_pages
    current_page = page.number
    page_range = range(max(1, current_page - 2), min(max_pages, current_page + 2) + 1)

    context={
        'patients': patients,
        'medications': medications,
        'medication_orders': page,
        'order_items': order_items,
        'page_range': page_range,
    }
    return render (request, 'medicationOrder.html', context)

def fetch_patient_name(request):
    if request.method == 'GET':
        nric_passport = request.GET.get('nric_passport')
        try:
            patient = Patient.objects.get(nric_passport=nric_passport)
            patient_name = patient.fullname
            return JsonResponse({'patient_name': patient_name})
        except Patient.DoesNotExist:
            return JsonResponse({'error': 'Patient not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def addOrder(request):
    medications = Medication.objects.all()

    if request.method == "POST":
        nric_passport = request.POST.get('nric_passport')
        medication_ids = request.POST.getlist('medication')
        quantities = request.POST.getlist('quantity')

        try:
            patient = Patient.objects.get(nric_passport=nric_passport)
        except Patient.DoesNotExist:
            messages.error(request, "Patient not found!")
            return redirect('addOrder')
        
        # Generate order number
        try:
            latest_order = MedicationOrder.objects.latest('created_at')
            last_number = int(latest_order.order_number.split('-')[1])
            next_number = last_number + 1
        except MedicationOrder.DoesNotExist:
            next_number = 1

        order_number = f'ORD-{next_number:06d}'


        medication_order = MedicationOrder.objects.create(
            patient=patient, 
            order_number=order_number,
            order_status = 'Pending')

        for med_id, qty in zip(medication_ids, quantities):
            medication = Medication.objects.get(pk=med_id)
            quantity = int(qty)

            # Set the order field explicitly
            order_item = OrderItem.objects.create(order=medication_order, medication=medication, quantity=quantity)
        
        messages.success(request, "Order placed successfully!")
        return redirect('medicationOrder')

    context = {
        'medications': medications,
    }

    return render(request, 'addOrder.html', context)




def check_allergy(request):
    if request.method == 'POST':
        medication_id = request.POST.get('medication')
        nric_passport = request.POST.get('nric_passport')

        # Retrieve patient and medication
        try:
            patient = Patient.objects.get(nric_passport=nric_passport)
            medication = Medication.objects.get(pk=medication_id)
        except Patient.DoesNotExist:
            return HttpResponse("Patient not found!")  # Return an error message if patient not found
        except Medication.DoesNotExist:
            return HttpResponse("Medication not found!")  # Return an error message if medication not found

        # Check for allergies
        patient_allergies = patient.allergies.all()
        medication_properties = medication.properties.all()

        for allergy in patient_allergies:
            for property in medication_properties:
                if allergy == property:
                    return JsonResponse({'allergic': True, 'message': 'Patient is allergic to this medication!'})
        return JsonResponse({'allergic': False})
    
    return render (request,'medicationOrder.html')

def complete_order(request,pk):
    order_number = get_object_or_404(MedicationOrder, id=pk)

    if request.method == "POST":
        order_number.order_status = 'Fulfilled'
        order_number.save()

        messages.success(request,'The order has been completed successfully!')
        return redirect('medicationOrder')
    return render(request, 'medicationOrder.html')

def changePassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,'Your password was successfully changed.')
            return redirect('changePassword')
        else:
            messages.error(request,'Your current password or new password or confirm new password is incorrect. Please try again.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'changePassword.html', {'form': form})


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect ('login')
            
       
