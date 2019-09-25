import cv2, numpy as np, math as mth

from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from config import DevConfig


app = Flask(__name__, static_url_path='')
app.config.from_object(DevConfig)

image = 'images/1.tif'

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory('images', path)

@app.route('/')
def home():
    return '<h1>Hello World!</h1>'

@app.route('/upload')
def upload():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      f = request.files['file']
    #   f.save(secure_filename(f.filename))
      f.save(image)
      return 'file uploaded successfully'

@app.route('/read_img')
def read_img():
    img = cv2.imread(image)
    imgpng = 'images/1.png'
    cv2.imwrite(imgpng, img)

    print('original image shape:', img.shape)
    # print('img[0]', img[0])

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print('Converted to grayscale')
    print('Shape:', gray.shape)
    print('Data type:', gray.dtype)

    return '<img src="/' + imgpng + '"/>'

@app.route('/reverse')
def reverse():
    img = cv2.imread(image)
    imgpng = 'images/1.png'

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    w, h = gray.shape[1], gray.shape[0]

    nu = np.full(img.shape, 255, np.uint8)
    nugray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    nupng = 'images/1_nu.png'

    for iw in range(w):
        for ih in range(h):
            nugray[ih-1][iw-1] = gray[h-ih-1][w-iw-1]
            # print(ih, iw, gray[ih][iw])

    cv2.imwrite(imgpng, img)
    cv2.imwrite(nupng, nugray)
    return '<img src="/' + imgpng + '"/><img src="/' + nupng + '"/>'

@app.route('/intensity')
def intensity():
    img = cv2.imread(image)
    img = img.astype(np.float32) / 255
    imgpng = 'images/1.png'

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    w, h = gray.shape[1], gray.shape[0]

    nu = np.full(img.shape, 255, np.float32)
    nugray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    nupng = 'images/1_nu.png'

    for iw in range(w):
        for ih in range(h):
            if( gray[ih-1][iw-1] > 0 ):
                nugray[ih-1][iw-1] = mth.log( gray[ih-1][iw-1] )
            else:
                nugray[ih-1][iw-1] = 0
            # print(ih, iw, gray[ih][iw])

    img = (img * 255).astype(np.uint8)
    nugray = (nugray * 255).astype(np.uint8)
    cv2.imwrite(imgpng, img)
    cv2.imwrite(nupng, nugray)
    return '<img src="/' + imgpng + '"/><img src="/' + nupng + '"/>'

@app.route('/avg')
def average():
    img = cv2.imread(image)
    imgpng = 'images/1.png'

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    w, h = gray.shape[1], gray.shape[0]

    nugray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    nupng = 'images/1_nu.png'

    for iw in range(2,w-2):
        for ih in range(2,h-2):
            nugray[ih-1][iw-1] = avg(gray, ih-1,iw-1)

    cv2.imwrite(imgpng, img)
    cv2.imwrite(nupng, nugray)
    return '<img src="/' + imgpng + '"/><img src="/' + nupng + '"/>'

@app.route('/convolution')
def convolution():
    img = cv2.imread(image)
    imgpng = 'images/1.png'

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    w, h = gray.shape[1], gray.shape[0]

    nugray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    nupng = 'images/1_nu.png'

    for iw in range(2,w-2):
        for ih in range(2,h-2):
            nugray[ih-1][iw-1] = gray[ih-1][iw-1]

    cv2.imwrite(imgpng, img)
    cv2.imwrite(nupng, nugray)
    return '<img src="/' + imgpng + '"/><img src="/' + nupng + '"/>'

# @app.route('/read_img')
# def read_img():
#     img = cv2.imread(image)
#     print('original image shape:', img.shape)
#     return '<h1>readimg</h1>'

def avg(mtrx, h, w):
    return np.mean([
        mtrx[h-1][w-1], mtrx[h-1][w], mtrx[h-1][w+1], 
        mtrx[h][w-1], mtrx[h][w], mtrx[h][w+1],
        mtrx[h+1][w-1], mtrx[h+1][w], mtrx[h+1][w+1] ])


if __name__ == '__main__':
    app.run()