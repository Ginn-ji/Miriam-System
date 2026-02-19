import React, { useState } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Languages } from 'lucide-react';
import apiClient from '../api/apiClient';
import { toast } from 'sonner';

export const Translate = () => {
  const { t, language: currentLang } = useLanguage();
  const [sourceText, setSourceText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [sourceLang, setSourceLang] = useState('auto');
  const [targetLang, setTargetLang] = useState(currentLang === 'en' ? 'tl' : 'en');
  const [loading, setLoading] = useState(false);

  const handleTranslate = async () => {
    if (!sourceText.trim()) {
      toast.error('Please enter text to translate');
      return;
    }

    setLoading(true);
    try {
      const response = await apiClient.post('/translate', {
        text: sourceText,
        source_language: sourceLang,
        target_language: targetLang,
      });
      setTranslatedText(response.data.translated_text);
      toast.success('Translation completed');
    } catch (error) {
      console.error('Translation error:', error);
      toast.error('Translation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6" data-testid="translate-page">
      <div>
        <h1 className="text-4xl font-serif font-bold tracking-tight text-primary" data-testid="translate-title">
          {t('translateText')}
        </h1>
        <p className="text-muted-foreground mt-1">Translate documents between English and Tagalog</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)]">
          <CardHeader>
            <CardTitle className="font-serif">{t('original')}</CardTitle>
            <div className="flex items-center gap-2 mt-3">
              <Select value={sourceLang} onValueChange={setSourceLang}>
                <SelectTrigger className="w-[180px]" data-testid="source-lang-select">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="auto">{t('detectLanguage')}</SelectItem>
                  <SelectItem value="en">{t('english')}</SelectItem>
                  <SelectItem value="tl">{t('tagalog')}</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardHeader>
          <CardContent>
            <Textarea
              placeholder={t('typeMessage')}
              value={sourceText}
              onChange={(e) => setSourceText(e.target.value)}
              className="min-h-[300px] document-pane font-sans"
              data-testid="source-text-input"
            />
            <div className="flex items-center justify-between mt-4">
              <span className="text-xs text-muted-foreground">
                {sourceText.length} characters
              </span>
            </div>
          </CardContent>
        </Card>

        <Card className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)]">
          <CardHeader>
            <CardTitle className="font-serif">{t('translation')}</CardTitle>
            <div className="flex items-center gap-2 mt-3">
              <Select value={targetLang} onValueChange={setTargetLang}>
                <SelectTrigger className="w-[180px]" data-testid="target-lang-select">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="en">{t('english')}</SelectItem>
                  <SelectItem value="tl">{t('tagalog')}</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardHeader>
          <CardContent>
            <Textarea
              value={translatedText}
              readOnly
              className="min-h-[300px] document-pane font-sans"
              placeholder="Translation will appear here..."
              data-testid="translated-text-output"
            />
            <div className="flex items-center justify-between mt-4">
              <span className="text-xs text-muted-foreground">
                {translatedText.length} characters
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="flex justify-center">
        <Button
          onClick={handleTranslate}
          disabled={loading || !sourceText.trim()}
          size="lg"
          className="min-w-[200px]"
          data-testid="translate-submit-btn"
        >
          <Languages className="h-5 w-5 mr-2" />
          {loading ? t('translating') : t('translate_btn')}
        </Button>
      </div>

      <Card className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)] bg-muted/30">
        <CardContent className="pt-6">
          <p className="text-sm text-muted-foreground italic">
            Note: Translation service requires Google Cloud API keys. Please contact administrator to enable full translation functionality.
          </p>
        </CardContent>
      </Card>
    </div>
  );
};