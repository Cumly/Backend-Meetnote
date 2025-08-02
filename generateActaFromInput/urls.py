from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('getTranscriptionByVideo/', views.TranscriptionByVideo),
    path('getTranscriptionByAudio/', views.TranscriptionByAudio),
    path('getTranscriptionByText/', views.TranscriptionByText),
    path('generateFormat/', views.TranscriptionByText)

]
