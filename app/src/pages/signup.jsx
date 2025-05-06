import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const SignUp = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
const api = import.meta.env.VITE_API_URL;
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Sign up the user
      const response = await axios.post(`${api}/signup`, {
        username,
        password
      });

      if (response.status === 201) {
        // Assign initial challenges to the user
        await axios.post(`${api}/assign_challenges`, {
          username
        });
        
        // Redirect to login page after successful signup
        navigate('/login');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'An error occurred during signup');
    }
  };

  return (
    <div>
      <div>
        <h2>Sign Up</h2>
        {error && (
          <div>
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="username">
              Username
            </label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="password">
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
          >
            Sign Up
          </button>
        </form>
      </div>
    </div>
  );
};

export default SignUp;