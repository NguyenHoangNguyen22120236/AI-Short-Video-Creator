import { useState, useContext } from "react";
import { Rnd } from "react-rnd";
import "../styles/StickerTab.css";
import { ThumbnailContext } from "../context/ThumbnailContext";

export default function StickerTab({
  stockStickers,
  selectedStickers,
  setSelectedStickers,
}) {

  const thumbnail = useContext(ThumbnailContext);
  console.log("Thumbnail in StickerTab:", thumbnail);

  //const [stickers, setStickers] = useState([]);
  const [selectedId, setSelectedId] = useState(null);

  const handleAddSticker = (sticker) => {
    const newSticker = {
      id: Date.now(), // unique id based on timestamp
      url: sticker.url,
      x: 50,
      y: 50,
      width: 70,
      height: 70,
    };
    setSelectedStickers([...selectedStickers, newSticker]);
  };

  const handleDeleteSticker = (id) => {
    setSelectedStickers(selectedStickers.filter((s) => s.id !== id));
    if (selectedId === id) setSelectedId(null);
  };

  const updateSticker = (id, newProps) => {
    setSelectedStickers((prev) =>
      prev.map((s) => (s.id === id ? { ...s, ...newProps } : s))
    );
  };

  return (
    <div style={{ display: "flex", padding: 16 }}>
      {/* Sticker Picker */}
      <div style={{ width: 150, paddingRight: 16 }}>
        <h3>Stickers</h3>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          {stockStickers.map((sticker) => (
            <img
              key={sticker.id}
              src={sticker.url}
              alt="sticker"
              style={{ width: 50, height: 50, cursor: "pointer" }}
              onClick={() => handleAddSticker(sticker)}
            />
          ))}
        </div>
      </div>

      {/* Video Preview */}
      <div
        style={{
          position: "relative",
          width: 360,
          height: 640,
          backgroundImage: `url(${thumbnail})`, // replace with your video frame
          backgroundSize: "cover",
          backgroundPosition: "center",
          border: "1px solid #ccc",
        }}
      >
        {selectedStickers.map((sticker) => (
          <Rnd
            key={sticker.id}
            default={{
              x: sticker.x,
              y: sticker.y,
              width: sticker.width,
              height: sticker.height,
            }}
            onDragStop={(_, d) => updateSticker(sticker.id, { x: d.x, y: d.y })}
            onResizeStop={(_, __, ref, ___, position) =>
              updateSticker(sticker.id, {
                width: parseInt(ref.style.width),
                height: parseInt(ref.style.height),
                ...position,
              })
            }
            bounds="parent"
            onClick={() => setSelectedId(sticker.id)}
            style={{ zIndex: selectedId === sticker.id ? 10 : 1 }}
          >
            <div
              style={{ position: "relative", width: "100%", height: "100%" }}
            >
              <img
                src={sticker.url}
                alt="sticker"
                style={{ width: "100%", height: "100%" }}
              />
              {selectedId === sticker.id && (
                <button
                  onClick={() => handleDeleteSticker(sticker.id)}
                  className="delete-button"
                >
                  ×
                </button>
              )}
            </div>
          </Rnd>
        ))}
      </div>
    </div>
  );
}
