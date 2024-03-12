from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('login/', views.login, name="login"),
    path('homepage/', views.homepage, name="homepage"),
    path('check_duplicate_nric/', views.check_duplicate_nric, name="check_duplicate_nric"),
    path('addPatient/', views.addPatient, name="addPatient"),
    path('editPatient/<int:pk>/', views.editPatient, name="editPatient"),
    path('deletePatient/<int:pk>/', views.deletePatient, name="deletePatient"),
    path('deletedRecordsArchive/', views.deletedRecordsArchive, name="deletedRecordsArchive"),
    path('medicationOrder/', views.medicationOrder, name="medicationOrder"),
    path('fetch_patient_name/', views.fetch_patient_name, name="fetch_patient_name"),
    path('check_allergy/', views.check_allergy, name="check_allergy"),
    path('addOrder/', views.addOrder, name="addOrder"),
    path('complete_order/<int:pk>/', views.complete_order, name="complete_order"),
    path('changePassword/', views.changePassword, name="changePassword"),
    path('search_patients', views.search_patients, name="search_patients"),
    path('logout/', views.logout, name="logout")
]