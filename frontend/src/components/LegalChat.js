import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Send, Bot, Paperclip, BookOpen, ChevronDown } from 'lucide-react';
import apiClient from '../api/apiClient';
import { toast } from 'sonner';

export const LawResultCard = ({ lawData }) => {
  return (
    <Card className="mt-4 mb-2 shadow-sm border border-gray-200 overflow-hidden w-full text-left bg-white">
      <div className="p-4 border-b bg-gray-50 flex items-center gap-2">
        <BookOpen className="h-5 w-5 text-primary" />
        <h3 className="font-serif font-bold text-lg text-gray-900">
          {lawData.article ? `${lawData.article}: ${lawData.title}` : lawData.title}
        </h3>
      </div>
      <div className="p-0">
        <div className="p-4 bg-blue-50/50 m-4 rounded border border-blue-100">
          <p className="text-[10px] font-bold uppercase tracking-wider text-blue-600 mb-1">Simple Explanation:</p>
          <p className="text-sm text-gray-700 leading-relaxed">{lawData.simplified_text}</p>
        </div>
        {lawData.best_match_chunk && (
          <div className="px-4 pb-4">
            <p className="text-[10px] font-bold uppercase tracking-wider text-gray-400 mb-1">Relevant Section:</p>
            <div className="pl-3 border-l-4 border-gray-200 italic text-gray-500 text-sm">
              "{lawData.best_match_chunk}"
            </div>
          </div>
        )}
        <details className="group border-t border-gray-100">
          <summary className="flex items-center justify-between p-4 cursor-pointer hover:bg-gray-50 text-xs font-semibold text-gray-500 uppercase tracking-widest list-none">
            <span>View Full Article</span>
            <ChevronDown className="h-4 w-4 transition-transform group-open:rotate-180" />
          </summary>
          <div className="p-4 pt-2 text-sm text-gray-600 whitespace-pre-wrap bg-gray-50/50 leading-relaxed border-t border-gray-100">
            {lawData.chunks ? lawData.chunks.join('\n\n') : 'Full text not available.'}
          </div>
        </details>
      </div>
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
    /* Changed h-[calc...] to h-full and min-h-[calc(100vh-120px)] to take up all vertical space */
    <div className="flex flex-col h-full min-h-[calc(100vh-120px)]">
      <div className="mb-4">
        <h1 className="text-4xl font-serif font-bold tracking-tight text-primary">Labor Law Retrieval</h1>
        <p className="text-muted-foreground mt-1">Ask LACBot questions related to Philippine Labor Law</p>
      </div>

      {/* Added flex-1 to make the Card grow and fill all available space */}
      <Card className="flex-1 flex flex-col shadow-lg overflow-hidden border-gray-200 mb-2">
        <CardHeader className="border-b bg-white py-3">
          <CardTitle className="font-serif flex items-center gap-2 text-lg">
            <Bot className="h-5 w-5 text-primary" /> LACBot Assistant
          </CardTitle>
        </CardHeader>
        
        <CardContent className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div className={`max-w-[90%] w-full ${msg.role === 'user' ? 'bg-[#1e293b] text-white px-4 py-3 rounded-2xl rounded-tr-none shadow-sm ml-auto' : ''}`}>
                {msg.role === 'assistant' ? (
                   <p className="text-sm text-gray-800 leading-relaxed mb-2">{msg.content}</p>
                ) : (
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                )}
                {msg.fileName && <p className="text-xs mt-1 opacity-70 italic">📎 Attached: {msg.fileName}</p>}
                {msg.role === 'assistant' && msg.laws && msg.laws.map((law, i) => (
                  <LawResultCard key={i} lawData={law} />
                ))}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </CardContent>

        <div className="border-t p-4 bg-white">
          <div className="flex gap-2 items-center">
            <input type="file" hidden ref={fileInputRef} onChange={(e) => setFile(e.target.files[0])} />
            <Button variant="ghost" size="icon" onClick={() => fileInputRef.current.click()}>
              <Paperclip className="h-5 w-5" />
            </Button>
            <Textarea 
              value={input} 
              onChange={(e) => setInput(e.target.value)} 
              placeholder="Type your question about Labor Law..." 
              className="min-h-[60px] max-h-[120px] resize-none focus-visible:ring-primary flex-1" 
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
            />
            <Button onClick={handleSend} disabled={loading || (!input.trim() && !file)} className="px-6 h-[60px] shadow-sm">
              <Send className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
};