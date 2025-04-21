# 🚦 Smart Adaptive Traffic Signal System

An AI-powered, real-time traffic signal management system that reduces congestion, prioritizes emergency vehicles, and promotes sustainable urban mobility — built completely using *Free and Open Source Software (FOSS)*.

---

## 🌍 Project Vision

Urban traffic systems today are blind — operating on fixed timers, without considering actual road conditions. This causes:

- Long wait times ⏱  
- Unnecessary emissions 💨  
- Delays for ambulances 🚑  

Our solution: a smart, adaptive traffic system that uses *AI + Computer Vision* to respond to live traffic and prioritize emergency vehicles — reducing congestion and saving lives.

---

## 🌱 Why This Project Is Sustainable

This project supports *sustainability and smart city goals* in the following ways:

- ✅ *FOSS-first*: Built entirely on free and open source tools (no vendor lock-in or license costs)
- 🔋 *Energy-efficient*: Reduces idle vehicle time, fuel usage, and CO₂ emissions
- 🧩 *Modular*: Can be integrated with existing traffic infrastructure (CCTV feeds, Raspberry Pi, Jetson Nano)
- 🌐 *Scalable*: Easily extendable to multi-lane and multi-signal intersections

---

## 🔧 Built With (FOSS Stack)

| Tool            | Purpose                                 | License        |
|-----------------|------------------------------------------|----------------|
| *YOLOv8*      | Object detection (vehicles & ambulances) | GPL-3.0 / Hybrid |
| *OpenCV*      | Image processing and computer vision     | BSD License    |
| *Scikit-learn*| Machine learning (Random Forest)         | BSD License    |
| *NumPy*       | Numerical operations                     | BSD License    |
| *Pandas*      | Data handling, CSV management            | BSD License    |
| *Streamlit*   | Real-time dashboard and UI               | Apache 2.0     |

All components are *freely available*, well-documented, and supported by global developer communities.

---

## 🧠 Key Features

- 🎯 Adaptive green light control using real-time data
- 🧠 Machine learning model (Random Forest) for time prediction
- 🚑 Ambulance detection and emergency lane prioritization
- 💡 Intelligent traffic flow control
- 📊 CSV output for logs, analytics, and future integrations
- 🖥 Live dashboard with signal simulation via Streamlit

---

## 🚀 How It Works

1. Input images from traffic lanes are passed into YOLOv8
2. Vehicle counts (car, bike, bus/truck, ambulance) are extracted
3. Features are passed into a Random Forest Regressor
4. Green light time is predicted for each lane (10s–90s)
5. If an ambulance is detected, emergency priority is applied
6. Output is visualized on a dashboard and saved as a CSV

---

## 👥 Team – Dynamic Duo
This project was proudly developed by two passionate developers focused on innovation, sustainability, and impact.

🔹 Shravan Deshpande – Team Leader

🔹 Prathmesh Pawar – Co-Developer
