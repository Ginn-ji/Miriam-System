import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useLanguage } from '../contexts/LanguageContext';
import { Button } from './ui/button';
import { 
  Home, 
  FileText, 
  Languages, 
  MessageSquare, 
  History, 
  BookOpen,
  Globe
} from 'lucide-react';

export const Sidebar = () => {
  const location = useLocation();
  const { t, language, toggleLanguage } = useLanguage();

  const navItems = [
    { path: '/', icon: Home, label: t('dashboard') },
    { path: '/documents', icon: FileText, label: t('documents') },
    { path: '/translate', icon: Languages, label: t('translate') },
    { path: '/chat', icon: MessageSquare, label: t('legalChat') },
    { path: '/history', icon: History, label: t('history') },
    { path: '/knowledge', icon: BookOpen, label: t('knowledge') },
  ];

  return (
    <div className="w-64 flex-shrink-0 border-r bg-background hidden md:flex md:flex-col" data-testid="sidebar">
      <div className="p-6 border-b">
        <h1 className="text-2xl font-serif font-bold text-primary" data-testid="app-title">
          {t('appName')}
        </h1>
        <p className="text-xs text-muted-foreground mt-1">{t('tagline')}</p>
      </div>

      <nav className="flex-1 p-4 space-y-1" data-testid="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-sm border-l-2 sidebar-nav-link ${
                isActive ? 'active border-l-primary' : 'border-l-transparent'
              }`}
              data-testid={`nav-${item.path}`}
            >
              <Icon className="h-5 w-5" />
              <span className="text-sm">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t">
        <Button
          variant="outline"
          size="sm"
          onClick={toggleLanguage}
          className="w-full flex items-center justify-center gap-2"
          data-testid="language-toggle"
        >
          <Globe className="h-4 w-4" />
          {language === 'en' ? 'Tagalog' : 'English'}
        </Button>
      </div>
    </div>
  );
};