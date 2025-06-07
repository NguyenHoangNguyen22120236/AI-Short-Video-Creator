// googleAuth.js
export const initializeGoogleLogin = ({ clientId, callback }) => {
  if (!window.google) {
    console.error("Google Identity Services not loaded");
    return;
  }

  window.google.accounts.id.initialize({
    client_id: clientId,
    callback: callback, // callback receives `credential` (ID token)
  });

  window.google.accounts.id.renderButton(
    document.getElementById("google-signin-btn"),
    {
      theme: "outline",
      size: "large",
      shape: "",
    }
  );

  window.google.accounts.id.prompt(); // Optional: show One Tap prompt
};