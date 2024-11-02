from flask import Flask, render_template, request, send_file
import barcode
from barcode.writer import ImageWriter
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        barcode_value = request.form['barcode_value']
        barcode_type = 'code128'
        
        # Generar el código de barras
        bar = barcode.get(barcode_type, barcode_value, writer=ImageWriter())
        file_obj = BytesIO()
        bar.write(file_obj)
        
        # Retrocede el puntero al inicio del archivo para que se lea desde el comienzo
        file_obj.seek(0)
        
        return send_file(
            file_obj,
            mimetype='image/png',
            as_attachment=True,
            download_name=f'{barcode_value}.png'  # Cambiado a download_name
        )
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
