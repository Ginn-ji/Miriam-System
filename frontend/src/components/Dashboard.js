import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { FileText, Languages, MessageSquare, BookOpen, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import apiClient from '../api/apiClient';

export const Dashboard = () => {
  const { t } = useLanguage();
  const [stats, setStats] = useState({
    documents: 0,
    translations: 0,
    chat_sessions: 0,
    legal_articles: 0,
  });
  const [recentDocs, setRecentDocs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, docsRes] = await Promise.all([
        apiClient.get('/stats'),
        apiClient.get('/documents?limit=5'),
      ]);
      setStats(statsRes.data);
      setRecentDocs(docsRes.data.documents || []);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    { icon: FileText, label: t('recentDocuments'), value: stats.documents, color: 'text-blue-600' },
    { icon: Languages, label: t('recentTranslations'), value: stats.translations, color: 'text-green-600' },
    { icon: MessageSquare, label: t('chatSessions'), value: stats.chat_sessions, color: 'text-purple-600' },
    { icon: BookOpen, label: t('legalArticles'), value: stats.legal_articles, color: 'text-orange-600' },
  ];

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
            <Card key={idx} className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)]" data-testid={`stat-card-${idx}`}>
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
        <Card className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)]">
          <CardHeader>
            <CardTitle className="font-serif">{t('recentDocuments')}</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <p className="text-sm text-muted-foreground">Loading...</p>
            ) : recentDocs.length > 0 ? (
              <div className="space-y-3">
                {recentDocs.map((doc) => (
                  <div
                    key={doc.id}
                    className="flex items-center justify-between p-3 rounded-sm bg-muted/50 hover:bg-muted transition-colors"
                    data-testid="recent-document"
                  >
                    <div className="flex items-center gap-3">
                      <FileText className="h-4 w-4 text-primary" />
                      <div>
                        <p className="text-sm font-medium">{doc.filename}</p>
                        <p className="text-xs text-muted-foreground">{doc.language}</p>
                      </div>
                    </div>
                    <Link to={`/documents/${doc.id}`}>
                      <Button variant="ghost" size="sm">
                        <ArrowRight className="h-4 w-4" />
                      </Button>
                    </Link>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-3" />
                <p className="text-sm text-muted-foreground">{t('noDocuments')}</p>
                <Link to="/documents">
                  <Button variant="outline" size="sm" className="mt-3" data-testid="upload-first-doc-btn">
                    {t('uploadHere')}
                  </Button>
                </Link>
              </div>
            )}
          </CardContent>
        </Card>

        <Card
          className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)] bg-gradient-to-br from-primary/5 to-primary/10"
          data-testid="quick-actions-card"
        >
          <CardHeader>
            <CardTitle className="font-serif">Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Link to="/documents" className="block">
              <Button variant="outline" className="w-full justify-start" data-testid="quick-upload-btn">
                <FileText className="h-4 w-4 mr-2" />
                {t('uploadDocument')}
              </Button>
            </Link>
            <Link to="/translate" className="block">
              <Button variant="outline" className="w-full justify-start" data-testid="quick-translate-btn">
                <Languages className="h-4 w-4 mr-2" />
                {t('translateText')}
              </Button>
            </Link>
            <Link to="/chat" className="block">
              <Button variant="outline" className="w-full justify-start" data-testid="quick-chat-btn">
                <MessageSquare className="h-4 w-4 mr-2" />
                {t('askLegalQuestion')}
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};