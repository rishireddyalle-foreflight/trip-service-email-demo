import streamlit as st
from emailmonitor import *
from gpt_connector import *
from Constants import *
import json
import time
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title="Automating Trip Service Requests", layout="wide")

cols_header = st.columns([0.5, 0.9, 0.4])
with cols_header[0]:
    with stylable_container(
        key="green_button",
        css_styles="""
            {
                color: black;
            },
            header {
                font-size: 30px;
            }
            """,
        ):
        imageTitle = st.columns([0.03,0.5])
        with imageTitle[0]:
            st.image("headerLogo.png", width=20)
        with imageTitle[1]:
            st.write("**Trip Request Visualizer**")

st.markdown(
    r"""
    <style>
        .ezrtsby0{
            display:none;
        },
        .stAppDeployButton {
            display:none;
        },
        .st-emotion-cache-czk5ss {
            display:none;
        },
        .stHeading {
            background-color: 'white'
        }
    </style>
    """, unsafe_allow_html=True
)

if 'latest_email' not in st.session_state:
    st.session_state['latest_email'] = ''
if 'formatted_email' not in st.session_state:
    st.session_state['formatted_email'] = ''
if 'isJsonFormatted' not in st.session_state:
    st.session_state['isJsonFormatted'] = False
if 'format_type' not in st.session_state:
    st.session_state['format_type'] = 'Indented Preview'

choose_option_selector = st.columns([0.5,0.2])

button_title = ""

def onJsonClick():
    st.session_state.latest_email = get_latest_email()
    print(f"first email is {st.session_state.latest_email}")
    st.session_state.isJsonFormatted = (st.session_state.format_type == "Json")


def onFormatClick():
    st.session_state.isJsonFormatted = (st.session_state.format_type == "Json")
    st.session_state.formatted_email = get_chatgpt_response(prompt_for_email(st.session_state.latest_email, st.session_state.isJsonFormatted), st.session_state.isJsonFormatted)
    # st.session_state.formatted_email = get_chatgpt_response("convert given string to the json format {\"message\": \"Hello, world\", \"This is a backslash\": \"slash\"}", True)
    # print(f"onFormatClick {st.session_state.formatted_email} isJson {(st.session_state.format_type == "Json")}")


with choose_option_selector[0]:
    with stylable_container(
            key="green_button",
            css_styles="""
                {
                    color: black;
                }
                """,
            ):
                st.write("""
                    **Welcome back,**
                    <br>
                    Easily convert email to successfull Trip Request
                    """, unsafe_allow_html=True)

def onIndented():
    st.session_state.format_type = "Indented Preview"
    onFormatClick()

def onJsonFormatted():
    st.session_state.format_type = "Json"
    onFormatClick()

with choose_option_selector[1]:
    
    with stylable_container(
            key="container4_with_border",
            css_styles="""
                {
                    color: black;
                    font-size: 32px;
                }
                """,
            ):
                # with st.container():
            right_segment_tabs = st.columns(2)
            with right_segment_tabs[0]:
                with stylable_container(
                    key="csegment1_with_border",
                    css_styles="""
                        button{
                            color: white;
                            background: #2446A6;
                        }
                        """,
                ):
                    st.button("Indented Preview", on_click = onIndented)
            with right_segment_tabs[1]:
                with stylable_container(
                    key="segment2_with_border",
                    css_styles="""
                        button{
                            color: #2446A6;
                            background: #8EE4FF33;
                        }
                        """,
                ):
                    st.button("Json", on_click = onJsonFormatted)
                    # with right_segment_tabs[0]:
                    #     with stylable_container(
                    #         key="container1_with_border",
                    #         css_styles="""
                    #             button{
                    #                 color: white;
                    #                 background: #2446A6;
                    #             }
                    #             """,
                    #         ):
                        

                    # with right_segment_tabs[1]:
                    #     with stylable_container(
                    #         key="container2_with_border",
                    #         css_styles="""
                    #             button{
                    #                 background: transparent;
                    #                 border: none;
                    #             }
                    #             """,
                    #         ):
                                # st.button("Json", on_click = onJsonFormatted)
#     format_type = st.radio(
#     "**Select visualization mode**",
#     ["Formatted Preview", "Json"],
# )
# col1, col2 ,col3 = st.columns(3)
cols_mr = st.columns([10.9, 0.2, 10.9])


cols_left_content = st.columns([0.5,0.5])

with cols_mr[0]:
    # with stylable_container(
    #     key="green_button",
    #     css_styles="""
    #         button {
    #             background: #2446A6;
    #             color: white;
    #         }
    #         """,
    #     ):    
    #         st.button("Fetch Email", on_click = onJsonClick)

        with stylable_container(
            key="container_with_border",
            css_styles="""
                {
                    color: black;
                    font-size: 32px;
                    background: #E7E8E8;
                    padding: 16px;
                    border-radius: 0.5rem;
                }
                """,
            ):
            with st.container(height=450, border=False):
                # st.write("**Received Email**")
                st.write(st.session_state.latest_email)
                if st.session_state.formatted_email == "" :
                    with stylable_container(
                        key="btn8_with_border",
                        css_styles="""
                         button{
                                color: white;
                                font-size: 32px;
                                background: #E7E8E8;
                                border: none;
                                color: white;
                                margin-left: 46%;
                                background: #2446A6;
                            }                        
                            """,
                        ):
                        st.html(
                            '''
                                <div class="center-align-text">
                                <b>No Data Added</b><br>
                                Click <b>Fetch Email</b> to start
                                </div>
                                <style>
                                    .center-align-text {
                                        margin-left: 10%;
                                        margin-top: 28%;
                                        font-size: 16px;
                                        text-align: center;
                                    }
                                </style>
                            '''
                        )
                        st.button("Fetch Email", on_click = onJsonClick)
                else:
                    st.empty()


# with st.container(border=True):

# st.text_area(":red-background[**Latest Email**]", value = st.session_state.latest_email, height = 300, placeholder = "Tap on fetch email to Sync", key = "key_latest_email")


button_title = st.session_state.format_type

with cols_mr[1]:
    st.html(
        '''
            <div class="divider-vertical-line"></div>
            <style>
                .divider-vertical-line {
                    border-left: 0px solid rgba(49, 51, 63, 0.2);
                    height: 320px;
                    margin: auto;
                }
            </style>
        '''
    )

with cols_mr[2]: 
    # with stylable_container(
    #     key="green_button",
    #     css_styles="""
    #         button {
    #             background: #2446A6;
    #             color: white;
    #         }
    #         """,
    #     ):    
    #         st.button("View "+button_title, on_click = onFormatClick)
    # st.session_state.formatted_email = get_chatgpt_response(prompt_for_email(st.session_state.latest_email))
    with stylable_container(
        key="container9_with_border",
        css_styles="""
            {
                color: black;
                font-size: 32px;
                background: #E7E8E8;
                border-radius: 0.5rem;
                padding: 16px;
            }
            """,
        ):
            with st.container(height = 450, border=False):
                if st.session_state.formatted_email != "" :
                    if st.session_state.isJsonFormatted :
                        st.json({st.session_state.formatted_email})
                    else :
                        st.markdown(f"{st.session_state.formatted_email}")
                with stylable_container(
                    key="btn8_with_border",
                    css_styles="""
                     button{
                            color: white;
                            font-size: 32px;
                            background: #E7E8E8;
                            color: white;
                            margin-left: 46%;
                            background: #2446A6;
                        }                        
                        """,
                    ):
                    st.html(
                        '''
                            <div class="center-align-text">
                            <b>Indented Preview</b><br>
                            Click <b>Preview</b> to see magic
                            </div>
                            <style>
                                .center-align-text {
                                    margin-left: 10%;
                                    margin-top: 28%;
                                    font-size: 16px;
                                    text-align: center;
                                }
                            </style>
                        '''
                    )
                    st.button("Preview", on_click = onFormatClick, disabled = (st.session_state.latest_email == ""))                    # with stylable_container(
                    #     key="btn7_with_border",
                    #     css_styles="""
                    #      button{
                    #             color: white;
                    #             font-size: 32px;
                    #             margin-left: calc(45% - 10px);
                    #             background: #2446A6;
                    #             border-radius: 0px;
                    #             padding-top: -32px;
                    #             height: 20px;
                    #         }                        
                    #         """,
                    #     ):
                            # st.button("Preview", on_click = onJsonClick, disabled = (st.session_state.latest_email == ""))




