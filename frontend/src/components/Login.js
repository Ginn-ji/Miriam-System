import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Shield, UserCircle, UserPlus } from 'lucide-react';
import apiClient from '../api/apiClient';
import { toast } from 'sonner';

const Login = ({ onLogin }) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [registerStep, setRegisterStep] = useState(0); 
  const [registerCode, setRegisterCode] = useState('');
  
  const [loginType, setLoginType] = useState('email'); 
  const [loginIdentifier, setLoginIdentifier] = useState('');
  
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const [forgotStep, setForgotStep] = useState(0); 
  const [resetEmail, setResetEmail] = useState('');
  const [resetCode, setResetCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  
  const [showDisclaimer, setShowDisclaimer] = useState(false);

  useEffect(() => {
    const hasAgreed = localStorage.getItem('shield_disclaimer_agreed');
    if (!hasAgreed) setShowDisclaimer(true);
  }, []);

  const handleAcceptDisclaimer = () => {
    localStorage.setItem('shield_disclaimer_agreed', 'true');
    setShowDisclaimer(false);
  };
  
  const validatePassword = (pwd) => {
    if (pwd.length < 8) return "Password must be at least 8 characters long.";
    if (!/[^a-zA-Z]/.test(pwd)) return "Password must contain at least one number or special character.";
    return null;
  };

  const getErrorMessage = (err, defaultMessage) => {
    const detail = err.response?.data?.detail;
    if (Array.isArray(detail)) {
      return detail.map(e => `${e.loc[e.loc.length - 1]}: ${e.msg}`).join(', ');
    }
    if (typeof detail === 'string') {
      return detail;
    }
    return defaultMessage;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (isRegistering) {
      const pwdError = validatePassword(password);
      if (pwdError) return setError(pwdError);
      
      setLoading(true);
      try {
        const payload = { username, email, password, role: 'user' };
        await apiClient.post('/users/register', payload);
        toast.success('Verification code sent to your email.');
        setRegisterStep(1); 
      } catch (err) {
        setError(getErrorMessage(err, 'Registration request failed.'));
      }
      setLoading(false);
    } else {
      setLoading(true);
      try {
        const payload = { login_type: loginType, identifier: loginIdentifier, password };
        const response = await apiClient.post('/login', payload);
        onLogin(response.data);
      } catch (err) {
        setError(getErrorMessage(err, 'Invalid credentials'));
      }
      setLoading(false);
    }
  };

  const handleVerifyRegistration = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const response = await apiClient.post('/users/register/verify', { 
        email: email, 
        code: registerCode 
      });
      toast.success('Account verified and created successfully!');
      onLogin({ id: response.data.id, role: response.data.role, username: response.data.username });
    } catch (err) {
      setError(getErrorMessage(err, 'Verification failed. Invalid code.'));
    }
    setLoading(false);
  };

  const handleForgotRequest = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await apiClient.post('/users/forgot-password', { email: resetEmail });
      toast.success(res.data.message);
      setForgotStep(2);
    } catch (err) {
      const message = getErrorMessage(err, 'Failed to request reset.');
      setError(message);
      toast.error(message);
    }
    setLoading(false);
  };

  const handleVerifyCode = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await apiClient.post('/users/verify-reset-code', { email: resetEmail, code: resetCode });
      setForgotStep(3);
    } catch (err) {
      setError(getErrorMessage(err, 'Invalid code.'));
    }
    setLoading(false);
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    setError('');
    
    const pwdError = validatePassword(newPassword);
    if (pwdError) return setError(pwdError);
    
    setLoading(true);
    try {
      await apiClient.post('/users/reset-password', { 
        email: resetEmail, 
        code: resetCode, 
        new_password: newPassword 
      });
      toast.success('Password reset successful. Please log in.');
      setForgotStep(0);
      setLoginType('email');
      setLoginIdentifier(resetEmail);
      setPassword('');
    } catch (err) {
      setError(getErrorMessage(err, 'Failed to reset password.'));
    }
    setLoading(false);
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center bg-secondary p-4 font-manrope">

      <Card className="w-full max-w-md shadow-lg border-t-4 border-t-primary">
        <CardHeader className="text-center space-y-1">
          <div className="flex justify-center mb-2">
            <div className="p-3 rounded-full bg-primary/10">
              <Shield className="h-8 w-8 text-primary" />
            </div>
          </div>
          <CardTitle className="text-3xl font-serif font-bold text-primary"> LACBot </CardTitle>
          <CardDescription className="text-sm text-muted-foreground">
            {forgotStep > 0 ? "Account Recovery" : (isRegistering ? "Create your account" : "Legal Awareness Chat Bot")}
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-4 pt-4">
          
          {isRegistering && registerStep === 1 ? (
             <form onSubmit={handleVerifyRegistration} className="space-y-4">
              <p className="text-sm text-center text-muted-foreground">Enter the 6-digit code sent to <strong>{email}</strong>.</p>
              <Input type="text" placeholder="123456" maxLength={6} value={registerCode} onChange={(e) => setRegisterCode(e.target.value)} required className="text-center tracking-widest text-lg" />
              {error && <p className="text-red-500 text-sm text-center">{error}</p>}
              <Button type="submit" className="w-full h-12" disabled={loading}>Verify & Create Account</Button>
              <Button type="button" variant="ghost" className="w-full" onClick={() => setRegisterStep(0)}>Back</Button>
            </form>
          ) : forgotStep === 0 ? (
            <form onSubmit={handleSubmit} className="space-y-4">
              
              {isRegistering ? (
                  <>
                    <Input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required />
                    <Input type="email" placeholder="Registered Email Address" value={email} onChange={(e) => setEmail(e.target.value)} required />
                  </>
                ) : (
                  <Input 
                    type="email"
                    placeholder="Email Address"
                    value={loginIdentifier} 
                    onChange={(e) => setLoginIdentifier(e.target.value)} 
                    required 
                  />
                )}
              
              <Input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
              
              {error && <p className="text-red-500 text-sm text-center">{error}</p>}
              
              {!isRegistering && (
                <div className="text-right">
                  <button type="button" onClick={() => { setForgotStep(1); setError(''); }} className="text-xs text-primary hover:underline">
                    Forgot Password?
                  </button>
                </div>
              )}

              <Button type="submit" className="w-full h-12 text-base" disabled={loading}>
                {isRegistering ? "Send Verification Code" : "Login"}
              </Button>
            </form>
          ) : forgotStep === 1 ? (
            <form onSubmit={handleForgotRequest} className="space-y-4">
              <Input type="email" placeholder="Enter Registered Email Address" value={resetEmail} onChange={(e) => setResetEmail(e.target.value)} required />
              {error && <p className="text-red-500 text-sm text-center">{error}</p>}
              <Button type="submit" className="w-full h-12" disabled={loading}>Send Verification Code</Button>
              <Button type="button" variant="ghost" className="w-full" onClick={() => setForgotStep(0)}>Cancel</Button>
            </form>
          ) : forgotStep === 2 ? (
            <form onSubmit={handleVerifyCode} className="space-y-4">
              <p className="text-sm text-center text-muted-foreground">Enter the 6-digit code sent to your email.</p>
              <Input type="text" placeholder="123456" maxLength={6} value={resetCode} onChange={(e) => setResetCode(e.target.value)} required className="text-center tracking-widest text-lg" />
              {error && <p className="text-red-500 text-sm text-center">{error}</p>}
              <Button type="submit" className="w-full h-12" disabled={loading}>Verify Code</Button>
              <Button type="button" variant="ghost" className="w-full" onClick={() => setForgotStep(0)}>Cancel</Button>
            </form>
          ) : (
            <form onSubmit={handleResetPassword} className="space-y-4">
              <p className="text-sm text-center text-muted-foreground">Password must be at least 8 characters with a number or special character.</p>
              <Input type="password" placeholder="New Password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required />
              {error && <p className="text-red-500 text-sm text-center">{error}</p>}
              <Button type="submit" className="w-full h-12" disabled={loading}>Reset Password</Button>
            </form>
          )}

          {forgotStep === 0 && !isRegistering && (
            <>
              <div className="relative my-4">
                <div className="absolute inset-0 flex items-center"><span className="w-full border-t" /></div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-card px-2 text-muted-foreground">Or access without account</span>
                </div>
              </div>
              <Button variant="outline" className="w-full flex items-center gap-3 h-12 text-base justify-center hover:bg-muted" onClick={() => onLogin({ id: 'g1', role: 'guest', username: 'Guest' })}>
                <UserCircle className="h-5 w-5 text-muted-foreground" /> Continue as Guest
              </Button>
            </>
          )}

          {forgotStep === 0 && (
            <div className="mt-4 pt-4 border-t text-center">
              <Button variant="ghost" className="w-full text-sm text-muted-foreground" onClick={() => { 
                setIsRegistering(!isRegistering); 
                setError(''); 
                setPassword(''); 
                setRegisterStep(0); 
              }}>
                {isRegistering ? "Already have an account? Log in" : <div className="flex items-center gap-2"><UserPlus className="h-4 w-4" /> Don't have an account? Register here</div>}
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Login;