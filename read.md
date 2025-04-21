# 🚦 Smart Adaptive Traffic Signal System

An AI-powered, real-time traffic signal management system that reduces congestion, prioritizes emergency vehicles, and promotes sustainable urban mobility — powered entirely by *Free and Open Source Software (FOSS)*.

---

## 🌍 Project Vision

Urban traffic is often managed by *static signal systems* that cannot adapt to real-time road conditions. This results in unnecessary delays, increased emissions, and dangerous blockages for ambulances and emergency vehicles.

*Our solution:* A dynamic, intelligent traffic signal system that uses *computer vision* and *machine learning* to:
- Detect real-time vehicle counts and emergency vehicles
- Predict optimal green light durations
- Prioritize ambulances and reduce emissions from idling traffic

All using *100% FOSS tools*.

---

## 🔧 Built With (FOSS Stack)

| Tool            | Purpose                               | License        |
|-----------------|----------------------------------------|----------------|
| *YOLOv8*      | Object detection (vehicles & ambulances) | GPL-3.0 / Hybrid |
| *OpenCV*      | Image processing and analysis          | BSD License    |
| *Scikit-learn*| Machine learning (Random Forest)       | BSD License    |
| *NumPy*       | Numerical computations                 | BSD License    |
| *Pandas*      | Data manipulation and CSV handling     | BSD License    |
| *Streamlit*   | Real-time dashboard simulation         | Apache 2.0     |

All tools are free to use, modify, and distribute — enabling rapid, affordable, and community-driven innovation.

---

## 🧠 Features

- ✅ *Real-time vehicle detection* using YOLOv8
- 🚑 *Ambulance detection & prioritization* with a custom-trained model (6000+ images)
- ⏱ *ML-based green light time prediction* using Random Forest
- 📊 *Automatic CSV report generation* for transparency and analytics
- 🖥 *Streamlit dashboard* with visual traffic light simulation

---

## 🌱 Why This Project Is Sustainable

- *Reduced emissions:* Adaptive timing lowers engine idling at intersections
- *FOSS-first approach:* No proprietary tools or licenses required — anyone can build, deploy, or extend it
- *Lightweight and scalable:* Can be deployed on low-cost hardware like Raspberry Pi or Jetson Nano
- *Open for collaboration:* Built for municipalities, civic developers, and smart city initiatives

---

## 🚀 How It Works

1. Images from traffic lanes are processed using YOLOv8
2. Vehicle types and counts are extracted
3. A trained ML model predicts green light durations per lane
4. Ambulance presence is flagged and prioritized
5. Signals are simulated in a Streamlit interface
6. Output is saved in final_lane_output.csv

---
