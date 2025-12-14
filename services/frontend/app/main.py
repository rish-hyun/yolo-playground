import os
import sys
import time

import streamlit as st

_ROOT = os.path.join(os.path.dirname(__file__), "../../..")
if _ROOT not in sys.path and os.path.isdir(os.path.join(_ROOT, "common")):
    sys.path.insert(0, _ROOT)

from client import orchestrator_client


def _is_orchestrator_healthy(attempts: int = 5, delay: int = 2) -> bool:
    for _ in range(attempts):
        healthy = orchestrator_client.is_orchestrator_healthy()
        if healthy:
            return True
        time.sleep(delay)
    return False


def _is_vision_healthy(attempts: int = 5, delay: int = 2) -> bool:
    for _ in range(attempts):
        healthy = orchestrator_client.is_vision_healthy()
        if healthy:
            return True
        time.sleep(delay)
    return False


def check_services_health():
    _health_status_box = st.empty()
    with _health_status_box.status(
        label="Checking services availability...",
        expanded=True,
    ) as status:

        try:
            with st.spinner("Checking orchestrator service health..."):
                healthy = _is_orchestrator_healthy()

            if healthy:
                status.success("Orchestrator service is healthy!")
            else:
                raise Exception("Orchestrator service is not healthy!")

            with st.spinner("Checking vision service health..."):
                healthy = _is_vision_healthy()

            if healthy:
                status.success("Vision service is healthy!")
            else:
                raise Exception(
                    "Vision service might be starting up or is unreachable!"
                )

        except Exception as error:
            status.error(str(error))
            status.update(label="Service health check failed.", state="error")
            st.stop()

        else:
            status.update(label="All services are healthy!", state="complete")

            time.sleep(1)
            _health_status_box.empty()


def main():

    st.set_page_config(
        page_title="YOLO Playground",
        page_icon="🤖",
        layout="wide",
    )

    st.markdown(
        "<style>.block-container {padding-top: 1rem;}</style>",
        unsafe_allow_html=True,
    )

    st.title("YOLO Playground")
    st.markdown("---")

    check_services_health()


if __name__ == "__main__":
    main()
