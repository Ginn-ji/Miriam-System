import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useLanguage } from '../contexts/LanguageContext';
import { Button } from './ui/button';
import { 
  Home, 
  MessageSquare, 
  History as HistoryIcon, 
  BookOpen,
  LogOut
} from 'lucide-react';

export const Sidebar = ({ user, onLogout }) => {
  const location = useLocation();
  const { t } = useLanguage();

  return (
    // REMOVED 'hidden md:flex' and ADDED 'flex flex-col h-full'
    <div className="w-64 flex-shrink-0 border-r bg-background flex flex-col h-full" data-testid="sidebar">
      <div className="p-6 border-b">
        <h1 className="text-2xl font-serif font-bold text-primary" data-testid="app-title">
          {t('appName')}
        </h1>
        <p className="text-xs text-muted-foreground mt-1">{t('tagline')}</p>
      </div>

      <nav className="flex-1 p-4 space-y-1" data-testid="sidebar-nav">
        <Link
          to="/"
          className={`flex items-center gap-3 px-3 py-2.5 rounded-sm border-l-2 sidebar-nav-link ${
            location.pathname === '/' ? 'active border-l-primary' : 'border-l-transparent'
          }`}
        >
          <Home className="h-5 w-5" />
          <span className="text-sm">{t('dashboard')}</span>
        </Link>

        <Link
          to="/chat"
          className={`flex items-center gap-3 px-3 py-2.5 rounded-sm border-l-2 sidebar-nav-link ${
            location.pathname === '/chat' ? 'active border-l-primary' : 'border-l-transparent'
          }`}
        >
          <MessageSquare className="h-5 w-5" />
          <span className="text-sm">{t('legalChat')}</span>
        </Link>

        {/* Hide History for guests */}
        {user.role !== 'guest' && (
          <Link
            to="/history"
            className={`flex items-center gap-3 px-3 py-2.5 rounded-sm border-l-2 sidebar-nav-link ${
              location.pathname === '/history' ? 'active border-l-primary' : 'border-l-transparent'
            }`}
          >
            <HistoryIcon className="h-5 w-5" />
            <span className="text-sm">{t('history')}</span>
          </Link>
        )}

        {/* Knowledge visible to all roles */}
        <Link
          to="/knowledge"
          className={`flex items-center gap-3 px-3 py-2.5 rounded-sm border-l-2 sidebar-nav-link ${
            location.pathname === '/knowledge' ? 'active border-l-primary' : 'border-l-transparent'
          }`}
        >
          <BookOpen className="h-5 w-5" />
          <span className="text-sm">{t('knowledge')}</span>
        </Link>
      </nav>

      <div className="p-4 border-t space-y-2">
        <Button
          variant="ghost"
          size="sm"
          onClick={onLogout}
          className="w-full flex items-center justify-center gap-2 text-destructive"
        >
          <LogOut className="h-4 w-4" />
          Logout ({user.username || user.name || 'Guest'})
        </Button>
      </div>
    </div>
  );
};