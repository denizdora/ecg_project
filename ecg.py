import streamlit as st
import neurokit2 as nk
import numpy as np
import matplotlib.pyplot as plt

# Streamlit Title
st.title("ECG Simulation with QRS Detection")

# Sliders for user input
duration = st.slider("Duration (seconds)", 5, 15, 10)
sampling_rate = st.slider("Sampling Rate (Hz)", 100, 1000, 500)
heart_rate = st.slider("Heart Rate (BPM)", 40, 200, 80)
hrv_std = st.slider("Heart Rate Variability (Std in BPM)", 0, 20, 5)

# Generating ECG signal
ecg = nk.ecg_simulate(
    duration=duration,
    sampling_rate=sampling_rate,
    heart_rate=heart_rate,
    heart_rate_std=hrv_std,
    method="ecgsyn"
)

# Detecting QRS complexes
signals, info = nk.ecg_process(ecg, sampling_rate=sampling_rate)
rpeaks_indices = info["ECG_R_Peaks"]  # indices of the R-peak samples

# Creating time axis
time = np.linspace(0, duration, len(ecg))

# 3) Plotting ECG + Detected R-peaks
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(time, ecg, label="ECG Signal", color="blue")

# Plotting R-peaks as red circles
ax.plot(time[rpeaks_indices], ecg[rpeaks_indices],
        "ro", label="Detected R-peaks", markersize=8, fillstyle="none")
    
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Amplitude")
ax.set_title("ECG Signal with Detected QRS Complexes")
ax.legend()

# Displaying the plot in Streamlit
st.pyplot(fig)

# --- Collapsible Explanations Section ---
with st.expander("What is HRV (Heart Rate Variability)?"):
    st.write(
        """
        **Heart Rate Variability (HRV)** is the measure of the variation in
        time (in milliseconds) between consecutive heartbeats. It’s a 
        non-invasive way to assess how well the body’s autonomic nervous 
        system (ANS) responds to internal and external stressors.
        
        - **Why it matters:** 
          - A **higher HRV** often indicates a healthy balance between the 
            'fight-or-flight' (sympathetic) and 'rest-and-digest' 
            (parasympathetic) branches of the ANS. This can correlate with
            better cardiovascular fitness and stress resilience.
          - A **lower HRV** can be a sign of fatigue, overtraining (in 
            athletes), or chronic stress. It may also be associated 
            with certain cardiovascular or metabolic conditions.
        - **Common uses:** 
          - Monitoring stress and recovery in sports and wellness.
          - Detecting early signs of health issues or tracking chronic 
            conditions.
          - Biofeedback training, where people learn to regulate HRV to 
            improve relaxation and stress response.
        """
    )

with st.expander("What is the QRS Complex?"):
    st.write(
        """
        The **QRS Complex** on an ECG trace represents the rapid 
        depolarization (electrical activation) of the ventricles, which 
        triggers the main pumping action of the heart. It typically 
        includes three main parts:
        
        - **Q wave:** A small negative deflection that appears just before 
          the large R wave.
        - **R wave:** The prominent, tall spike and the most visually 
          recognizable component of the ECG cycle.
        - **S wave:** A negative deflection following the R wave.
        
        **Why it matters:**
        - **R-Peaks** (the highest point of the QRS Complex) are commonly 
          used to calculate heart rate, as they mark one cardiac cycle.
        - **Shape & Duration** of the QRS Complex can help identify
          conduction abnormalities, ventricular hypertrophy, or arrhythmias.
        - Accurate detection of QRS complexes is crucial for reliable 
          measurement of Heart Rate Variability (HRV) and for diagnosing 
          various heart conditions.
        """
    )
