import gradio as gr
from lite_deploy import transcribe_audio, predict_distress, detect_distress_once
import tempfile

def gradio_predict_audio(file_path):
    prediction, features = predict_distress(file_path)
    transcript = transcribe_audio(file_path)
    keyword_hit = any(word in transcript for word in ["help", "emergency", "save me", "please help", "danger", "call police", "stop"])
    
    output_message = ""
    
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

def gradio_record_audio(duration=5):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        file_path = f.name
    detect_distress_once(duration)
    return file_path

iface = gr.Interface(
    fn=gradio_predict_audio,
    inputs=gr.Audio(type="filepath"),
    outputs=["text", "text"],
    live=True,
    title="Distress Detection",
    description="Upload an audio file or record directly to detect distress signals from voice and keywords."
)

if __name__ == "__main__":
    iface.launch()
