# Meme Wizard (Meme Generation and Sentiment Analysis App)

This project is a **web-based application** that uses AI to generate memes and perform sentiment analysis on user input. It combines modern technologies like Flask, MongoDB, Gemini AI, and Imgflip API to deliver a fun, engaging, and interactive experience.

---

## Table of Contents

1. [Features](#features)  
2. [Technologies Used](#technologies-used)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [API Endpoints](#api-endpoints)  
6. [How It Works](#how-it-works)  
7. [Contributing](#contributing)  
8. [License](#license)  

---

## Features

- **Sentiment Analysis**: Classifies user input into multiple emotions like Joyful, Sad, Angry, etc.
- **Meme Templates**: Includes popular meme templates such as Drake, Distracted Boyfriend, Two Buttons, and more.
- **Meme Text Generation**: Creates funny meme captions based on user input and meme context.
- **Sentiment-Based Meme Recommendations**: Fetches memes related to detected emotions from a MongoDB database.
- **Real-Time Streaming**: Uses Server-Sent Events (SSE) to stream live results to the user.
- **Parallel Execution**: Generates memes concurrently for optimal performance.

---

## Technologies Used

- **Backend**:  
  - Flask (Python)
  - MongoDB (NoSQL Database)
  - Imgflip API (Meme creation)

- **AI**:  
  - Gemini AI (Sentiment analysis and text generation)

- **Utilities**:  
  - Multithreading with `ThreadPoolExecutor` for parallel meme generation.
  - Base64 encoding for embedding images during API calls.

- **Frontend**:  
  - HTML templates (Jinja2)
  - Real-time updates with Server-Sent Events (SSE).

---

## Installation

### Prerequisites
- Python 3.8 or higher
- MongoDB instance (local or cloud)
- Imgflip API credentials

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/meme-generator-sentiment-analysis.git
   cd meme-generator-sentiment-analysis
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the project root and add the following:
   ```
   MONGO_URI=mongodb+srv://<your_username>:<your_password>@<your_cluster>.mongodb.net/?retryWrites=true&w=majority
   IMGFLIP_USERNAME=your_imgflip_username
   IMGFLIP_PASSWORD=your_imgflip_password
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the app**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

---

## Usage

1. Open the app in your browser.
2. Enter a prompt describing a situation, emotion, or idea.
3. View the detected sentiments and browse relevant memes.
4. Explore AI-generated memes based on the provided context.

---

## API Endpoints

### 1. `GET /`
**Description**: Displays the landing page.

### 2. `POST /process`
**Description**: Processes user input and generates memes.  
**Request Body**: 
```json
{
  "prompt": "Your text input here"
}
```
**Response**:
```json
{
  "sentiments": ["joyful", "excited"],
  "sentiment_meme_urls": ["url1", "url2"],
  "ai_meme_urls": ["ai_url1", "ai_url2"]
}
```

### 3. `GET /process`
**Description**: Streams real-time results using SSE.

---

## How It Works

1. **User Input**: The user provides text describing an idea or emotion.
2. **Sentiment Analysis**: The app uses Gemini AI to classify the input into emotions.
3. **Meme Recommendations**:
   - Retrieves emotion-matched memes from MongoDB.
   - Generates new memes using AI and Imgflip API.
4. **Real-Time Results**: Sentiments and memes are streamed live to the user.

---

## Contributing

We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push to your fork:
   ```bash
   git commit -m "Add feature or fix bug"
   git push origin feature-name
   ```
4. Open a pull request and describe your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Enjoy creating memes with the power of AI! 🎉
