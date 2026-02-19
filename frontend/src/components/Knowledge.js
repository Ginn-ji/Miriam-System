import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { BookOpen, Search } from 'lucide-react';
import apiClient from '../api/apiClient';

export const Knowledge = () => {
  const { t } = useLanguage();
  const [laws, setLaws] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedLanguage, setSelectedLanguage] = useState('all');

  useEffect(() => {
    fetchLaws();
  }, [selectedCategory, selectedLanguage]);

  const fetchLaws = async () => {
    try {
      const params = {};
      if (selectedCategory !== 'all') params.category = selectedCategory;
      if (selectedLanguage !== 'all') params.language = selectedLanguage;
      if (searchQuery) params.q = searchQuery;

      const response = await apiClient.get('/legal-knowledge', { params });
      setLaws(response.data.laws || []);
    } catch (error) {
      console.error('Error fetching laws:', error);
    }
  };

  const handleSearch = () => {
    fetchLaws();
  };

  const categories = ['all', 'Civil Law', 'Labor Law', 'Criminal Law', 'Family Law', 'Privacy Law'];

  return (
    <div className="space-y-6" data-testid="knowledge-page">
      <div>
        <h1 className="text-4xl font-serif font-bold tracking-tight text-primary" data-testid="knowledge-title">
          {t('knowledge')}
        </h1>
        <p className="text-muted-foreground mt-1">Browse Philippine legal articles and statutes</p>
      </div>

      <Card className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)]">
        <CardHeader>
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 flex items-center gap-2">
              <Search className="h-5 w-5 text-muted-foreground" />
              <Input
                placeholder="Search legal knowledge..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                data-testid="knowledge-search-input"
              />
            </div>
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger className="w-[180px]" data-testid="category-filter">
                <SelectValue placeholder="Category" />
              </SelectTrigger>
              <SelectContent>
                {categories.map((cat) => (
                  <SelectItem key={cat} value={cat}>
                    {cat === 'all' ? 'All Categories' : cat}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
              <SelectTrigger className="w-[180px]" data-testid="language-filter">
                <SelectValue placeholder="Language" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Languages</SelectItem>
                <SelectItem value="en">English</SelectItem>
                <SelectItem value="tl">Tagalog</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardHeader>
        <CardContent>
          {laws.length > 0 ? (
            <div className="space-y-4">
              {laws.map((law) => (
                <div
                  key={law.id}
                  className="p-4 rounded-sm border hover:bg-muted/50 transition-colors"
                  data-testid="law-item"
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-serif font-semibold text-lg">{law.title}</h3>
                    <span className="legal-badge">{law.language}</span>
                  </div>
                  <p className="text-sm text-muted-foreground mb-3">{law.content}</p>
                  <div className="flex flex-wrap gap-2">
                    <span className="px-2 py-1 rounded-sm bg-primary/10 text-primary text-xs font-medium">
                      {law.category}
                    </span>
                    {law.tags.map((tag, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-1 rounded-sm bg-muted text-muted-foreground text-xs"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12" data-testid="empty-knowledge">
              <BookOpen className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">No legal articles found</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};