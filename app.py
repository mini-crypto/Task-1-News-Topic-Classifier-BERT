import gradio as gr
import torch

from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load model
model_path = "saved_model"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

model.eval()

# Labels
id2label = {
    0: "World",
    1: "Sports",
    2: "Business",
    3: "Sci/Tech"
}

# Prediction function
def classify_news(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

    prediction = torch.argmax(outputs.logits, dim=1).item()

    return id2label[prediction]


# Create Gradio Interface
interface = gr.Interface(
    fn=classify_news,

    inputs=gr.Textbox(
        lines=3,
        placeholder="Enter a news headline..."
    ),

    outputs=gr.Textbox(label="Predicted Category"),

    title="News Topic Classifier Using BERT",

    description="Predict whether a news headline belongs to World, Sports, Business or Sci/Tech."
)

# Launch App
interface.launch()