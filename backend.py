# imports
import os
import glob
import json
from llm_utils import llm_summary, llm_answer
from yt_utils import get_subtitles
import weaviate as weav

WEAVIATE_API_KEY = os.getenv('WEAVIATE_API_KEY')
WEAVIATE_URL = os.getenv('WEAVIATE_URL')

# clean up

def cleaner():
    if not os.path.exists('output'):
        os.makedirs('output')
    else:
        files = glob.glob('output/*')
        for f in files:
            os.remove(f)

    client = weav.Client(
        url=WEAVIATE_URL,
        auth_client_secret=weav.AuthApiKey(api_key=WEAVIATE_API_KEY), 
    )
    for value in client.data_object.get()['objects']:
        client.data_object.delete(value['id'])

# function to generate summary of a video

def get_summary(video_link):
    cleaner()
    status, data = get_subtitles(video_link)
    if status == 'success':
        status, data = llm_summary(data)
    return status, data
    

# function to get an answer

def get_answer(question):
    with open('output/refined_data.json') as fb:
        subtitles = json.load(fb)
    status, data = llm_answer(question, subtitles)
    return status, data