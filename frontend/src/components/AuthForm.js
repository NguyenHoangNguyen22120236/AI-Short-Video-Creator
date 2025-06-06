import React, { useState } from "react";
import "../styles/AuthForm.css"; // Import your CSS
import LoginForm from "./LoginForm";

export default function AuthForm() {
  const [activeForm, setActiveForm] = useState("login");

  return (
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
          <LoginForm setActiveForm={setActiveForm} />

          <form
            className={`signup ${activeForm === "signup" ? "show" : ""}`}
            onSubmit={(e) => e.preventDefault()}
          >
            <div className="field">
              <input type="text" placeholder="Email Address" required />
            </div>
            <div className="field">
              <input type="password" placeholder="Password" required />
            </div>
            <div className="field">
              <input type="password" placeholder="Confirm password" required />
            </div>
            <div className="field btn">
              <div className="btn-layer"></div>
              <input type="submit" value="Signup" />
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
