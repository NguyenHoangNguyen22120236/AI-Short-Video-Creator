import { useEffect, useRef, useState } from 'react';
import ReactHowler from 'react-howler';
import '../styles/MusicTab.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPause, faPlay } from '@fortawesome/free-solid-svg-icons';

export default function MusicCard({ music, isPlaying, onPlayToggle, handleReplaceMusic }) {
    const howlerRef = useRef(null);
    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);
    const [intervalId, setIntervalId] = useState(null);

    useEffect(() => {
        if (isPlaying) {
            const id = setInterval(() => {
                if (howlerRef.current) {
                    setCurrentTime(howlerRef.current.seek());
                    setDuration(howlerRef.current.duration());
                }
            }, 500); // update every 0.5s
            setIntervalId(id);
        } else {
            clearInterval(intervalId);
        }

        return () => clearInterval(intervalId);
    }, [isPlaying]);

    const handleSeek = (e) => {
        const rect = e.currentTarget.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        const newTime = percent * duration;
        if (howlerRef.current) {
            howlerRef.current.seek(newTime);
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
        <div className="music-card d-flex justify-content-between align-items-center p-2 rounded bg-dark w-100 flex-lg-row flex-md-row flex-sm-column flex-column">
            <div className="d-flex align-items-center w-100">
                <ReactHowler
                    src={music.url}
                    playing={isPlaying}
                    ref={howlerRef}
                    //html5={true} // Important for mobile support
                    onLoad={() => {
                        if (howlerRef.current) {
                            setDuration(howlerRef.current.duration());
                        }
                    }}
                />

                <div
                    className="play-btn me-3 d-flex justify-content-center align-items-center"
                    onClick={() => onPlayToggle(music)}
                >
                    <span className="text-black">
                        {isPlaying ? <FontAwesomeIcon icon={faPause} /> : <FontAwesomeIcon icon={faPlay} />}
                    </span>
                </div>

                <div className="music-info w-75">
                    <div className="fw-semibold text-white">{music.title}</div>
                    <div className="d-flex align-items-center text-white-50 text-sm mt-1">
                        <span style={{ minWidth: '40px' }}>{formatTime(currentTime)}</span>

                        <div className="progress-bar flex-grow-1 mx-2" onClick={handleSeek}>
                            <div
                                className="progress-filled"
                                style={{
                                    width: `${(currentTime / duration) * 100 || 0}%`,
                                }}
                            ></div>
                        </div>

                        <span style={{ minWidth: '40px' }}>{formatTime(duration)}</span>
                    </div>
                </div>
            </div>

            {handleReplaceMusic ? (
                <button className="btn btn-outline-light btn-sm ms-3" onClick={handleReplaceMusic}>
                    Replace
                </button>
                ): 
                <div className="replace-placeholder ms-3" style={{ width: '80px' }}></div>
            }
        </div>
    );
}
