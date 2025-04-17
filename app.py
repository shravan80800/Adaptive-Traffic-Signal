import streamlit as st
import pandas as pd
import time

# Configuration
FIXED_CYCLE_TIME = 65  # Traditional system cycle time
YELLOW_TRANSITION_TIME = 5  # Transition period between phases
MIN_GREEN_TIME = 15  # Minimum green light duration
MAX_GREEN_TIME = 65  # Maximum green light duration

# Vehicle weights (adjust these as needed)
VEHICLE_WEIGHTS = {
    'Cars': 1.0,
    'Motorcycle': 0.6,
    'Trucks_Buses': 1.8,
    'Ambulance': 3.0  # Highest weight for emergency vehicles
}

# ---------------------------
# Traffic Light Component
# ---------------------------
def create_traffic_light(col, lane_data, phase, timer, transition_alert=False):
    with col:
        with st.container(border=True):
            # Header with alerts
            header_cols = st.columns([4, 1])
            header_cols[0].markdown(f"### {lane_data['Lane'].upper().replace('_', ' ')}")

            # Status indicators
            if lane_data['Emergency'].lower() == 'yes':
                header_cols[1].markdown("""<span style='color:red; font-size:24px'>🚨</span>""", unsafe_allow_html=True)
            elif transition_alert:
                header_cols[1].markdown("""<span style='color:orange; font-size:24px'>⚠️</span>""", unsafe_allow_html=True)

            # Light indicators
            light_cols = st.columns(3)
            colors = {
                'green': ('#00ff00' if phase == 'green' else '#004400'),
                'yellow': ('#ffd700' if phase == 'yellow' else '#443300'),
                'red': ('#ff0000' if phase == 'red' else '#440000')
            }

            for lcol, (name, color) in zip(light_cols, colors.items()):
                lcol.markdown(f"<div style='height:30px; width:30px; border-radius:50%; background:{color}; margin:auto;'></div>", unsafe_allow_html=True)

            # Timer display
            max_time = (FIXED_CYCLE_TIME if phase == 'red' else
                        lane_data['Green_Light_Time'] if phase == 'green' else
                        YELLOW_TRANSITION_TIME)
            progress = timer / max_time if max_time > 0 else 0
            st.progress(min(progress, 1.0))

            delta_value = (f"Saved {FIXED_CYCLE_TIME - lane_data['Green_Light_Time']}s" if phase == 'green' else None)
            st.metric("Time Remaining", f"{max(0, timer)}s", delta=delta_value)

            st.caption(f"""
            **Live Traffic**
            🚗 {lane_data['Cars']} (×{VEHICLE_WEIGHTS['Cars']}) |
            🏍 {lane_data['Motorcycle']} (×{VEHICLE_WEIGHTS['Motorcycle']}) |
            🚚 {lane_data['Trucks_Buses']} (×{VEHICLE_WEIGHTS['Trucks_Buses']}) |
            🚑 {lane_data['Ambulance']} (×{VEHICLE_WEIGHTS['Ambulance']})
            """)

# ---------------------------
# Simulation Logic
# ---------------------------
def calculate_weighted_priority(lane):
    """Calculate priority score based on vehicle counts and weights"""
    weighted_sum = (
        lane['Cars'] * VEHICLE_WEIGHTS['Cars'] +
        lane['Motorcycle'] * VEHICLE_WEIGHTS['Motorcycle'] +
        lane['Trucks_Buses'] * VEHICLE_WEIGHTS['Trucks_Buses']
    )
    return weighted_sum

def run_synchronized_simulation(data):
    lanes = data.to_dict('records')
    total_saved = 0
    cumulative_saving = 0
    start_time = time.time()

    # Calculate weighted priority for each lane
    for lane in lanes:
        lane['Weighted_Priority'] = calculate_weighted_priority(lane)

    # Sort lanes: Emergency lanes first (prioritizing lanes with any ambulance),
    # then by the number of ambulances (descending), then by weighted priority
    lanes.sort(key=lambda lane: (
        lane['Emergency'].lower() != 'yes',  # Non-emergency later
        -lane['Ambulance'],                  # More ambulances first
        -lane['Weighted_Priority']           # Then highest weighted priority
    ))

    total_weight = sum(lane['Weighted_Priority'] for lane in lanes if lane['Emergency'].lower() != 'yes')

    # Dynamically adjust green light time based on weighted priority
    for lane in lanes:
        if lane['Emergency'].lower() == 'yes':
            lane['Green_Light_Time'] = max(MIN_GREEN_TIME, min(MAX_GREEN_TIME, FIXED_CYCLE_TIME)) # Give full cycle or max time to emergency
        elif total_weight > 0:
            ratio = lane['Weighted_Priority'] / total_weight
            dynamic_time = int(ratio * FIXED_CYCLE_TIME)
            lane['Green_Light_Time'] = max(MIN_GREEN_TIME, min(MAX_GREEN_TIME, dynamic_time))
        else:
            lane['Green_Light_Time'] = MIN_GREEN_TIME

    base_waiting = {lane['Lane']: i * FIXED_CYCLE_TIME for i, lane in enumerate(lanes)}
    cols = st.columns(len(lanes))
    placeholders = {lane['Lane']: col.empty() for lane, col in zip(lanes, cols)}

    try:
        for current_idx, current_lane in enumerate(lanes):
            green_time = current_lane['Green_Light_Time']
            saved_time = FIXED_CYCLE_TIME - green_time

            # GREEN PHASE
            phase_start = time.time()
            while (time.time() - phase_start) < green_time:
                total_elapsed = time.time() - start_time
                remaining_green = green_time - (time.time() - phase_start)

                # Current lane green
                create_traffic_light(
                    placeholders[current_lane['Lane']],
                    current_lane,
                    'green',
                    int(remaining_green)
                )

                # Others red
                for lane in lanes:
                    if lane['Lane'] != current_lane['Lane']:
                        expected_wait = base_waiting[lane['Lane']] - cumulative_saving
                        remaining_wait = max(0, expected_wait - total_elapsed)
                        create_traffic_light(
                            placeholders[lane['Lane']],
                            lane,
                            'red',
                            int(remaining_wait)
                        )
                time.sleep(0.1)

            # YELLOW PHASE
            phase_start = time.time()
            while (time.time() - phase_start) < YELLOW_TRANSITION_TIME:
                total_elapsed = time.time() - start_time
                remaining_yellow = YELLOW_TRANSITION_TIME - (time.time() - phase_start)

                # Current lane yellow
                create_traffic_light(
                    placeholders[current_lane['Lane']],
                    current_lane,
                    'yellow',
                    int(remaining_yellow),
                    transition_alert=True
                )

                # Others red
                for lane in lanes:
                    if lane['Lane'] != current_lane['Lane']:
                        expected_wait = base_waiting[lane['Lane']] - cumulative_saving
                        remaining_wait = max(0, expected_wait - total_elapsed)
                        create_traffic_light(
                            placeholders[lane['Lane']],
                            lane,
                            'red',
                            int(remaining_wait)
                        )
                time.sleep(0.1)

            # Reset emergency after it's handled
            current_lane['Emergency'] = 'no'

            # Update cumulative saving
            cumulative_saving += saved_time
            total_saved += saved_time

            # Reset current lane to red
            create_traffic_light(
                placeholders[current_lane['Lane']],
                current_lane,
                'red',
                0
            )

    except KeyboardInterrupt:
        st.stop()

    st.success(f"✅ Total Time Saved This Cycle: **{total_saved} seconds**")

# ---------------------------
# Main Interface
# ---------------------------
st.set_page_config(page_title="Smart Traffic Control", layout="wide")
st.title("🚦 Weighted Adaptive Traffic Signal System")

# Load data
df = pd.read_csv("final_lane_output.csv")

# Configuration panel
with st.expander("⚙️ System Configuration", expanded=True):
    st.write(f"""
    - **Traditional Cycle Time**: {FIXED_CYCLE_TIME}s per lane
    - **Yellow Transition Time**: {YELLOW_TRANSITION_TIME}s
    - **Dynamic Priority**: Emergency → Number of Ambulances → Weighted Vehicle Count
    - **Vehicle Weights**:
        - Cars: {VEHICLE_WEIGHTS['Cars']}
        - Motorcycles: {VEHICLE_WEIGHTS['Motorcycle']}
        - Trucks/Buses: {VEHICLE_WEIGHTS['Trucks_Buses']}
        - Ambulances: {VEHICLE_WEIGHTS['Ambulance']}
    - **Min Green Light Time**: {MIN_GREEN_TIME}s
    - **Max Green Light Time**: {MAX_GREEN_TIME}s
    """)
    st.dataframe(df, use_container_width=True)

if st.button("▶️ Start Smart Simulation", type="primary"):
    run_synchronized_simulation(df)