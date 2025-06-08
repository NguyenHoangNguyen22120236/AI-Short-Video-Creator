import "../styles/EditModal.css";
import { useState } from "react";
import TextEffectTab from "./TextEffectTab";
import MusicTab from "./MusicTab";
import StickerTab from "./StickerTab";
import { textEffects, stockMusics, stockStickers } from "../data/mockData";
import ConfirmUpdateVideoModal from "./ConfirmUpdateVideoModal";


export default function EditModal({
  currentData,
  onClose,
  onApplyTextEffect,
  onApplyMusic,
  onApplyStickers,
  onUpdateData,
}) {
  const [activeTab, setActiveTab] = useState("Text Effect");
  const [selectedEffect, setSelectedEffect] = useState(
    currentData.selectedEffect
  );
  const [currentMusic, setCurrentMusic] = useState(currentData.currentMusic);
  const [selectedStickers, setSelectedStickers] = useState(
    currentData.selectedStickers
  );

  const [showConfirmModal, setShowConfirmModal] = useState(false);

  const hasChanged = () => {
    console.log(selectedEffect);
    console.log(currentData.selectedEffect);
    return (
      selectedEffect !== currentData.selectedEffect ||
      currentMusic !== currentData.currentMusic ||
      JSON.stringify(selectedStickers) !==
        JSON.stringify(currentData.selectedStickers)
    );
  };

  const handleSave = () => {
    if (hasChanged()) {
      setShowConfirmModal(true); // ask for confirmation
    }else{
      onClose(); // close modal without changes
    }
  };

  const applyChanges = () => {
    onApplyTextEffect(selectedEffect);
    onApplyMusic(currentMusic);
    onApplyStickers(selectedStickers);
    onUpdateData(selectedEffect, currentMusic, selectedStickers);
    onClose();
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

      {showConfirmModal && (
        <ConfirmUpdateVideoModal 
          showUpdateModal={showConfirmModal}
          setShowUpdateModal={setShowConfirmModal}
          videoTitle={currentData.topic}
          onConfirmUpdate={applyChanges}
        />
      )}
    </div>
  );
}
