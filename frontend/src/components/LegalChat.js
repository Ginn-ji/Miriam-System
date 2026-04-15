import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Send, Bot, Paperclip, BookOpen, ChevronDown, ChevronUp } from 'lucide-react';
import apiClient from '../api/apiClient';
import { toast } from 'sonner';

export const LawResultCard = ({ lawData }) => {
  const [showFullArticle, setShowFullArticle] = useState(false);

  return (
    <Card className="mt-3 mb-2 shadow-sm border-l-4 border-l-primary w-full text-left">
      <CardHeader className="pb-2 pt-4 px-4">
        <CardTitle className="text-base font-serif flex items-center gap-2">
          <BookOpen className="h-4 w-4 text-primary" />
          {lawData.article ? `${lawData.article}: ${lawData.title}` : lawData.title}
        </CardTitle>
      </CardHeader>
      <CardContent className="px-4 pb-4 space-y-3">
        <div className="bg-primary/5 p-3 rounded-md border border-primary/10">
          <p className="text-xs font-semibold text-primary mb-1">Simple Explanation:</p>
          <p className="text-sm">{lawData.simplified_text}</p>
        </div>
        
        {lawData.best_match_chunk && (
          <div>
            <p className="text-xs font-semibold text-primary mb-1">Relevant Section:</p>
            <p className="text-sm italic border-l-2 border-primary/40 pl-3 py-1 text-muted-foreground">
              "{lawData.best_match_chunk}"
            </p>
          </div>
        )}

        <Button
          variant="ghost"
          size="sm"
          className="w-full flex justify-between items-center text-muted-foreground hover:text-primary mt-1 h-8 text-xs"
          onClick={() => setShowFullArticle(!showFullArticle)}
        >
          {showFullArticle ? "Hide Full Article" : "View Full Article"}
          {showFullArticle ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
        </Button>

        {showFullArticle && (
          <div className="pt-3 border-t mt-2 animate-in fade-in">
            <p className="text-xs font-semibold mb-2">Full Legal Text:</p>
            <div className="space-y-2">
              {lawData.chunks && lawData.chunks.map((chunk, index) => (
                <p key={index} className="text-sm text-muted-foreground">
                  • {chunk}
                </p>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

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

    const userMessage = { role: 'user', content: input, fileName: file?.name };
    setMessages((prev) => [...prev, userMessage]);
    
    const formData = new FormData();
    formData.append("message", input);
    formData.append("session_id", sessionId);
    if (file) formData.append("file", file);
    if (user && user.role !== 'guest') formData.append("user_id", user.id);

    setInput('');
    setFile(null);
    setLoading(true);

    try {
      const response = await apiClient.post('/chat', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setMessages((prev) => [...prev, { 
        role: 'assistant', 
        content: response.data.response,
        laws: response.data.laws 
      }]);
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
        <h1 className="text-4xl font-serif font-bold tracking-tight text-primary">Labor Law Retrieval</h1>
        <p className="text-muted-foreground mt-1">Ask questions related to Philippine Labor Law</p>
      </div>

      <Card className="flex-1 flex flex-col shadow-lg">
        <CardHeader className="border-b">
          <CardTitle className="font-serif flex items-center gap-2">
            <Bot className="h-5 w-5 text-primary" /> Miriam Assistant
          </CardTitle>
        </CardHeader>
        <CardContent className="flex-1 overflow-y-auto p-6 space-y-4 bg-secondary/20">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex items-start gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}>
              <div className={`max-w-[80%] px-4 py-3 rounded-sm ${msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-card border'}`}>
                <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                {msg.fileName && <p className="text-xs mt-1 opacity-70 italic">📎 Attached: {msg.fileName}</p>}
                
                {/* Render the Law Cards if the assistant returned structured data */}
                {msg.role === 'assistant' && msg.laws && msg.laws.map((law, i) => (
                  <LawResultCard key={i} lawData={law} />
                ))}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </CardContent>
        <div className="border-t p-4 bg-card">
          {file && <div className="text-xs text-primary mb-2">📎 Prepared to upload: {file.name}</div>}
          <div className="flex gap-2 items-center">
            <input type="file" hidden ref={fileInputRef} onChange={(e) => setFile(e.target.files[0])} />
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