from django.shortcuts import render
from .forms import MultiplierForm
import matplotlib.pyplot as plt
import numpy as np
import io
import urllib, base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_svg import FigureCanvasSVG
from .calculations import calculate_output 

CLASS_A_PRESET = {
    'ibias': 0,  # Example value
    'isig': 1,   # Example value
    'i2': 0,     # Example value
    'i3': 0,     # Example value
    'vknee': 0.1,  # Example value
    'vdc': 1.1,   # Example value
    'mag_v1': 1.155, # Example value
    'mag_v2': 0, # Example value
    'mag_v3': 0.3, # Example value
    'ang_v1': 180, # Example value
    'ang_v2': 0,  # Example value
    'ang_v3': 0,  # Example value
}

def plot_view(request):
    plot_url = None

    if request.method == 'POST':
        form = MultiplierForm(request.POST)
        if form.is_valid():
            preset = form.cleaned_data.get('preset')
            output_format = form.cleaned_data.get('output_format', 'svg')

            # Apply the preset logic
            if preset == 'A':
                # If preset is 'A', use CLASS_A_PRESET for calculations
                output_values = calculate_output(CLASS_A_PRESET)
            else:
                # If preset is 'custom', use the form data for calculations
                output_values = calculate_output(form.cleaned_data)

    else:
        # On GET request or initial load, apply the Class A preset
        form = MultiplierForm(initial=CLASS_A_PRESET)
        output_values = calculate_output(CLASS_A_PRESET)
        output_format = 'svg'
    


    # Generate the plot based on output_values
    if output_values.get('voltage_wfm'):
        x = output_values['angles_wfm']
        y = output_values['voltage_wfm']

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(output_values['current_angles_wfm'],output_values['zeroknee'], label="Zeroknee",linewidth=1.8)
        ax.plot(x, y, label="Voltage", linewidth=1.8)
        ax.plot(output_values['current_angles_wfm'],output_values['current_wfm'], label="Current",linewidth=1.8)
        ax.set_ylim([0, None])
        ax.set_xlim([min(output_values['angles_wfm'][0], output_values['current_angles_wfm'][0]),
                    max(output_values['angles_wfm'][-1], output_values['current_angles_wfm'][-1])])
        ax.legend()

        buf = io.BytesIO()
        if output_format == 'png':
            canvas = FigureCanvas(fig)
            canvas.print_png(buf)
            content_type = 'image/png'
        else:
            canvas = FigureCanvasSVG(fig)
            canvas.print_svg(buf)
            content_type = 'image/svg+xml'

        buf.seek(0)
        string = base64.b64encode(buf.read()).decode()
        plot_url = f"data:{content_type};base64,{string}"
        plt.close(fig)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'plotter/plot.html', {
            'form': form,
            'plot_url': plot_url,
            'output_format': output_format,
            'output_values': output_values
        })

    return render(request, 'plotter/plot.html', {
        'form': form,
        'plot_url': plot_url,
        'output_format': output_format,
        'output_values': output_values
    })
