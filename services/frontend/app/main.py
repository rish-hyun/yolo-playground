import os
import sys
import time

_ROOT = os.path.join(os.path.dirname(__file__), "../../..")
if _ROOT not in sys.path and os.path.isdir(os.path.join(_ROOT, "common")):
    sys.path.insert(0, _ROOT)

import streamlit as st

from client import orchestrator_client
from common.schemas.enums import Mode, Task
from common.schemas.requests import ImageFile

# from streamlit_webrtc import webrtc_streamer

st.session_state.setdefault("services_health_checked", False)


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
    _placeholder = st.empty()
    with _placeholder.container():
        with st.status(
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

    _placeholder.empty()


def image_mode(task: str):
    image_file = st.file_uploader(
        label="Upload an image file",
        type=["png", "jpg", "jpeg"],
    )

    if image_file is not None:
        _input, _output = st.columns(2)

        with _input:
            st.text("Input")
            st.image(image_file)

        with _output:
            st.text("Result")
            image_file = ImageFile(
                file_name=image_file.name,
                file_content=image_file.read(),
                content_type=image_file.type,
            )

            with st.spinner("Performing inference..."):
                img_bytes = getattr(orchestrator_client, task)(file=image_file)
            st.image(img_bytes)


def video_mode(task: str):
    # video_file = st.file_uploader(
    #     label="Upload a video file",
    #     type=["mp4", "avi", "mov"],
    # )
    st.info("Video mode is not yet implemented.")


def webcam_mode(task: str):
    # webrtc_streamer(
    #     key="yolo-playground-webrtc",
    #     video_frame_callback=None,
    #     media_stream_constraints={"video": True, "audio": False},
    # )
    st.info("Webcam mode is not yet implemented.")


def main():

    st.set_page_config(
        page_title="YOLO Playground",
        page_icon="🤖",
        layout="wide",
    )

    st.markdown(
        """
        <style>
            .stMainBlockContainer {
                padding-left: 5rem;
                padding-right: 5rem;
                padding-top: 0rem;
                padding-bottom: 0rem;
            }
            .stAppHeader {
                background-color: rgba(255, 255, 255, 0.0);
            }
            button[data-baseweb="tab"] {
                font-size: 24px;
                margin: 0;
                width: 100%;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("YOLO Playground")

    with st.sidebar:
        st.header("Inference Settings")
        mode = st.radio("Select Mode:", iter(Mode))
        task = st.radio("Select Task:", iter(Task))

    if st.session_state["services_health_checked"] is False:
        check_services_health()
        st.session_state["services_health_checked"] = True

    match mode:
        case Mode.IMAGE:
            image_mode(task)
        case Mode.VIDEO:
            video_mode(task)
        case Mode.WEBCAM:
            webcam_mode(task)


if __name__ == "__main__":
    main()
