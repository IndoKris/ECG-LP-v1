import pandas as pd
import numpy as np
import wfdb
import matplotlib.pyplot as plt
import os
import ssl

# Ensure SSL context for downloading record files from PhysioNet
ssl._create_default_https_context = ssl._create_unverified_context

os.makedirs('images', exist_ok=True)
selected_df = pd.read_csv('selected.csv')

answer_key = []

for idx, row in selected_df.iterrows():
    ecg_id = row['ecg_id']
    true_class = row['class']
    code = row['code']
    filename_hr = row['filename_hr']

    # Path in PhysioNet repository (base url is https://physionet.org/files/ptb-xl/1.0.3/)
    # wfdb.rdsamp can download directly using pn_dir='ptb-xl/1.0.3/' + path or similar, or local download
    # Let's test wfdb.rdsamp with pn_dir='ptb-xl/1.0.3/' + dirname and record_name
    dirname = os.path.dirname(filename_hr)
    basename = os.path.basename(filename_hr)

    try:
        signal, fields = wfdb.rdsamp(basename, pn_dir=f'ptb-xl/1.0.3/{dirname}')
    except Exception as e:
        print(f'Error reading record {ecg_id} ({filename_hr}): {e}')
        continue

    # Plot 12 leads in a 3x4 layout, plus long lead II strip
    # Standard 12 leads: I, II, III, aVR, aVL, aVF, V1, V2, V3, V4, V5, V6
    # PTB-XL signal channel names usually correspond to these. Let's check fields['sig_name']
    sig_names = fields['sig_name']

    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

    # Standard 12-lead layout:
    # Row 0: I, aVR, V1, V4 (or standard conventional 3x4: I, II, III / aVR, aVL, aVF / V1, V2, V3 / V4, V5, V6)
    # Let's do standard 3x4 grid:
    # 3 rows of 4 leads each:
    # Row 1: I, II, III
    # Row 2: aVR, aVL, aVF
    # Row 3: V1, V2, V3
    # Row 4: V4, V5, V6
    # Or 3 rows for 12 leads + 1 long strip (Lead II) at the bottom.

    fs = fields['fs']
    # Plot 10 seconds or full signal
    samples_to_plot = int(10 * fs)
    t = np.arange(samples_to_plot) / fs

    standard_leads = ['I', 'II', 'III', 'avr', 'avl', 'avf', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6']
    # Match case-insensitively or exact
    lead_indices = []
    for sl in ['I', 'II', 'III', 'AVR', 'AVL', 'AVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']:
        # find in sig_names
        match_idx = -1
        for i, sn in enumerate(sig_names):
            if sn.upper() == sl.upper():
                match_idx = i
                break
        lead_indices.append(match_idx)

    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)

    # Let's create a clean clinical 12-lead plot or simple subplots
    # Grid: 12 subplots in 3x4 or similar, plus long strip
    fig, axes = plt.subplots(4, 3, figsize=(15, 10))
    axes = axes.flatten()

    grid_leads = ['I', 'aVR', 'V1', 'V4', 'II', 'aVL', 'V2', 'V5', 'III', 'aVF', 'V3', 'V6']

    # Map lead name to index in sig_names
    lead_map = {sn.upper(): i for i, sn in enumerate(sig_names)}

    for i, lead in enumerate(grid_leads):
        ax = axes[i]
        orig_lead = lead.lower() if lead in ['i', 'ii', 'iii'] else lead
        # search
        matched_i = -1
        for sn_idx, sn in enumerate(sig_names):
            if sn.upper() == lead.upper() or sn.upper() == orig_lead.upper() or sn.upper() == lead.replace('a', 'aVR' if 'VR' in lead else '').upper():
                matched_i = sn_idx
                break
        # Fallback exact matching
        if matched_i == -1:
            for sn_idx, sn in enumerate(sig_names):
                if lead.lower() in sn.lower():
                    matched_i = sn_idx
                    break

        if matched_i != -1:
            sig_data = signal[:samples_to_plot, matched_i]
            ax.plot(t, sig_data, color='black', linewidth=0.6)
            ax.set_title(lead, fontsize=10, loc='left')
        ax.grid(True, which='both', color='#ff9999', linestyle='-', linewidth=0.5)
        ax.minorticks_on()
        ax.grid(True, which='minor', color='#ffcccc', linestyle=':', linewidth=0.3)
        ax.set_yticklabels([])
        ax.set_xticklabels([])

    plt.suptitle(f'ECG ID: {ecg_id}', fontsize=14)
    plt.tight_layout()

    # Random file name for the image
    rand_name = f'ecg_{ecg_id}_{np.random.randint(10000, 99999)}.png'
    img_path = os.path.join('images', rand_name)
    plt.savefig(img_path, dpi=150)
    plt.close()

    answer_key.append({
        'ecg_id': ecg_id,
        'image_filename': rand_name,
        'true_class': true_class,
        'code': code,
        'patient_id': row['patient_id']
    })
    print(f'Processed {idx+1}/48: ECG {ecg_id} -> {rand_name}')

ans_df = pd.DataFrame(answer_key)
ans_df.to_csv('answer_key.csv', index=False)
print('Generated all images and answer_key.csv successfully.')
