import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Send, Bot, User, Paperclip } from 'lucide-react';
import apiClient from '../api/apiClient';
import { toast } from 'sonner';

export const LegalChat = ({ user }) => {
  const { t } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    setSessionId(`session_${Date.now()}`);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if ((!input.trim() && !file) || loading) return;

    // Display user message in UI
    const userMessage = { role: 'user', content: input, fileName: file?.name };
    setMessages((prev) => [...prev, userMessage]);
    
    const formData = new FormData();
    formData.append("message", input);
    formData.append("session_id", sessionId);
    if (file) formData.append("file", file);
    if (user.role !== 'guest') formData.append("user_id", user.id);

    setInput('');
    setFile(null);
    setLoading(true);

    try {
      const response = await apiClient.post('/chat', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setMessages((prev) => [...prev, { role: 'assistant', content: response.data.response }]);
    } catch (error) {
      toast.error('Failed to get response');
      setMessages((prev) => [...prev, { role: 'assistant', content: 'Error: Could not connect to the server.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      <div className="mb-4">
        <h1 className="text-4xl font-serif font-bold tracking-tight text-primary">{t('legalChat')}</h1>
        <p className="text-muted-foreground mt-1">{t('askLegalQuestion')}</p>
      </div>

      <Card className="flex-1 flex flex-col shadow-lg">
        <CardHeader className="border-b">
          <CardTitle className="font-serif flex items-center gap-2">
            <Bot className="h-5 w-5 text-primary" /> {t('assistant')}
          </CardTitle>
        </CardHeader>
        <CardContent className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex items-start gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}>
              <div className={`max-w-[80%] px-4 py-3 rounded-sm ${msg.role === 'user' ? 'chat-message-user' : 'chat-message-assistant'}`}>
                <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                {msg.fileName && <p className="text-xs mt-1 opacity-70 italic">📎 Attached: {msg.fileName}</p>}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </CardContent>
        <div className="border-t p-4">
          {file && <div className="text-xs text-primary mb-2">📎 Prepared to upload: {file.name}</div>}
          <div className="flex gap-2 items-center">
            <input 
              type="file" 
              hidden 
              ref={fileInputRef} 
              onChange={(e) => setFile(e.target.files[0])} 
            />
            <Button variant="ghost" size="icon" onClick={() => fileInputRef.current.click()}>
              <Paperclip className="h-5 w-5" />
            </Button>
            <Textarea 
              value={input} 
              onChange={(e) => setInput(e.target.value)} 
              placeholder={t('typeMessage')} 
              className="min-h-[60px] resize-none" 
            />
            <Button onClick={handleSend} disabled={loading || (!input.trim() && !file)} size="lg">
              <Send className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
};