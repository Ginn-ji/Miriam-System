import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useLanguage } from '../contexts/LanguageContext';
import { Home, MessageSquare, History as HistoryIcon, BookOpen, LogOut, ShieldPlus } from 'lucide-react';

export const Sidebar = ({ user, onLogout }) => {
  const location = useLocation();
  const { t } = useLanguage();

  const getLinkStyle = (path) => {
    const isActive = location.pathname === path;
    return `flex items-center gap-3 px-4 py-2.5 rounded-sm border-l-4 transition-colors ${
      isActive 
        ? 'bg-amber-500/10 text-amber-500 border-amber-500' // Active: Gold accent with subtle gold background
        : 'border-transparent text-slate-300 hover:bg-slate-800/60 hover:text-amber-400' // Inactive: Light gray, hovers to gold
    }`;
  };

  return (
    <div className="w-64 flex-shrink-0 bg-slate-950 border-r border-slate-800 flex flex-col h-full" data-testid="sidebar">
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-2xl font-serif font-bold text-amber-500 tracking-wide" data-testid="app-title">
          {t('appName')}
        </h1>
        <p className="text-xs text-slate-400 mt-1">{t('tagline')}</p>
      </div>

      <nav className="flex-1 p-4 space-y-2" data-testid="sidebar-nav">
        <Link to="/" className={getLinkStyle('/')}>
          <Home className="h-5 w-5" /> <span className="text-sm font-medium">{t('dashboard')}</span>
        </Link>

        <Link to="/chat" className={getLinkStyle('/chat')}>
          <MessageSquare className="h-5 w-5" /> <span className="text-sm font-medium">{t('legalChat')}</span>
        </Link>

        {user.role !== 'guest' && (
          <Link to="/history" className={getLinkStyle('/history')}>
            <HistoryIcon className="h-5 w-5" /> <span className="text-sm font-medium">{t('history')}</span>
          </Link>
        )}

        <Link to="/knowledge" className={getLinkStyle('/knowledge')}>
          <BookOpen className="h-5 w-5" /> <span className="text-sm font-medium">{t('knowledge')}</span>
        </Link>

        {(user.role === 'admin' || user.role === 'super_admin') && (
          <div className="pt-4 mt-4 border-t border-slate-800">
            <Link to="/admin" className={getLinkStyle('/admin')}>
              <ShieldPlus className="h-5 w-5" /> <span className="text-sm font-medium">Admin Dashboard</span>
            </Link>
          </div>
        )}
      </nav>

      <div className="p-4 border-t border-slate-800">
        <button
          onClick={onLogout}
          className="w-full flex items-center justify-center gap-2 px-4 py-2 text-slate-400 hover:bg-slate-900 hover:text-red-400 border border-transparent hover:border-red-900/50 rounded-md transition-all text-sm font-medium"
        >
          <LogOut className="h-4 w-4" />
          Logout ({user.username || user.name || 'Guest'})
        </button>
      </div>
    </div>
  );
};