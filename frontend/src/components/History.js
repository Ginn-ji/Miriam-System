import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { MessageSquare, ArrowLeft, Send, Bot, Calendar, X, Trash2, ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { useLocation } from 'react-router-dom';
import apiClient from '../api/apiClient';
import { toast } from 'sonner';
import { LawResultCard } from './LegalChat';

const SESSIONS_PER_PAGE = 20;
const todayStr = new Date().toLocaleDateString('en-CA');

export const History = ({ user }) => {
  const { t } = useLanguage();
  const location = useLocation();
  const [sessions, setSessions]           = useState([]);
  const [totalSessions, setTotalSessions] = useState(0);
  const [oldestDate, setOldestDate]       = useState(undefined);
  const [sessionsPage, setSessionsPage]   = useState(1);
  const [selectedSession, setSelectedSession] = useState(null);
  const [messages, setMessages]           = useState([]);
  const [startDate, setStartDate]         = useState('');
  const [endDate, setEndDate]             = useState('');
  const [chatInput, setChatInput]         = useState('');
  const [chatLoading, setChatLoading]     = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (user && user.role !== 'guest') fetchSessions(1);
  }, [user]);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const sessionId = params.get('session');
    if (sessionId) loadSession(sessionId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.search]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchSessions = async (page) => {
    const skip = (page - 1) * SESSIONS_PER_PAGE;
    try {
      const response = await apiClient.get(
        `/chat/sessions?user_id=${user.id}&skip=${skip}&limit=${SESSIONS_PER_PAGE}`
      );
      setSessions(response.data.sessions || []);
      setTotalSessions(response.data.total || 0);
      if (response.data.oldest_date) {
        setOldestDate(new Date(response.data.oldest_date).toLocaleDateString('en-CA'));
      }
      setSessionsPage(page);
    } catch (error) {
      console.error('Error fetching sessions:', error);
    }
  };

  const loadSession = async (sessionId) => {
    try {
      const response = await apiClient.get(`/chat/sessions/${sessionId}`);
      setMessages(response.data.messages || []);
      setSelectedSession(sessionId);
      setChatInput('');
    } catch (error) {
      toast.error('Could not load this session.');
    }
  };

  const handleDeleteSession = async (e, sessionId) => {
    e.stopPropagation();
    if (!window.confirm('Delete this conversation? This cannot be undone.')) return;
    try {
      await apiClient.delete(`/chat/sessions/${sessionId}`);
      toast.success('Conversation deleted.');
      fetchSessions(sessionsPage); // re-fetch current page
    } catch { toast.error('Failed to delete conversation.'); }
  };

  const handleContinueSend = async () => {
    if (!chatInput.trim() || chatLoading || !selectedSession) return;
    const optimistic = { user_message: chatInput, assistant_response: null, laws: [] };
    setMessages(prev => [...prev, optimistic]);
    const fd = new FormData();
    fd.append('message', chatInput);
    fd.append('session_id', selectedSession);
    if (user && user.role !== 'guest') fd.append('user_id', user.id);
    setChatInput(''); setChatLoading(true);
    try {
      const response = await apiClient.post('/chat', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
      setMessages(prev => { const u = [...prev]; u[u.length - 1] = { user_message: optimistic.user_message, assistant_response: response.data.response, laws: response.data.laws || [] }; return u; });
    } catch { toast.error('Failed to get response.'); setMessages(prev => prev.slice(0, -1)); }
    finally { setChatLoading(false); }
  };

  // Client-side date filter on loaded page
  const filteredSessions = sessions.filter((session) => {
    const d = new Date(session.timestamp).toLocaleDateString('en-CA');
    if (startDate && d < startDate) return false;
    if (endDate && d > endDate) return false;
    return true;
  });

  const totalPages = Math.max(1, Math.ceil(totalSessions / SESSIONS_PER_PAGE));
  const clearFilter = () => { setStartDate(''); setEndDate(''); };
  const hasFilter = startDate || endDate;
  const fmt = (d) => d ? new Date(d + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : '';

  return (
    <div className="space-y-6" data-testid="history-page">
      <div>
        <h1 className="text-4xl font-serif font-bold tracking-tight text-primary">{t('history')}</h1>
        <p className="text-muted-foreground mt-1">View and continue your past Labor Code inquiries</p>
      </div>

      <Tabs defaultValue="chats" className="w-full">
        <TabsList className="grid w-full max-w-md grid-cols-2">
          <TabsTrigger value="chats" data-testid="chats-tab">
            <MessageSquare className="h-4 w-4 mr-2" /> Chat Sessions
          </TabsTrigger>
        </TabsList>

        <TabsContent value="chats" className="mt-6">
          {user.role === 'guest' ? (
            <Card><CardContent className="text-center py-12 text-muted-foreground">Please log in to view chat history.</CardContent></Card>
          ) : selectedSession ? (
            <Card className="shadow-sm">
              <CardHeader className="flex flex-row items-center gap-4 border-b pb-4">
                <Button variant="outline" size="icon" onClick={() => setSelectedSession(null)}><ArrowLeft className="h-4 w-4" /></Button>
                <div className="flex-1">
                  <CardTitle className="font-serif">Conversation History</CardTitle>
                  <p className="text-xs text-muted-foreground mt-0.5">You can continue this conversation below</p>
                </div>
              </CardHeader>
              <CardContent className="space-y-6 pt-6 max-h-[500px] overflow-y-auto bg-secondary/20">
                {messages.map((msg, idx) => (
                  <div key={idx} className="space-y-4">
                    <div className="flex justify-end">
                      <div className="bg-primary text-primary-foreground px-4 py-3 rounded-sm max-w-[80%]">
                        <p className="text-xs font-semibold opacity-70 mb-1">You</p>
                        <p className="text-sm">{msg.user_message}</p>
                      </div>
                    </div>
                    {msg.assistant_response !== null && (
                      <div className="flex justify-start">
                        <div className="bg-card border px-4 py-3 rounded-sm max-w-[80%]">
                          <p className="text-xs font-semibold text-primary mb-1 flex items-center gap-1"><Bot className="h-3 w-3" /> LACBot</p>
                          <p className="text-sm whitespace-pre-wrap">{msg.assistant_response}</p>
                          {msg.laws && msg.laws.map((law, i) => <LawResultCard key={i} lawData={law} />)}
                        </div>
                      </div>
                    )}
                    {msg.assistant_response === null && chatLoading && idx === messages.length - 1 && (
                      <div className="flex justify-start">
                        <div className="bg-card border px-4 py-3 rounded-sm">
                          <p className="text-xs font-semibold text-primary mb-1 flex items-center gap-1"><Bot className="h-3 w-3" /> LACBot</p>
                          <p className="text-sm text-muted-foreground animate-pulse">LACBot is thinking...</p>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </CardContent>
              <div className="border-t p-4 bg-white">
                <div className="flex gap-2 items-center">
                  <Textarea value={chatInput} onChange={(e) => setChatInput(e.target.value)} placeholder="Continue this conversation..."
                    className="min-h-[50px] max-h-[100px] resize-none focus-visible:ring-primary flex-1 text-sm"
                    onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleContinueSend(); } }} />
                  <Button onClick={handleContinueSend} disabled={chatLoading || !chatInput.trim()} className="h-[50px] px-4 shadow-sm"><Send className="h-4 w-4" /></Button>
                </div>
                <p className="text-xs text-muted-foreground mt-1 text-right">Enter to send · Shift+Enter for new line</p>
              </div>
            </Card>
          ) : (
            <div className="space-y-4">
              {/* Date Range Filter */}
              <Card className="shadow-sm">
                <CardContent className="py-4">
                  <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3 flex-wrap">
                    <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground">
                      <Calendar className="h-4 w-4" /> Filter by date:
                    </div>
                    <div className="flex items-center gap-2">
                      <label className="text-xs text-muted-foreground whitespace-nowrap">From</label>
                      <input type="date" value={startDate} min={oldestDate} max={endDate || todayStr} onChange={(e) => setStartDate(e.target.value)}
                        className="border rounded-md px-3 py-1.5 text-sm bg-background outline-none focus:ring-2 focus:ring-primary" />
                    </div>
                    <div className="flex items-center gap-2">
                      <label className="text-xs text-muted-foreground whitespace-nowrap">To</label>
                      <input type="date" value={endDate} min={startDate || oldestDate} max={todayStr} onChange={(e) => setEndDate(e.target.value)}
                        className="border rounded-md px-3 py-1.5 text-sm bg-background outline-none focus:ring-2 focus:ring-primary" />
                    </div>
                    {hasFilter && (
                      <button onClick={clearFilter} className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground border rounded-md px-2 py-1.5">
                        <X className="h-3.5 w-3.5" /> Clear
                      </button>
                    )}
                    {hasFilter && (
                      <span className="text-xs text-muted-foreground ml-auto">
                        {filteredSessions.length} on this page match
                        {startDate && endDate ? ` · ${fmt(startDate)} → ${fmt(endDate)}` : startDate ? ` from ${fmt(startDate)}` : ` up to ${fmt(endDate)}`}
                      </span>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Session list */}
              <div className="grid gap-3">
                {filteredSessions.length === 0 ? (
                  <Card><CardContent className="text-center py-10">
                    <MessageSquare className="h-10 w-10 text-muted-foreground mx-auto mb-3" />
                    <p className="text-muted-foreground text-sm">{hasFilter ? 'No conversations match the selected dates on this page.' : 'No chat history found.'}</p>
                    {hasFilter && <button onClick={clearFilter} className="mt-2 text-xs text-primary hover:underline">Clear filter</button>}
                  </CardContent></Card>
                ) : (
                  filteredSessions.map((session) => (
                    <Card key={session._id} className="cursor-pointer hover:bg-muted transition-colors border-l-4 border-l-transparent hover:border-l-primary" onClick={() => loadSession(session._id)}>
                      <CardContent className="p-4 flex justify-between items-center gap-3">
                        <div className="truncate flex-1">
                          <p className="font-medium truncate">{session.last_message}</p>
                          <p className="text-xs text-muted-foreground mt-1 flex items-center gap-1"><Calendar className="h-3 w-3" />{new Date(session.timestamp).toLocaleString()}</p>
                        </div>
                        <div className="flex items-center gap-2 shrink-0">
                          <MessageSquare className="h-5 w-5 text-muted-foreground" />
                          <button onClick={(e) => handleDeleteSession(e, session._id)} className="p-1.5 rounded-md text-muted-foreground hover:bg-destructive/10 hover:text-destructive transition-colors" title="Delete">
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </CardContent>
                    </Card>
                  ))
                )}
              </div>

              {/* Pagination — backend-paged */}
              {totalPages > 1 && (
                <div className="flex items-center justify-between pt-2">
                  <p className="text-sm text-muted-foreground">
                    Page {sessionsPage} of {totalPages} · {totalSessions} total sessions
                  </p>
                  <div className="flex items-center gap-2">
                    <button onClick={() => fetchSessions(sessionsPage - 1)} disabled={sessionsPage === 1}
                      className="p-2 rounded-md border hover:bg-muted disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                      <ChevronLeft className="h-4 w-4" />
                    </button>
                    <span className="text-sm font-medium px-2">{sessionsPage}</span>
                    <button onClick={() => fetchSessions(sessionsPage + 1)} disabled={sessionsPage === totalPages}
                      className="p-2 rounded-md border hover:bg-muted disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                      <ChevronRight className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
};