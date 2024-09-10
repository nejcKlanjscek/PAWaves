import numpy as np
from collections import defaultdict

def calculate_output(form_data):
    # Constants
    lt = 10 / np.log(10)
    output_values = defaultdict(list)

    # Extract values from form_data
    ibias = form_data['ibias']
    i1 = form_data['i1']
    i2 = form_data['i2']
    i3 = form_data['i3']
    i4 = form_data['i4']
    i5 = form_data['i5']
    i6 = form_data['i6']
    i7 = form_data['i7']
    
    vknee = form_data.get('vknee', 0.001)
    vdc = form_data['vdc']
    
    mag_v1 = form_data['mag_v1']
    mag_v2 = form_data['mag_v2']
    mag_v3 = form_data['mag_v3']
    mag_v4 = form_data['mag_v4']
    mag_v5 = form_data['mag_v5']
    mag_v6 = form_data['mag_v6']
    mag_v7 = form_data['mag_v7']
    
    ang_v1 = np.pi * form_data['ang_v1'] / 180
    ang_v2 = np.pi * form_data['ang_v2'] / 180
    ang_v3 = np.pi * form_data['ang_v3'] / 180
    ang_v4 = np.pi * form_data['ang_v4'] / 180
    ang_v5 = np.pi * form_data['ang_v5'] / 180
    ang_v6 = np.pi * form_data['ang_v6'] / 180
    ang_v7 = np.pi * form_data['ang_v7'] / 180

    number_of_points = 360

    vmin = 10
    

    # Vmin Voltage calculation
    for n in range(number_of_points):
        ang = 4 * np.pi * n / number_of_points #Calculation of timesteps of ang for 2 periods of the input signal
        v = vdc + mag_v1 * np.cos(ang + ang_v1) + mag_v2 * np.cos((2 * ang) + ang_v2) + mag_v3 * np.cos((3 * ang) + ang_v3) + mag_v4 * np.cos((4*ang) + ang_v4) + mag_v5 * np.cos((5 * ang) + ang_v5) + mag_v6 * np.cos((6 * ang) + ang_v6) + mag_v7 * np.cos((7 * ang) + ang_v7) #Summming up harmonics
        if v < vmin:    #Update vmin value
            vmin = v
        output_values['voltage_wfm'].append(v)     # Plot point v - y axis
        output_values['angles_wfm'].append(ang)    # Plot point ang - x axis
        output_values['vmin'] = np.round(vmin, 3)  # Output vmin


    # Initialize harmonic arrays
    ihc = np.zeros(7)
    ihs = np.zeros(7)
    Idc = 0
    delt = 4 * np.pi / number_of_points     #Calculation of minimal timestep for 2 periods of the input signal


    # Current waveform and Fourier analysis
    for n in range(number_of_points):
        ang = 4 * np.pi * n / number_of_points  #Calculation of timesteps of ang for 2 periods of the input signal
        i = ibias + i1 * (np.cos(ang) + i2 * np.sin(2 * ang) - i3 * np.cos(3 * ang) + i4 * np.sin(4 * ang) - i5 * np.cos(5 * ang) + i6 * np.sin(6 * ang) - i7 * np.cos(7 * ang))
        if i < 0:   #Clip the current
            i = 0
        output_values['zeroknee'].append(i) # Plot point i without knee voltage - y axis
        v = vdc + mag_v1 * np.cos(ang + ang_v1) + mag_v2 * np.cos((2 * ang) + ang_v2) + mag_v3 * np.cos((3 * ang) + ang_v3) + mag_v4 * np.cos((4*ang) + ang_v4) + mag_v5 * np.cos((5 * ang) + ang_v5) + mag_v6 * np.cos((6 * ang) + ang_v6) + mag_v7 * np.cos((7 * ang) + ang_v7)
        if i < 0:   #Clip the current
            i = 0
        i = i * (1 - np.exp(-v / vknee))        #Calculate the approximation of knee voltage
        output_values['current_wfm'].append(i)  #Plot point i with knee voltage - y axis
        output_values['current_angles_wfm'].append(ang) #Plot point ang - x axis
        
        Idc += i * delt

        #Fourier analysis loop
        for j in range(7):  #These arrays store the cosine coefficients for the current waveform at harmonic j
            ihc[j] += i * delt * np.cos((j+1) * ang)    #Accumulated cosine coefficient for the j-th harmonic
            ihs[j] += i * delt * np.sin((j+1) * ang)    #Accumulated sine coefficient for the j-th harmonic

    #Normalization of the coeeficients
    ihc /= (2 * np.pi)
    ihs /= (2 * np.pi)
    Idc /= (4 * np.pi)

    # Normalization and power calculations
    Prf = -(ihc[0] * mag_v1 * np.cos(ang_v1) - ihs[0] * mag_v1 * np.sin(ang_v1)) / 2
    PclA = (vdc - 0.001) / 4
    PdB = lt * np.log(Prf / PclA)
    output_values['pout'] = np.round(PdB, 2)  # Output PdB


    Pdc = vdc * Idc
    effcy = 100 * Prf / Pdc
    output_values['eta'] = np.round(effcy, 2)  # Output efficiency

    # Harmonic impedances
    mag1 = -(ihc[0] ** 2 + ihs[0] ** 2)
    R1 = (1 / mag1) * (ihc[0] * (mag_v1 * np.cos(ang_v1)) + ihs[0] * (-mag_v1 * np.sin(ang_v1)))
    X1 = -(1 / mag1) * (ihc[0] * (-mag_v1 * np.sin(ang_v1)) - ihs[0] * (mag_v1 * np.cos(ang_v1)))
    output_values['re_v1'] = np.round(R1 / 2, 3)  # Output R1 
    output_values['im_v1'] = np.round(X1 / 2, 3)  # Output X1

    mag2 = -(ihc[1] ** 2 + ihs[1] ** 2)
    R2 = (1 / mag2) * (ihc[1] * (mag_v2 * np.cos(ang_v2)) + ihs[1] * (-mag_v2 * np.sin(ang_v2)))
    X2 = -(1 / mag2) * (ihc[1] * (-mag_v2 * np.sin(ang_v2)) - ihs[1] * (mag_v2 * np.cos(ang_v2)))
    output_values['re_v2'] = np.round(R2 / 2, 3)  # Output R2
    output_values['im_v2'] = np.round(X2 / 2, 3)  # Output X2

    mag3 = -(ihc[2] ** 2 + ihs[2] ** 2)
    R3 = (1 / mag3) * (ihc[2] * (mag_v3 * np.cos(ang_v3)) + ihs[2] * (-mag_v3 * np.sin(ang_v3)))
    X3 = -(1 / mag3) * (ihc[2] * (-mag_v3 * np.sin(ang_v3)) - ihs[2] * (mag_v3 * np.cos(ang_v3)))
    output_values['re_v3'] = np.round(R3 / 2, 3)  # Output R3
    output_values['im_v3'] = np.round(X3 / 2, 3)  # Output X3

    mag4 = -(ihc[3] ** 2 + ihs[3] ** 2)
    R4 = (1 / mag4) * (ihc[3] * (mag_v4 * np.cos(ang_v4)) + ihs[3] * (-mag_v4 * np.sin(ang_v4)))
    X4 = -(1 / mag4) * (ihc[3] * (-mag_v4 * np.sin(ang_v4)) - ihs[3] * (mag_v4 * np.cos(ang_v4)))
    output_values['re_v4'] = np.round(R4 / 2, 3)  # Output R4
    output_values['im_v4'] = np.round(X4 / 2, 3)  # Output X4

    mag5 = -(ihc[4] ** 2 + ihs[4] ** 2)
    R5 = (1 / mag5) * (ihc[4] * (mag_v5 * np.cos(ang_v5)) + ihs[4] * (-mag_v5 * np.sin(ang_v5)))
    X5 = -(1 / mag5) * (ihc[4] * (-mag_v5 * np.sin(ang_v5)) - ihs[4] * (mag_v5 * np.cos(ang_v5)))
    output_values['re_v5'] = np.round(R5 / 2, 3)  # Output R5
    output_values['im_v5'] = np.round(X5 / 2, 3)  # Output X5

    mag6 = -(ihc[5] ** 2 + ihs[5] ** 2)
    R6 = (1 / mag6) * (ihc[5] * (mag_v6 * np.cos(ang_v6)) + ihs[5] * (-mag_v6 * np.sin(ang_v6)))
    X6 = -(1 / mag6) * (ihc[5] * (-mag_v6 * np.sin(ang_v6)) - ihs[5] * (mag_v6 * np.cos(ang_v6)))
    output_values['re_v6'] = np.round(R6 / 2, 3)  # Output R6
    output_values['im_v6'] = np.round(X6 / 2, 3)  # Output X6

    mag7 = -(ihc[6] ** 2 + ihs[6] ** 2)
    R7 = (1 / mag7) * (ihc[6] * (mag_v7 * np.cos(ang_v7)) + ihs[6] * (-mag_v7 * np.sin(ang_v7)))
    X7 = -(1 / mag7) * (ihc[6] * (-mag_v7 * np.sin(ang_v7)) - ihs[6] * (mag_v7 * np.cos(ang_v7)))
    output_values['re_v7'] = np.round(R7 / 2, 3)  # Output R7
    output_values['im_v7'] = np.round(X7 / 2, 3)  # Output X7

    return output_values
