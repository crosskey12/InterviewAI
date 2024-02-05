from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import fitz  # PyMuPDF
from gradio_client import Client
# Set the upload folder and allowed extensions
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ocr_pdf(filepath):
    doc = fitz.open(filepath)
    text = ''
    for i in range(doc.page_count):
        page = doc[i]
        text += f'Page {i + 1}:\n{page.get_text()}\n\n'
    return text

def generate_prompt(pdf_content):
    # Customize your prompt here, using the extracted PDF content
    return f"i will give you ocr of a resume.Give me 25 probable interview questions for role of Machine Learning engineer personalized for the resume.Ocr:{pdf_content}"

def query_huggingface(prompt, model, tokenizer):
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(input_ids, max_length=1200, num_return_sequences=1, no_repeat_ngram_size=2)
    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
    return decoded_output
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        # Create the 'uploads' directory if it doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Perform OCR on the uploaded PDF
    pdf_content = ocr_pdf(filepath)

        # Generate prompt
    prompt = generate_prompt(pdf_content)

        # Load Hugging Face model and tokenizer
    client = Client("https://stabilityai-stablelm-2-1-6b-zephyr.hf.space/--replicas/lb85n/")
    result = client.predict(
		    prompt,	# str  in 'Message' Textbox component
		    api_name="/chat"
    )

    return jsonify({'message': 'File uploaded, processed, and response obtained',
                        'model_output': result})

if __name__ == '__main__':
    app.run(debug=True)