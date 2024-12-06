from flask import Flask, Response, send_file, render_template
from picamera2 import Picamera2, Preview
from io import BytesIO
import cv2

app = Flask(__name__)

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

@app.route('/')
def index():
    """Serve the HTML page."""
    return render_template('index.html')  # Map to the HTML file

@app.route('/video_feed')
def video_feed():
    """Stream the live video feed from the camera."""
    def generate():
        while True:
            frame = picam2.capture_array()
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture_image')
def capture_image():
    """Capture an image from the camera."""
    frame = picam2.capture_array()
    _, buffer = cv2.imencode('.jpg', frame)
    image_io = BytesIO(buffer)
    return send_file(image_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
