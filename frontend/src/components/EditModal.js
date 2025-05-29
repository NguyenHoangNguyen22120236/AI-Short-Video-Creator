import "../styles/EditModal.css";
import { useState } from "react";
import TextEffectTab from "./TextEffectTab";
import MusicTab from "./MusicTab";
import StickerTab from "./StickerTab";

const textEffects = ["Fade", "Slide In", "Scale", "Typewriter"];
// https://res.cloudinary.com/dfa9owyll/video/upload/v1748337941/rt1u8omiiqhbsbrmerlz.mp3 -----> Background music soft corporate
// https://res.cloudinary.com/dfa9owyll/video/upload/v1748338050/oh2gnk6er7wwoin5excj.mp3 -----> Cinematic ambient music beautiful sunset mood
// https://res.cloudinary.com/dfa9owyll/video/upload/v1748338080/xlaoaxquy1zthenfoftg.mp3 -----> Faded memories lofi hip hop background music
// https://res.cloudinary.com/dfa9owyll/video/upload/v1748338164/htzggi0cx0pwnvzrrsam.mp3 -----> Music happy kids

const stockMusics = [
  {
    id: 1,
    title: "Background music soft corporate",
    url: "https://res.cloudinary.com/dfa9owyll/video/upload/v1748337941/rt1u8omiiqhbsbrmerlz.mp3",
  },
  {
    id: 2,
    title: "Cinematic ambient music beautiful sunset mood",
    url: "https://res.cloudinary.com/dfa9owyll/video/upload/v1748338050/oh2gnk6er7wwoin5excj.mp3",
  },
  {
    id: 3,
    title: "Faded memories lofi hip hop background music",
    url: "https://res.cloudinary.com/dfa9owyll/video/upload/v1748338080/xlaoaxquy1zthenfoftg.mp3",
  },
  {
    id: 4,
    title: "Music happy kids",
    url: "https://res.cloudinary.com/dfa9owyll/video/upload/v1748338164/htzggi0cx0pwnvzrrsam.mp3",
  },
];

const stockStickers = [
  "stickers/bear.png", 
  "stickers/bear.png"
];

export default function EditModal({
  currentData,
  onClose,
  onApplyTextEffect,
  onApplyMusic,
  onApplyStickers
}) {
  const [activeTab, setActiveTab] = useState("Text Effect");
  const [selectedEffect, setSelectedEffect] = useState(currentData.selectedEffect);
  const [currentMusic, setCurrentMusic] = useState(currentData.audioUrl);
  const [selectedStickers, setSelectedStickers] = useState(currentData.selectedStickers);

  const handleSave = () => {
    //if (activeTab === "Text Effect") {
    onApplyTextEffect(selectedEffect);
    onApplyMusic(currentMusic);
    onApplyStickers(selectedStickers);
    //}
    onClose(); // close modal
  };

  return (
    <div className="modal-overlay">
      <div className="modal-container col-lg-8 col-md-8 col-sm-10 col mx-auto h-auto">
        {/* Tabs */}
        <div className="modal-header d-flex justify-content-between align-items-center p-3">
          <ul className="modal-tabs d-flex justify-content-start align-items-center gap-4 m-0 p-0">
            <li
              className={activeTab === "Music" ? "active-tab" : ""}
              onClick={() => setActiveTab("Music")}
            >
              Music
            </li>
            <li
              className={activeTab === "Text Effect" ? "active-tab" : ""}
              onClick={() => setActiveTab("Text Effect")}
            >
              Text Effect
            </li>
            <li
              className={activeTab === "Sticker" ? "active-tab" : ""}
              onClick={() => setActiveTab("Sticker")}
            >
              Sticker
            </li>
          </ul>
          <button onClick={onClose}>✕</button>
        </div>

        {/* Body */}
        <div className="modal-body p-4">
          {activeTab === "Text Effect" && (
            <TextEffectTab
              textEffects={textEffects}
              selectedEffect={selectedEffect}
              setSelectedEffect={setSelectedEffect}
            />
          )}
          {activeTab === "Music" && (
            <MusicTab
              stockMusics={stockMusics}
              currentMusic={currentMusic}
              setCurrentMusic={setCurrentMusic}
            />
          )}
          {activeTab === "Sticker" && (
            <StickerTab 
              stockStickers={stockStickers}
              selectedStickers={selectedStickers}
              setSelectedStickers={setSelectedStickers}
            />
          )}
        </div>

        {/* Footer */}
        <div className="modal-footer p-3 d-flex justify-content-end">
          <button className="save-button" onClick={handleSave}>
            Save Change
          </button>
        </div>
      </div>
    </div>
  );
}
