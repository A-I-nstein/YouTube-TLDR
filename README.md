# YouTube-TLDR
Using LLM to summarize and enhance media consumption experience.

Hi, this site can answer questions based on the link to the YouTube video provided by the user. The site also tells you where exactly (time stamp) on the video the question is answered.

## Instructions:
1. Paste the link of a YouTube video in the textbox and click 'Process Video'.
2. Once the video gets processed enter your query and click on 'Get Answer'
3. The answer appears with the related time stamp.
4. Click on 'Go To Timestamp' to go to the section of the video where the question is answered.
5. Refresh the page befor you paste a new link to clear cache. 

## Technology used:
1. LangChain: To integrate OpenAI models and Weaviate vector database.
2. AssemblyAI: To generate transcript for videos that do not come with captions.
3. Weaviate: To store vector data.
