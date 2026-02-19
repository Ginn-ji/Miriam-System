import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Languages, MessageSquare } from 'lucide-react';
import apiClient from '../api/apiClient';

export const History = () => {
  const { t } = useLanguage();
  const [translations, setTranslations] = useState([]);

  useEffect(() => {
    fetchTranslations();
  }, []);

  const fetchTranslations = async () => {
    try {
      const response = await apiClient.get('/translations');
      setTranslations(response.data.translations || []);
    } catch (error) {
      console.error('Error fetching translations:', error);
    }
  };

  return (
    <div className="space-y-6" data-testid="history-page">
      <div>
        <h1 className="text-4xl font-serif font-bold tracking-tight text-primary">
          {t('history')}
        </h1>
        <p className="text-muted-foreground mt-1">View your translation and chat history</p>
      </div>

      <Tabs defaultValue="translations" className="w-full">
        <TabsList className="grid w-full max-w-md grid-cols-2">
          <TabsTrigger value="translations" data-testid="translations-tab">
            <Languages className="h-4 w-4 mr-2" />
            Translations
          </TabsTrigger>
          <TabsTrigger value="chats" data-testid="chats-tab">
            <MessageSquare className="h-4 w-4 mr-2" />
            Chat Sessions
          </TabsTrigger>
        </TabsList>

        <TabsContent value="translations" className="mt-6">
          <Card className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)]">
            <CardHeader>
              <CardTitle className="font-serif">{t('recentTranslations')}</CardTitle>
            </CardHeader>
            <CardContent>
              {translations.length > 0 ? (
                <div className="space-y-4">
                  {translations.map((trans) => (
                    <div
                      key={trans.id}
                      className="p-4 rounded-sm border hover:bg-muted/50 transition-colors"
                      data-testid="translation-item"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <span className="legal-badge">{trans.source_language}</span>
                          <span className="text-muted-foreground">→</span>
                          <span className="legal-badge">{trans.target_language}</span>
                        </div>
                        <span className="text-xs text-muted-foreground">
                          {new Date(trans.created_at).toLocaleString()}
                        </span>
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
                        <div>
                          <p className="text-xs text-muted-foreground mb-1">Original</p>
                          <p className="text-sm line-clamp-3">{trans.original_text}</p>
                        </div>
                        <div>
                          <p className="text-xs text-muted-foreground mb-1">Translation</p>
                          <p className="text-sm line-clamp-3">{trans.translated_text}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12" data-testid="empty-translations">
                  <Languages className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground">No translations yet</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="chats" className="mt-6">
          <Card className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)]">
            <CardHeader>
              <CardTitle className="font-serif">Chat History</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12">
                <MessageSquare className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground">Chat history available per session</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};