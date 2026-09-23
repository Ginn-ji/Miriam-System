import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { FileText, MessageSquare, BookOpen, History as HistoryIcon, ArrowRight } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import apiClient from '../api/apiClient';

export const Dashboard = ({ user }) => {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    documents: 0,
    translations: 0,
    chat_sessions: 0,
    legal_articles: 0,
  });
  const [loading, setLoading] = useState(true);

  // ── NEW STATE ──────────────────────────────────────────────
  const [recentSessions, setRecentSessions] = useState([]);
  const [tip, setTip] = useState(null);
  // ──────────────────────────────────────────────────────────

  useEffect(() => {
    fetchData();
    fetchTip();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  const fetchData = async () => {
    try {
      // Only fetch the global stats now
      const statsRes = await apiClient.get('/stats');

      let userChatCount = 0;

      // If the user is logged in (not a guest), fetch their specific chat sessions
      if (user && user.role !== 'guest') {
        const sessionsRes = await apiClient.get(`/chat/sessions?user_id=${user.id}`);
        const sessions = sessionsRes.data.sessions || [];
        userChatCount = sessions.length;
        setRecentSessions(sessions.slice(0, 3));
      }

      setStats({
        ...statsRes.data,
        chat_sessions: userChatCount, // Override global chat stats with user's personal count
      });
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  // ── NEW: fetch daily tip — same tip all day, changes at midnight ──
  const fetchTip = async () => {
    try {
      const res = await apiClient.get('/legal-knowledge');
      const laws = res.data.laws || [];
      if (laws.length > 0) {
        const today = new Date();
        const seed = today.getFullYear() * 10000 + (today.getMonth() + 1) * 100 + today.getDate();
        const index = seed % laws.length;
        setTip(laws[index]);
      }
    } catch (err) {
      // non-critical, silently ignore
    }
  };

  // Base cards that everyone sees
  // Base cards that everyone sees
  const baseCards = [
    { id: 'chat', icon: MessageSquare, label: t('chatSessions'), value: stats.chat_sessions, color: 'text-purple-600' },
    { id: 'laws', icon: BookOpen, label: t('legalArticles'), value: stats.legal_articles, color: 'text-orange-600' },
  ];

  // Filter out the 'chat' card if the user is a guest
  const statCards = user?.role === 'guest'
    ? baseCards.filter(card => card.id !== 'chat')
    : baseCards;

  return (
    <div className="dashboard-container" data-testid="dashboard">
      <div>
        <h1 className="dashboard-title" data-testid="dashboard-title">
          Welcome to LACBot, {user?.username || 'Guest'}!
        </h1>
        <p className="dashboard-subtitle">{t('welcomeDesc')}</p>
      </div>

      <div className="stats-grid">
        {statCards.map((stat, idx) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.id || idx} className="card-elevated" data-testid={`stat-card-${idx}`}>
              <CardContent className="pt-6">
                <div className="stat-card-body">
                  <div>
                    <p className="stat-label">{stat.label}</p>
                    <p className="stat-value">{stat.value}</p>
                  </div>
                  <Icon className={`icon-10 ${stat.color}`} />
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="quick-actions-row">

        {/* ── LEFT COLUMN: Quick Actions + Recent Conversations stacked ── */}
        <div className="flex flex-col gap-4">

          {/* Quick Actions Card — ORIGINAL, history button removed */}
          <Card
            className="quick-actions-card"
            data-testid="quick-actions-card"
          >
            <CardHeader>
              <CardTitle className="font-serif">Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="quick-actions-list">
              <Link to="/chat" className="block">
                <Button variant="outline" className="quick-action-btn" data-testid="quick-chat-btn">
                  <MessageSquare className="icon-4 mr-2" />
                  {t('askLegalQuestion')}
                </Button>
              </Link>

              <Link to="/knowledge" className="block">
                <Button variant="outline" className="quick-action-btn" data-testid="quick-knowledge-btn">
                  <BookOpen className="icon-4 mr-2" />
                  {t('knowledge')}
                </Button>
              </Link>
            </CardContent>
          </Card>

          {/* Recent Conversations — only for logged-in users, redirects to /history?session=ID */}
          {user?.role !== 'guest' && (
            <Card className="shadow-sm flex-1">
              <CardHeader className="pb-3 border-b">
                <CardTitle className="font-serif flex items-center gap-2 text-base">
                  <HistoryIcon className="h-4 w-4 text-primary" />
                  Recent Conversations
                </CardTitle>
              </CardHeader>
              <CardContent className="pt-4 space-y-2">
                {recentSessions.length === 0 ? (
                  <div className="text-center py-4">
                    <MessageSquare className="h-8 w-8 text-muted-foreground mx-auto mb-2" />
                    <p className="text-sm text-muted-foreground">No conversations yet.</p>
                    <Link to="/chat">
                      <Button variant="outline" size="sm" className="mt-3">Start a Chat</Button>
                    </Link>
                  </div>
                ) : (
                  <>
                    {recentSessions.map((session) => (
                      <div
                        key={session._id}
                        onClick={() => navigate(`/history?session=${session._id}`)}
                        className="flex items-center justify-between p-3 rounded-md border cursor-pointer hover:bg-muted/50 hover:border-primary/40 transition-colors group"
                      >
                        <div className="truncate flex-1 mr-2">
                          <p className="text-sm font-medium truncate">{session.last_message}</p>
                          <p className="text-xs text-muted-foreground mt-0.5">
                            {new Date(session.timestamp).toLocaleString()}
                          </p>
                        </div>
                        <ArrowRight className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors shrink-0" />
                      </div>
                    ))}
                    <Link to="/history" className="block">
                      <Button variant="ghost" size="sm" className="w-full mt-1 text-xs text-muted-foreground">
                        View all history
                      </Button>
                    </Link>
                  </>
                )}
              </CardContent>
            </Card>
          )}
        </div>

        {/* ── RIGHT COLUMN: Legal Tip of the Day — full height, everyone ── */}
        <Card className="shadow-sm border-amber-200 bg-amber-50/40 flex flex-col">
          <CardHeader className="pb-3 border-b border-amber-200">
            <div className="flex items-start justify-between">
              <CardTitle className="font-serif flex items-center gap-2 text-base text-amber-800">
                <BookOpen className="h-4 w-4 shrink-0" />
                Legal Tip of the Day
              </CardTitle>
              <span className="text-xs text-amber-600 font-medium bg-amber-100 px-2 py-0.5 rounded-full shrink-0">
                {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              </span>
            </div>
          </CardHeader>
          <CardContent className="pt-4 flex-1 flex flex-col">
            {tip ? (
              <div className="flex flex-col h-full space-y-3">
                <p className="text-xs font-bold uppercase tracking-wider text-amber-600">
                  {tip.title}
                </p>
                <p className="text-sm text-gray-700 leading-relaxed flex-1">
                  {tip.content || 'No preview available.'}
                </p>
                <div className="pt-3 border-t border-amber-200 mt-auto">
                  <p className="text-xs text-amber-500 mb-2">Tip changes daily at midnight.</p>
                  <Link to="/chat" className="block">
                    <Button
                      variant="outline"
                      size="sm"
                      className="w-full border-amber-300 text-amber-800 hover:bg-amber-100"
                    >
                      <MessageSquare className="h-3.5 w-3.5 mr-2" />
                      Ask LACBot About This
                    </Button>
                  </Link>
                </div>
              </div>
            ) : (
              <div className="flex-1 flex items-center justify-center">
                <p className="text-sm text-muted-foreground">Loading today's tip...</p>
              </div>
            )}
          </CardContent>
        </Card>

      </div>
    </div>
  );
};