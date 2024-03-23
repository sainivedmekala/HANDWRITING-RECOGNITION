from io import BytesIO
from flask import Flask, request, render_template,send_file
import pytesseract
from PIL import Image
import os
from reportlab.pdfgen import canvas

tessdata_dir_config = '--tessdata-dir "C:\Program Files\Tesseract-OCR\\tesseract.exe"'

tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/htt')
def htt():
    return render_template('htt.html')

@app.route('/tth')
def tth():
    return render_template('tth.html')


@app.route('/upload', methods=['GET', 'POST'])
def process_image():
    image_file = request.files['image']

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(image_path)

    with Image.open(image_path) as img:
        img = img.convert('L')

        text = pytesseract.image_to_string(img)

        os.remove(image_path)

        return render_template("result.html", text=text)
    
@app.route('/convert', methods=['POST'])
def convert():
  
  text = request.form['text']

  lines = text.split('\n')
    
  buffer = BytesIO()

  pdf = canvas.Canvas(buffer)

  x = 100
  y = 750
  
  for line in lines:
    pdf.drawString(x, y, line)
    y -= 20

  pdf.save()
  buffer.seek(0)
  return send_file(buffer, as_attachment=True, download_name='handwriting.pdf')

if __name__ == '__main__':
    app.run(debug=True)
