from flask import Flask, render_template, request, redirect, url_for, Response
import os
from ultralytics import YOLO
import cv2
from alert import Alert

app = Flask(__name__)

# Load the YOLO model
model = YOLO("models/best.pt")

# Folder to save uploaded video
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed video extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        video_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(video_path)
        
        # Start streaming the processed video
        return redirect(url_for('video_feed', filename=file.filename))
    
    return 'Invalid file type. Please upload a .mp4, .avi, or .mov file.'

@app.route('/video_feed/<filename>')
def video_feed(filename):
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    return Response(run_inference(video_path), mimetype='multipart/x-mixed-replace; boundary=frame')

def run_inference(input_video_path):
    # Initialize OpenCV for video processing
    cap = cv2.VideoCapture(input_video_path)

    # Flag to ensure the alert is only sent once per video
    alert_sent = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run inference on the current frame
        results = model.predict(frame)

        # Process the results and annotate the frame
        annotated_frame = results[0].plot()

        # Check if an object (e.g., a pothole) is detected and send alert only once
        if len(results[0].boxes) > 0 and not alert_sent:  # Only send the alert once
            Alert()  # Send the alert when an object is detected
            alert_sent = True  # Set flag to True to prevent further alerts

        # Convert the frame to JPEG format for streaming
        _, jpeg = cv2.imencode('.jpg', annotated_frame)
        if jpeg is not None:
            # Yield the JPEG image as a part of a multipart stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    cap.release()

if __name__ == '__main__':
    app.run(debug=True)