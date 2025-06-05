import "../styles/HistorySeeAll.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus, faClock } from "@fortawesome/free-solid-svg-icons";
import { format, parseISO } from "date-fns";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";

const token =   "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjNAZXhhbXBsZS5jb20iLCJ1c2VyX2lkIjoyLCJleHAiOjE3NDkzMDkxNjB9.68rcsvQZwqaxQ6WEbkh28Q6AV_d99xRDHtEoZyFDi1M";

export default function HistorySeeAll() {
  const [historyData, setHistoryData] = useState({});

  // Fetch history data from the API
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/video/get_all_videos_history",
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`
            },
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setHistoryData(data);
      } catch (error) {
        console.error("Failed to fetch video history:", error);
      } finally {
        //setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  return (
    <div className="container px-lg-5 py-lg-3 px-md-3 py-md-2 px-sm-1 py-sm-1 text-white">
      <div className="d-flex justify-content-start gap-5 p-0 flex-column">
        <div className="history-header d-flex justify-content-between align-items-center p-3">
          <h2>History</h2>
          <Link to="/create-video" className="text-decoration-none">
            <button className="create-button p-2">
              Create new <FontAwesomeIcon icon={faPlus} />
            </button>
          </Link>
        </div>

        {Object.entries(historyData).map(([date, videos]) => (
          <div key={date} className="d-flex flex-column gap-3 p-0 mt-2">
            <h4 className="date-label mb-3">{date}</h4>
            {videos.map((video) => (
              <Link
                to={`/preview-video/${video.id}`}
                key={video.id}
                className="history-card d-flex justify-content-between align-items-center p-3 text-decoration-none"
              >
                <div className="d-flex align-items-center flex-column">
                  <div className="d-flex gap-3 align-items-center fs-5">
                    <FontAwesomeIcon icon={faClock} />
                    <h4>{video.topic}</h4>
                  </div>
                  <p className="m-0">
                    Updated at: {format(parseISO(video.updated_at), "HH:mm")}
                  </p>
                </div>
                <div className="dots">⋮</div>
              </Link>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
