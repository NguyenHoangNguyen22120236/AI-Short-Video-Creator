import "../styles/LoadingStatus.css";
import { useEffect, useState } from "react";

export default function LoadingStatus({ message }) {
  const [dots, setDots] = useState("");

  useEffect(() => {
    const interval = setInterval(() => {
      setDots(prev => (prev.length >= 3 ? "" : prev + "."));
    }, 500); // After every 500ms, add a dot until it reaches 3 dots, then reset

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="blocking-overlay d-flex flex-column justify-content-center align-items-center">
      <div className="loader"></div>
      <div className="loading-message">
        {message}{dots}
      </div>
    </div>
  );
}

