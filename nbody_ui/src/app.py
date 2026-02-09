import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import time

import streamlit as st
import plotly.graph_objects as go

from simulation import create_two_body_orbit, advance


VIEW_RANGE = 3.0
STEPS_PER_FRAME = 6
TARGET_FPS = 30
FRAME_INTERVAL = 1.0 / TARGET_FPS
FRAMES_PER_BATCH = 30

st.set_page_config(page_title="N-Body Gravity", layout="wide")
st.title("N-Body Gravity Simulation")


def create_figure(state):
    return go.Figure(
        data=go.Scatter(
            x=state.position[:, 0].tolist(),
            y=state.position[:, 1].tolist(),
            mode="markers",
            marker=dict(size=10, color="white"),
        ),
        layout=go.Layout(
            xaxis=dict(
                range=[-VIEW_RANGE, VIEW_RANGE],
                scaleanchor="y",
                showgrid=False,
                zeroline=False,
                showticklabels=False,
            ),
            yaxis=dict(
                range=[-VIEW_RANGE, VIEW_RANGE],
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
                text=f"t = {state.elapsed_time:.4f}",
                font=dict(color="#666", size=14, family="monospace"),
            ),
        ),
    )


def update_figure_data(fig, state):
    fig.data[0].x = state.position[:, 0].tolist()
    fig.data[0].y = state.position[:, 1].tolist()
    fig.layout.title.text = f"t = {state.elapsed_time:.4f}"


def reset_simulation():
    state, config = create_two_body_orbit()
    st.session_state.state = state
    st.session_state.config = config
    st.session_state.running = False
    st.session_state.frame_count = 0
    st.session_state.fig = create_figure(state)


if "state" not in st.session_state:
    reset_simulation()

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

state = st.session_state.state
config = st.session_state.config
fig = st.session_state.fig

placeholder = st.empty()

if st.session_state.running:
    for _ in range(FRAMES_PER_BATCH):
        frame_start = time.time()

        for _ in range(STEPS_PER_FRAME):
            advance(state, config)

        st.session_state.frame_count += 1
        update_figure_data(fig, state)
        placeholder.plotly_chart(
            fig,
            width="stretch",
            key=f"frame_{st.session_state.frame_count}",
        )

        frame_elapsed = time.time() - frame_start
        time.sleep(max(0.0, FRAME_INTERVAL - frame_elapsed))

    st.rerun()
else:
    update_figure_data(fig, state)
    placeholder.plotly_chart(fig, width="stretch")
