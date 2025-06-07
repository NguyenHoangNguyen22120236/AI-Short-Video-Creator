import { useState } from "react";
import "../styles/MusicTab.css";
import MusicCard from "./MusicCard";

export default function MusicTab({
  stockMusics,
  currentMusic,
  setCurrentMusic,
}) {
  const [playingStockMusicId, setPlayingStockMusicId] = useState(null);
  const [playingCurrentMusicId, setPlayingCurrentMusicId] = useState(null);

  const handlePlayStockMusicToggle = (music) => {
    if (playingStockMusicId === music.id) {
      // Pause if the same music is already playing
      setPlayingStockMusicId(null);
    } else {
      // Switch to new track
      setPlayingStockMusicId(music.id);
    }
  };

  const handlePlayCurrentMusicToggle = () => {
    if (playingCurrentMusicId === currentMusic?.id) {
      // Pause if the same music is already playing
      setPlayingCurrentMusicId(null);
    } else {
      // Switch to new track
      setPlayingCurrentMusicId(currentMusic?.id);
    }
  };
  return (
    <div className="music-tab-content d-flex flex-column gap-3">
      <div className="section current-music pb-1 px-3 d-flex flex-column gap-3">
        <div className="section-title">Current Music info:</div>
        {currentMusic ? (
          <MusicCard
            music={currentMusic}
            isPlaying={playingCurrentMusicId === currentMusic.id}
            onPlayToggle={handlePlayCurrentMusicToggle}
            handleReplaceMusic={null}
            handleDeleteCurrentMusic={() => setCurrentMusic(null)}
          />
        ) : (
          <span>No music selected</span>
        )}
      </div>

      <div className="section stock-music pb-3 px-3 d-flex flex-column gap-3 p-1">
        <div className="section-title">Stock music</div>
        <div className="music-list d-flex flex-column gap-3">
          {stockMusics.map(
            (music) =>
              currentMusic?.id !== music.id && (
                <div
                  key={music.id}
                  className="d-flex align-items-center justify-content-between music-card"
                >
                  <MusicCard
                    music={music}
                    isPlaying={playingStockMusicId === music.id}
                    onPlayToggle={handlePlayStockMusicToggle}
                    handleReplaceMusic={() => setCurrentMusic(music)}
                    handleDeleteCurrentMusic={null}
                  />
                </div>
              )
          )}
        </div>
      </div>
    </div>
  );
}
