import "../styles/Home.css";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowRight, faClock } from "@fortawesome/free-solid-svg-icons";
import { formatDistanceToNow } from "date-fns";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    const fetchVideos = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/video/get_videos_history"
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        setVideos(data.videos);
      } catch (error) {
        console.error("Error fetching history:", error);
      }
    };
    fetchVideos();
  }, []);

  const handleCreateClick = () => {
    navigate("/create"); // Navigate to the AI video creation page
  };

  return (
    <div className="container p-1">
      <div className="row p-3">
        <Link to="/create-video" className="text-decoration-none">
          <div className="create-button col-lg-4 col-md-6 col-sm-10 col-10 d-flex justify-content-between align-items-center">
            <div className=" d-flex flex-column justify-content-around align-items-center">
              <span className="main-text">Create AI Video</span>
              <span className="extra-text">Start from scratch</span>
            </div>
            <FontAwesomeIcon className="text-white" icon={faArrowRight} />
          </div>
        </Link>
      </div>
      <div className="row p-3">
        <div className="d-flex justify-content-start align-items-center gap-3 p-0">
          <h2 className="main-text">History</h2>
          <a href="/history-see-all" className="see-all">
            See all
          </a>
        </div>
        <div className="d-flex flex-wrap justify-content-between align-items-center p-0">
          {videos.map((video) => (
            <div
              className="col-lg-4 col-md-6 col-sm-6 col-6 p-lg-5 p-md-3 p-sm-3 p-2"
              key={video.video_id}
            >
              <div className="card">
                <img
                  src={video.thumbnail_url}
                  alt={video.topic}
                  className="thumbnail"
                />
                <div className="d-flex justify-content-between align-items-center p-3">
                  <div>
                    <div className="d-flex gap-3 align-items-center fs-5">
                      <FontAwesomeIcon icon={faClock} />
                      <h4>{video.topic}</h4>
                    </div>
                    <h5>
                      {formatDistanceToNow(new Date(video.created_at), {
                        addSuffix: true,
                      })}
                    </h5>
                  </div>
                  <div className="dots">⋮</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
