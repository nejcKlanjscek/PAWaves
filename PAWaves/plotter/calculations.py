import numpy as np
from collections import defaultdict

def calculate_output(form_data):
    # Constants
    lt = 10 / np.log(10)
    output_values = defaultdict(list)

    # Extract values from form_data
    ibias = form_data['ibias']
    isig = form_data['isig']
    i2 = form_data['i2']
    i3 = form_data['i3']
    
    vknee = form_data.get('vknee', 0.000001)
    vdc = form_data['vdc']
    
    mag_v1 = form_data['mag_v1']
    mag_v2 = form_data['mag_v2']
    mag_v3 = form_data['mag_v3']
    
    ang_v1 = np.pi * form_data['ang_v1'] / 180
    ang_v2 = np.pi * form_data['ang_v2'] / 180
    ang_v3 = np.pi * form_data['ang_v3'] / 180

    number_of_points = 360

    vmin = 10
    

    # Voltage calculation
    for n in range(1, number_of_points):
        ang = (4 * np.pi * n) / number_of_points
        v = vdc + mag_v1 * np.cos(ang + ang_v1) + mag_v2 * np.cos((2 * ang) + ang_v2) + mag_v3 * np.cos((3 * ang) + ang_v3)
        if v < vmin:
            vmin = v
        output_values['voltage_wfm'].append(v)
        output_values['angles_wfm'].append(ang)
        

    #? this is textbox 17.. idk
    output_values['vmin'] = np.floor(1000 * vmin) / 1000  # Output vmin

    # Initialize harmonic arrays
    ihc = np.zeros(11)
    ihs = np.zeros(11)
    Idc = 0
    delt = 4 * np.pi / number_of_points

    # Current waveform and Fourier analysis
    for n in range(number_of_points):
        ang = 4 * np.pi * n / number_of_points
        i = ibias + isig * (np.cos(ang) + i2 * np.sin(2 * ang) - i3 * np.cos(3 * ang))
        output_values['zeroknee'].append(i)
        if i < 0:
            i = 0
        v = vdc + mag_v1 * np.cos(ang + ang_v1) + mag_v2 * np.cos(2 * ang + ang_v2) + mag_v3 * np.cos(3 * ang + ang_v3)
        if v < 0:
            v = 0
        i = i * (1 - np.exp(-v / vknee))
        output_values['current_wfm'].append(i)
        output_values['current_angles_wfm'].append(ang)
        
        Idc += i * delt
        for j in range(1, 11):
            ihc[j] += i * delt * np.cos(j * ang)
            ihs[j] += i * delt * np.sin(j * ang)

    ihc /= (2 * np.pi)
    ihs /= (2 * np.pi)
    Idc /= (4 * np.pi)

    # Normalization and power calculations
    Prf = -(ihc[1] * mag_v1 * np.cos(ang_v1) - ihs[1] * mag_v1 * np.sin(ang_v1)) / 2
    PclA = (vdc - 0.001) / 4
    PdB = lt * np.log(Prf / PclA)
    PdB = np.floor(10 * PdB) / 10
    output_values['pout'] = PdB  # Output PdB

    Pdc = vdc * Idc
    effcy = 100 * Prf / Pdc
    output_values['eta'] = np.floor(10 * effcy) / 10  # Output efficiency

    # Harmonic impedances
    mag1 = -(ihc[1] ** 2 + ihs[1] ** 2)
    R1 = (1 / mag1) * (ihc[1] * mag_v1 * np.cos(ang_v1) + ihs[1] * mag_v1 * np.sin(ang_v1))
    X1 = -(1 / mag1) * (ihc[1] * mag_v1 * np.sin(ang_v1) - ihs[1] * mag_v1 * np.cos(ang_v1))
    output_values['re_v1'] = np.floor(100 * (R1 / 2)) / 100  # Output R1
    output_values['im_v1'] = np.floor(100 * (X1 / 2)) / 100  # Output X1

    mag2 = -(ihc[2] ** 2 + ihs[2] ** 2)
    R2 = (1 / mag2) * (ihc[2] * mag_v2 * np.cos(ang_v2) + ihs[2] * mag_v2 * np.sin(ang_v2))
    output_values['re_v2'] = np.floor(100 * (R2 / 2)) / 100  # Output R2
    X2 = -(1 / mag2) * (ihc[2] * mag_v2 * np.sin(ang_v2) - ihs[2] * mag_v2 * np.cos(ang_v2))
    output_values['im_v2'] = np.floor(100 * (X2 / 2)) / 100  # Output X2

    mag3 = -(ihc[3] ** 2 + ihs[3] ** 2)
    R3 = (1 / mag3) * (ihc[3] * mag_v3 * np.cos(ang_v3) + ihs[3] * mag_v3 * np.sin(ang_v3))
    output_values['re_v3'] = np.floor(100 * (R3 / 2)) / 100  # Output R3
    X3 = -(1 / mag3) * (ihc[3] * mag_v3 * np.sin(ang_v3) - ihs[3] * mag_v3 * np.cos(ang_v3))
    output_values['im_v3'] = np.floor(100 * (X3 / 2)) / 100  # Output X3

    return output_values
