import "../styles/EditModal.css";
import { useState } from "react";
import TextEffectTab from "./TextEffectTab";
import MusicTab from "./MusicTab";
import StickerTab from "./StickerTab";

const textEffects = ["Fade", "Slide In", "Scale", "Typewriter"];

const stockMusics = [
  {
    id: 1,
    title: "Funny tango dramatic music",
    url: "https://res.cloudinary.com/dfa9owyll/raw/upload/v1748671858/d7emufgt2vj3qujxpahl.mp3",
  },
  {
    id: 2,
    title: "Moon dance background dramatic hip hop music",
    url: "https://res.cloudinary.com/dfa9owyll/raw/upload/v1748671860/im4ebjxdmebgokj47vc2.mp3",
  },
  {
    id: 3,
    title: "Shopping day",
    url: "https://res.cloudinary.com/dfa9owyll/raw/upload/v1748671862/gpixnuvp3pyntzptedbt.mp3",
  },
  {
    id: 4,
    title: "Beautiful",
    url: "https://res.cloudinary.com/dfa9owyll/raw/upload/v1748671864/esxogdylyk4qhhm3lbc5.mp3",
  },
];

const stockStickers = [
  {
    id: 1,
    url: "https://res.cloudinary.com/dfa9owyll/image/upload/v1748673384/qf8ylj8gpharbdurvcc8.png",
  },
  {
    id: 2,
    url: "https://res.cloudinary.com/dfa9owyll/image/upload/v1748673385/jldqihwdmre62kyc1ook.png",
  }
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
  const [currentMusic, setCurrentMusic] = useState(currentData.currentMusic);
  const [selectedStickers, setSelectedStickers] = useState(currentData.selectedStickers);

  const handleSave = () => {
    onApplyTextEffect(selectedEffect);
    onApplyMusic(currentMusic);
    onApplyStickers(selectedStickers);
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
