import os
import json
import assemblyai as aai
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, _errors

def parse(data, dataType, durationAnchor):
    
    refined_data = []
    
    start = None
    duration = 0
    EOL = False
    text = ''
    flag = False

    for splits in data:

        if not start:
            if dataType == 'subtitles':
                start = splits['start']
            else:
                start = splits['start'] / 1000

        EOL = False
        text += f" {parseText(splits['text'])}"
        
        if dataType == 'subtitles':
            duration += splits['duration']
        else:
            duration += splits['end'] - splits['start']
        
        if '.' in splits['text']:
            EOL = True

        if dataType == 'subtitles':
            flag = duration > durationAnchor
        else:
            flag = duration > durationAnchor and EOL     

        if flag:
            refined_data.append({'text': text, 'start': start})
            text = ''
            EOL = False
            start = None
            duration = 0

    with open(f'output/refined_data.json', 'w') as f:
        f.write(json.dumps(refined_data))

def parseText(text):

    newText = ""
    text = text.replace('\n', ' ')
    for i in text:
        if i.isalnum() or i == " ":
            newText += i
    return newText

def generate_subtitles(link):

    try:
        youtubeObject = YouTube(link)
        if youtubeObject.length > 360:
            return 'fail', 'Please try with a video that is shorter than 5 minutes.'
        youtubeObject = youtubeObject.streams.get_audio_only()
        youtubeObject.download('output/')
    except Exception as e:
        return 'fail', 'Please try again with a different link.'
    else:
        try:
            aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe('output/' + youtubeObject.default_filename)
        except Exception as e:
            return 'fail', 'AssemblyAI token limit exceeded.'
        else:
            parse(transcript.json_response['words'], 'transcript', 20000)
            return 'success', transcript.text

def get_subtitles(link):

    try:
        id = link[-11:]
        srt = YouTubeTranscriptApi.get_transcript(id)
    except _errors.TranscriptsDisabled as e:
        status, data = generate_subtitles(link)
        if status != 'success':
            return 'fail', data
        else:
            return status, data
    except Exception as e:
        return 'fail', 'Please try again with a different link.'
    else: 
        parse(srt, 'subtitles', 20)
        subtitles = ""
        count = 0
        for parts in srt:
            subString = parseText(parts['text'])
            subtitles = f"{subtitles} {subString}"
        status = 'success'
        return status, subtitles