import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader } from './ui/card';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { BookOpen, Search, ChevronDown, ChevronUp, Calendar, Tag, ChevronLeft, ChevronRight, ExternalLink, Loader2 } from 'lucide-react';
import apiClient from '../api/apiClient';
import { toast } from 'sonner';

const LAWS_PER_PAGE = 20;

const BOOKS = [
  { value: 'all',               label: 'All Books' },
  { value: 'Preliminary Title', label: 'Preliminary Title' },
  { value: 'Book I',            label: 'Book I — Pre-Employment' },
  { value: 'Book II',           label: 'Book II — Human Resources Development' },
  { value: 'Book III',          label: 'Book III — Conditions of Employment' },
  { value: 'Book IV',           label: 'Book IV — Health, Safety & Social Welfare' },
  { value: 'Book V',            label: 'Book V — Labor Relations' },
  { value: 'Book VI',           label: 'Book VI — Post-Employment' },
  { value: 'Book VII',          label: 'Book VII — Transitory & Final Provisions' },
];

const getBookLabel = (category) =>
  BOOKS.find(b => b.value === category)?.label || category || 'Uncategorized';

// ==================== MAIN KNOWLEDGE COMPONENT ====================
export const Knowledge = ({ user }) => {
  const { t } = useLanguage();

  // ── Server-side paginated state ─────────────────────────────
  const [laws, setLaws]           = useState([]);
  const [total, setTotal]         = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading]     = useState(false);
  // ───────────────────────────────────────────────────────────

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedBook, setSelectedBook] = useState('all');
  const [expandedId, setExpandedId]   = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showDeleteForm, setShowDeleteForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [uploadFile, setUploadFile]   = useState(null);
  const [selectedIds, setSelectedIds] = useState([]);
  const [pageInput, setPageInput]     = useState('');
  const [newLaw, setNewLaw] = useState({
    article: '', title: '', category: 'Book I', content: '', tags: '', language: 'en'
  });
  const [editingLaw, setEditingLaw] = useState(null);
  const lawFileInputRef   = useRef(null);
  const searchDebounceRef = useRef(null);
  const isStaff = user?.role === 'admin' || user?.role === 'super_admin';

  // ── Core fetch — only requests 20 laws from backend ────────
  const fetchLaws = useCallback(async (page, search, book) => {
    setLoading(true);
    try {
      const params = {
        skip:  (page - 1) * LAWS_PER_PAGE,
        limit: LAWS_PER_PAGE,
      };
      if (search && search.trim()) params.q = search.trim();
      if (book && book !== 'all')   params.category = book;

      const response = await apiClient.get('/legal-knowledge', { params });
      setLaws(response.data.laws   || []);
      setTotal(response.data.total || 0);
    } catch (error) {
      console.error('Error fetching laws:', error);
    } finally {
      setLoading(false);
    }
  }, []);
  // ───────────────────────────────────────────────────────────

  // Load first page on mount
  useEffect(() => {
    fetchLaws(1, '', 'all');
  }, [fetchLaws]);

  // Search: debounced, resets to page 1
  const handleSearchChange = (value) => {
    setSearchQuery(value);
    if (searchDebounceRef.current) clearTimeout(searchDebounceRef.current);
    searchDebounceRef.current = setTimeout(() => {
      setCurrentPage(1);
      fetchLaws(1, value, selectedBook);
    }, 400);
  };

  // Book filter: immediate, resets to page 1
  const handleBookChange = (book) => {
    setSelectedBook(book);
    setCurrentPage(1);
    fetchLaws(1, searchQuery, book);
  };

  // Page navigation
  const totalPages = Math.max(1, Math.ceil(total / LAWS_PER_PAGE));

  const goToPage = (page) => {
    const clamped = Math.max(1, Math.min(page, totalPages));
    setCurrentPage(clamped);
    setExpandedId(null);
    fetchLaws(clamped, searchQuery, selectedBook);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handlePageInputKeyDown = (e) => {
    if (e.key === 'Enter') {
      const p = parseInt(pageInput, 10);
      if (!isNaN(p)) goToPage(p);
      setPageInput('');
      e.target.blur();
    }
  };
  const handlePageInputBlur = () => {
    const p = parseInt(pageInput, 10);
    if (!isNaN(p)) goToPage(p);
    setPageInput('');
  };

  // ── Activity logger ──────────────────────────────────────────
  const logActivity = async (action, articleTitle) => {
    if (!user || user.role === 'guest') return;
    try {
      await apiClient.post('/admin/activity-log', {
        admin_id: user.id, admin_username: user.username,
        action, article_title: articleTitle,
      });
    } catch (_) {}
  };
  // ───────────────────────────────────────────────────────────

  const toggleExpand = (id) => setExpandedId(expandedId === id ? null : id);

  const handleAddLaw = async () => {
    if (!newLaw.title) { toast.error('Please enter a title'); return; }
    try {
      if (uploadFile) {
        const fd = new FormData();
        fd.append('file', uploadFile); fd.append('title', newLaw.title);
        fd.append('category', newLaw.category); fd.append('tags', newLaw.tags); fd.append('language', newLaw.language);
        await apiClient.post('/legal-knowledge/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
      } else {
        if (!newLaw.content) { toast.error('Please enter content or upload a file'); return; }
        await apiClient.post('/legal-knowledge', { ...newLaw, tags: newLaw.tags.split(',').map(t => t.trim()).filter(t => t) });
      }
      await logActivity('ADD', newLaw.title);
      setShowAddForm(false); setUploadFile(null);
      setNewLaw({ article: '', title: '', category: 'Book I', content: '', tags: '', language: 'en' });
      fetchLaws(currentPage, searchQuery, selectedBook);
      toast.success('Legal article added successfully!');
    } catch { toast.error('Failed to add legal article'); }
  };

  const handleUpdateLaw = async () => {
    if (!editingLaw.title) { toast.error('Please enter a title'); return; }
    try {
      await apiClient.put(`/legal-knowledge/${editingLaw.id}`, {
        ...editingLaw,
        tags: typeof editingLaw.tags === 'string'
          ? editingLaw.tags.split(',').map(t => t.trim()).filter(t => t)
          : editingLaw.tags
      });
      await logActivity('EDIT', editingLaw.title);
      setShowEditForm(false); setEditingLaw(null);
      fetchLaws(currentPage, searchQuery, selectedBook);
      toast.success('Legal article updated successfully!');
    } catch { toast.error('Failed to update legal article'); }
  };

  const handleSelectCheckbox = (id) =>
    setSelectedIds(prev => prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]);

  const handleBulkDelete = async () => {
    if (selectedIds.length === 0) return;
    if (!window.confirm(`Delete ${selectedIds.length} laws?`)) return;
    try {
      const titles = laws.filter(l => selectedIds.includes(l.id)).map(l => l.title).join(', ');
      await apiClient.post('/legal-knowledge/bulk-delete', { ids: selectedIds });
      await logActivity('DELETE (bulk)', titles);
      toast.success('Selected laws deleted!');
      setSelectedIds([]); setShowDeleteForm(false);
      fetchLaws(1, searchQuery, selectedBook);
    } catch { toast.error('Failed to delete selected laws'); }
  };

  const handleDeleteAll = async () => {
    if (!window.confirm('⚠️ WARNING: Delete ALL legal articles?')) return;
    try {
      await apiClient.delete('/legal-knowledge/delete-all');
      await logActivity('DELETE ALL', '(all articles)');
      toast.success('All laws deleted!');
      setSelectedIds([]); setShowDeleteForm(false);
      setCurrentPage(1); setTotal(0); setLaws([]);
    } catch { toast.error('Failed to clear database'); }
  };

  // Edit form book options — includes legacy DB categories
  const editBookOptions = BOOKS.filter(b => b.value !== 'all');

  return (
    <div className="space-y-6" data-testid="knowledge-page">
      <div className="page-header">
        <div>
          <h1 className="page-title" data-testid="knowledge-title">{t('knowledge')}</h1>
          <p className="page-subtitle">Browse Philippine Labor Code articles and statutes</p>
          <a href="https://dole.gov.ph/labor-code-of-the-philippines-2/" target="_blank" rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-xs text-primary hover:underline mt-1">
            <ExternalLink className="h-3 w-3" />
            Source: DOLE — Labor Code of the Philippines
          </a>
        </div>
        {isStaff && (
          <div className="header-actions">
            <button onClick={() => { setShowAddForm(!showAddForm); setShowDeleteForm(false); setShowEditForm(false); }} className="btn-header-primary">
              {showAddForm ? 'Cancel' : '+ Add Labor Code'}
            </button>
            <button onClick={() => { setShowDeleteForm(!showDeleteForm); setShowAddForm(false); setShowEditForm(false); }} className="btn-header-destructive">
              {showDeleteForm ? 'Cancel' : '🗑 Delete Labor Code'}
            </button>
          </div>
        )}
      </div>

      {/* EDIT FORM */}
      {showEditForm && isStaff && editingLaw && (
        <Card className="edit-card">
          <CardContent className="pt-6 space-y-3">
            <h3 className="edit-card-title">Edit Legal Article</h3>
            <Input placeholder="Article Number (e.g., Art. 82)" value={editingLaw.article || ''} onChange={(e) => setEditingLaw({...editingLaw, article: e.target.value})} />
            <Input placeholder="Title" value={editingLaw.title || ''} onChange={(e) => setEditingLaw({...editingLaw, title: e.target.value})} />
            <Select value={editingLaw.category || ''} onValueChange={(val) => setEditingLaw({...editingLaw, category: val})}>
              <SelectTrigger><SelectValue placeholder="Select Book" /></SelectTrigger>
              <SelectContent>
                {editBookOptions.map((book) => (
                  <SelectItem key={book.value} value={book.value}>{book.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Input placeholder="Tags (comma separated)"
              value={Array.isArray(editingLaw.tags) ? editingLaw.tags.join(', ') : (editingLaw.tags || '')}
              onChange={(e) => setEditingLaw({...editingLaw, tags: e.target.value})} />
            <textarea placeholder="Content" value={editingLaw.content || ''} onChange={(e) => setEditingLaw({...editingLaw, content: e.target.value})} className="textarea-field" />
            <div className="form-actions">
              <button onClick={handleUpdateLaw} className="btn-amber">Save Changes</button>
              <button onClick={() => { setShowEditForm(false); setEditingLaw(null); }} className="btn-muted">Cancel</button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* ADD LAW FORM */}
      {showAddForm && isStaff && (
        <Card className="card-elevated">
          <CardContent className="pt-6 space-y-3">
            <h3 className="font-serif font-semibold">Add New Legal Article</h3>
            <Input placeholder="Article Number (e.g., Art. 82)" value={newLaw.article} onChange={(e) => setNewLaw({...newLaw, article: e.target.value})} />
            <Input placeholder="Title" value={newLaw.title} onChange={(e) => setNewLaw({...newLaw, title: e.target.value})} />
            <Select value={newLaw.category} onValueChange={(val) => setNewLaw({...newLaw, category: val})}>
              <SelectTrigger><SelectValue placeholder="Select Book" /></SelectTrigger>
              <SelectContent>
                {BOOKS.filter(b => b.value !== 'all' && !['Labor Law','Civil Law','Criminal Law','Family Law','Privacy Law'].includes(b.value)).map((book) => (
                  <SelectItem key={book.value} value={book.value}>{book.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Input placeholder="Tags (comma separated)" value={newLaw.tags} onChange={(e) => setNewLaw({...newLaw, tags: e.target.value})} />
            {!uploadFile ? (
              <>
                <textarea placeholder="Content (or upload a PDF/text file below)" value={newLaw.content} onChange={(e) => setNewLaw({...newLaw, content: e.target.value})} className="textarea-field-sm" />
                <div className="upload-dropzone">
                  <input type="file" hidden ref={lawFileInputRef} accept=".pdf,.txt" onChange={(e) => { setUploadFile(e.target.files[0]); setNewLaw({...newLaw, content: ''}); }} />
                  <p className="upload-hint">Or upload a PDF/text file instead of typing</p>
                  <button onClick={() => lawFileInputRef.current.click()} className="btn-choose-file">Choose File (.pdf or .txt)</button>
                </div>
              </>
            ) : (
              <div className="upload-file-row">
                <span className="upload-file-name">📎 {uploadFile.name}</span>
                <button onClick={() => setUploadFile(null)} className="link-remove">Remove</button>
              </div>
            )}
            <div className="form-actions">
              <button onClick={handleAddLaw} className="btn-save-law">Save</button>
              <button onClick={() => { setShowAddForm(false); setUploadFile(null); setNewLaw({ article: '', title: '', category: 'Book I', content: '', tags: '', language: 'en' }); }} className="btn-muted">Cancel</button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* BULK DELETE BAR */}
      {showDeleteForm && isStaff && (
        <Card className="bulk-bar">
          <CardContent className="bulk-bar-body">
            <div>
              <h3 className="bulk-title">Article Deletion</h3>
              <p className="bulk-desc">Select checkboxes from the list or delete all.</p>
            </div>
            <div className="bulk-actions">
              <button onClick={handleBulkDelete} disabled={selectedIds.length === 0} className="btn-delete-selected">Delete Selected ({selectedIds.length})</button>
              <button onClick={handleDeleteAll} className="btn-delete-all">Delete All Laws</button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* SEARCH AND LISTINGS */}
      <Card className="card-elevated">
        <CardHeader>
          <div className="search-toolbar">
            <div className="search-input-group">
              <Search className="icon-5 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search by article number or title..."
                value={searchQuery}
                onChange={(e) => handleSearchChange(e.target.value)}
                className="search-input"
              />
            </div>
            <Select value={selectedBook} onValueChange={handleBookChange}>
              <SelectTrigger className="w-[260px]" data-testid="book-filter">
                <SelectValue placeholder="All Books" />
              </SelectTrigger>
              <SelectContent>
                {BOOKS.map((book) => (
                  <SelectItem key={book.value} value={book.value}>{book.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardHeader>

        <CardContent>
          {/* Loading state */}
          {loading ? (
            <div className="flex items-center justify-center py-16 gap-2 text-muted-foreground">
              <Loader2 className="h-5 w-5 animate-spin" />
              <span className="text-sm">Loading articles...</span>
            </div>
          ) : laws.length > 0 ? (
            <>
              {/* Results info */}
              <div className="flex items-center justify-between mb-3 text-sm text-muted-foreground">
                <span>
                  Showing {((currentPage - 1) * LAWS_PER_PAGE) + 1}–{Math.min(currentPage * LAWS_PER_PAGE, total)} of {total} articles
                </span>
                <span>Page {currentPage} of {totalPages}</span>
              </div>

              <div className="law-list">
                {laws.map((law) => (
                  <div key={law.id} className="law-item" data-testid="law-item">
                    {isStaff && showDeleteForm && (
                      <input type="checkbox" checked={selectedIds.includes(law.id)} onChange={() => handleSelectCheckbox(law.id)} className="law-checkbox" />
                    )}
                    <div className="flex-1">
                      <div className="law-row" onClick={() => toggleExpand(law.id)}>
                        <div className="law-title-group">
                          <BookOpen className="icon-4 text-primary flex-shrink-0" />
                          <div>
                            <h3 className="law-title">{law.title}</h3>
                            <span className="law-category-label">{getBookLabel(law.category)}</span>
                          </div>
                        </div>
                        <div className="law-badges">
                          {expandedId === law.id ? <ChevronUp className="icon-4 text-muted-foreground" /> : <ChevronDown className="icon-4 text-muted-foreground" />}
                        </div>
                      </div>

                      {expandedId === law.id && (
                        <div className="law-detail">
                          <div>
                            <p className="law-detail-label">Content</p>
                            <p className="law-content-text">{law.content}</p>
                          </div>
                          <div>
                            <div className="law-tag-header">
                              <Tag className="icon-3 text-muted-foreground" />
                              <p className="law-detail-label">Tags</p>
                            </div>
                            <div className="law-tags">
                              {(law.tags || []).map((tag, idx) => <span key={idx} className="law-tag">{tag}</span>)}
                            </div>
                          </div>
                          <div className="law-footer">
                            <span className="law-category-badge">{getBookLabel(law.category)}</span>
                            <div className="law-meta">
                              {isStaff && (
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    setEditingLaw({ ...law, tags: Array.isArray(law.tags) ? law.tags.join(', ') : (law.tags || '') });
                                    setShowEditForm(true); setShowAddForm(false); setShowDeleteForm(false);
                                    window.scrollTo({ top: 0, behavior: 'smooth' });
                                  }}
                                  className="btn-edit-law"
                                >
                                  Edit Labor Code
                                </button>
                              )}
                              <div className="law-date">
                                <Calendar className="icon-3" />
                                <span>Added: {new Date(law.created_at).toLocaleDateString()}</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="flex items-center justify-center gap-2 mt-6 pt-4 border-t flex-wrap">
                  <button onClick={() => goToPage(currentPage - 1)} disabled={currentPage === 1 || loading}
                    className="p-2 rounded-md border hover:bg-muted disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                    <ChevronLeft className="h-4 w-4" />
                  </button>

                  {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => {
                    const show = page === 1 || page === totalPages || Math.abs(page - currentPage) <= 1;
                    const ellBefore = page === currentPage - 2 && currentPage > 3;
                    const ellAfter  = page === currentPage + 2 && currentPage < totalPages - 2;
                    if (ellBefore) return <span key={`eb${page}`} className="px-1 text-muted-foreground">…</span>;
                    if (ellAfter)  return <span key={`ea${page}`} className="px-1 text-muted-foreground">…</span>;
                    if (!show) return null;
                    return (
                      <button key={page} onClick={() => goToPage(page)} disabled={loading}
                        className={`min-w-[36px] h-9 px-3 rounded-md border text-sm font-medium transition-colors ${currentPage === page ? 'bg-primary text-primary-foreground border-primary' : 'hover:bg-muted'}`}>
                        {page}
                      </button>
                    );
                  })}

                  <div className="flex items-center gap-1 ml-2">
                    <span className="text-xs text-muted-foreground">Go to</span>
                    <input type="number" min={1} max={totalPages} value={pageInput}
                      onChange={(e) => setPageInput(e.target.value)}
                      onKeyDown={handlePageInputKeyDown} onBlur={handlePageInputBlur}
                      placeholder="pg"
                      className="w-14 h-9 px-2 text-sm text-center border rounded-md focus:outline-none focus:ring-2 focus:ring-primary bg-background" />
                  </div>

                  <button onClick={() => goToPage(currentPage + 1)} disabled={currentPage === totalPages || loading}
                    className="p-2 rounded-md border hover:bg-muted disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                    <ChevronRight className="h-4 w-4" />
                  </button>
                </div>
              )}
            </>
          ) : (
            <div className="empty-state" data-testid="empty-knowledge">
              <BookOpen className="empty-state-icon" />
              <p className="text-muted-foreground">
                {searchQuery
                  ? `No results for "${searchQuery}"`
                  : selectedBook !== 'all'
                  ? `No articles in ${getBookLabel(selectedBook)} yet.`
                  : 'No legal articles found'}
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};