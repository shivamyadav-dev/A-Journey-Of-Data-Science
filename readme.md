<h1 align="center">
🌐 Global Translator Pro 🚀
</h1>

<p align="center">
<strong>Why just <i>read</i> a translation when you can <i>listen</i> to it?</strong>
</p>

<p align="center">
<!-- Badges: Replace 'your-username' and 'global-translator-pro' with your GitHub details -->
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
<a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-1.30%2B-red.svg" alt="Streamlit"></a>
<a href="https://www.google.com/search?q=https://github.com/your-username/global-translator-pro/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
<a href="https://github.com/your-username/global-translator-pro/pulls"><img src="https://img.shields.io/badge/PRs-Welcome-brightgreen.svg" alt="PRs Welcome"></a>
</p>

<p align="center"> <!--

==> IMPORTANT: Replace this URL with a real screenshot of your app!

-->
<img src="https://www.google.com/search?q=https://placehold.co/800x450/0E1117/E0E0E0%3Ftext%3DYour%2BApp%2BScreenshot%2BHere" alt="App Screenshot" width="80%">





<i>(Screenshot of the Global Translator Pro application)</i>
</p>

🎯 The Problem

Language barriers aren't just about text; they're about the confidence to speak. Most translation tools show you what to say, but not how to say it. This leaves a critical gap for learners, travelers, and professionals who need to communicate with correct pronunciation.

✨ The Solution

Global Translator Pro is an interactive web application that bridges this gap by solving two problems at once:

The "What": Instantly translates your text into over 100 languages.

The "How": Provides high-quality, one-click audio playback 🔊 for dozens of them, so you know exactly how the words should sound.

This tool transforms a simple translator into a powerful communication and learning aid.

🌟 Key Features

Feature

Description

Benefit

🔊 Instant TTS

Integrates Google Text-to-Speech (gTTS) to generate clear audio.

Hear the correct pronunciation instantly.

📥 Audio Download

Listen in the app or download the .mp3 file for offline practice.

Practice on the go, anytime, anywhere.

🎨 Sleek Dark Mode UI

A fully custom, responsive interface built with Streamlit and advanced CSS.

Easy on the eyes and a pleasure to use.

🔍 Smart Language Selection

"Quick Select" grid for common languages and a fully searchable list.

Find your target language in seconds.

⏯️ Interactive Controls

"Translate!" button for all actions and a "Clear ⌫" button to reset.

A fluid, easy-to-use experience.

💾 Stateful Design

Uses Streamlit's session_state and on_click callbacks.

Remembers your inputs without full page reloads.

💡 Benefits of the App

Learn Correct Pronunciation: Don't just guess—hear the correct pronunciation from a native-sounding voice.

Build Speaking Confidence: Practice along with the audio to build confidence before a conversation or presentation.

Offline Access: Save audio clips to your phone or computer for learning on the go.

All-in-One Tool: No need to copy-paste text between a translator and a separate TTS app.

Visually Pleasing: The custom dark-mode UI is modern and comfortable for long sessions.

🛠️ Tech Stack & Tools

<details>
<summary>Click to see the technologies used</summary>

Core Framework: Streamlit

Translation API: mtranslate Python library

Audio Generation: gTTS (Google Text-to-Speech) library

Frontend: Custom CSS (injected via st.markdown)

State Management: Streamlit's st.session_state and Callbacks

Language: Python 3

</details>

🚀 How to Run Locally

<details>
<summary>Click for step-by-step installation instructions</summary>

Clone the repository: (Replace your-username with your GitHub username)

git clone [https://github.com/your-username/global-translator-pro.git](https://github.com/your-username/global-translator-pro.git)
cd global-translator-pro


Create and activate a virtual environment (Recommended):

# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate


Install the dependencies: (Your app.py only requires these)

pip install streamlit mtranslate gTTS


Run the Streamlit app:

streamlit run app.py


Your browser will automatically open to http://localhost:8501. Enjoy!

</details>

🤝 How to Contribute

Contributions, issues, and feature requests are welcome!

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

🙏 Acknowledgments

Designed & Developed by Shivam Kumar Yadav.

Built with the awesome Streamlit framework.

Powered by gTTS and mtranslate.
