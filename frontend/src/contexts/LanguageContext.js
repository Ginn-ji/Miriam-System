import React, { createContext, useContext, useState } from 'react';

const LanguageContext = createContext();

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within LanguageProvider');
  }
  return context;
};

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState('en');

  const translations = {
    en: {
      appName: 'Miriam',
      tagline: 'Legal Awareness Support System',
      dashboard: 'Dashboard',
      documents: 'Documents',
      translate: 'Translate',
      legalChat: 'Legal Chat',
      history: 'History',
      knowledge: 'Legal Knowledge',
      uploadDocument: 'Upload Document',
      recentDocuments: 'Recent Documents',
      recentTranslations: 'Recent Translations',
      chatSessions: 'Chat Sessions',
      legalArticles: 'Legal Articles',
      welcome: 'Welcome to Miriam',
      welcomeDesc: 'Your AI-powered Philippine legal assistant',
      noDocuments: 'No documents uploaded yet',
      uploadHere: 'Upload your first document',
      dragDrop: 'Drag and drop or click to upload',
      supportedFormats: 'Supported formats: PDF, TXT',
      translateText: 'Translate Text',
      sourceLanguage: 'Source Language',
      targetLanguage: 'Target Language',
      english: 'English',
      tagalog: 'Tagalog',
      detectLanguage: 'Auto-detect',
      translate_btn: 'Translate',
      translating: 'Translating...',
      original: 'Original',
      translation: 'Translation',
      askLegalQuestion: 'Ask a Legal Question',
      typeMessage: 'Type your legal question here...',
      send: 'Send',
      assistant: 'Legal Assistant',
      you: 'You',
      
    },
    tl: {
      appName: 'Miriam',
      tagline: 'Legal Awareness Support System',
      dashboard: 'Dashboard',
      documents: 'Mga Dokumento',
      translate: 'Isalin',
      legalChat: 'Legal Chat',
      history: 'Kasaysayan',
      knowledge: 'Kaalaman sa Batas',
      uploadDocument: 'Mag-upload ng Dokumento',
      recentDocuments: 'Kamakailang Dokumento',
      recentTranslations: 'Kamakailang Pagsasalin',
      chatSessions: 'Mga Chat Session',
      legalArticles: 'Mga Artikulo ng Batas',
      welcome: 'Maligayang pagdating sa Miriam',
      welcomeDesc: 'Ang iyong AI-powered na tulong legal ng Pilipinas',
      noDocuments: 'Walang naka-upload na dokumento',
      uploadHere: 'Mag-upload ng iyong unang dokumento',
      dragDrop: 'I-drag at i-drop o i-click upang mag-upload',
      supportedFormats: 'Suportadong format: PDF, TXT',
      translateText: 'Isalin ang Teksto',
      sourceLanguage: 'Pinagmulang Wika',
      targetLanguage: 'Target na Wika',
      english: 'Ingles',
      tagalog: 'Tagalog',
      detectLanguage: 'Auto-detect',
      translate_btn: 'Isalin',
      translating: 'Nagsasalin...',
      original: 'Orihinal',
      translation: 'Salin',
      askLegalQuestion: 'Magtanong ng Legal na Katanungan',
      typeMessage: 'I-type ang iyong legal na tanong dito...',
      send: 'Ipadala',
      assistant: 'Legal Assistant',
      you: 'Ikaw',
    },
  };

  const t = (key) => translations[language][key] || key;

  const toggleLanguage = () => {
    setLanguage((prev) => (prev === 'en' ? 'tl' : 'en'));
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, toggleLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};