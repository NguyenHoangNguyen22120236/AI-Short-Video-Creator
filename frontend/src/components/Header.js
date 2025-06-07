import "../styles/Header.css";
import { Link } from "react-router-dom";
import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function Header() {
  const [showLogout, setShowLogout] = useState(false);
  const userRef = useRef(null);

  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/authentication");
  };

  // Hide logout when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (userRef.current && !userRef.current.contains(event.target)) {
        setShowLogout(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className="d-flex justify-content-between align-items-center header px-3 py-2">
      <div className="d-flex gap-3 align-items-center">
        <img src="/logo.png" alt="logo" className="logo" />
        <Link to="/" className="text-decoration-none">
          <h1 className="text-center text-white fs-4">
            AI Short Video Creator
          </h1>
        </Link>
      </div>

      <div className="position-relative" ref={userRef}>
        <div
          className="user d-flex justify-content-center align-items-center gap-2"
          onClick={() => setShowLogout((prev) => !prev)}
        >
          <img src="/user.png" alt="account" width={32} height={32} />
        </div>

        <div
          className={`show-logout position-absolute bg-white border rounded shadow-sm px-3 py-2 ${
            showLogout ? "visible" : ""
          }`}
          onClick={handleLogout}
        >
          Logout
        </div>
      </div>
    </div>
  );
}
