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

# Plotting ECG + Detected R-peaks
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

# Expander for more info
with st.expander("What is HRV (Heart Rate Variability)?"):
    st.write(
        """
        **Heart Rate Variability (HRV)** is simply how much the time
        between one heartbeat and the next changes. Even though we often
        think our heart beats like a metronome, there's always a bit of
        variation — and that variation can tell us a lot about our health
        and stress levels.

        - **Why it matters:** 
          - A **higher HRV** suggests your heart is flexible and responds
            well to changes (like stress or rest), often linked to better
            fitness and overall health.
          - A **lower HRV** may point to stress, fatigue, or potential
            health issues. Athletes sometimes see a drop if they're
            overtraining.
        - **Common uses:** 
          - Checking how well your body recovers from exercise or daily
            stress.
          - Spotting early signs of heart or health problems.
          - Biofeedback (learning techniques to help control and improve
            your HRV, which can reduce stress).
        """
    )

with st.expander("What is the QRS Complex?"):
    st.write(
        """
        The **QRS Complex** is the main spike you see on an ECG, which
        measures the heart’s electrical signals. It reflects the moment
        your heart’s lower chambers (ventricles) contract to pump blood
        throughout the body.

        - **Parts of the QRS Complex:** 
          - **Q wave:** A small dip before the biggest spike.
          - **R wave:** The tall, sharp peak that's easiest to spot.
          - **S wave:** A small dip right after the R wave.
        
        **Why it matters:**
        - **R-Peaks** (the tips of those tall spikes) help us figure out
          your heart rate.
        - The **shape & duration** of the QRS can reveal if there’s an
          electrical or structural issue with the heart (like blocked
          signals or thickened muscle).
        - Getting accurate QRS readings is crucial for measuring HRV
          (to see how your heartbeat varies) and for diagnosing heart
          conditions.
        """
    )

with st.expander("Example ECG QRS Diagram"):
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/9/9e/SinusRhythmLabels.svg",
        caption="Annotated ECG waveform showing P, QRS, and T waves",
        width=512
    )
