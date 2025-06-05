import "../styles/Home.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowRight, faClock } from "@fortawesome/free-solid-svg-icons";
import { formatDistanceToNow, set } from "date-fns";
import { useEffect, useState, useRef } from "react";
import { Link } from "react-router-dom";
import { deleteVideo } from "../utils/deleteVideo";
import UpdateStatusModal from "./UpdateStatusModal";
import LoadingStatus from "./LoadingStatus";
import ConfirmDeleteVideoModal from "./ConfirmDeleteVideoModal";

const token =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjNAZXhhbXBsZS5jb20iLCJ1c2VyX2lkIjoyLCJleHAiOjE3NDkzMDkxNjB9.68rcsvQZwqaxQ6WEbkh28Q6AV_d99xRDHtEoZyFDi1M";

export default function Home() {
  const [videos, setVideos] = useState([]);
  const [isDeleting, setIsDeleting] = useState(false);

  const [showUpdateModal, setShowUpdateModal] = useState(false);
  const [updateMessage, setUpdateMessage] = useState("");

  const [showDeleteForId, setShowDeleteForId] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  const [videoIdToDelete, setVideoIdToDelete] = useState(null);

  console.log("video Id to delete:", videoIdToDelete);

  const dotsRefs = useRef({});

  useEffect(() => {
    const handleClickOutside = (event) => {
      // Check if click is outside all dots
      const isClickInsideAny = Object.values(dotsRefs.current).some(
        (ref) => ref && ref.contains(event.target)
      );

      if (!isClickInsideAny) {
        setShowDeleteForId(null);
      }
    };

    document.addEventListener("click", handleClickOutside, true);
    return () => {
      document.removeEventListener("click", handleClickOutside, true);
    };
  }, []);

  const handleDelete = async (videoId) => {
    setShowDeleteModal(false);
    setIsDeleting(true);

    const deleteMessage = await deleteVideo(videoId, token);
    if (deleteMessage.success) {
      setVideos(videos.filter((video) => video.id !== videoId));
    }

    setUpdateMessage(deleteMessage.message);
    setShowUpdateModal(true);
    setIsDeleting(false);
  };

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
                  <div
                    ref={
                      (dotsRefs.current[video.id] = (el) => {
                        dotsRefs.current[video.id] = el;
                      })
                    }
                    className="container-dots d-flex align-items-center px-2"
                    onClick={(e) => {
                      e.preventDefault(); // prevent Link navigation
                      e.stopPropagation(); // stop event bubbling
                      setVideoIdToDelete(video.id);
                      setShowDeleteForId(
                        showDeleteForId === video.id ? null : video.id
                      );
                    }}
                  >
                    <div className="dots">⋮</div>

                    {showDeleteForId === video.id && (
                      <div
                        className="delete-text show"
                        onClick={(e) => {
                          console.log("dots clicked for video", video.id);
                          e.preventDefault();
                          e.stopPropagation();

                          setShowDeleteModal(true);
                          setShowDeleteForId(null); // hide after delete
                        }}
                      >
                        Delete
                      </div>
                    )}
                  </div>
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

      {showDeleteModal && (
        <ConfirmDeleteVideoModal
          showDeleteModal={showDeleteModal}
          setShowDeleteModal={setShowDeleteModal}
          videoTitle={videos.find((v) => v.id === videoIdToDelete)?.topic || ""}
          onConfirmDelete={() => handleDelete(videoIdToDelete)}
          setVideoIdToDelete={setVideoIdToDelete}
        />
      )}
    </div>
  );
}
