import { useState } from "react";
import validator from "validator";

export default function SignUp() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [errorEmail, setErrorEmail] = useState("");
  const [passwordStrength, setPasswordStrength] = useState("");

  const handleEmailChange = (e) => {
    const value = e.target.value;
    setEmail(value);

    if (value.length === 0) {
      setErrorEmail("");
      return;
    }

    if (!validator.isEmail(value)) {
      setErrorEmail("Please enter a valid email");
    } else {
      setErrorEmail("");
    }
  };

  const handlePasswordChange = (e) => {
    const value = e.target.value;
    setPassword(value);

    if (value.length === 0) {
      setPasswordStrength("");
    } else if (validator.isStrongPassword(value)) {
      setPasswordStrength("strong");
    } else if (value.length >= 6) {
      setPasswordStrength("medium");
    } else {
      setPasswordStrength("weak");
    }
  };

  const getStrengthColor = (strength) => {
    switch (strength) {
      case "weak":
        return "red";
      case "medium":
        return "orange";
      case "strong":
        return "green";
      default:
        return "transparent";
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    if (!validator.isEmail(email)) {
      return;
    }

    if (password !== confirmPassword) {
      setMessage("Passwords do not match");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/api/user/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
          name,
        }),
      });

      if (response.status === 201) {
        setMessage(`Success! Please login with your email`);
        // Optional: redirect user or clear form
      } else {
        const error = await response.json();
        setError(error.detail || "Signup failed");
      }
    } catch (err) {
      console.error("Signup error:", err);
      setError("An error occurred while signing up. Please try again.");
    }
  };

  return (
    <form className="signup" onSubmit={handleSubmit}>
      <div className="field">
        <input
          type="text"
          placeholder="Your Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>
      <div className="field">
        <input
          type="text"
          placeholder="Email Address"
          value={email}
          onChange={handleEmailChange}
          required
        />
      </div>
      {errorEmail && <div style={{ color: "red" }}>{errorEmail}</div>}
      <div className="field">
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={handlePasswordChange}
          required
        />
      </div>
      {password && (
        <div
          style={{
            height: "6px",
            marginTop: "5px",
            backgroundColor: getStrengthColor(passwordStrength),
            borderRadius: "4px",
            transition: "background-color 0.3s ease",
          }}
        ></div>
      )}
      {password && (
        <div
          style={{
            fontSize: "0.85em",
            color: getStrengthColor(passwordStrength),
            marginTop: "3px",
          }}
        >
          Password strength: {passwordStrength}
        </div>
      )}
      <div className="field">
        <input
          type="password"
          placeholder="Confirm password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />
      </div>

      <div className="field btn">
        <div className="btn-layer"></div>
        <input type="submit" value="Signup" />
      </div>
      {error && <div style={{ color: "red", marginTop: "10px" }}>{error}</div>}
      {message && (
        <div style={{ color: "green", marginTop: "10px" }}>{message}</div>
      )}
    </form>
  );
}
