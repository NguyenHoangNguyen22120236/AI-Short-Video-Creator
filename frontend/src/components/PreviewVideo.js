import "../styles/PreviewVideo.css";
import { useEffect, useState, useRef } from "react";
import applyEffect from "../utils/applyEffect";
import EditModal from "./EditModal";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPause, faPlay } from "@fortawesome/free-solid-svg-icons";
import { useLocation } from "react-router-dom";

export default function PreviewVideo() {
  const location = useLocation();
  const passedData = location.state?.data || null;

  const [data, setData] = useState({
    id: 1,
    video:
      "https://res.cloudinary.com/dfa9owyll/video/upload/v1748754976/engtqh8xj9vi4qctfpsu.mp4",
    text_effect: null,
    music:{
      id: 1,
      title:'Funny tango dramatic music',
      url:'https://res.cloudinary.com/dfa9owyll/raw/upload/v1748671858/d7emufgt2vj3qujxpahl.mp3'
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
  });
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [selectedEffect, setSelectedEffect] = useState(data.text_effect || null);
  const [currentMusic, setCurrentMusic] = useState(data.music || null);
  const [selectedStickers, setSelectedStickers] = useState(data.stickers || []);


  console.log('selectedEffect:', selectedEffect);
  console.log('currentMusic:', currentMusic.title);
  console.log('selectedStickers:', selectedStickers);

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
        />
      )}
    </div>
  );
}
