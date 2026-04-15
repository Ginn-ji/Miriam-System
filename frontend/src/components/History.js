import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { MessageSquare, ArrowLeft } from 'lucide-react';
import { Button } from './ui/button';
import apiClient from '../api/apiClient';
import { LawResultCard } from './LegalChat'; // Import the new card UI

export const History = ({ user }) => {
  const { t } = useLanguage();
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    if (user && user.role !== 'guest') {
      fetchSessions();
    }
  }, [user]);

  const fetchSessions = async () => {
    try {
      const response = await apiClient.get(`/chat/sessions?user_id=${user.id}`);
      setSessions(response.data.sessions || []);
    } catch (error) {
      console.error('Error fetching sessions:', error);
    }
  };

  const loadSession = async (sessionId) => {
    try {
      const response = await apiClient.get(`/chat/sessions/${sessionId}`);
      setMessages(response.data.messages || []);
      setSelectedSession(sessionId);
    } catch (error) {
      console.error('Error fetching chat history:', error);
    }
  };

  return (
    <div className="space-y-6" data-testid="history-page">
      <div>
        <h1 className="text-4xl font-serif font-bold tracking-tight text-primary">{t('history')}</h1>
        <p className="text-muted-foreground mt-1">View your past Labor Law inquiries</p>
      </div>

      <Tabs defaultValue="chats" className="w-full">
        <TabsList className="grid w-full max-w-md grid-cols-2">
          <TabsTrigger value="chats" data-testid="chats-tab">
            <MessageSquare className="h-4 w-4 mr-2" />
            Chat Sessions
          </TabsTrigger>
        </TabsList>

        <TabsContent value="chats" className="mt-6">
          {user.role === 'guest' ? (
            <Card>
              <CardContent className="text-center py-12 text-muted-foreground">
                Please log in to view chat history.
              </CardContent>
            </Card>
          ) : selectedSession ? (
            <Card className="shadow-sm">
              <CardHeader className="flex flex-row items-center gap-4 border-b pb-4">
                <Button variant="outline" size="icon" onClick={() => setSelectedSession(null)}>
                  <ArrowLeft className="h-4 w-4" />
                </Button>
                <CardTitle className="font-serif">Conversation History</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6 pt-6 max-h-[600px] overflow-y-auto bg-secondary/20">
                {messages.map((msg, idx) => (
                  <div key={idx} className="space-y-4">
                    <div className="flex justify-end">
                      <div className="bg-primary text-primary-foreground px-4 py-3 rounded-sm max-w-[80%]">
                        <p className="text-xs font-semibold opacity-70 mb-1">You</p>
                        <p className="text-sm">{msg.user_message}</p>
                      </div>
                    </div>
                    <div className="flex justify-start">
                      <div className="bg-card border px-4 py-3 rounded-sm max-w-[80%]">
                        <p className="text-xs font-semibold text-primary mb-1">Miriam</p>
                        <p className="text-sm whitespace-pre-wrap">{msg.assistant_response}</p>
                        
                        {/* Render the Law Cards from history! */}
                        {msg.laws && msg.laws.map((law, i) => (
                          <LawResultCard key={i} lawData={law} />
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          ) : (
            <div className="grid gap-4">
              {sessions.length === 0 ? (
                <p className="text-muted-foreground">No chat history found.</p>
              ) : (
                sessions.map((session) => (
                  <Card 
                    key={session._id} 
                    className="cursor-pointer hover:bg-muted transition-colors border-l-4 border-l-transparent hover:border-l-primary" 
                    onClick={() => loadSession(session._id)}
                  >
                    <CardContent className="p-4 flex justify-between items-center">
                      <div className="truncate max-w-[80%]">
                        <p className="font-medium truncate">{session.last_message}</p>
                        <p className="text-xs text-muted-foreground mt-1">
                          {new Date(session.timestamp).toLocaleString()}
                        </p>
                      </div>
                      <MessageSquare className="h-5 w-5 text-muted-foreground" />
                    </CardContent>
                  </Card>
                ))
              )}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
};