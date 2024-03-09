from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import Patient, Property, Medication
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import datetime, date
from django.urls import reverse

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

    context={
        'patients': patients,
        'allergies': allergies,
    }

    return render(request,'homepage.html', context)

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

    context={
        'patients': patients,
    }

    return render(request,'deletedRecordsArchive.html',context)

def medicationOrder(request):
    patients = Patient.objects.filter(deleted=False).order_by('created_at')
    medications = Medication.objects.all()

    context={
        'patients': patients,
        'medications': medications,
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

def check_allergy(request):
    if request.method == "POST" and request.is_ajax():
        medication_id = request.POST.get('medication_id')
        nric_passport = request.POST.get('nric_passport')

        try:
            medication = Medication.objects.get(pk=medication_id)
            patient = Patient.objects.get(nric_passport=nric_passport)

            allergies = patient.allergies.all()
            medication_properties = medication.properties.all()

            # Check if any property ID of the medication matches any property ID of the patient's allergies
            matched_allergy = any(property.id in [allergy.id for allergy in allergies] for property in medication_properties)

            return JsonResponse({'has_allergy': matched_allergy})
        except Medication.DoesNotExist:
            return JsonResponse({'error': 'Medication not found'}, status=400)
        except Patient.DoesNotExist:
            return JsonResponse({'error': 'Patient not found'}, status=400)
        
    return JsonResponse({'error': 'Invalid request'}, status=400)
        
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect ('login')
            
       
