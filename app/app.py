import time

import streamlit as st
import plotly.graph_objects as go

from nbody import two_body_orbit, random_disk, solar_system

TARGET_FPS = 30
FRAME_INTERVAL = 1.0 / TARGET_FPS
FRAMES_PER_BATCH = 30

# View ranges per preset
VIEW_RANGES = {
    "Two-Body Orbit": 3.0,
    "Random Disk": 8.0,
    "Solar System": 16.0,
}

st.set_page_config(page_title="N-Body Gravity", layout="wide")
st.title("N-Body Gravity Simulation")

# sidebar parameters

with st.sidebar:
    st.header("Scenario")

    preset = st.selectbox("Preset", list(VIEW_RANGES.keys()))

    n_bodies = 200
    seed = 42
    if preset == "Random Disk":
        n_bodies = st.slider("Number of bodies", 10, 2000, 200)
        seed = st.number_input("Seed", value=42, step=1)

    st.header("Physics")

    dt = st.number_input(
        "Time step (dt)", value=0.005, format="%.4f",
        min_value=0.0001, max_value=0.1, step=0.001,
    )
    steps_per_frame = st.slider("Steps per frame", 1, 50, 6)


# preset factories

PRESETS = {
    "Two-Body Orbit": lambda: two_body_orbit(),
    "Random Disk": lambda: random_disk(n=n_bodies, seed=seed),
    "Solar System": lambda: solar_system(),
}


def create_simulator():
    return PRESETS[preset]()


def create_figure(sim):
    pos = sim.positions()
    view = VIEW_RANGES[preset]
    return go.Figure(
        data=go.Scatter(
            x=pos[:, 0].tolist(),
            y=pos[:, 1].tolist(),
            mode="markers",
            marker=dict(size=6, color="white"),
        ),
        layout=go.Layout(
            xaxis=dict(
                range=[-view, view],
                scaleanchor="y",
                showgrid=False,
                zeroline=False,
                showticklabels=False,
            ),
            yaxis=dict(
                range=[-view, view],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
            ),
            plot_bgcolor="black",
            paper_bgcolor="black",
            showlegend=False,
            margin=dict(l=0, r=0, t=40, b=0),
            height=600,
            title=dict(
                text="t = 0.0000",
                font=dict(color="#666", size=14, family="monospace"),
            ),
        ),
    )


def update_figure(fig, sim, elapsed_time):
    pos = sim.positions()
    fig.data[0].x = pos[:, 0].tolist()
    fig.data[0].y = pos[:, 1].tolist()
    fig.layout.title.text = f"t = {elapsed_time:.4f}"


# session state init

def reset_simulation():
    st.session_state.sim = create_simulator()
    st.session_state.running = False
    st.session_state.fig = create_figure(st.session_state.sim)
    st.session_state.frame_count = 0
    st.session_state.elapsed_time = 0.0
    st.session_state.initial_energy = st.session_state.sim.total_energy()
    st.session_state.current_preset = preset


if "sim" not in st.session_state:
    reset_simulation()

# reset if the user switched presets
if st.session_state.get("current_preset") != preset:
    reset_simulation()

# controls

col_start, col_pause, col_reset = st.columns(3)
with col_start:
    if st.button("Start", width="stretch"):
        st.session_state.running = True
with col_pause:
    if st.button("Pause", width="stretch"):
        st.session_state.running = False
with col_reset:
    if st.button("Reset", width="stretch"):
        reset_simulation()

# simulation loop

sim = st.session_state.sim
fig = st.session_state.fig
placeholder = st.empty()

if st.session_state.running:
    for _ in range(FRAMES_PER_BATCH):
        frame_start = time.time()

        sim.step(dt, n_steps=steps_per_frame)
        st.session_state.elapsed_time += dt * steps_per_frame
        st.session_state.frame_count += 1

        update_figure(fig, sim, st.session_state.elapsed_time)
        placeholder.plotly_chart(
            fig,
            width="stretch",
            key=f"frame_{st.session_state.frame_count}",
        )

        frame_elapsed = time.time() - frame_start
        time.sleep(max(0.0, FRAME_INTERVAL - frame_elapsed))

    st.rerun()
else:
    update_figure(fig, sim, st.session_state.elapsed_time)
    placeholder.plotly_chart(fig, width="stretch")

# sidebar performance and energy

with st.sidebar:
    with st.expander("Performance"):
        st.metric("Bodies", sim.n)
        st.metric("Total steps", sim.total_steps())
        step_time = sim.last_step_time_sec()
        if step_time > 0:
            st.metric("Steps/sec", f"{steps_per_frame / step_time:.0f}")
            st.metric("Step time", f"{step_time * 1000:.1f} ms")

    with st.expander("Energy"):
        current_e = sim.total_energy()
        initial_e = st.session_state.initial_energy
        if initial_e != 0:
            drift = abs(current_e - initial_e) / abs(initial_e)
        else:
            drift = 0.0
        st.metric("Total energy", f"{current_e:.6f}")
        st.metric("Initial energy", f"{initial_e:.6f}")
        st.metric("Relative drift", f"{drift:.2e}")
