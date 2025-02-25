import streamlit as st
from PIL import Image
import base64
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


def encode_image(image):
    image = Image.open(image)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    buffered.close()
    return encoded_image

def call_openai_api(
    encoded_image, starting_prompt, format, is_json_formatted, additional_instructions=""
):
    try:
        prompt = starting_prompt + "\n" + additional_instructions
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {
                    "role": "system",
                    "content": "You are an Aviation Expert specializing in interpreting Jeppesen Approach Charts. Your task is to analyze uploaded chart images and extract detailed information, organizing it into structured sections. Ensure all extracted data is accurate, corresponds exactly to the information presented in the chart image, and uses appropriate aviation terminology. Your expertise is crucial in ensuring that pilots and aviation personnel receive accurate and detailed information extracted from the Jeppesen Approach Charts. Your thoroughness and attention to detail contribute to the safety and efficiency of flight operations.",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_image}"
                            },
                        },
                    ],
                },
            ],
            max_tokens=4086,
            temperature=0.1,
            n=1,
            response_format=(
                 {"type": "text"}
            ),
        )

        message_content = response.choices[0].message.content
        return {
            "statusCode": 200,
            "body": json.loads(message_content) if is_json_formatted else message_content,
        }
    except json.JSONDecodeError as e:
        return {"statusCode": 500, "body": f"JSON decoding problem: {e}"}
    except Exception as e:
        return {"statusCode": 500, "body": f"An error occurred: {e}"}


def process_chart_header(encoded_image, is_json_formatted):

    chart_header_prompt = "Please analyze the attached Jeppesen Approach Chart image and extract the chart header information available at the top of the chart. Organize it into the specified sections and ensure that all extracted data is accurate and presented in the structured format provided below with no additional text in the response:\n"

    heading_prompt = """
    Analyze the heading section of the Jeppesen Approach Chart. Extract and organize the following details:
	1.	ICAO and IATA airport identifiers.
	2.	Airport name.
	3.	Chart index number, sequenced by runway and approach type.
	4.	Chart revision date.
	5.	Chart effective date.
	6.	Procedure identification (e.g., ILS, LOC, RNAV).
	7.	Geographical location (city and region)."""

    communications_prompt = """
    Extract the communication details from the Jeppesen Approach Chart, providing:
	1.	Call sign or service name omission details for broadcast-only services.
	2.	Functionality of the service (e.g., transmit/receive, transmit only).
	3.	All available primary radio frequencies.
	4.	Radar service availability and part-time indicators.
	5.	Defined sectors for each frequency.
	6.	Omitted call signs if the service is secondary."""

    approach_briefing_prompt = """
    From the Approach Briefing Information section, extract:
	1.	Primary navigation aid used (e.g., LOC, VOR).
	2.	Final approach course bearing.
	3.	FAF (Final Approach Fix) altitude or crossing altitudes for precision approaches.
	4.	DA(H) or MDA(H) values (Decision Altitude or Minimum Descent Altitude).
	5.	Airport elevation and Touchdown Zone elevation.
	6.	Complete textual Missed Approach Procedure.
	7.	Transition level and altitude information.
	8.	Any specific notes relevant to the approach procedure."""

    starting_prompt = "\n".join(
        [
            chart_header_prompt,
            heading_prompt,
            communications_prompt,
            approach_briefing_prompt,
        ]
    )

    return call_openai_api(
        encoded_image, starting_prompt, "", is_json_formatted, ""
    )

def process_image(image, option, is_json_formatted=False):
    encoded_image = encode_image(image)
    return process_chart_header(encoded_image, is_json_formatted)


#########################################################################
# Streamlit code for the UI
#########################################################################
# streamlit run demo.py
st.markdown(
    "<h1 style='text-align: center;'>Jepp Approach Charts Interpreter</h1>",
    unsafe_allow_html=True,
)

col1, col2 = st.columns([4, 5], vertical_alignment="top", gap="small")

with col1:
    st.header("Upload Jepp Chart", divider="gray")
    uploaded_image = st.file_uploader(
        "Choose an image file", type=["jpg", "png", "jpeg"]
    )
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

with col2:
    st.header("Extracted Data", divider="gray")
    if uploaded_image is not None:
        toggle_view = "Text"

        if st.button("Process Image", key="process"):
            result = process_image(uploaded_image, "All", toggle_view == "JSON")

            if result["statusCode"] == 200:
                text = result["body"]
                if toggle_view == "Text":
                    st.markdown(text)
                elif toggle_view == "JSON":
                    json_text = json.dumps(text, indent=8)
                    st.text_area("Formatted JSON Output", json_text, height=1000)
            else:
                st.error(result["body"])
