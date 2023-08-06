"""Test script."""

import argparse
import uuid

import streamlit as st
from streamlitopencvplayer.app import display_video


# Initiate all session states used
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0
if 'frames' not in st.session_state:
    st.session_state['frames'] = []
if 'alerts' not in st.session_state:
    st.session_state['alerts'] = []
if 'data' not in st.session_state:
    st.session_state['data'] = []
if 'alerts_list' not in st.session_state:
    st.session_state['alerts_list'] = []
if 'name_vid_sel' not in st.session_state:
    st.session_state['name_vid_sel'] = "1678352121.8713963_1678352127.8713963"

class opencvplayer:
    """Class streamlit opencv player."""

    def __init__(self, video_path, json_file):
        self.video_path = video_path
        self.json_file = json_file


    #@st.cache_data()
    def main(self):
        """Test function.

        Args:
            video_path (required): video file path or video url.
            alerts_dict (Optional) : Dictionary of alerts passed to the alerts table.
            alerts (Required when data is used) : List of alerts time
            data (Optional) : bounding box coordinates, score and class
            This is an example for test :
                self.alerts_dict = {"Alerts": [43, 64]}
                self.alerts = [43, 64]
                self.data = [[[10, 100, 290, 200], 0.82, 0, "Class 0"],
                        [[55, 22, 100, 120], 0.9, 1, "Class 1"]]

        Returns:
            The video Player.
        """
        if self.video_path is not None:
            return display_video(self.video_path, self.json_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runnnig...")
    parser.add_argument(
        "--video-path",
        "-V",
        help="Enter the video path",
        default=str(uuid.uuid4().hex),
    )
    parser.add_argument(
        "--json-file",
        "-J",
        help="Enter the json file path",
    )
    args = parser.parse_args()
    opencvplayer = opencvplayer(
        args.video_path, args.json_file)
    opencvplayer.main()
