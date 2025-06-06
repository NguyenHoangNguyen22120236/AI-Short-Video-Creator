import { useEffect, useState } from "react";
import ConfirmDeleteVideoModal from "./ConfirmDeleteVideoModal";
import { deleteVideo } from "../utils/deleteVideo";
import "../styles/DotsSetting.css";

const token =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjNAZXhhbXBsZS5jb20iLCJ1c2VyX2lkIjoyLCJleHAiOjE3NDkzMDkxNjB9.68rcsvQZwqaxQ6WEbkh28Q6AV_d99xRDHtEoZyFDi1M";

export default function DotsSetting({
  videoId,
  dotsRefs,
  videos,
  setVideos,
  setUpdateMessage,
  setShowUpdateModal,
  setIsDeleting,
  videoTitle,
}) {
  const [showDeleteForId, setShowDeleteForId] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [videoIdToDelete, setVideoIdToDelete] = useState(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      const isClickInsideAny = Object.values(dotsRefs.current).some(
        (ref) => ref instanceof HTMLElement && ref.contains(event.target)
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
    /*const deleteMessage = {
      success: true,
      message: "Video deleted successfully",
    }; // Mocked response for testing*/
    if (deleteMessage.success) {
      if (Array.isArray(videos)) {
        setVideos(videos.filter((video) => video.id !== videoId));
      } else if (typeof videos === "object" && videos !== null) {
        const newVideos = Object.fromEntries(
          Object.entries(videos).map(([date, videoList]) => [
            date,
            videoList.filter((video) => video.id !== videoId),
          ])
        );

        // Filter out the dates with no videos left
        const filteredVideos = Object.fromEntries(
          Object.entries(newVideos).filter(
            ([date, videoList]) => videoList.length > 0
          )
        );

        setVideos(filteredVideos);
      } else {
        console.warn("Unexpected type for 'videos':", typeof videos);
      }
    }

    setUpdateMessage(deleteMessage.message);
    setShowUpdateModal(true);
    setIsDeleting(false);
  };

  return (
    <div
      ref={
        (dotsRefs.current[videoId] = (el) => {
          dotsRefs.current[videoId] = el;
        })
      }
      className="container-dots d-flex align-items-center px-2"
      onClick={(e) => {
        e.preventDefault(); // prevent Link navigation
        e.stopPropagation(); // stop event bubbling
        setVideoIdToDelete(videoId);
        setShowDeleteForId(showDeleteForId === videoId ? null : videoId);
      }}
    >
      <div className="dots">⋮</div>

      {showDeleteForId === videoId && (
        <div
          className="delete-text show"
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();

            setShowDeleteModal(true);
            setShowDeleteForId(null); // hide after delete
          }}
        >
          Delete
        </div>
      )}

      {showDeleteModal && (
        <ConfirmDeleteVideoModal
          showDeleteModal={showDeleteModal}
          setShowDeleteModal={setShowDeleteModal}
          videoTitle={videoTitle}
          onConfirmDelete={() => handleDelete(videoIdToDelete)}
          setVideoIdToDelete={setVideoIdToDelete}
        />
      )}
    </div>
  );
}
