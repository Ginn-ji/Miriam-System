import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Button } from './ui/button';
import { Shield, User, ShieldCheck, UserCircle } from 'lucide-react';

const Login = ({ onLogin }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-secondary p-4 font-manrope">
      <Card className="w-full max-w-md shadow-lg border-t-4 border-t-primary">
        <CardHeader className="text-center space-y-1">
          <div className="flex justify-center mb-2">
            <div className="p-3 rounded-full bg-primary/10">
              <Shield className="h-8 w-8 text-primary" />
            </div>
          </div>
          <CardTitle className="text-3xl font-serif font-bold text-primary"> Astraea </CardTitle>
          <CardDescription className="text-sm text-muted-foreground">
            Legal Awareness Support System
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4 pt-4">
          <div className="grid gap-3">
            <Button 
              variant="default" 
              className="w-full flex items-center gap-3 h-12 text-base justify-start px-6"
              onClick={() => onLogin({ id: 'a1', role: 'admin', name: 'Administrator' })}
            >
              <ShieldCheck className="h-5 w-5" />
              Login as Admin
            </Button>
            
            <Button 
              variant="outline" 
              className="w-full flex items-center gap-3 h-12 text-base justify-start px-6 border-primary/20 hover:bg-primary/5"
              onClick={() => onLogin({ id: 'u1', role: 'user', name: 'Registered User' })}
            >
              <User className="h-5 w-5 text-primary" />
              Login as User
            </Button>

            <div className="relative my-4">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-card px-2 text-muted-foreground">Or access without account</span>
              </div>
            </div>

            <Button 
              variant="ghost" 
              className="w-full flex items-center gap-3 h-12 text-base justify-start px-6 hover:bg-muted"
              onClick={() => onLogin({ id: 'g1', role: 'guest', name: 'Guest' })}
            >
              <UserCircle className="h-5 w-5 text-muted-foreground" />
              Continue as Guest
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