from django.urls import path
from . import views

# Define the URL patterns for the plotter app
urlpatterns = [
    # Map the root URL (e.g., /plotter/) to the plot_view function
    path('', views.plot_view, name='plot_view'),
]
