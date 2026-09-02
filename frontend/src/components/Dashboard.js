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
    <div className="dashboard-container" data-testid="dashboard">
      <div>
        <h1 className="dashboard-title" data-testid="dashboard-title">
          {t('welcome')}
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
        {/* Quick Actions Card */}
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

            {user?.role !== 'guest' && (
              <Link to="/history" className="block">
                <Button variant="outline" className="quick-action-btn" data-testid="quick-history-btn">
                  <HistoryIcon className="icon-4 mr-2" />
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