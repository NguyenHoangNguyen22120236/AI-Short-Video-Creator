import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function LoginForm({ setActiveForm }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');

    try {
      console.log('Logging in with:', { email, password });
      const response = await fetch('http://127.0.0.1:8000/api/user/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      const data = await response.json();
      localStorage.setItem('token', data.access_token); // Save token
      console.log('Login success:', data);
      navigate('/'); // Redirect to home page
    } catch (err) {
      console.error(err);
      setError('Invalid credentials. Please try again.');
    }
  };

  return (
    <form className={`login`} onSubmit={handleLogin}>
      <div className="field">
        <input
          type="text"
          placeholder="Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div className="field">
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <div className="pass-link">
        <a href="#">Forgot password?</a>
      </div>
      <div className="field btn">
        <div className="btn-layer"></div>
        <input type="submit" value="Login" />
      </div>
      {error && <div style={{ color: 'red', marginTop: '10px' }}>{error}</div>}
      <div className="signup-link">
        Not a member?{' '}
        <a href="#" onClick={() => setActiveForm('signup')}>
          Signup now
        </a>
      </div>
    </form>
  );
}