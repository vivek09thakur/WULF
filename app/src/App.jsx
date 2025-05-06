import React from "react";
import SignUp from "./pages/signup";
import Login from "./pages/login";
import { AuthProvider } from "./auth/authprovider";
import { ProtectedRoute } from "./auth/protected_routes";
import MainPage from "./pages/main";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import "./App.css";

const App = () => {
  return (
    <>
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/signup" element={<SignUp />} />
            <Route path="/login" element={<Login />} />
          
            <Route
              path="/main"
              element={<ProtectedRoute element={<MainPage />} />}
            />
            <Route path="*" element={<Login />} />
          </Routes>
        </Router>
      </AuthProvider>
    </>
  );
};

export default App;
