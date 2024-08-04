import streamlit as st
import rock_paper_scizor as rps

import ballon1 as Ballon
import json
# rock paper scizor requierment

from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
def load_lottie(filepath):
    with open(filepath,'r', encoding="utf-8") as f :
        return json.load(f)

st.title('**GAME DUO**')
st.header('**R0CK PAPER SCISSORS AND BALLON CHALLENGE**')
selected = option_menu(
    menu_title=None,
    options=['Home','ROCK_PAPER_SCISSORS','BALLON GAME'],
    icons=['house','hand','ballon'],
    menu_icon = "cast",
    orientation = 'horizontal'
)

if selected == "Home":
    hcol1,hcol2  =st.columns(2)
    with hcol1:
        hcol1.title('PEC WELCOME\'S YOU')
        hcol1.write("Welcome to the ultimate OpenCV gaming platform. Discover a variety of exciting games powered by computer vision. Challenge yourself, compete with friends, or simply relax and have fun.")
    with hcol2:
        path = load_lottie(r"animation/robot-hi.json")
        st_lottie(
            path,
            speed=1,
            reverse=False,
            loop=True,
            key='home_lottie'
        )
    

if selected == 'ROCK_PAPER_SCISSORS':
    st.write('Think you can outsmart a computer? Prove it! Our Rock, Paper, Scissors game uses advanced OpenCV technology to analyze your hand gestures in real-time. Show us your best rock, paper, or scissors and see if you can beat the AI opponent. It\'s more than just a game; it\'s a battle of human ingenuity against machine learning!')
    col1,col2 = st.columns(2,gap='medium')
    with col1 :
        col1.image("rps_img.jpeg",use_column_width=True)
    with col2:
        path = load_lottie(r"animation/start.json")
        st_lottie(
            path,
            speed=1,
            reverse=False,
            loop=True,
            key='start1_lottie'
        )
        rock_game = col2.button('**START**',use_container_width= True,key='rps_key')
        if rock_game:
            rock1 = rps.rock()

if selected == 'BALLON GAME':
    st.write("Ready for an explosive challenge? Our Balloon Pop game uses OpenCV magic to turn your hand into a virtual fist. Watch colorful balloons float across the screen and then, with a powerful punch, pop them! It's a fun and addictive way to test your reflexes and accuracy. Can you pop all the balloons before time runs out?")
    bcol1,bcol2 = st.columns(2,gap='medium')
    with bcol1 :
        path = load_lottie(r"animation/ballon.json")
        st_lottie(
            path,
            speed=1,
            reverse=False,
            loop=True,
            key='ballon_lottie'
        )
    with bcol2:
        path = load_lottie(r"animation/start.json")
        st_lottie(
            path,
            speed=1,
            reverse=False,
            loop=True,
            key='start_lottie'
        )
        ballon_game = bcol2.button('**START**',use_container_width= True,key='ballon_key')
        if ballon_game:
            Ballon1 =  Ballon.run_ballon_game()


