import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Send, Bot, User } from 'lucide-react';
import apiClient from '../api/apiClient';
import { toast } from 'sonner';

export const LegalChat = () => {
  const { t } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const newSessionId = `session_${Date.now()}`;
    setSessionId(newSessionId);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await apiClient.post('/chat', {
        message: input,
        session_id: sessionId,
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      toast.error('Failed to get response');
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'I apologize, but I encountered an error. Please try again.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col" data-testid="chat-page">
      <div className="mb-4">
        <h1 className="text-4xl font-serif font-bold tracking-tight text-primary" data-testid="chat-title">
          {t('legalChat')}
        </h1>
        <p className="text-muted-foreground mt-1">{t('askLegalQuestion')}</p>
      </div>

      <Card className="flex-1 flex flex-col shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)]">
        <CardHeader className="border-b">
          <CardTitle className="font-serif flex items-center gap-2">
            <Bot className="h-5 w-5 text-primary" />
            {t('assistant')}
          </CardTitle>
        </CardHeader>
        <CardContent className="flex-1 overflow-y-auto p-6 space-y-4" data-testid="chat-messages">
          {messages.length === 0 ? (
            <div className="text-center py-12" data-testid="empty-chat">
              <Bot className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">{t('askLegalQuestion')}</p>
              <p className="text-sm text-muted-foreground mt-2">{t('disclaimer')}</p>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex items-start gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}
                data-testid={`chat-message-${msg.role}`}
              >
                {msg.role === 'assistant' && (
                  <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                    <Bot className="h-5 w-5 text-primary-foreground" />
                  </div>
                )}
                <div
                  className={`max-w-[80%] px-4 py-3 rounded-sm ${
                    msg.role === 'user'
                      ? 'chat-message-user'
                      : 'chat-message-assistant'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                </div>
                {msg.role === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-muted flex items-center justify-center flex-shrink-0">
                    <User className="h-5 w-5 text-foreground" />
                  </div>
                )}
              </div>
            ))
          )}
          {loading && (
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                <Bot className="h-5 w-5 text-primary-foreground" />
              </div>
              <div className="max-w-[80%] px-4 py-3 rounded-sm chat-message-assistant">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-primary rounded-full animate-bounce" />
                  <span className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:0.2s]" />
                  <span className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:0.4s]" />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </CardContent>
        <div className="border-t p-4">
          <div className="flex gap-2">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={t('typeMessage')}
              className="min-h-[60px] resize-none"
              disabled={loading}
              data-testid="chat-input"
            />
            <Button
              onClick={handleSend}
              disabled={loading || !input.trim()}
              size="lg"
              data-testid="chat-send-btn"
            >
              <Send className="h-5 w-5" />
            </Button>
          </div>
          <p className="text-xs text-muted-foreground mt-2 italic">{t('disclaimer')}</p>
        </div>
      </Card>
    </div>
  );
};