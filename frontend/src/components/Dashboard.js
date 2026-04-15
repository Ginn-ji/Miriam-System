import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { FileText, MessageSquare, BookOpen, History as HistoryIcon } from 'lucide-react';
import { Link } from 'react-router-dom';
import apiClient from '../api/apiClient';

export const Dashboard = ({ user }) => {
  const { t } = useLanguage();
  const [stats, setStats] = useState({
    documents: 0,
    translations: 0,
    chat_sessions: 0,
    legal_articles: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
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
        userChatCount = sessionsRes.data.sessions ? sessionsRes.data.sessions.length : 0;
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

  // Base cards that everyone sees
  const baseCards = [
    { id: 'docs', icon: FileText, label: t('recentDocuments'), value: stats.documents, color: 'text-blue-600' },
    { id: 'chat', icon: MessageSquare, label: t('chatSessions'), value: stats.chat_sessions, color: 'text-purple-600' },
    { id: 'laws', icon: BookOpen, label: t('legalArticles'), value: stats.legal_articles, color: 'text-orange-600' },
  ];

  // Filter out the 'chat' card if the user is a guest
  const statCards = user?.role === 'guest' 
    ? baseCards.filter(card => card.id !== 'chat') 
    : baseCards;

  return (
    <div className="space-y-8" data-testid="dashboard">
      <div>
        <h1 className="text-4xl md:text-5xl font-serif font-bold tracking-tight text-primary" data-testid="dashboard-title">
          {t('welcome')}
        </h1>
        <p className="text-lg text-muted-foreground mt-2">{t('welcomeDesc')}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat, idx) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.id || idx} className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)]" data-testid={`stat-card-${idx}`}>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">{stat.label}</p>
                    <p className="text-3xl font-bold mt-2">{stat.value}</p>
                  </div>
                  <Icon className={`h-10 w-10 ${stat.color}`} />
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Quick Actions Card */}
        <Card
          className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)] bg-gradient-to-br from-primary/5 to-primary/10"
          data-testid="quick-actions-card"
        >
          <CardHeader>
            <CardTitle className="font-serif">Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Link to="/chat" className="block">
              <Button variant="outline" className="w-full justify-start" data-testid="quick-chat-btn">
                <MessageSquare className="h-4 w-4 mr-2" />
                {t('askLegalQuestion')}
              </Button>
            </Link>

            <Link to="/knowledge" className="block">
              <Button variant="outline" className="w-full justify-start" data-testid="quick-knowledge-btn">
                <BookOpen className="h-4 w-4 mr-2" />
                {t('knowledge')}
              </Button>
            </Link>

            {user?.role !== 'guest' && (
              <Link to="/history" className="block">
                <Button variant="outline" className="w-full justify-start" data-testid="quick-history-btn">
                  <HistoryIcon className="h-4 w-4 mr-2" />
                  {t('history')}
                </Button>
              </Link>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};