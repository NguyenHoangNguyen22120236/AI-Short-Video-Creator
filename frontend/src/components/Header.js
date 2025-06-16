import "../styles/Header.css";
import { Link } from "react-router-dom";
import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function Header() {
  const [showLogout, setShowLogout] = useState(false);
  const [userData, setUserData] = useState({ username: "", avatar: null });
  const userRef = useRef(null);

  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/authentication");
  };

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem("token");
        const res = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/user/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (res.ok) {
          const data = await res.json();
          setUserData({
            username: data.username || "Anonymous",
            avatar: data.avatar,
          });
        } else {
          console.error("Failed to fetch user data");
        }
      } catch (err) {
        console.error("Error fetching user data:", err);
      }
    };

    fetchUserData();
  }, []);

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

  const renderAvatar = () => {
    if (userData.avatar) {
      return (
        <img
          src={userData.avatar}
          alt="account"
          style={{ borderRadius: "50%" }}
        />
      );
    } else {
      const initials = userData.username
        .split(" ")
        .map((n) => n[0])
        .join("")
        .slice(0, 2)
        .toUpperCase();

      return (
        <div className="initials-avatar">
          {initials || "U"}
        </div>
      );
    }
  };

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

      <div className="position-relative d-flex justify-content-center flex-column align-items-center" ref={userRef}>
        <div
          className="user d-flex justify-content-center align-items-center"
          onClick={() => setShowLogout((prev) => !prev)}
        >
          {renderAvatar()}
        </div>

        <span className="username text-white ms-2">
          {userData.username || "Anonymous"}
        </span>

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
