import time
from streamlit import session_state as state

class Timer:
    def __init__(self):
        if 'start_time' not in state:
            state.start_time = None
            state.accumulated = 0

    def start(self):
        state.start_time = time.time()

    def pause(self):
        state.accumulated += time.time() - state.start_time
        state.start_time = None

    def resume(self):
        if state.start_time is None:
            state.start_time = time.time()

    def stop(self) -> int:
        if state.start_time:
            self.pause()
        duration = int(state.accumulated)
        state.accumulated = 0
        return duration