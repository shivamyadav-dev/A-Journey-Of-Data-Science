import streamlit as st
from mtranslate import translate
import os
from gtts import gTTS
import base64

# --- Page Configuration ---
# Set up the Streamlit page with a title, icon, and wide layout
st.set_page_config(
    page_title="Global Translator",
    page_icon="🌐",
    layout="wide"
)

# --- Language Data ---
LANGUAGES = {
    "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar",
    "Armenian": "hy", "Azerbaijani": "az", "Basque": "eu", "Belarusian": "be",
    "Bengali": "bn", "Bosnian": "bs", "Bulgarian": "bg", "Catalan": "ca",
    "Cebuano": "ceb", "Chichewa": "ny", "Chinese": "zh-CN", "Corsican": "co",
    "Croatian": "hr", "Czech": "cs", "Danish": "da", "Dutch": "nl",
    "English": "en", "Esperanto": "eo", "Estonian": "et", "Filipino": "tl",
    "Finnish": "fi", "French": "fr", "Frisian": "fy", "Galician": "gl",
    "Georgian": "ka", "German": "de", "Greek": "el", "Gujarati": "gu",
    "Haitian Creole": "ht", "Hausa": "ha", "Hawaiian": "haw", "Hebrew": "he",
    "Hindi": "hi", "Hmong": "hmn", "Hungarian": "hu", "Icelandic": "is",
    "Igbo": "ig", "Indonesian": "id", "Irish": "ga", "Italian": "it",
    "Japanese": "ja", "Javanese": "jw", "Kannada": "kn", "Kazakh": "kk",
    "Khmer": "km", "Kinyarwanda": "rw", "Korean": "ko", "Kurdish": "ku",
    "Kyrgyz": "ky", "Lao": "lo", "Latin": "la", "Latvian": "lv",
    "Lithuanian": "lt", "Luxembourgish": "lb", "Macedonian": "mk",
    "Malagasy": "mg", "Malay": "ms", "Malayalam": "ml", "Maltese": "mt",
    "Maori": "mi", "Marathi": "mr", "Mongolian": "mn", "Myanmar": "my",
    "Nepali": "ne", "Norwegian": "no", "Odia": "or", "Pashto": "ps",
    "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Punjabi": "pa",
    "Romanian": "ro", "Russian": "ru", "Samoan": "sm", "Scots Gaelic": "gd",
    "Serbian": "sr", "Sesotho": "st", "Shona": "sn", "Sindhi": "sd",
    "Sinhala": "si", "Slovak": "sk", "Slovenian": "sl", "Somali": "so",
    "Spanish": "es", "Sundanese": "su", "Swahili": "sw", "Swedish": "sv",
    "Tajik": "tg", "Tamil": "ta", "Tatar": "tt", "Telugu": "te",
    "Thai": "th", "Turkish": "tr", "Turkmen": "tk", "Ukrainian": "uk",
    "Urdu": "ur", "Uyghur": "ug", "Uzbek": "uz", "Vietnamese": "vi",
    "Welsh": "cy", "Xhosa": "xh", "Yiddish": "yi", "Yoruba": "yo", "Zulu": "zu"
}

# Set of language codes supported by gTTS (from your original code)
# This helps in deciding whether to show the audio player
GTTS_SUPPORTED_CODES = {
    "af", "ar", "bg", "bn", "bs", "ca", "cs", "cy", "da", "de", "el", "en",
    "eo", "es", "et", "fi", "fr", "gu", "hi", "hr", "hu", "hy", "id", "is",
    "it", "ja", "jw", "km", "kn", "ko", "la", "lv", "mk", "ml", "mr", "my",
    "ne", "nl", "no", "pl", "pt", "ro", "ru", "si", "sk", "sq", "sr", "su",
    "sv", "sw", "ta", "te", "th", "tl", "tr", "uk", "ur", "vi", "zh-CN"
}


# --- Helper Function ---
# Function to create a downloadable link for the audio file
def get_binary_file_downloader_html(bin_file, file_label='File'):
    """
    Generates a link to download the given file.
    """
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        # Custom styled download link (looks like a button)
        href = (
            f'<a href="data:application/octet-stream;base64,{bin_str}" '
            f'download="{os.path.basename(bin_file)}" '
            f'style="display: inline-block; padding: 6px 12px; background-color: #3498DB; color: white; '
            f'text-decoration: none; border-radius: 5px; font-weight: bold;">'
            f'Download {file_label}</a>'
        )
        return href
    except FileNotFoundError:
        # Gracefully handle if the file doesn't exist yet
        return ""

# --- Custom CSS ---
# Add custom styles for a "creative" and "interactive" dark theme
st.markdown("""
<style>
    /* Force page to a single view, no vertical scroll */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    body {
        overflow-y: hidden;
        height: 100vh;
    }

    /* Main app styling */
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
    }

    h1 {
        color: #9B59B6; /* Bright Purple */
        text-align: center;
        font-weight: bold;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }

    /* Style subheaders for dark mode */
    h3 {
        color: #E0E0E0;
    }
    
    h2 {
        color: #FAFAFA;
    }

    /* Style the text areas for dark mode */
    .stTextArea[data-testid="stTextArea"] > div > div > textarea {
        background-color: #1A1C24;
        color: #FAFAFA;
        border: 1px solid #333;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Style the output text area (disabled) */
    .stTextArea[data-testid="stTextArea"] > div > div > textarea[disabled] {
        background-color: #101318; /* Even darker for read-only */
        color: #E0E0E0;
    }

    /* Style the main translate button with a gradient (pops on dark) */
    .stButton>button {
        width: 100%;
        color: white;
        background-image: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
        border: none;
        padding: 12px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.1em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* Interactive hover effect for the main button */
    .stButton>button:hover {
        background-image: linear-gradient(to right, #2575fc 0%, #6a11cb 100%);
        transform: scale(1.03);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        filter: brightness(1.1);
    }
    
    /* Style for a secondary button (like 'Clear') in dark mode */
    div[data-testid="stHorizontalBlock"] button {
        background-color: #333;
        color: #FAFAFA;
        border: 1px solid #555;
        font-weight: bold;
    }
    
    div[data-testid="stHorizontalBlock"] button:hover {
        background-color: #444;
        border: 1px solid #666;
    }

    /* Style the sidebar for dark mode */
    [data-testid="stSidebar"] {
        background-color: #1A1C24;
        border-right: 1px solid #333;
    }
    
    [data-testid="stSidebar"] h2 {
        color: #9B59B6;
    }

    /* --- New Style for Highlighted 'Selected' Text --- */
    /* This styles the "Selected: Hindi" text */
    .selected-lang-label {
        font-weight: bold;
        color: #3498DB; /* Bright Blue */
        font-size: 1.1em;
        background-color: #101318;
        padding: 5px 10px;
        border-radius: 5px;
        display: block;
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* --- Button Highlighting --- */
    
    /* Style for SECONDARY sidebar buttons (NOT selected) */
    [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-secondary"] {
        background-color: #333;
        color: #FAFAFA;
        border: 1px solid #555;
        padding: 8px 5px;
    }
    
    [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-secondary"]:hover {
        background-color: #444;
        border: 1px solid #666;
    }

    /* Style for PRIMARY sidebar button (SELECTED) */
    /* This highlights the currently active language button */
    [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] {
        background-color: #9B59B6; /* Bright Purple */
        color: white;
        border: 1px solid #b073c9;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(155, 89, 182, 0.5); /* Glowing effect */
    }
    
    [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"]:hover {
        background-color: #a663c9;
        border: 1px solid #b073c9;
    }
    
    /* New style for developer credit in col1, under buttons */
    .developer-credit-col1-bottom {
        text-align: center;
        font-style: italic;
        color: #999;
        font-size: 1.1em; /* Larger */
        padding-top: 20px; /* Space from buttons */
        line-height: 1.4;
    }
    
    /* Style audio player */
    .stAudio > audio {
        width: 100%;
        background-color: #1A1C24;
        border: 1px solid #333;
        border-radius: 10px;
    }

</style>
""", unsafe_allow_html=True)


# --- App Layout ---

st.title("🌐 Global Translator Pro 🚀")
st.markdown("---")

# --- Initialize Session State ---
# This holds the app's memory (current text, translation, etc.)
if 'translation' not in st.session_state:
    st.session_state.translation = ""
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'target_lang_name' not in st.session_state:
    st.session_state.target_lang_name = "Hindi" # Default language
if 'audio_file_path' not in st.session_state:
    st.session_state.audio_file_path = None
if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None # Store audio in memory

# --- Callback Functions ---
# These functions are triggered by button clicks

def clear_text():
    """Clears all input, output, and audio from session state."""
    st.session_state.input_text = ""
    st.session_state.translation = ""
    st.session_state.audio_file_path = None
    st.session_state.audio_bytes = None

def set_language(lang_name):
    """Sets the target language when a sidebar button is clicked."""
    st.session_state.target_lang_name = lang_name

def handle_translate():
    """
    The main translation logic. This is called when
    the 'Translate!' button is clicked.
    """
    # --- FIX: Clear old audio state at the very beginning ---
    st.session_state.audio_file_path = None
    st.session_state.audio_bytes = None

    if st.session_state.input_text:
        target_lang_name = st.session_state.target_lang_name
        target_lang_code = LANGUAGES.get(target_lang_name, "en") # Default to 'en' if not found
        
        with st.spinner(f"Translating to {target_lang_name}..."):
            try:
                # Perform the translation
                output = translate(st.session_state.input_text, target_lang_code)
                st.session_state.translation = output
                st.toast(f"Translated to {target_lang_name}!", icon="✅")

                # --- Audio Generation ---
                # Check if the target language is supported by gTTS
                if target_lang_code in GTTS_SUPPORTED_CODES:
                    try:
                        # Generate the audio file
                        aud_file = gTTS(text=output, lang=target_lang_code, slow=False)
                        audio_path = "translation.mp3"
                        aud_file.save(audio_path)
                        
                        # --- FIX: Read bytes *immediately* after saving ---
                        # This solves the "two-click" audio problem
                        with open(audio_path, 'rb') as f:
                            audio_bytes = f.read()
                        
                        st.session_state.audio_file_path = audio_path
                        st.session_state.audio_bytes = audio_bytes # <--- STORE BYTES
                        st.toast(f"Audio for {target_lang_name} generated!", icon="🔊")

                    except Exception as audio_e:
                        st.error(f"Error generating audio: {audio_e}")
                        # audio_file_path and audio_bytes are already None
                else:
                    # If gTTS doesn't support the language
                    st.info(f"Audio playback is not supported for {target_lang_name}.")
                    # audio_file_path and audio_bytes are already None

            except Exception as e:
                # Handle translation errors
                st.error(f"An error occurred during translation: {e}")
                st.session_state.translation = "Translation failed. Please try again."
                # audio_file_path and audio_bytes are already None
    else:
        st.warning("Please enter some text to translate.", icon="⚠️")


# --- Sidebar for Language Selection ---
st.sidebar.header("Translation Settings")

# --- Creative Language Selection: Quick Select Grid (More Horizontal) ---
st.sidebar.subheader("Quick Select")
quick_select_langs = ["English", "Spanish", "Hindi", "French", "German", "Japanese"]
# Use 3 columns to give full language names space
q_cols = st.sidebar.columns(3)
for i, lang in enumerate(quick_select_langs):
    with q_cols[i % 3]:
        # Set button type to "primary" if selected, else "secondary"
        btn_type = "primary" if lang == st.session_state.target_lang_name else "secondary"
        st.button(lang, on_click=set_language, args=(lang,), use_container_width=True, help=lang, type=btn_type)

st.sidebar.markdown("---")

# --- Full Language Selection: Searchable Button Grid ---
st.sidebar.subheader("All Languages")

# Use new HTML/CSS for the highlighted "Selected" text
st.sidebar.markdown(f'<span class="selected-lang-label">Selected: {st.session_state.target_lang_name}</span>', unsafe_allow_html=True)

search_term = st.sidebar.text_input("Search all languages...", "", key="lang_search")

lang_list = sorted(LANGUAGES.keys())

if search_term:
    filtered_langs = [lang for lang in lang_list if search_term.lower() in lang.lower()]
else:
    filtered_langs = lang_list  # Show all if no search

# Displaying languages in a 2-column layout inside the sidebar
# This gives more space for full language names
N_COLS = 2
lang_cols = st.sidebar.columns(N_COLS)
for i, lang_name in enumerate(filtered_langs):
    with lang_cols[i % N_COLS]:
        # Set button type to "primary" if selected, else "secondary"
        btn_type = "primary" if lang_name == st.session_state.target_lang_name else "secondary"
        # Use a specific key for each button to make them unique
        st.button(lang_name, key=f"lang_btn_{lang_name}", on_click=set_language, args=(lang_name,), use_container_width=True, type=btn_type)


# --- Main Interface (Input/Output) ---
# This layout is designed to fit on one screen without vertical scrolling
col1, col2 = st.columns(2)

with col1:
    st.subheader("Enter Text to Translate")
    
    input_text = st.text_area(
        "Your text:",
        label_visibility="collapsed", # Hide the label, subheader is enough
        height=250,
        placeholder="Type or paste your text here...",
        key="input_text" # Bind to session state
    )
    
    # --- Interactive Buttons ---
    b_col1, b_col2 = st.columns([3, 1]) # Give Translate button more space
    with b_col1:
        # Attach the callback function here to fix the "two-click" bug
        translate_button = st.button("Translate!", use_container_width=True, on_click=handle_translate)
    with b_col2:
        # "Clear" button is a new interactive element
        clear_button = st.button("Clear ⌫", on_click=clear_text, use_container_width=True)

    # --- Developer Credit moved here, as requested by screenshot ---
    st.markdown(
        "<div class='developer-credit-col1-bottom'>Designed & Developed  by<br><strong>Shivam Kumar Yadav</strong></div>", 
        unsafe_allow_html=True
    )


with col2:
    st.subheader("Translation")
    
    # Display the translation in a disabled text area (styled by our CSS)
    # This now reads directly from the session state updated by the callback
    st.text_area(
        "Translated text:",
        value=st.session_state.translation,
        height=250,
        disabled=True,
        label_visibility="collapsed", # Hide the label, subheader is enough
        key="translation_output" # Give it a key
    )

    st.markdown("---")
    st.subheader("Audio Playback")

    # This is now the main audio block
    audio_placeholder = st.empty()

    # --- Display Audio ---
    # This logic now just *displays* the audio and download link
    # if they exist in session state, set by the handle_translate callback.
    if st.session_state.audio_bytes:
        with audio_placeholder.container():
            st.audio(st.session_state.audio_bytes, format='audio/mp3')
            
            if st.session_state.audio_file_path:
                st.markdown(
                    get_binary_file_downloader_html(st.session_state.audio_file_path, 'Audio File'),
                    unsafe_allow_html=True
                )
    else:
        # Fill the space if no audio
        with audio_placeholder.container():
            st.markdown("&nbsp;", unsafe_allow_html=True) # just empty space

