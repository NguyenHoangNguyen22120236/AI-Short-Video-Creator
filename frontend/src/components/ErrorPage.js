import { useLocation, useNavigate } from "react-router-dom";
import { useEffect } from "react";
import "../styles/ErrorPage.css"; // Optional: for styling

export default function ErrorPage() {
  const location = useLocation();
  const navigate = useNavigate();

  // Optional: auto-redirect after delay
  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/");
    }, 5000); // redirect after 5s
    return () => clearTimeout(timer);
  }, [navigate]);

  const errorMessage =
    location.state?.message || "Oops! Something went wrong. Please try again.";

  return (
    <div className="error-page d-flex flex-column align-items-center justify-content-center text-center p-4">
      <img src="/warning.png" alt="Error" className="error-image mb-3" />
      <h2 className="mb-2">Error</h2>
      <p className="mb-3">{errorMessage}</p>
      <button className="btn btn-primary" onClick={() => navigate("/")}>
        Go to Homepage
      </button>
    </div>
  );
}
