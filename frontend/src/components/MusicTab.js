import { useState, useRef } from 'react';
import '../styles/MusicTab.css';
import MusicCard from './MusicCard';

export default function MusicTab({ stockMusics, currentMusic, setCurrentMusic }) {
    const [playingId, setPlayingId] = useState(null);
    const audioRef = useRef(new Audio());

    const handlePlayToggle = (music) => {
        if (playingId === music.id) {
          audioRef.current.pause();
          setPlayingId(null);
        } else {
          if (!audioRef.current.paused) {
              audioRef.current.pause();
          }

          if (audioRef.current.src !== music.url) {
            audioRef.current.src = music.url;
          }
          audioRef.current.play();
          setPlayingId(music.id);
          setCurrentMusic(music);
        }
    };

    return (
        <div className="music-tab-content p-3">
        <div className="section current-music mb-4">
            <h5 className="section-title mb-3">Current Music info:</h5>
            {currentMusic ? (
            <MusicCard
                music={currentMusic}
                isPlaying={playingId === currentMusic.id}
                onPlayToggle={handlePlayToggle}
            />
            ) : (
            <p>No music selected</p>
            )}
        </div>

        <div className="section stock-music mb-4">
            <h5 className="section-title mb-3">Stock music</h5>
            {stockMusics.map((music) => (
            <div key={music.id} className="d-flex align-items-center justify-content-between music-card mb-3">
                <MusicCard
                    music={music}
                    isPlaying={playingId === music.id}
                    onPlayToggle={handlePlayToggle}
                />
                <button className="btn btn-outline-light btn-sm ms-3" onClick={() => setCurrentMusic(music)}>
                Replace
                </button>
            </div>
            ))}
        </div>

        <div className="text-end">
            <button className="btn btn-primary">Save Change</button>
        </div>
        </div>
    );
}