import pandas as pd
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template # <-- Import render_template
import os # <-- Import os for environment variables (recommended)

app = Flask(__name__)

# 🔥 GEMINI API KEY (RECOMMENDED: Use Environment Variable)
GEMINI_API_KEY = "AIzaSyAdBxiYzraEbo9GhBhkARAvH5W7XEijT0U" # <-- Avoid hardcoding
# GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    # In a real deployment, you might want Flask to exit or log a critical error
    print("WARNING: GEMINI_API_KEY environment variable not set.")
    # For local testing you could fallback, but avoid in production:
    # GEMINI_API_KEY = "YOUR_FALLBACK_KEY_FOR_LOCAL_TEST_ONLY"

# Only configure if the key exists
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Error configuring GenerativeAI: {e}") # Log configuration error
else:
    print("GenerativeAI client not configured due to missing API key.")


# --- Data Loading ---
# It's generally better to load data once at startup if possible
# Handle potential file errors gracefully
try:
    background = open('background.txt').read()
except FileNotFoundError:
    print("ERROR: background.txt not found. Background context will be missing.")
    background = "Background information is unavailable." # Provide default

try:
    # Use a relative path, assuming the file is in the /app directory
    data_df = pd.read_excel('tracking_reviews.xlsx')
    data = data_df.to_csv(index=False)
except FileNotFoundError:
    print("ERROR: tracking_reviews.xlsx not found. Data snapshot will be missing.")
    data = "Data snapshot is unavailable." # Provide default
except Exception as e:
    print(f"Error reading tracking_reviews.xlsx: {e}")
    data = f"Error loading data: {e}"


# --- Global History (Be careful with this in concurrent environments) ---
# In a real-world app serving multiple users, storing history globally like this
# will mix conversations. You'd need user sessions or another state management method.
history = []


# --- Helper Functions ---
def create_prompt_with_history(current_data, current_background, current_history, user_prompt):
    history_text = ""
    # Limit history length to avoid overly long prompts
    max_history_items = 5
    limited_history = current_history[-max_history_items:]
    for i, (q, a) in enumerate(limited_history):
        history_text += f"\nPrevious Question {i+1}: {q}\nPrevious Answer {i+1}: {a}\n"

    return (
        f"You are a professional marketing analyst.\n\n"
        f"Background Information:\n{current_background}\n\n"
        f"Data Snapshot:\n{current_data}\n\n"
        f"Conversation History (last {len(limited_history)} turns):\n{history_text}\n\n"
        f"Never ask for more data or criticize the given data.\n\n"
        f"Current Prompt: {user_prompt}\n\n"
        f"Provide your analysis:" # Added instruction
    )

def get_insights(prompt):
    # Check if API key was configured
    if not GEMINI_API_KEY:
         return "Error: Gemini API key is not configured."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        # Add basic check for response content
        if response.parts:
             return response.text
        else:
             # Handle cases where the response might be blocked or empty
             print(f"Warning: Gemini response was empty or blocked. Prompt Safety Feedback: {response.prompt_feedback}")
             return "Sorry, I couldn't generate a response for that prompt. It might have been blocked due to safety settings or resulted in empty content."

    except Exception as e:
        print(f"Error during Gemini API call: {e}") # Log the error server-side
        # Provide a more user-friendly error message
        return f"Sorry, an error occurred while generating insights. Please try again later."

# --- Flask Routes ---

@app.route('/') # <-- NEW: Route for the main page
def index():
    # This route serves the index.html file from the 'templates' folder
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    user_prompt = request.json.get('prompt')
    if not user_prompt:
        return jsonify({"error": "No prompt provided."}), 400

    # Pass the currently loaded data/background/history
    full_prompt = create_prompt_with_history(data, background, history, user_prompt)
    insights = get_insights(full_prompt)

    # Check if insights is an error message before appending
    if not insights.startswith("Error:") and not insights.startswith("Sorry,"):
        # Append to history ONLY if successful and you want to maintain context
        # Be mindful of the global history issue mentioned above for multi-user scenarios
        history.append((user_prompt, insights))
        # Optional: Limit overall history size in memory
        if len(history) > 20: # Keep last 20 turns total, for example
            history.pop(0)


    # Always return a JSON response, even for errors generated by get_insights
    if insights.startswith("Error:") or insights.startswith("Sorry,"):
         return jsonify({"error": insights}) # Return error as JSON
    else:
         return jsonify({"insights": insights})


if __name__ == "__main__":
    # Use environment variable for port, default to 8080
    port = int(os.environ.get("PORT", 8080))
    # Host 0.0.0.0 makes it accessible externally (needed for container)
    app.run(host="0.0.0.0", port=port)
