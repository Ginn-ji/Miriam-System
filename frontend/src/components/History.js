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
        <p className="text-muted-foreground mt-1">View your chat history</p>
      </div>

      <Tabs defaultValue="translations" className="w-full">
        <TabsList className="grid w-full max-w-md grid-cols-2">
          <TabsTrigger value="chats" data-testid="chats-tab">
            <MessageSquare className="h-4 w-4 mr-2" />
            Chat Sessions
          </TabsTrigger>
        </TabsList>

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