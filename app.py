import os
import json
import base64
import requests
import google.generativeai as genai
from flask import Flask, request, render_template, jsonify, Response
from pymongo import MongoClient
import concurrent.futures
import random
import concurrent.futures
import random
import threading
import queue

# Configure Gemini API keys
API_KEYS = [

    "AIzaSyAFC3ZLRndhFVuj5KUtDV1INDDlrSby6H8",
    "AIzaSyAygKoZWZZ1-_Pv7lKpymuK_1HTS7ezL3o",
    "AIzaSyCiwJJN4RIcvz9KGgKrvGa1BtMidaeltS8",
    "AIzaSyDVjfxEgUIrVmHz5lHhhwHNkAuR-8qrHrw"

]
def download_image(img_url):
    """Download image and return base64 encoded content"""
    try:
        response = requests.get(img_url)
        response.raise_for_status()
        return base64.b64encode(response.content).decode('utf-8')
    except Exception as e:
        print(f"Error downloading image {img_url}: {e}")
        return None
class APIKeyManager:
    def __init__(self, api_keys):
        self._queue = queue.Queue()
        for key in api_keys:
            self._queue.put(key)
        self._lock = threading.Lock()

    def get_api_key(self):
        with self._lock:
            if self._queue.empty():
                # Refill the queue if it's empty
                for key in API_KEYS:
                    self._queue.put(key)
            return self._queue.get()

    def release_api_key(self, key):
        with self._lock:
            self._queue.put(key)

# Initialize API Key Manager
api_key_manager = APIKeyManager(API_KEYS)

# MongoDB Connection
MONGO_URI = "mongodb+srv://123gamein:123gamein@memer.tcml6.mongodb.net/?retryWrites=true&w=majority&appName=Memer"
client = MongoClient(MONGO_URI)
db = client["SentimentDB"]
collection = db["SentimentCollection"]

def configure_gemini_api():
    """Obtain and configure a Gemini API key from the pool"""
    api_key = api_key_manager.get_api_key()
    genai.configure(api_key=api_key)
    return api_key

def aigenrator(user_input):
    """Classify sentiments of the input text"""
    api_key = None
    try:
        api_key = configure_gemini_api()
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(f"""classify the below text into Joyful,Sad,Angry,Fearful,Surprised,Disgusted,Confident,Nostalgic,Sarcastic,Excited,Bored,Anxious,Content,Motivated,Romantic,Frustrated,Jealous,Grateful,Curious,Embarrassed 
        if there are multiple also add it , just only respond with the classified keywords and nothing else or else the app will crash 

        {user_input}""")
        return response.text.strip().split(",")
    finally:
        if api_key:
            api_key_manager.release_api_key(api_key)

def generate_meme_texts(template, user_input):
    """Generate meme texts using Gemini API with improved error handling"""
    api_key = None
    try:
        # Download image
        img_encoded = download_image(template['url'])
        if not img_encoded:
            return None

        # Obtain API key
        api_key = configure_gemini_api()
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")

        # Construct the prompt
        prompt = f"""
        You are a meme-generating API. Create 5 funny memes based on the given template and context.
        Do not add unnecessary text or JSON markers. Respond directly with the JSON format below.
        Meme Template: {template['id']}
        Description: {template['explanation']}
        Context: {user_input}
        Output exactly in this format:
        [
            {{
                "template_id": "{template['id']}",
                "text0": "Meme text for top position",
                "text1": "Meme text for bottom position"
            }},
            ...  // Continue for a total of 5 memes
        ]
        """

        # Generate content using the model
        request_payload = [{'mime_type': 'image/jpeg', 'data': img_encoded}, prompt]
        api_response = model.generate_content(request_payload)
        return json.loads(api_response.text)
    except Exception as e:
        print(f"Error generating meme texts: {e}")
        return None
    finally:
        if api_key:
            api_key_manager.release_api_key(api_key)


def generate_meme(template_id, texts):
    """Generate a meme using the Imgflip API"""
    url = "https://api.imgflip.com/caption_image"

    params = {
        "template_id": template_id,
        "username": "alphamemer456",
        "password": "alphamemer",
    }
    params.update(texts)
    response = requests.post(url, data=params)

    if response.status_code == 200:
        data = response.json()
        return data['data']['url'] if data['success'] else f"Error: {data['error_message']}"
    return f"HTTP Error: {response.status_code}"


def fetch_ranked_image_urls(input_sentiments):
    """Fetch sentiment-based meme URLs from MongoDB"""
    input_sentiments = [sentiment.strip().lower() for sentiment in input_sentiments]
    results = collection.find({}, {"Image_URL": 1, "Sentimental": 1, "_id": 0})

    ranked_results = []
    for result in results:
        sentimental_value = result.get("Sentimental", "")
        if not isinstance(sentimental_value, str):
            continue

        doc_sentiments = [s.strip().lower() for s in sentimental_value.split(",")]
        match_count = len(set(input_sentiments) & set(doc_sentiments))
        if match_count > 0:
            ranked_results.append({"Image_URL": result.get("Image_URL"), "match_count": match_count})

    ranked_results.sort(key=lambda x: x["match_count"], reverse=True)
    return [result["Image_URL"] for result in ranked_results[:30]]


# Meme templates data
meme_templates = [
    {
        "id": "181913649",
        "explanation": "The Drake meme shows Drake in two different expressions: one with a dismissive hand gesture, and the other with a more approving, almost celebratory, pose. It's used to represent a shift in opinion or a change in attitude.",
        "url": "https://imgflip.com/s/meme/Drake-Hotline-Bling.jpg",
    },
    {
        "id": "112126428",
        "explanation": "This meme depicts a man seemingly oblivious to a woman who is clearly looking at him (and possibly flirting with him) in a way that implies he's not paying much attention or isn't interested.",
        "url": "https://imgflip.com/s/meme/Distracted-Boyfriend.jpg",
    },
    {
        "id": "87743020",
        "explanation": "This meme format typically shows a person facing a difficult choice (represented by two buttons). The bottom panel depicts the person's reaction to having to make that choice, usually stressed or anxious.",
        "url": "https://imgflip.com/s/meme/Two-Buttons.jpg",
    },
    {
        "id": "124822590",
        "explanation": "The meme uses a highway sign indicating a left turn (Exit 12) alongside a car performing a drift or uncontrolled turn to the right. It highlights the contrast between expected behavior and actual behavior.",
        "url": "https://imgflip.com/s/meme/Left-Exit-12-Off-Ramp.jpg",
    },
    {
        "id": "129242436",
        "explanation": "A meme template featuring a person sitting outdoors, presenting a blank space below 'CHANGE MY MIND'. The blank space is where the user inserts an argument or statement they want to challenge.",
        "url": "https://imgflip.com/s/meme/Change-My-Mind.jpg",
    },
    {
        "id": "4087833",
        "explanation": "skeleton waiting on bench in the park",
        "url": "https://imgflip.com/s/meme/Waiting-Skeleton.jpg",
    },

{
        "id": "97984",
        "explanation": "A meme featuring a young girl looking at a burning house with a seemingly unfazed expression. The meme is used to comment on the insensitivity or lack of awareness some people may show in the face of tragedy. It's often meant to be darkly humorous, drawing a contrast between the seriousness of the event and the child's reaction.",
        "url": "https://imgflip.com/s/meme/Disaster-Girl.jpg",
    }

]

# Flask App
app = Flask(__name__)


@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    user_input = request.json.get('prompt', '')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        # Get sentiments
        sentiments = aigenrator(user_input)

        # Fetch sentiment-based memes from MongoDB
        sentiment_meme_urls = fetch_ranked_image_urls(sentiments)

        # Generate AI memes in parallel
        ai_meme_urls = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(meme_templates)) as executor:
            # Generate meme texts for each template
            meme_texts_futures = {
                executor.submit(generate_meme_texts, template, user_input): template
                for template in meme_templates
            }

            for future in concurrent.futures.as_completed(meme_texts_futures):
                try:
                    response = future.result()
                    if response:
                        for meme in response:
                            template_id = meme["template_id"]
                            text_entries = {key: value for key, value in meme.items() if key.startswith("text")}
                            meme_url = generate_meme(template_id, text_entries)
                            ai_meme_urls.append(meme_url)
                except Exception as e:
                    print(f"Error generating AI meme: {e}")

        return jsonify({
            "sentiments": sentiments,
            "sentiment_meme_urls": sentiment_meme_urls,
            "ai_meme_urls": ai_meme_urls
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/process', methods=['GET'])
def process_streaming():
    user_input = request.args.get('prompt', '')
    if not user_input:
        return Response("data: error\n\n", content_type='text/event-stream')

    def generate():
        try:
            # Get sentiments
            sentiments = aigenrator(user_input)

            # Send sentiments
            yield f"event: sentiments\ndata: {json.dumps(sentiments)}\n\n"

            # Fetch sentiment-based memes from MongoDB
            sentiment_meme_urls = fetch_ranked_image_urls(sentiments)

            # Stream sentiment-based memes
            for url in sentiment_meme_urls:
                yield f"event: sentiment_meme\ndata: {url}\n\n"

            # Generate AI memes in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(meme_templates)) as executor:
                # Generate meme texts for each template
                meme_texts_futures = {
                    executor.submit(generate_meme_texts, template, user_input): template
                    for template in meme_templates
                }

                for future in concurrent.futures.as_completed(meme_texts_futures):
                    try:
                        response = future.result()
                        if response:
                            for meme in response:
                                template_id = meme["template_id"]
                                text_entries = {key: value for key, value in meme.items() if key.startswith("text")}
                                meme_url = generate_meme(template_id, text_entries)

                                # Stream AI-generated meme
                                yield f"event: ai_meme\ndata: {meme_url}\n\n"
                    except Exception as e:
                        print(f"Error generating AI meme: {e}")

            # Send completion event
            yield "event: complete\ndata: done\n\n"

        except Exception as e:
            yield f"event: error\ndata: {str(e)}\n\n"

    return Response(generate(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)