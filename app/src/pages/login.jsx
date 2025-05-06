import { useState } from "react";
import axios from "axios";
import { useNavigate ,Link} from "react-router-dom";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const api = import.meta.env.VITE_API_URL;
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${api}/login`, {
        username,
        password,
      });

      if (response.status === 200) {
        // Store the user info in localStorage or context
        localStorage.setItem("username", username);
        // Redirect to dashboard or home page
        window.location.href = "/dashboard";
      }
    } catch (err) {
      setError(err.response?.data?.message || "Login failed");
    }
  };

  return (
    <div>
      <div>
        <h2>Login to WULF</h2>
        {error && <p>{error}</p>}
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="username">
              Username
            </label>
            <input
              id="username"
              type="text"
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
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit">
            Sign in
          </button>
        </form>
        <p>Not a user? <Link to="/signup">Sign up</Link></p>
      </div>
    </div>
  );
};

export default Login;