import '../styles/EditModal.css';
import React, { useState } from 'react';
import TextEffect from './TextEffect';

const textEffects = ['Fade', 'Slide In', 'Scale', 'Typewriter'];

export default function EditModal({ onClose, onApplyTextEffect }) {
  const [activeTab, setActiveTab] = useState("Text Effect");
  const [selectedEffect, setSelectedEffect] = useState("Fade");

  const handleSave = () => {
    if (activeTab === "Text Effect") {
      onApplyTextEffect(selectedEffect);
    }
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
             <TextEffect
                textEffects={textEffects}
                selectedEffect={selectedEffect}
                setSelectedEffect={setSelectedEffect} />
          )}
        </div>

        {/* Footer */}
        <div className="modal-footer p-3 d-flex justify-content-end">
          <button className="save-button" onClick={handleSave}>Save Change</button>
        </div>
      </div>
    </div>
  );
}