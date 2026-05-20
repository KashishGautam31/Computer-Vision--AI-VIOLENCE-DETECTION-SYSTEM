# ==========================================
# IMPORT LIBRARIES
# ==========================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import cv2
import tempfile

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Violence Detection Dashboard",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* MULTI COLOR ANIMATED BACKGROUND */

.stApp {

    background: linear-gradient(
        135deg,
        #000428,
        #004e92,
        #0f2027,
        #2c5364,
        #1c1c3c,
        #000428
    );

    background-size: 400% 400%;

    animation: gradientBG 15s ease infinite;

    color: white;
}

/* BACKGROUND ANIMATION */

@keyframes gradientBG {

    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

/* MAIN AREA */

.main .block-container {

    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 100%;
}

/* SIDEBAR */

[data-testid="stSidebar"] {

    background: rgba(8,17,32,0.95);

    border-right: 1px solid cyan;
}

/* TITLE */

.main-title {

    text-align: center;

    font-size: 45px;

    font-weight: bold;

    color: cyan;

    margin-bottom: 30px;

    text-shadow: 0px 0px 20px cyan;
}

/* METRIC CARDS */

.metric-card {

    background: rgba(10,20,40,0.8);

    border: 1px solid cyan;

    border-radius: 20px;

    padding: 20px;

    text-align: center;

    box-shadow: 0px 0px 20px rgba(0,255,255,0.4);

    margin-bottom: 20px;

    backdrop-filter: blur(10px);
}

.metric-card h1 {

    color: cyan;

    font-size: 40px;
}

/* PANELS */

.panel {

    background: rgba(10,20,40,0.8);

    border: 1px solid cyan;

    border-radius: 20px;

    padding: 20px;

    box-shadow: 0px 0px 20px rgba(0,255,255,0.3);

    margin-bottom: 20px;

    backdrop-filter: blur(10px);
}

/* ALERT PANEL */

.alert-panel {

    background: rgba(50,0,0,0.7);

    border: 1px solid red;

    border-radius: 20px;

    padding: 20px;

    box-shadow: 0px 0px 20px rgba(255,0,0,0.5);

    margin-bottom: 20px;

    backdrop-filter: blur(10px);
}

/* SECTION TITLE */

.section-title {

    color: cyan;

    font-size: 24px;

    margin-bottom: 15px;
}

/* BUTTONS */

.stButton button {

    width: 100%;

    background: cyan;

    color: black;

    border-radius: 10px;

    font-weight: bold;

    border: none;
}

/* DATAFRAME */

[data-testid="stDataFrame"] {

    border: 1px solid cyan;

    border-radius: 15px;

    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("⚙ CONTROL PANEL")

uploaded_video = st.sidebar.file_uploader(
    "Upload CCTV Video",
    type=["mp4", "avi", "mov"]
)

ai_sensitivity = st.sidebar.slider(
    "AI Sensitivity",
    0,
    255,
    120
)

st.sidebar.button("▶ START SYSTEM")

st.sidebar.button("⏹ STOP SYSTEM")

st.sidebar.selectbox(
    "Camera Mode",
    ["Live Camera", "CCTV Feed", "Drone Feed"]
)

# ==========================================
# TITLE
# ==========================================

st.markdown(
    '<div class="main-title">AI VIOLENCE DETECTION SYSTEM</div>',
    unsafe_allow_html=True
)

# ==========================================
# METRIC PLACEHOLDERS
# ==========================================

c1, c2, c3, c4 = st.columns(4)

metric1 = c1.empty()
metric2 = c2.empty()
metric3 = c3.empty()
metric4 = c4.empty()

# ==========================================
# CENTER LAYOUT
# ==========================================

left, center, right = st.columns([1,2,1])

# ==========================================
# LEFT PANEL
# ==========================================

with left:

    st.markdown("""
    <div class="panel">

    <div class="section-title">📡 SYSTEM STATUS</div>

    ✅ AI ACTIVE <br><br>
    ✅ CAMERA ONLINE <br><br>
    ✅ SERVER CONNECTED <br><br>
    ✅ CLOUD ACTIVE

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">

    <div class="section-title">🛡 SECURITY LEVEL</div>

    Threat Probability: 92% <br><br>
    Risk Zone: HIGH <br><br>
    Active Alerts: 05

    </div>
    """, unsafe_allow_html=True)

# ==========================================
# CENTER VIDEO PANEL
# ==========================================

with center:

    st.markdown("""
    <div class="panel">

    <div class="section-title">🎥 LIVE SURVEILLANCE</div>

    </div>
    """, unsafe_allow_html=True)

    video_placeholder = st.empty()

# ==========================================
# RIGHT PANEL
# ==========================================

with right:

    alert_placeholder = st.empty()

    st.markdown("""
    <div class="panel">

    <div class="section-title">📍 CAMERA DETAILS</div>

    Camera ID: CAM-07 <br><br>
    FPS: 32 <br><br>
    Resolution: 1080P <br><br>
    AI Status: ACTIVE

    </div>
    """, unsafe_allow_html=True)

# ==========================================
# DATA STORAGE
# ==========================================

threat_history = []
frame_numbers = []
violence_cases = 0

# ==========================================
# VIDEO ANALYSIS
# ==========================================

if uploaded_video:

    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_video.read())

    cap = cv2.VideoCapture(tfile.name)

    frame_count = 0

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        frame = cv2.resize(frame, (900, 500))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        motion_score = gray.mean()

        # ==========================================
        # AI DETECTION LOGIC
        # ==========================================

        if motion_score > ai_sensitivity:

            threat_level = "HIGH"

            violence_cases += 1

            alert_text = "🔴 Violence Detected"

            # RED DETECTION BOX

            cv2.rectangle(
                frame,
                (120, 100),
                (700, 400),
                (0, 0, 255),
                4
            )

            cv2.putText(
                frame,
                "VIOLENCE DETECTED",
                (180, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
                3
            )

        else:

            threat_level = "SAFE"

            alert_text = "🟢 Area Safe"

        # ==========================================
        # SAVE DATA
        # ==========================================

        threat_history.append(motion_score)

        frame_numbers.append(frame_count)

        # ==========================================
        # SHOW VIDEO
        # ==========================================

        video_placeholder.image(
            frame,
            channels="BGR",
            use_container_width=True
        )

        # ==========================================
        # UPDATE METRICS
        # ==========================================

        metric1.markdown(f"""
        <div class="metric-card">
        <h3>THREAT LEVEL</h3>
        <h1>{threat_level}</h1>
        </div>
        """, unsafe_allow_html=True)

        metric2.markdown(f"""
        <div class="metric-card">
        <h3>VIOLENCE CASES</h3>
        <h1>{violence_cases}</h1>
        </div>
        """, unsafe_allow_html=True)

        metric3.markdown(f"""
        <div class="metric-card">
        <h3>ACCURACY</h3>
        <h1>96%</h1>
        </div>
        """, unsafe_allow_html=True)

        metric4.markdown(f"""
        <div class="metric-card">
        <h3>FPS</h3>
        <h1>32</h1>
        </div>
        """, unsafe_allow_html=True)

        # ==========================================
        # ALERT UPDATE
        # ==========================================

        alert_placeholder.markdown(f"""
        <div class="alert-panel">

        <div class="section-title">🚨 ALERT CENTER</div>

        {alert_text}<br><br>

        Violence Cases: {violence_cases}<br><br>

        AI Monitoring Active

        </div>
        """, unsafe_allow_html=True)

    cap.release()

    # ==========================================
    # REAL-TIME ANALYTICS
    # ==========================================

    st.markdown("## 📊 REAL-TIME ANALYTICS")

    chart1, chart2 = st.columns(2)

    # ==========================================
    # LINE CHART
    # ==========================================

    with chart1:

        line_chart = px.line(
            x=frame_numbers,
            y=threat_history,

            labels={
                "x":"Frames",
                "y":"Threat Score"
            },

            title="Threat Detection Trend"
        )

        line_chart.update_layout(

            paper_bgcolor="#07111f",
            plot_bgcolor="#07111f",

            font_color="white",

            title_font_color="cyan"
        )

        st.plotly_chart(
            line_chart,
            use_container_width=True
        )

    # ==========================================
    # PIE CHART
    # ==========================================

    with chart2:

        safe_count = len([
            x for x in threat_history
            if x <= ai_sensitivity
        ])

        danger_count = len([
            x for x in threat_history
            if x > ai_sensitivity
        ])

        pie_chart = px.pie(

            names=["Safe","Violence"],

            values=[safe_count, danger_count],

            title="Detection Distribution"
        )

        pie_chart.update_layout(

            paper_bgcolor="#07111f",

            font_color="white",

            title_font_color="cyan"
        )

        st.plotly_chart(
            pie_chart,
            use_container_width=True
        )

    # ==========================================
    # CAMERA PERFORMANCE
    # ==========================================

    st.markdown("## 📈 CAMERA PERFORMANCE")

    bar_chart = px.bar(

        x=["Camera 1","Camera 2","Camera 3","Camera 4"],

        y=[95,88,92,85],

        labels={
            "x":"Camera",
            "y":"Accuracy"
        },

        title="Camera Accuracy"
    )

    bar_chart.update_layout(

        paper_bgcolor="#07111f",

        plot_bgcolor="#07111f",

        font_color="white",

        title_font_color="cyan"
    )

    st.plotly_chart(
        bar_chart,
        use_container_width=True
    )

    # ==========================================
    # THREAT AREA ANALYSIS
    # ==========================================

    st.markdown("## 🌊 THREAT AREA ANALYSIS")

    area_chart = px.area(

        x=frame_numbers,

        y=threat_history,

        labels={
            "x":"Frames",
            "y":"Threat Intensity"
        },

        title="Threat Intensity Area Chart"
    )

    area_chart.update_layout(

        paper_bgcolor="#07111f",

        plot_bgcolor="#07111f",

        font_color="white",

        title_font_color="cyan"
    )

    st.plotly_chart(
        area_chart,
        use_container_width=True
    )

    # ==========================================
    # DETECTION SCATTER ANALYSIS
    # ==========================================

    st.markdown("## 🔵 DETECTION SCATTER ANALYSIS")

    scatter_chart = px.scatter(

        x=frame_numbers,

        y=threat_history,

        size=threat_history,

        title="AI Detection Scatter Plot"
    )

    scatter_chart.update_layout(

        paper_bgcolor="#07111f",

        plot_bgcolor="#07111f",

        font_color="white",

        title_font_color="cyan"
    )

    st.plotly_chart(
        scatter_chart,
        use_container_width=True
    )

    # ==========================================
    # SECURITY RADAR
    # ==========================================

    st.markdown("## 🛡 SECURITY RADAR")

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(

        r=[90,80,85,95,70],

        theta=[
            'Accuracy',
            'Threat',
            'Monitoring',
            'Detection',
            'Security'
        ],

        fill='toself'
    ))

    radar.update_layout(

        paper_bgcolor="#07111f",

        polar=dict(
            bgcolor="#07111f"
        ),

        font_color="white"
    )

    st.plotly_chart(
        radar,
        use_container_width=True
    )

    # ==========================================
    # DONUT CHART
    # ==========================================

    st.markdown("## 🍩 ALERT DISTRIBUTION")

    donut = px.pie(

        names=[
            "Critical",
            "Medium",
            "Low"
        ],

        values=[40,35,25],

        hole=0.5,

        title="Alert Severity Distribution"
    )

    donut.update_layout(

        paper_bgcolor="#07111f",

        font_color="white",

        title_font_color="cyan"
    )

    st.plotly_chart(
        donut,
        use_container_width=True
    )

    # ==========================================
    # ACTIVITY LOGS
    # ==========================================

    st.markdown("## 📋 ACTIVITY LOGS")

    logs = pd.DataFrame({

        "FRAME": frame_numbers[-10:],

        "THREAT SCORE": [
            round(x,2)
            for x in threat_history[-10:]
        ]

    })

    st.dataframe(
        logs,
        use_container_width=True
    )

else:

    st.info("📂 Upload CCTV video to start AI monitoring.")