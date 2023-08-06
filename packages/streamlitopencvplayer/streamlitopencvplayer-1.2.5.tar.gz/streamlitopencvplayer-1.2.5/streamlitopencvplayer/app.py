import time
import urllib.request,json

import cv2
import streamlit as st

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


# Function to display video in the Streamlit app

def display_video(video_path, json_file):
    # Open the video file
    # Opening JSON file and returns JSON object as a dictionnary
    response = urllib.request.urlopen(json_file)
    fileReader = json.loads(response.read())
    list_json = []
    list_json.append(fileReader['timestamp'])
    list_json.append(fileReader['data'])
    st.session_state['alerts_list'].append(list_json)
    #st.write(st.session_state['alerts_list'])
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    if not st.session_state['alerts'] and not st.session_state['data'] :
        st.session_state['alerts'] = []
        st.session_state['data'] = []
        for x in range(len(st.session_state['alerts_list'])):
            time_alert = st.session_state['alerts_list'][x][0]-float(
                st.session_state['name_vid_sel'].partition('_')[0])
            st.session_state['alerts'].append(int((time_alert)*fps))
            st.session_state['data'].append(st.session_state['alerts_list'][x][1])
    i = 0
    #st.write(st.session_state['alerts'])
    data = st.session_state['data']
    alerts = st.session_state['alerts']
    resume = False
    column1, column2, column3 = st.columns([1, 2, 1])
    with column1:
        # zone to display images
        stframe = st.empty()
    with column3:
        # Alerts
        st.subheader('Alerts :')
        num_buttons = len(alerts)

        button_values = {f'{i}': 0 for i in range(num_buttons)}

        for button_label, button_value in button_values.items():
            if st.button(str('Alert ')+button_label):
                button_values = {label: 1 if label == button_label else 0 for label in button_values}

        for button_label, button_value in button_values.items():
            if button_value == 1:
                st.session_state['counter'] = alerts[int(button_label)]
                #st.write(f'Alert "{button_label}", Frame: {alerts[int(button_label)]}')


    # Buttons and zone of display
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        st.write('')
        st.write('')
        container_2 = st.empty()
        pause = container_2.button('⏸')

    with col2:
        st.write('')
    with col3:
        st.write('')
        st.write('')
        replay = st.button("↻")
    with col4:
        st.write('')
        st.write('')
        plus = st.button("➕")
    with col5:
        st.write('')
        st.write('')
        minus = st.button("➖")

    if replay:
        st.session_state['counter'] = 0
        st.session_state['frames'] = []
        resume = False


        # get all the frames from video when the list is empty
    if not st.session_state['frames']:
        while True:
            successs, frames = cap.read()
            if successs:
                frames = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)
                st.session_state['frames'].append(frames)
            else:
                break
        cap.release()
    # back to the first frame if the video is finished
    if st.session_state['counter'] == len(st.session_state['frames']):
        st.session_state['counter'] = 0

    stframe.image(st.session_state['frames']
                  [st.session_state['counter']], caption='', width=450)

    while st.session_state['counter'] < len(st.session_state['frames']):
        if not resume:
            if i < len(data):
                if st.session_state['counter'] == int(alerts[i]*fps):
                    # draw all detections on the frame
                    for j in range(len(data[i])):
                        output = cv2.rectangle(st.session_state['frames'][st.session_state['counter']], (data[i][j][0][0], data[i][j][0][1]), (
                            data[i][j][0][2], data[i][j][0][3]), color=(128, 0, 0), thickness=2)
                        output = cv2.putText(
                            st.session_state['frames'][st.session_state['counter']], data[i][j][3], (data[i][j][0][0], data[i][j][0][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                    # update image zone with detections
                    stframe.image(output, caption='', width=500)
                    time.sleep(0.08)
                    # the detection is drawn, to the next one
                    i += 1
                    st.session_state['counter'] += 1

            stframe.image(
                st.session_state['frames'][st.session_state['counter']], caption='', width=500)
            time.sleep(0.08)
            st.session_state['counter'] += 1
                

            if pause:
                resume = True
                break
            if plus:
                resume = True
                break
            if minus:
                st.session_state['counter'] = st.session_state['counter']-2           
                resume = True
                break

                # back to the first frame if the video is finished
            if st.session_state['counter'] == len(st.session_state['frames']):
                st.session_state['counter'] = 0
                resume = True
                break


    if resume:
        container_2.empty()
        pause = container_2.button('▶')
        resume = False

def main():


    video_path = "https://cvlogger.blob.core.windows.net/clientsample/1678352121.8713963_1678352127.8713963.webm?se=2023-06-20T10%3A49%3A01Z&sp=r&sv=2021-08-06&sr=b&sig=9o/0AhqY8v3E%2B8WATBI69aYNddekddb49g9YuXG1wVU%3D"
    down_json = "https://cvlogger.blob.core.windows.net/clientsample/1678352123.8713963.json?sp=r&st=2023-06-19T22:46:06Z&se=2023-06-20T16:46:06Z&sv=2022-11-02&sr=b&sig=GoE3UurhwkYgjKRd7yiBVRpKgIPHCt0WvTEK84CERqg%3D"
    
    if video_path is not None:
        display_video(video_path, down_json)



if __name__ == "__main__":
    main()

