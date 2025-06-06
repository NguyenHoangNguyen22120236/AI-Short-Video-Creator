import "../styles/PreviewVideo.css";
import { useEffect, useState, useRef } from "react";
import EditModal from "./EditModal";
import { useLocation, useParams } from "react-router-dom";
import UpdateStatusModal from "./UpdateStatusModal";
import LoadingStatus from "./LoadingStatus";
import { ThumbnailContext } from "../context/ThumbnailContext";

const token =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjNAZXhhbXBsZS5jb20iLCJ1c2VyX2lkIjoyLCJleHAiOjE3NDkzMDkxNjB9.68rcsvQZwqaxQ6WEbkh28Q6AV_d99xRDHtEoZyFDi1M";

export default function PreviewVideo() {
  const videoRef = useRef(null);
  const location = useLocation();
  const { id } = useParams();
  const passedData = location.state?.data || null;

  const [data, setData] = useState(null);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [selectedEffect, setSelectedEffect] = useState(null);
  const [currentMusic, setCurrentMusic] = useState(null);
  const [selectedStickers, setSelectedStickers] = useState([]);
  const [isUpdating, setIsUpdating] = useState(false);

  const [showUpdateModal, setShowUpdateModal] = useState(false);
  const [updateMessage, setUpdateMessage] = useState("");

  // Fetch from backend if no passedData
  useEffect(() => {
    if (passedData) {
      setData(passedData);
      setSelectedEffect(passedData.text_effect || null);
      setCurrentMusic(passedData.music || null);
      setSelectedStickers(passedData.stickers || []);
    } else if (id) {
      const fetchVideo = async () => {
        try {
          const response = await fetch(
            `http://127.0.0.1:8000/api/video/get_video/${id}`,
            {
              method: "GET",
              headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
              },
            }
          );

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }

          const videoData = await response.json();
          setData(videoData);
          setSelectedEffect(videoData.text_effect || null);
          setCurrentMusic(videoData.music || null);
          setSelectedStickers(videoData.stickers || []);
        } catch (error) {
          console.error("Failed to fetch video data:", error);
        }
      };

      fetchVideo();
    }
  }, [passedData, id]);

  useEffect(() => {
    if (isEditOpen && videoRef.current) {
      videoRef.current.pause();
    }
  }, [isEditOpen]);

  const handleUpdateData = async (
    selectedEffect,
    currentMusic,
    selectedStickers
  ) => {
    setIsUpdating(true);

    const newData = {
      text_effect: selectedEffect,
      music: currentMusic,
      stickers: selectedStickers,
    };

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/video/update_video/${id}`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(newData),
        }
      );

      if (!response.ok) {
        throw new Error(`Update failed with status ${response.status}`);
      }

      const videoData = await response.json();
      setData(videoData);
      setSelectedEffect(videoData.text_effect || null);
      setCurrentMusic(videoData.music || null);
      setSelectedStickers(videoData.stickers || []);

      setUpdateMessage("Video updated successfully!");
      setShowUpdateModal(true);
    } catch (error) {
      setUpdateMessage(
        "Failed to update video. Please Try Again.\n" +
          "Error: " +
          error.message
      );
      setShowUpdateModal(true);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleApplyTextEffect = (effect) => {
    setSelectedEffect(effect);
  };

  const handleApplyMusic = (music) => {
    setCurrentMusic({ ...music });
  };

  const handleApplyStickers = (stickers) => {
    setSelectedStickers(stickers);
  };

  const handleOpenEditModal = () => {
    setIsEditOpen(true);
  };

  const handleDownloadVideo = async () => {
    try {
      const videoUrl = videoRef.current?.currentSrc || videoRef.current?.src;
      if (!videoUrl) {
        console.error("Video source not found");
        return;
      }

      const response = await fetch(videoUrl, { mode: "cors" });
      const blob = await response.blob();
      const blobUrl = URL.createObjectURL(blob);

      const fileName = `${sanitizeFileName(data.topic)}-video.mp4`;
      const link = document.createElement("a");
      link.href = blobUrl;
      link.download = fileName;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(blobUrl);
    } catch (error) {
      console.error("Download failed:", error);
    }
  };

  const sanitizeFileName = (name) => name.replace(/[\\/:*?"<>|]/g, "");

  return (
    <div className="d-flex flex-column align-items-center justify-content-center text-white py-5">
      <div className="video-container">
        <video
          ref={videoRef}
          src={data?.video}
          controls
          width={360}
          height={640}
          style={{ background: "#000" }}
        />
      </div>

      <div className="video-info">
        <button className="btn fs-5" onClick={handleOpenEditModal}>
          Edit
        </button>
        <button className="btn btn-primary" onClick={handleDownloadVideo}>
          Download
        </button>
      </div>

      {currentMusic && (
        <audio
          src={currentMusic.url}
          style={{ display: "none" }}
          preload="auto"
        />
      )}

      {isUpdating && <LoadingStatus message="Updating" />}

      {isEditOpen && (
        <ThumbnailContext.Provider value={data.thumbnail}>
          <EditModal
            currentData={{
              selectedEffect,
              currentMusic,
              selectedStickers,
            }}
            onClose={() => setIsEditOpen(false)}
            onApplyTextEffect={handleApplyTextEffect}
            onApplyMusic={handleApplyMusic}
            onApplyStickers={handleApplyStickers}
            onUpdateData={handleUpdateData}
          />
        </ThumbnailContext.Provider>
      )}

      <UpdateStatusModal
        showUpdateModal={showUpdateModal}
        setShowUpdateModal={setShowUpdateModal}
        updateMessage={updateMessage}
      />
    </div>
  );
}
