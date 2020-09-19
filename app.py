import uuid
import json
import os
import cv2
import base64
import numpy as np
from flask import render_template, jsonify, request
from flask import Flask
import numpy as np
from PIL import Image
from inpaint import predict as region_wise
from generative_inpainting import predict as generative
from pluralistic import predict as plural

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["CACHE_TYPE"] = "null"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index_all():
    return render_template('index.html')


def resize(path, size=(256, 256)):
    img = Image.open(path)
    img = img.resize(size, Image.ANTIALIAS)
    img.save(path)


@app.route('/process', methods=["POST"])
def process():
    try:
        filename = str(uuid.uuid4())
        file_path_raw = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.png')
        file_path_mask = os.path.join(app.config['UPLOAD_FOLDER'], 'mask_' + filename + '.png')
        file_path_output_1 = os.path.join(app.config['UPLOAD_FOLDER'], 'output_1_' + filename + '.png')
        file_path_output_2 = os.path.join(app.config['UPLOAD_FOLDER'], 'output_2_' + filename + '.png')

        # decode and save mask
        mask_b64 = request.values[('mask_b64')]
        imgstr = mask_b64.split(',')[1]
        output = open(file_path_mask, 'wb')
        decoded = base64.b64decode(imgstr)
        output.write(decoded)
        output.close()
        resize(file_path_mask)

        # save raw image
        file_raw = request.files.get('input_file')
        file_raw.save(file_path_raw)
        resize(file_path_raw)

        # Region Wise
        output = region_wise.run_fill(file_path_raw, file_path_mask)
        cv2.imwrite(file_path_output_1, output)
        resize(file_path_output_1, size=(384, 384))

        # Generative Wise
        output2 = generative.run_fill(file_path_raw, file_path_mask)
        cv2.imwrite(file_path_output_2, output2)
        resize(file_path_output_2, size=(384, 384))

        # Pluralistic
        output3 = plural.run_fill(file_path_raw, file_path_mask, UPLOAD_FOLDER)
        for r in output3:
            resize(r, size=(384, 384))

        return jsonify(
            {
                'output_image_1': os.path.join('static', 'uploads', os.path.basename(file_path_output_1)),
                'output_image_2': os.path.join('static', 'uploads', os.path.basename(file_path_output_2)),
                'output_image_3': output3
            }
        )
    except Exception as error:
        print(error)
        return jsonify({'status': 'error'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000, use_reloader=True, threaded=False)
