from django.shortcuts import render
from .forms import MultiplierForm
import matplotlib.pyplot as plt
import numpy as np
import io
import urllib, base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_svg import FigureCanvasSVG
from .calculations import calculate_output 
from pathlib import Path
from django.conf import settings
import csv
from matplotlib.ticker import FormatStrFormatter, MultipleLocator


def plot_view(request):
    plot_url = None
    import json

    json_file_path = Path(settings.STATIC_ROOT) / 'presets' / 'class_presets.json'

    # Load the JSON data
    with open(json_file_path, 'r') as f:
        preset_values = json.load(f)


    if request.method == 'POST':
        form = MultiplierForm(request.POST)
        if form.is_valid():
            preset = form.cleaned_data.get('preset')
            output_format = form.cleaned_data.get('output_format', 'svg')

            if preset != 'custom':
                output_values = calculate_output(preset_values[preset])
            else:
                output_values = calculate_output(form.cleaned_data)

    else:
        # On GET request or initial load, apply the Class A preset
        form = MultiplierForm(initial=preset_values['A'])
        # output_values = calculate_output(preset_values['A'])
        output_values = calculate_output(preset_values['A'])
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
        ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
        ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi / 12))
        ax.xaxis.set_major_formatter(plt.FuncFormatter(multiple_formatter()))
        ax.grid()
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=14)

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

        
        # Create a CSV file in memory
        csv_output = io.StringIO()
        writer = csv.writer(csv_output)

        # Write the header
        writer.writerow(['X(Angle)','Y(Voltage)', 'Y(Current)', 'Y(Zeroknee)'])

        # Write the data rows
        for angle, voltage, current, zeroknee in zip(output_values['current_angles_wfm'],output_values['voltage_wfm'], output_values['current_wfm'], output_values['zeroknee']):
            writer.writerow([angle, voltage, current, zeroknee])

        csv_output.seek(0)  # Rewind the CSV file to the beginning

        # Create a downloadable link for the CSV file
        csv_download_url = f"data:text/csv;base64,{base64.b64encode(csv_output.getvalue().encode()).decode()}"


    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'plotter/plot.html', {
            'form': form,
            'plot_url': plot_url,
            'output_format': output_format,
            'output_values': output_values,
            'csv_download_url': csv_download_url
        })

    return render(request, 'plotter/plot.html', {
        'form': form,
        'plot_url': plot_url,
        'output_format': output_format,
        'output_values': output_values,
        'csv_download_url': csv_download_url
    })


def multiple_formatter(denominator=2, number=np.pi, latex='\pi'):
    def gcd(a, b):
        while b:
            a, b = b, a%b
        return a
    def _multiple_formatter(x, pos):
        den = denominator
        num = int(np.rint(den*x/number))
        com = gcd(num,den)
        (num,den) = (int(num/com),int(den/com))
        if den==1:
            if num==0:
                return r'$0$'
            if num==1:
                return r'$%s$'%latex
            elif num==-1:
                return r'$-%s$'%latex
            else:
                return r'$%s%s$'%(num,latex)
        else:
            if num==1:
                return r'$\frac{%s}{%s}$'%(latex,den)
            elif num==-1:
                return r'$\frac{-%s}{%s}$'%(latex,den)
            else:
                return r'$\frac{%s%s}{%s}$'%(num,latex,den)
    return _multiple_formatter