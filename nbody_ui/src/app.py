import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import json
import time
from string import Template

import streamlit as st
import streamlit.components.v1 as components

from simulation import create_two_body_orbit, advance


ADVANCES_PER_FRAME = 8
FRAMES_PER_BATCH = 120
VIEW_RANGE = 3.0
CANVAS_SIZE = 600
TARGET_FPS = 60

ANIMATION_TEMPLATE = Template("""
<canvas id="nbody" width="$size" height="$size"
        style="background:#000; display:block; margin:0 auto"></canvas>
<script>
(function() {
    var frames = $frames_json;
    var canvas = document.getElementById('nbody');
    var ctx = canvas.getContext('2d');
    var S = $size;
    var R = $view_range;
    var interval = 1000 / $fps;
    var i = 0;
    var lastTime = 0;

    function draw(timestamp) {
        if (timestamp - lastTime < interval) {
            requestAnimationFrame(draw);
            return;
        }
        lastTime = timestamp;

        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, S, S);

        ctx.fillStyle = '#fff';
        var positions = frames[i];
        for (var j = 0; j < positions.length; j++) {
            var sx = (positions[j][0] / R + 1) * S / 2;
            var sy = (-positions[j][1] / R + 1) * S / 2;
            ctx.beginPath();
            ctx.arc(sx, sy, 5, 0, 6.2832);
            ctx.fill();
        }

        i++;
        if (i < frames.length) {
            requestAnimationFrame(draw);
        }
    }

    requestAnimationFrame(draw);
})();
</script>
""")

STATIC_TEMPLATE = Template("""
<canvas id="nbody" width="$size" height="$size"
        style="background:#000; display:block; margin:0 auto"></canvas>
<script>
(function() {
    var positions = $positions_json;
    var canvas = document.getElementById('nbody');
    var ctx = canvas.getContext('2d');
    var S = $size;
    var R = $view_range;

    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, S, S);

    ctx.fillStyle = '#fff';
    for (var j = 0; j < positions.length; j++) {
        var sx = (positions[j][0] / R + 1) * S / 2;
        var sy = (-positions[j][1] / R + 1) * S / 2;
        ctx.beginPath();
        ctx.arc(sx, sy, 5, 0, 6.2832);
        ctx.fill();
    }
})();
</script>
""")


def reset_simulation():
    state, config = create_two_body_orbit()
    st.session_state.state = state
    st.session_state.config = config
    st.session_state.running = False


def compute_frame_batch(state, config):
    frames = []
    for _ in range(FRAMES_PER_BATCH):
        for _ in range(ADVANCES_PER_FRAME):
            advance(state, config)
        frames.append(state.position.tolist())
    return frames


def main():
    st.set_page_config(page_title="N-Body Gravity", layout="wide")
    st.title("N-Body Gravity Simulation")

    if "state" not in st.session_state:
        reset_simulation()

    col_start, col_pause, col_reset = st.columns(3)
    with col_start:
        if st.button("Start", use_container_width=True):
            st.session_state.running = True
    with col_pause:
        if st.button("Pause", use_container_width=True):
            st.session_state.running = False
    with col_reset:
        if st.button("Reset", use_container_width=True):
            reset_simulation()

    state = st.session_state.state
    st.text(f"t = {state.elapsed_time:.4f}")

    if st.session_state.running:
        frames = compute_frame_batch(state, st.session_state.config)
        html = ANIMATION_TEMPLATE.substitute(
            size=CANVAS_SIZE,
            frames_json=json.dumps(frames),
            view_range=VIEW_RANGE,
            fps=TARGET_FPS,
        )
        components.html(html, height=CANVAS_SIZE + 10)
        time.sleep(FRAMES_PER_BATCH / TARGET_FPS)
        st.rerun()
    else:
        html = STATIC_TEMPLATE.substitute(
            size=CANVAS_SIZE,
            positions_json=json.dumps(state.position.tolist()),
            view_range=VIEW_RANGE,
        )
        components.html(html, height=CANVAS_SIZE + 10)


if __name__ == "__main__":
    main()
