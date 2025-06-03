import "../styles/CreateVideo.css";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Modal from "react-bootstrap/Modal";

export default function CreateVideo() {
  const [topic, setTopic] = useState("");
  const [language, setLanguage] = useState("English");
  const [showModal, setShowModal] = useState(false);
  const [trendyTopics, setTrendyTopics] = useState([]);
  const [location, setLocation] = useState("US");
  const [isGenerating, setIsGenerating] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchTrendyTopics = async () => {
      setTrendyTopics([]);
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/trendy_fetcher/fetch_trends?location=${location}`
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        setTrendyTopics(data["trendy_topics"]);
      } catch (error) {
        console.error("Error fetching trendy topics:", error);
      }
    };
    fetchTrendyTopics();
  }, [location]);

  const handleTopicClick = (selected) => {
    setTopic(selected);
    setShowModal(false);
  };

  const handleGenerateVideo = async () => {
    if (!topic.trim()) {
      alert("Please enter or select a topic first.");
      return;
    }

    setIsGenerating(true);

    try {
      //const token = localStorage.getItem('access_token');

      const token = ""; // Replace with your actual token logic

      const response = await fetch(
        "http://127.0.0.1:8000/api/video/create_video",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            topic,
            language,
          }),
        }
      );

      const data = await response.json();

      if (data) {
        // Navigate to preview page and pass the video URL
        navigate("/preview-video", { state: { data: data } });
        //console.log('Video generated successfully:', data);
      } else {
        alert("Video generation failed.");
      }
    } catch (error) {
      console.error("Error generating video:", error);
      alert("An error occurred while generating the video.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="container px-lg-5 py-lg-3 px-md-3 py-md-2 px-sm-1 py-sm-1 text-white">
      <div className="input-box mx-lg-5 mt-lg-5 mx-md-3 mt-md-3 mx-sm-3 mt-sm-1 mt-3 mx-1">
        <textarea
          placeholder="Give me a topic in English or Vietnamese"
          maxLength={100}
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />
        <div className="d-flex justify-content-between align-items-center flex-lg-row flex-md-row flex-sm-column flex-column">
          <span className="char-limit">{topic.length} / 100</span>
          <div className="d-flex gap-5 align-items-center">
            <button className="btn" onClick={() => setShowModal(true)}>
              Suggest Trendy Topics
            </button>
            <button
              className="btn btn-primary"
              onClick={handleGenerateVideo}
              disabled={isGenerating}
            >
              {isGenerating ? "Generating..." : "Generate Video"}
            </button>
          </div>
        </div>
      </div>

      <div className="language-selector d-flex mx-lg-5 mt-lg-5 mx-md-3 mt-md-3 mx-sm-3 mt-sm-1 mt-3 mx-1 gap-5 align-items-center">
        <label htmlFor="language">Language:</label>
        <select
          id="language"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
        >
          <option>English</option>
          <option>Vietnamese</option>
        </select>
      </div>

      {showModal && (
        <Modal
          show={showModal}
          onHide={() => setShowModal(false)}
          className="custom-modal"
        >
          <Modal.Header closeButton>
            <Modal.Title>Trendy Topics</Modal.Title>
            <select
              className="location-selector"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            >
              <option value="US">US</option>
              <option value="VN">Vietnam</option>
            </select>
          </Modal.Header>

          <Modal.Body className="d-flex gap-3 flex-wrap justify-content-start align-items-center">
            {setTrendyTopics.length > 0 ? (
              trendyTopics.map((item, index) => (
                <button
                  key={index}
                  className="topic-btn"
                  onClick={() => handleTopicClick(item)}
                >
                  {item}
                </button>
              ))
            ) : (
              <h3 className="text-white">Loading trendy topics...</h3>
            )}
          </Modal.Body>
        </Modal>
      )}
    </div>
  );
}
