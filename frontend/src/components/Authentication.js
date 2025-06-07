import { useState } from "react";
import "../styles/Authentication.css";
import LoginForm from "./LoginForm";
import SignupForm from "./SignupForm";

export default function Authentication() {
  const [activeForm, setActiveForm] = useState("login");

  return (
    <div className="d-flex justify-content-center align-items-center vh-100 bg-dark">
      <div className="text-center p-4" style={{ maxWidth: "600px" }}>
        {/* Logo + App Title */}
        <div className="d-flex align-items-center mb-3 text-white">
          <img
            src="/logo.png" // Replace with your actual logo path
            alt="Logo"
            style={{ width: "30px", height: "30px", marginRight: "10px" }}
          />
          <span className="fw-bold fs-5">AI Short Video Creator</span>
        </div>

        {/* Main Heading with Gradient */}
        <h3 className="fw-bold mb-4 text-white">
          Welcome to{" "}
          <span className="text-gradient">AI Short Video Creator</span>
        </h3>

        {/* Auth Form */}
        <div className="wrapper">
          <div className="title-text">
            <div className={`title ${activeForm}`}>
              {activeForm === "login" ? "Login" : "Signup"}
            </div>
          </div>
          <div className="form-container">
            <div className="slide-controls">
              <input
                type="radio"
                name="slide"
                id="login"
                checked={activeForm === "login"}
                onChange={() => setActiveForm("login")}
              />
              <input
                type="radio"
                name="slide"
                id="signup"
                checked={activeForm === "signup"}
                onChange={() => setActiveForm("signup")}
              />
              <label htmlFor="login" className="slide login">
                Login
              </label>
              <label htmlFor="signup" className="slide signup">
                Signup
              </label>
              <div className="slider-tab"></div>
            </div>

            <div className="form-inner">
              {activeForm === "login" && (
                <LoginForm setActiveForm={setActiveForm} />
              )}

              {activeForm === "signup" && <SignupForm />}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
