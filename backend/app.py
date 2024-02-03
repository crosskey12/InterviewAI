from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import fitz  # PyMuPDF
import pytesseract

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'InterviewAI/backend/uploads'
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

        return jsonify({'message': 'File uploaded and processed successfully', 'pdf_content': pdf_content})

    return jsonify({'error': 'Invalid file format'})

if __name__ == '__main__':
    app.run(debug=True)
