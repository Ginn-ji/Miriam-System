import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Shield, UserCircle, UserPlus } from 'lucide-react';
import apiClient from '../api/apiClient';
import { toast } from 'sonner';

const Login = ({ onLogin }) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

if (isRegistering) {
      try {
        // Send a clean JSON object instead of FormData
        const payload = {
          username: username,
          password: password,
          role: 'user',
          current_user_role: 'guest'
        };

        const response = await apiClient.post('/users/register', payload);
        toast.success('Registration successful! Logging you in...');
        
        // Auto-login after registration
        onLogin({ 
          id: response.data.id, 
          role: response.data.role, 
          username: response.data.username 
        });
      } catch (err) {
        const detail = err.response?.data?.detail;
        if (Array.isArray(detail)) {
          setError(`Error: ${detail[0].loc[detail[0].loc.length - 1]} ${detail[0].msg}`); 
        } else if (typeof detail === 'string') {
          setError(detail);
        } else {
          setError('Registration failed. Please check your connection.');
        }
      }
    } else {
      try {
        const response = await apiClient.post('/login', { username, password });
        onLogin(response.data);
      } catch (err) {
        setError('Invalid username or password');
      }
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-secondary p-4 font-manrope">
      <Card className="w-full max-w-md shadow-lg border-t-4 border-t-primary">
        <CardHeader className="text-center space-y-1">
          <div className="flex justify-center mb-2">
            <div className="p-3 rounded-full bg-primary/10">
              <Shield className="h-8 w-8 text-primary" />
            </div>
          </div>
          <CardTitle className="text-3xl font-serif font-bold text-primary"> LACBot </CardTitle>
          <CardDescription className="text-sm text-muted-foreground">
            {isRegistering ? "Create your account" : "Legal Awareness Chat Bot"}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4 pt-4">
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input 
              type="text" 
              placeholder="Username" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <Input 
              type="password" 
              placeholder="Password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            {error && <p className="text-red-500 text-sm text-center">{error}</p>}
            
            <Button type="submit" className="w-full h-12 text-base" disabled={loading}>
              {isRegistering ? "Sign Up" : "Login"}
            </Button>
          </form>

          {!isRegistering && (
            <>
              <div className="relative my-4">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-card px-2 text-muted-foreground">Or access without account</span>
                </div>
              </div>

              <Button 
                variant="outline" 
                className="w-full flex items-center gap-3 h-12 text-base justify-center hover:bg-muted"
                onClick={() => onLogin({ id: 'g1', role: 'guest', username: 'Guest' })}
              >
                <UserCircle className="h-5 w-5 text-muted-foreground" />
                Continue as Guest
              </Button>
            </>
          )}

          <div className="mt-4 pt-4 border-t text-center">
            <Button 
              variant="ghost" 
              className="w-full text-sm text-muted-foreground"
              onClick={() => {
                setIsRegistering(!isRegistering);
                setError('');
              }}
            >
              {isRegistering ? (
                "Already have an account? Log in"
              ) : (
                <div className="flex items-center gap-2">
                  <UserPlus className="h-4 w-4" />
                  Don't have an account? Register here
                </div>
              )}
            </Button>
          </div>
          
          <p className="text-[10px] text-center text-muted-foreground mt-6 italic">
            By continuing, you acknowledge that this AI system provides legal awareness and is not a substitute for professional legal advice.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

export default Login;