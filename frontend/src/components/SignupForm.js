import React from "react";

const SignUp = () => {
  const handleSubmit = (e) => {
    e.preventDefault();
    // Add sign-up logic here (e.g., form validation, API call)
  };

  return (
    <form
      className='signup'
      onSubmit={handleSubmit}
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
  );
};

export default SignUp;