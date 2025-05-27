import { useEffect, useRef, useState } from 'react';
import '../styles/MusicTab.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPause, faPlay } from '@fortawesome/free-solid-svg-icons';

export default function MusicCard({ music, isPlaying, onPlayToggle }) {
    const audioRef = useRef(null);
    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);

        // Track progress
    useEffect(() => {
        console.log('Setting up audio event listeners');

        const audio = new Audio(music.url);
        audioRef.current = audio;


        const handleTimeUpdate = () => setCurrentTime(audio.currentTime);
        const handleLoadedMetadata = () => setDuration(audio.duration);

        audio.addEventListener('timeupdate', handleTimeUpdate);
        audio.addEventListener('loadedmetadata', handleLoadedMetadata);

        return () => {
            audio.removeEventListener('timeupdate', handleTimeUpdate);
            audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
        };
    }, []);

    // Sync play/pause
    useEffect(() => {
        const audio = audioRef.current;

        if (isPlaying) {
            audio.play();
        } else {
            audio.pause();
        }

        return () => {
            console.log('Cleaning up audio event listeners');
            audio.pause();
        };
    }, [isPlaying]);

    const handleSeek = (e) => {
        const rect = e.currentTarget.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        const newTime = percent * duration;
        if (audioRef.current) {
            audioRef.current.currentTime = newTime;
            setCurrentTime(newTime);
        }
    };

    const formatTime = (sec) => {
        if (!sec || isNaN(sec)) return '0:00';
        const minutes = Math.floor(sec / 60);
        const seconds = Math.floor(sec % 60).toString().padStart(2, '0');
        return `${minutes}:${seconds}`;
    };

    return (
        <div className="music-card d-flex align-items-center p-2 rounded bg-dark w-50">
        <div className="play-btn me-3 d-flex justify-content-center align-items-center" onClick={() => onPlayToggle(music)}> 
            <span className='text-black'>
            {isPlaying ? <FontAwesomeIcon icon={faPause} /> : <FontAwesomeIcon icon={faPlay} />}
            </span>
        </div>

        <div className="music-info w-100">
            <div className="fw-semibold text-white">{music.title}</div>
            <div className="d-flex align-items-center text-white-50 text-sm mt-1">
            <span style={{ minWidth: '40px' }}>{formatTime(currentTime)}</span>

            <div
                className="progress-bar flex-grow-1 mx-2"
                onClick={handleSeek}
            >
                <div
                className="progress-filled"
                style={{
                    width: `${(currentTime / duration) * 100 || 0}%`
                }}
                ></div>
            </div>

            <span style={{ minWidth: '40px' }}>{formatTime(duration)}</span>
            </div>
        </div>
        </div>
    );
}