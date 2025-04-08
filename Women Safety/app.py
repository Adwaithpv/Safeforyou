# Import required libraries
import gradio as gr
from lite_deploy import transcribe_audio, predict_distress, detect_distress_once
import tempfile

# Function to process uploaded audio and predict distress
def gradio_predict_audio(file_path):
    """
    Given an audio file path, this function:
    1. Predicts distress using a trained model (via `predict_distress`).
    2. Transcribes speech using `transcribe_audio`.
    3. Checks for specific distress-related keywords in the transcript.
    4. Combines both sources (ML + keywords) to decide the final alert message.
    
    Returns:
        A tuple of (result_message, transcript_text).
    """
    prediction, features = predict_distress(file_path)
    transcript = transcribe_audio(file_path)

    # List of distress keywords to check in transcript
    keyword_hit = any(word in transcript.lower() for word in [
        "help", "emergency", "save me", "please help", "danger", "call police", "stop"
    ])
    
    output_message = ""
    
    # Define output based on model prediction and keyword detection
    if prediction is not None:
        if prediction > 0.6 and keyword_hit:
            output_message = "HIGH ALERT: Distress detected via voice + keywords."
        elif prediction > 0.6:
            output_message = "Voice distress detected."
        elif keyword_hit:
            output_message = "Keyword-based distress detected."
        else:
            output_message = "No distress detected."
    else:
        output_message = "Prediction failed."

    return output_message, transcript

# Optional: function to trigger audio recording (if needed later)
def gradio_record_audio(duration=5):
    """
    Records live audio for a specified duration (in seconds)
    and saves it temporarily as a WAV file.

    Returns:
        Path to the recorded WAV file.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        file_path = f.name
    detect_distress_once(duration)
    return file_path

# Gradio interface setup
iface = gr.Interface(
    fn=gradio_predict_audio,                   # Function called on input
    inputs=gr.Audio(type="filepath"),          # Accept uploaded audio file
    outputs=["text", "text"],                  # Display prediction result and transcript
    live=True,
    title="🎙️ Distress Detection",
    description="Upload or record an audio file to detect distress using voice emotion analysis and keyword spotting."
)

# Run the Gradio app
if __name__ == "__main__":
    iface.launch()
