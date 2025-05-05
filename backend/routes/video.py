from flask import Blueprint
from controllers.video import VideoController

video_routes = Blueprint('video', __name__)

video_controller = VideoController()
video_routes.route('/create_video', methods=['GET'])(video_controller.create_video)