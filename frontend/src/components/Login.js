import React from 'react';

const Login = ({ onLogin }) => {
  const handleGuest = () => onLogin({ id: 'guest', role: 'guest', name: 'Guest' });
  
  return (
    <div className="login-page">
      <h1>SHIELD Login</h1>
      <button onClick={() => onLogin({ id: 'u1', role: 'user', name: 'User' })}>Login as User</button>
      <button onClick={() => onLogin({ id: 'a1', role: 'admin', name: 'Admin' })}>Login as Admin</button>
      <hr />
      <button onClick={handleGuest}>Continue as Guest</button>
    </div>
  );
};

export default Login;