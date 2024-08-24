from django.shortcuts import render
from .forms import MultiplierForm
import matplotlib.pyplot as plt
import numpy as np
import io
import urllib, base64
from django.http import HttpResponse, JsonResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_svg import FigureCanvasSVG

def plot_view(request):
    """
    Handles the user input, generates a plot based on the input, and renders the plot in the desired format.
    """

    # Instantiate the form with POST data if available, otherwise create a blank form
    form = MultiplierForm(request.POST or None)

    # Initialize plot_url to None; this will hold the image data URL once generated
    plot_url = None
    output_format = 'png'  # Default format

    # Check if the request is a POST request and if the submitted form data is valid
    if request.method == 'POST' and form.is_valid():
        # Retrieve the multiplier value from the form
        multiplier = form.cleaned_data['multiplier']

        # Retrieve the selected output format (PNG or SVG)
        output_format = form.cleaned_data['format']

        # Generate random data for the x and y axes
        x = np.random.rand(10)
        y = np.random.rand(10) * multiplier

        # Create a new plot using Matplotlib
        fig, ax = plt.subplots()
        ax.plot(x, y, marker='o')  # Plot the random data with circular markers
        ax.set_title('Random Data with Multiplier')  # Set the title of the plot
        ax.set_xlabel('X values')  # Label the x-axis
        ax.set_ylabel('Y values')  # Label the y-axis

        # Create an in-memory buffer to hold the plot image data
        buf = io.BytesIO()

        # Check if the user selected PNG as the output format
        if output_format == 'png':
            # Render the plot to the buffer as a PNG image
            canvas = FigureCanvas(fig)
            canvas.print_png(buf)
            content_type = 'image/png'  # Set the content type to PNG

        # Check if the user selected SVG as the output format
        elif output_format == 'svg':
            # Render the plot to the buffer as an SVG image
            canvas = FigureCanvasSVG(fig)
            canvas.print_svg(buf)
            content_type = 'image/svg+xml'  # Set the content type to SVG

        # Move the buffer's cursor to the beginning
        buf.seek(0)

        # Encode the image data to base64 to embed it directly in the HTML
        string = base64.b64encode(buf.read()).decode()

        # Create a data URL that can be used directly in the HTML <img> or <object> tag
        plot_url = f"data:{content_type};base64,{string}"

        # Close the plot to free memory
        plt.close(fig)

    # Check if the request is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # If it's an AJAX request, return only the updated part of the HTML (the plot part)
        return render(request, 'plotter/plot.html', {
            'form': form,
            'plot_url': plot_url,
            'output_format': output_format
        })

    # If it's a normal request, return the full page
    return render(request, 'plotter/plot.html', {
        'form': form,
        'plot_url': plot_url,
        'output_format': output_format  # Default to PNG if no format is selected
    })
