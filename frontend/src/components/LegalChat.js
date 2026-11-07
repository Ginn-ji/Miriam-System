import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { 
  Send, 
  Bot, 
  BookOpen, 
  ChevronDown, 
  ThumbsUp, 
  ThumbsDown, 
  Sparkles
} from 'lucide-react';
import apiClient from '../api/apiClient';
import { toast } from 'sonner';

// Must match the identifier the backend uses for an article (id, else article no.)
const lawKey = (law) => String(law?.id || law?.article || '');

const formatDate = (iso) =>
  iso
    ? new Date(iso).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
    : '';

// ── Queries list inside the per-article feedback view ───────────────────────
const FeedbackQueryList = ({ items, emptyText, tone }) => {
  if (!items.length) {
    return <p className="text-xs text-slate-400 py-1">{emptyText}</p>;
  }
  const box = tone === 'like'
    ? 'bg-emerald-50/60 border border-emerald-100'
    : 'bg-rose-50/60 border border-rose-100';
  const sub = tone === 'like' ? 'text-emerald-700' : 'text-rose-700';

  return (
    <div className="space-y-2">
      {items.map((item) => (
        <div key={item.message_id} className={`p-2.5 rounded-lg text-xs space-y-1 ${box}`}>
          <p className="font-semibold text-slate-900">"{item.query}"</p>
          {item.translated_query && (
            <p className={`text-[11px] italic ${sub}`}>Processed: {item.translated_query}</p>
          )}
          <span className="text-[10px] text-slate-400 block">{formatDate(item.updated_at)}</span>
        </div>
      ))}
    </div>
  );
};

// ── Per-article feedback: like / dislike / nothing + latest 3 queries ───────
const ArticleFeedback = ({ lawData, messageId, user, sessionId }) => {
  const [vote,           setVote]           = useState(null); // 'like' | 'dislike' | null
  const [submitting,     setSubmitting]     = useState(false);
  const [open,           setOpen]           = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [history,        setHistory]        = useState({ liked: [], disliked: [] });

  const loadHistory = async () => {
    setLoadingHistory(true);
    try {
      const params = { law_id: lawKey(lawData) };
      if (user && user.role !== 'guest') params.user_id = user.id;
      else params.session_id = sessionId;

      const res = await apiClient.get('/chat/feedback/article', { params });
      setHistory({ liked: res.data?.liked || [], disliked: res.data?.disliked || [] });
    } catch (error) {
      console.error('Failed to fetch article feedback:', error);
    } finally {
      setLoadingHistory(false);
    }
  };

  // One vote per query & article: same button again = remove, other button = switch
  const handleVote = async (type) => {
    if (submitting) return;
    setSubmitting(true);
    try {
      const res = await apiClient.post('/chat/feedback/article', {
        message_id: messageId,
        law_id:     lawKey(lawData),
        feedback:   type,
      });
      setVote(res.data.feedback);
      if (open) loadHistory();
    } catch (error) {
      toast.error('Failed to update feedback');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="border-t border-gray-100">
      <div className="flex items-center justify-between gap-2 px-4 py-3">
        <span className="text-[11px] text-slate-500">Is this article relevant to your query?</span>
        <div className="flex items-center gap-1.5">
          <button
            type="button"
            disabled={submitting}
            onClick={() => handleVote('like')}
            className={`p-1.5 rounded transition-colors disabled:opacity-50 ${
              vote === 'like'
                ? 'text-emerald-700 bg-emerald-100 border border-emerald-300'
                : 'text-slate-400 hover:text-slate-600 hover:bg-slate-200'
            }`}
            title="Relevant / Accurate"
          >
            <ThumbsUp className="h-3.5 w-3.5" />
          </button>
          <button
            type="button"
            disabled={submitting}
            onClick={() => handleVote('dislike')}
            className={`p-1.5 rounded transition-colors disabled:opacity-50 ${
              vote === 'dislike'
                ? 'text-rose-700 bg-rose-100 border border-rose-300'
                : 'text-slate-400 hover:text-slate-600 hover:bg-slate-200'
            }`}
            title="Irrelevant / Inaccurate"
          >
            <ThumbsDown className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>

      <details
        className="group border-t border-gray-100"
        onToggle={(e) => {
          const isOpen = e.currentTarget.open;
          setOpen(isOpen);
          if (isOpen) loadHistory();
        }}
      >
        <summary className="flex items-center justify-between p-4 cursor-pointer hover:bg-gray-50 text-xs font-semibold text-gray-500 uppercase tracking-widest list-none">
          <span>View Feedback for this Article</span>
          <ChevronDown className="h-4 w-4 transition-transform group-open:rotate-180" />
        </summary>

        <div className="p-4 pt-2 space-y-4 bg-gray-50/50 border-t border-gray-100">
          {loadingHistory ? (
            <p className="text-xs text-slate-400">Loading...</p>
          ) : (
            <>
              <div>
                <p className="flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-wider text-emerald-700 mb-2">
                  <ThumbsUp className="h-3 w-3" /> Liked queries (latest 3)
                </p>
                <FeedbackQueryList items={history.liked} emptyText="No liked queries yet." tone="like" />
              </div>
              <div>
                <p className="flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-wider text-rose-700 mb-2">
                  <ThumbsDown className="h-3 w-3" /> Disliked queries (latest 3)
                </p>
                <FeedbackQueryList items={history.disliked} emptyText="No disliked queries yet." tone="dislike" />
              </div>
            </>
          )}
        </div>
      </details>
    </div>
  );
};

// ── "How was my query processed?" — word-by-word breakdown ──────────────────
// Why a word was left out of the processed query (codes come from the backend).
const LEFT_OUT_REASONS = [
  { code: 'stopword',       text: 'Common filler words. They don’t help find a law.' },
  { code: 'too_short',      text: 'Too short to be meaningful.' },
  { code: 'not_in_vocab',   text: 'Not found anywhere in the Labor Code text.' },
  { code: 'no_close_match', text: 'Not found in the Labor Code text, and no close spelling match.' },
  { code: 'translated',     text: 'Tagalog words, replaced by their English translation (shown beside the word).' },
];

const WORD_CHIP = 'px-1.5 py-0.5 rounded border text-[11px]';

const QueryBreakdown = ({ messageId }) => {
  const [trace,   setTrace]   = useState(null);
  const [loading, setLoading] = useState(false);
  const [failed,  setFailed]  = useState(false);

  const load = async () => {
    if (trace || loading) return;
    setLoading(true);
    setFailed(false);
    try {
      const res = await apiClient.get(`/chat/trace/${messageId}`);
      setTrace(res.data);
    } catch (error) {
      setFailed(true);
    } finally {
      setLoading(false);
    }
  };

  const words    = trace?.words || [];
  const phrases  = trace?.phrases || [];
  const fillers  = trace?.fillers_removed || [];
  const leftOut  = LEFT_OUT_REASONS
    .map(r => ({ ...r, items: words.filter(w => w.status === 'dropped' && w.reason === r.code).map(w => w.word) }))
    .filter(r => r.items.length > 0);

  const renderWord = (w, i) => {
    const hasTranslation = w.translations && w.translations.length > 0;

    // Tagalog word replaced by English terms: show them right beside the word
    if (w.reason === 'translated') {
      return (
        <span key={i} className={`${WORD_CHIP} bg-sky-50 border-sky-200 text-sky-800`}>
          {w.word} <span className="text-sky-500">→</span> <span className="font-semibold">{w.translations.join(', ')}</span>
        </span>
      );
    }

    const chipTone =
      w.status === 'kept'      ? 'bg-emerald-50 border-emerald-200 text-emerald-800'
      : w.status === 'corrected' ? 'bg-amber-50 border-amber-200 text-amber-800'
      : 'bg-slate-100 border-slate-200 text-slate-400 line-through';

    return (
      <span key={i} className="inline-flex items-center gap-1">
        <span className={`${WORD_CHIP} ${chipTone}`}>
          {w.status === 'corrected' ? `${w.word} → ${w.corrected_to}` : w.word}
        </span>
        {hasTranslation && (
          <span className={`${WORD_CHIP} bg-sky-50 border-sky-200 text-sky-800`}>
            <span className="text-sky-500">→</span> <span className="font-semibold">{w.translations.join(', ')}</span>
          </span>
        )}
      </span>
    );
  };

  return (
    <details
      className="group mt-2"
      onToggle={(e) => { if (e.currentTarget.open) load(); }}
    >
      <summary className="flex items-center gap-1 cursor-pointer text-slate-500 hover:text-slate-700 font-medium list-none">
        <ChevronDown className="h-3 w-3 transition-transform -rotate-90 group-open:rotate-0" />
        How was my query processed?
      </summary>

      <div className="mt-2 p-3 bg-white border border-slate-200 rounded-lg space-y-3">
        {loading && <p className="text-slate-400">Loading...</p>}
        {failed && <p className="text-slate-400">Breakdown isn’t available for this message.</p>}

        {trace && (
          <>
            {/* Your words, in order, with translations beside them */}
            <div>
              <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">
                Your query, word by word
              </p>
              <div className="flex flex-wrap items-center gap-1.5">
                {words.map(renderWord)}
              </div>
              <p className="text-[10px] text-slate-400 mt-1.5">
                Green: used in the search · Gray, struck through: left out · Blue: replaced by its English translation
              </p>
            </div>

            {/* Whole-phrase translations */}
            {phrases.length > 0 && (
              <div>
                <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">
                  Phrase translations
                </p>
                <div className="space-y-1">
                  {phrases.map((p, i) => (
                    <p key={i} className="text-slate-700">
                      “{p.phrase}” <span className="text-sky-500">→</span>{' '}
                      <span className="font-semibold text-sky-800">{p.english.join(', ')}</span>
                    </p>
                  ))}
                </div>
              </div>
            )}

            {/* Full-sentence translation, when one was cached */}
            {trace.cached_translation && (
              <div>
                <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">
                  Full translation
                </p>
                <p className="text-slate-700 italic">“{trace.cached_translation}”</p>
              </div>
            )}

            {/* Why words were left out */}
            {(leftOut.length > 0 || fillers.length > 0) && (
              <div>
                <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">
                  Why some words were left out
                </p>
                <div className="space-y-1.5">
                  {fillers.length > 0 && (
                    <p className="text-slate-700">
                      <span className="font-semibold">{fillers.map(f => `“${f}”`).join(', ')}</span>
                      <span className="text-slate-500"> — conversational phrases, removed before searching.</span>
                    </p>
                  )}
                  {leftOut.map(r => (
                    <p key={r.code} className="text-slate-700">
                      <span className="font-semibold">{r.items.join(', ')}</span>
                      <span className="text-slate-500"> — {r.text}</span>
                    </p>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </details>
  );
};

// ── Law Result Card ──────────────────────────────────────────────────────────
// Feedback is opt-in (showFeedback). Other screens that reuse this card,
// such as the chat history, don't pass it, so they show no feedback controls.
export const LawResultCard = ({ lawData, showFeedback = false, messageId, user, sessionId }) => {
  const accuracyStr = lawData?.accuracy ?? null;
  const pct = accuracyStr ? parseInt(accuracyStr.replace('%', ''), 10) : null;

  const badgeClass = pct === null
    ? null
    : pct >= 75
      ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
      : pct >= 50
        ? 'bg-amber-100 text-amber-800 border border-amber-200'
        : 'bg-red-100 text-red-800 border border-red-200';

  return (
    <Card className="mt-4 mb-2 shadow-sm border border-gray-200 overflow-hidden w-full text-left bg-white">
      {/* Header: title + accuracy badge */}
      <div className="p-4 border-b bg-gray-50 flex items-center justify-between gap-2">
        <div className="flex items-center gap-2 flex-1 min-w-0">
          <BookOpen className="h-5 w-5 text-primary shrink-0" />
          <h3 className="font-serif font-bold text-lg text-gray-900 truncate">
            {lawData.article ? `${lawData.article}: ${lawData.title}` : lawData.title}
          </h3>
        </div>
        {pct !== null && badgeClass && (
          <span className={`shrink-0 text-xs font-bold px-2.5 py-1 rounded-full ${badgeClass}`}>
            {accuracyStr} Match
          </span>
        )}
      </div>

      {/* Best matching chunk */}
      <div className="p-0">
        {lawData.best_match_chunk && (
          <div className="p-4">
            <p className="text-[10px] font-bold uppercase tracking-wider text-gray-400 mb-1">
              Relevant Section:
            </p>
            <div className="pl-3 border-l-4 border-gray-200 italic text-gray-900 text-base leading-relaxed">
              "{lawData.best_match_chunk}"
            </div>
          </div>
        )}

        {/* Full article collapsible */}
        <details className="group border-t border-gray-100">
          <summary className="flex items-center justify-between p-4 cursor-pointer hover:bg-gray-50 text-xs font-semibold text-gray-500 uppercase tracking-widest list-none">
            <span>View Full Article</span>
            <ChevronDown className="h-4 w-4 transition-transform group-open:rotate-180" />
          </summary>
          <div className="p-4 pt-2 text-sm text-gray-600 whitespace-pre-wrap bg-gray-50/50 leading-relaxed border-t border-gray-100">
            {lawData.chunks
              ? (Array.isArray(lawData.chunks) ? lawData.chunks.join('\n\n') : lawData.chunks)
              : 'Full text not available.'}
          </div>
        </details>

        {/* Per-article feedback (chat screen only) */}
        {showFeedback && messageId && (
          <ArticleFeedback
            lawData={lawData}
            messageId={messageId}
            user={user}
            sessionId={sessionId}
          />
        )}
      </div>
    </Card>
  );
};

// ── Legal Chat Component ─────────────────────────────────────────────────────
export const LegalChat = ({ user }) => {
  const { t } = useLanguage();
  const [messages,  setMessages]  = useState([]);
  const [input,     setInput]     = useState('');
  const [loading,   setLoading]   = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => { 
    setSessionId(`session_${Date.now()}`); 
  }, []);

  useEffect(() => { 
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); 
  }, [messages, loading]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const currentMsg = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: currentMsg }]);

    const formData = new FormData();
    formData.append('message',    currentMsg);
    formData.append('session_id', sessionId);
    if (user && user.role !== 'guest') formData.append('user_id', user.id);

    setInput('');
    setLoading(true);

    try {
      const response = await apiClient.post('/chat', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setMessages(prev => [...prev, {
        id:               response.data.message_id,
        role:             'assistant',
        content:          response.data.response,
        translated_query: response.data.translated_query,
        laws:             response.data.laws || [],
      }]);
    } catch (error) {
      toast.error('Failed to get response');
      setMessages(prev => [...prev, {
        role:    'assistant',
        content: 'Error: Could not connect to the server.',
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full min-h-[calc(100vh-120px)]">
      <div className="mb-4">
        <h1 className="text-4xl font-serif font-bold tracking-tight text-primary">
          Labor Code Retrieval
        </h1>
        <p className="text-muted-foreground mt-1">
          Ask LACBot questions related to Philippine Labor Code
        </p>
      </div>

      <div className="flex-1 flex flex-col min-h-0 mb-2">
        {/* ── MAIN CHAT AREA ────────────────────────────────────────────── */}
        <Card className="flex-1 flex flex-col shadow-lg overflow-hidden border-gray-200">
          <CardHeader className="border-b bg-white py-3">
            <CardTitle className="font-serif flex items-center gap-2 text-lg">
              <Bot className="h-5 w-5 text-primary" /> LACBot Assistant
            </CardTitle>
          </CardHeader>

          <CardContent className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-50">
            {messages.length === 0 && (
              <div className="text-center py-20 text-slate-400 text-sm">
                Enter your inquiry in English, Tagalog, or Taglish to retrieve relevant Labor Code provisions.
              </div>
            )}

            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex w-full ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-[90%] ${
                  msg.role === 'user'
                    ? 'w-fit bg-[#1e293b] text-white px-4 py-3 rounded-2xl rounded-tr-none shadow-sm'
                    : 'w-full'
                }`}>
                  {/* Message content */}
                  {msg.role === 'assistant' ? (
                    <p className="text-sm text-slate-900 leading-relaxed mb-1">{msg.content}</p>
                  ) : (
                    <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                  )}

                  {/* Translated Query Badge */}
                  {msg.role === 'assistant' && msg.translated_query && (
                    <div className="mt-2 pt-2 border-t border-slate-200/60 text-xs">
                      <div className="flex flex-wrap items-center gap-2">
                        <div className="inline-flex items-center gap-1.5 text-slate-600 bg-white px-2 py-1 rounded border border-slate-200">
                          <Sparkles className="h-3 w-3 text-amber-500 shrink-0" />
                          <span className="font-medium text-slate-700">Processed Query:</span>
                          <span className="italic">"{msg.translated_query}"</span>
                        </div>
                      </div>
                      {msg.id && <QueryBreakdown messageId={msg.id} />}
                    </div>
                  )}

                  {/* Matched Laws (each article has its own feedback) */}
                  {msg.role === 'assistant' && msg.laws?.map((law, i) => (
                    <LawResultCard
                      key={i}
                      lawData={law}
                      showFeedback
                      messageId={msg.id}
                      user={user}
                      sessionId={sessionId}
                    />
                  ))}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex items-center gap-2 text-xs text-slate-500 py-2">
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-primary border-t-transparent" />
                Analyzing legal corpus &amp; calculating relevance...
              </div>
            )}
            <div ref={messagesEndRef} />
          </CardContent>

          <div className="border-t p-4 bg-white">
            <div className="flex gap-2 items-center">
              <Textarea
                value={input}
                onChange={e => setInput(e.target.value)}
                placeholder="Type your question about Labor Code..."
                className="min-h-[60px] max-h-[120px] resize-none focus-visible:ring-primary flex-1"
                onKeyDown={e => {
                  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
                }}
              />
              <Button
                onClick={handleSend}
                disabled={loading || !input.trim()}
                className="px-6 h-[60px] shadow-sm"
              >
                <Send className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};