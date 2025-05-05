from flask import Flask
from routes.video import video_routes

app = Flask(__name__)
app.register_blueprint(video_routes, url_prefix='/api/video')

if __name__ == '__main__':
    app.run(debug=True)