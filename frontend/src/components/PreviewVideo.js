import "../styles/PreviewVideo.css";
import { useEffect, useState, useRef } from "react";
import EditModal from "./EditModal";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPause, faPlay } from "@fortawesome/free-solid-svg-icons";
import { useLocation, useParams } from "react-router-dom";
const token =
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjNAZXhhbXBsZS5jb20iLCJ1c2VyX2lkIjoyLCJleHAiOjE3NDkxMzQ1OTh9.qWNxqwpozM-xds2ClF4bE27-v1y4WzEXmDMpbQY61hA";
const data = {
  id: 1,
  video:
    "https://res.cloudinary.com/dfa9owyll/video/upload/v1748754976/engtqh8xj9vi4qctfpsu.mp4",
  text_effect: null,
  music: {
    id: 1,
    title: "Funny tango dramatic music",
    url: "https://res.cloudinary.com/dfa9owyll/raw/upload/v1748671858/d7emufgt2vj3qujxpahl.mp3",
  },
  stickers: [
    {
      id: 1,
      url: "https://res.cloudinary.com/dfa9owyll/image/upload/v1748673384/qf8ylj8gpharbdurvcc8.png",
      x: 100,
      y: 50,
      width: 64,
      height: 64,
    },
    {
      id: 2,
      url: "https://res.cloudinary.com/dfa9owyll/image/upload/v1748673385/jldqihwdmre62kyc1ook.png",
      x: 300,
      y: 150,
      width: 48,
      height: 48,
    },
  ],
};

export default function PreviewVideo() {
  const location = useLocation();
  const { id } = useParams();
  const passedData = location.state?.data || null;

  const [data, setData] = useState(null);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [selectedEffect, setSelectedEffect] = useState(null);
  const [currentMusic, setCurrentMusic] = useState(null);
  const [selectedStickers, setSelectedStickers] = useState([]);

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

  if (!data) {
    return <h1 className="text-white">Loading...</h1>;
  }

  const handleUpdateData = async () => {
    console.log("Updating data");
    const newData = {
      text_effect: selectedEffect,
      music: currentMusic,
      stickers: selectedStickers,
    };

    try {
      /*const response = await fetch(
        `http://127.0.0.1:8000/api/video/update_video/${data.id}`,
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
      setSelectedStickers(videoData.stickers || []);*/

      alert("Video updated successfully!");
    } catch (error) {
      console.error("Error updating video:", error);
    }
  };

  console.log("selectedEffect:", selectedEffect);
  console.log("currentMusic:", currentMusic.title);
  console.log("selectedStickers:", selectedStickers);

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

  return (
    <div className="d-flex flex-column align-items-center justify-content-center text-white">
      <div className="video-container">
        <video
          src={data?.video}
          controls
          width={360}
          height={640}
          style={{ background: "#000" }}
        />
      </div>

      <button className="edit-button p2" onClick={handleOpenEditModal}>
        Edit
      </button>

      {currentMusic && (
        <audio
          src={currentMusic.url}
          style={{ display: "none" }}
          preload="auto"
        />
      )}

      {isEditOpen && (
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
      )}
    </div>
  );
}
