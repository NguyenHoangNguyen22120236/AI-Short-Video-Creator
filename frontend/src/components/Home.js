import "../styles/Home.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowRight, faClock } from "@fortawesome/free-solid-svg-icons";
import { formatDistanceToNow} from "date-fns";
import { useEffect, useState, useRef } from "react";
import { Link } from "react-router-dom";
import UpdateStatusModal from "./UpdateStatusModal";
import LoadingStatus from "./LoadingStatus";
import DotsSetting from "./DotsSetting";

const token =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjNAZXhhbXBsZS5jb20iLCJ1c2VyX2lkIjoyLCJleHAiOjE3NDkzMDkxNjB9.68rcsvQZwqaxQ6WEbkh28Q6AV_d99xRDHtEoZyFDi1M";

export default function Home() {
  const [videos, setVideos] = useState([]);
  const [isDeleting, setIsDeleting] = useState(false);

  const [showUpdateModal, setShowUpdateModal] = useState(false);
  const [updateMessage, setUpdateMessage] = useState("");

  const dotsRefs = useRef({});

  useEffect(() => {
    const fetchVideos = async () => {
      try {
        //const token = localStorage.getItem("token"); // or get it from context
        const response = await fetch(
          `http://127.0.0.1:8000/api/video/get_videos_history/${3}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        setVideos(data);
      } catch (error) {
        console.error("Error fetching history:", error);
      }
    };

    fetchVideos();
  }, []);

  return (
    <div className="container p-1">
      <div className="row p-3">
        <div>
          <Link to="/create-video" className="create-button col-lg-4 col-md-6 col-sm-10 col-10 d-flex justify-content-between align-items-center text-decoration-none">
            <div className=" d-flex flex-column justify-content-around align-items-center">
              <span className="main-text">Create AI Video</span>
              <span className="extra-text">Start from scratch</span>
            </div>
            <FontAwesomeIcon className="text-white" icon={faArrowRight} />
          </Link>
        </div>
      </div>
      <div className="row p-3">
        <div className="d-flex justify-content-start align-items-center gap-3 p-0">
          <h2 className="main-text">History</h2>
          <a href="/history-see-all" className="see-all">
            See all
          </a>
        </div>
        <div className="d-flex flex-wrap justify-content-center align-items-center p-0">
          {videos.map((video) => (
            <div
              className="col-lg-4 col-md-6 col-sm-6 col-8 p-lg-5 p-md-3 p-sm-3 p-2"
              key={video.id}
            >
              <Link
                to={`/preview-video/${video.id}`}
                className="card text-decoration-none"
              >
                <img
                  src={video.thumbnail}
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
                  
                  <DotsSetting 
                    videoId={video.id}
                    dotsRefs={dotsRefs}
                    videos={videos}
                    setVideos={setVideos}
                    setShowUpdateModal={setShowUpdateModal}
                    setUpdateMessage={setUpdateMessage}
                    setIsDeleting={setIsDeleting}
                    videoTitle={video.topic}
                  />
                </div>
              </Link>
            </div>
          ))}
        </div>
      </div>

      {isDeleting && <LoadingStatus message="Deleting" />}

      <UpdateStatusModal
        showUpdateModal={showUpdateModal}
        setShowUpdateModal={setShowUpdateModal}
        updateMessage={updateMessage}
      />
    </div>
  );
}
