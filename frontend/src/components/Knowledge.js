import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader } from './ui/card';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { BookOpen, Search, ChevronDown, ChevronUp, Calendar, Tag, ChevronLeft, ChevronRight, ExternalLink } from 'lucide-react';
import apiClient from '../api/apiClient';
import { toast } from 'sonner';

const LAWS_PER_PAGE = 20;

// Labor Code of the Philippines — Books
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

// ==================== MAIN KNOWLEDGE COMPONENT ====================
export const Knowledge = ({ user }) => {
  const { t } = useLanguage();
  const [allLaws, setAllLaws] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedBook, setSelectedBook] = useState('all');
  const [expandedId, setExpandedId] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showDeleteForm, setShowDeleteForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [uploadFile, setUploadFile] = useState(null);
  const [selectedIds, setSelectedIds] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageInput, setPageInput] = useState('');

  const [newLaw, setNewLaw] = useState({
    article: '', title: '', category: 'Book I', content: '', tags: '', language: 'en'
  });
  const [editingLaw, setEditingLaw] = useState(null);
  const lawFileInputRef = useRef(null);
  const isStaff = user?.role === 'admin' || user?.role === 'super_admin';

  // Fetch all laws when book filter changes
  useEffect(() => {
    fetchLaws();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedBook]);

  const fetchLaws = async () => {
    try {
      const params = {};
      if (selectedBook !== 'all') params.category = selectedBook;
      const response = await apiClient.get('/legal-knowledge', { params });
      setAllLaws(response.data.laws || []);
    } catch (error) {
      console.error('Error fetching laws:', error);
    }
  };

  // ── Client-side search: title + article number only ────────
  const filteredLaws = allLaws.filter((law) => {
    if (!searchQuery.trim()) return true;
    const q = searchQuery.toLowerCase();
    return (
      law.title?.toLowerCase().includes(q) ||
      law.article?.toLowerCase().includes(q)
    );
  });
  // ──────────────────────────────────────────────────────────

  const sortedLaws = [...filteredLaws].sort((a, b) => {
    const getNum = (str) => {
      if (!str) return 999999;
      const match = str.match(/\d+/);
      return match ? parseInt(match[0], 10) : 999999;
    };
    const numA = getNum(a.article || a.title);
    const numB = getNum(b.article || b.title);
    if (numA !== numB) return numA - numB;
    return (a.title || '').localeCompare(b.title || '');
  });

  // Pagination — clamp instead of reset
  const totalPages = Math.max(1, Math.ceil(sortedLaws.length / LAWS_PER_PAGE));
  const clampedPage = Math.min(currentPage, totalPages);
  const paginatedLaws = sortedLaws.slice(
    (clampedPage - 1) * LAWS_PER_PAGE,
    clampedPage * LAWS_PER_PAGE
  );

  const goToPage = (page) => {
    const clamped = Math.max(1, Math.min(page, totalPages));
    setCurrentPage(clamped);
    setExpandedId(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handlePageInputKeyDown = (e) => {
    if (e.key === 'Enter') {
      const page = parseInt(pageInput, 10);
      if (!isNaN(page)) goToPage(page);
      setPageInput('');
      e.target.blur();
    }
  };
  const handlePageInputBlur = () => {
    const page = parseInt(pageInput, 10);
    if (!isNaN(page)) goToPage(page);
    setPageInput('');
  };

  const toggleExpand = (id) => setExpandedId(expandedId === id ? null : id);

  const handleAddLaw = async () => {
    if (!newLaw.title) { toast.error('Please enter a title'); return; }
    try {
      if (uploadFile) {
        const formData = new FormData();
        formData.append('file', uploadFile);
        formData.append('title', newLaw.title);
        formData.append('category', newLaw.category);
        formData.append('tags', newLaw.tags);
        formData.append('language', newLaw.language);
        await apiClient.post('/legal-knowledge/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
      } else {
        if (!newLaw.content) { toast.error('Please enter content or upload a file'); return; }
        await apiClient.post('/legal-knowledge', {
          ...newLaw,
          tags: newLaw.tags.split(',').map(t => t.trim()).filter(t => t)
        });
      }
      setShowAddForm(false);
      setUploadFile(null);
      setNewLaw({ article: '', title: '', category: 'Book I', content: '', tags: '', language: 'en' });
      fetchLaws();
      toast.success('Legal article added successfully!');
    } catch (error) {
      console.error('Error adding law:', error);
      toast.error('Failed to add legal article');
    }
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
      setShowEditForm(false);
      setEditingLaw(null);
      fetchLaws();
      toast.success('Legal article updated successfully!');
    } catch (error) {
      toast.error('Failed to update legal article');
    }
  };

  const handleSelectCheckbox = (id) => {
    setSelectedIds(prev => prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]);
  };

  const handleBulkDelete = async () => {
    if (selectedIds.length === 0) return;
    if (!window.confirm(`Are you sure you want to delete these ${selectedIds.length} laws?`)) return;
    try {
      await apiClient.post('/legal-knowledge/bulk-delete', { ids: selectedIds });
      toast.success('Selected laws deleted successfully!');
      setSelectedIds([]);
      setShowDeleteForm(false);
      fetchLaws();
    } catch (error) {
      toast.error('Failed to delete selected laws');
    }
  };

  const handleDeleteAll = async () => {
    if (!window.confirm('⚠️ WARNING: This will delete ALL legal articles in the system. Are you completely sure?')) return;
    try {
      await apiClient.delete('/legal-knowledge/delete-all');
      toast.success('All laws deleted successfully!');
      setSelectedIds([]);
      setShowDeleteForm(false);
      fetchLaws();
    } catch (error) {
      toast.error('Failed to clear database');
    }
  };

  return (
    <div className="space-y-6" data-testid="knowledge-page">
      <div className="page-header">
        <div>
          <h1 className="page-title" data-testid="knowledge-title">{t('knowledge')}</h1>
          <p className="page-subtitle">Browse Philippine Labor Code articles and statutes</p>
          {/* ── DOLE Reference Link ── */}
          <a
            href="https://dole.gov.ph/labor-code-of-the-philippines-2/"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-xs text-primary hover:underline mt-1"
          >
            <ExternalLink className="h-3 w-3" />
            Source: DOLE — Labor Code of the Philippines
          </a>
        </div>

        {isStaff && (
          <div className="header-actions">
            <button onClick={() => { setShowAddForm(!showAddForm); setShowDeleteForm(false); setShowEditForm(false); }} className="btn-header-primary">
              {showAddForm ? 'Cancel' : '+ Add Law'}
            </button>
            <button onClick={() => { setShowDeleteForm(!showDeleteForm); setShowAddForm(false); setShowEditForm(false); }} className="btn-header-destructive">
              {showDeleteForm ? 'Cancel' : '🗑 Delete Law'}
            </button>
          </div>
        )}
      </div>

      {/* EDIT FORM */}
      {showEditForm && isStaff && editingLaw && (
        <Card className="edit-card">
          <CardContent className="pt-6 space-y-3">
            <h3 className="edit-card-title">Edit Legal Article</h3>
            <Input placeholder="Article Number (e.g., Art. 1)" value={editingLaw.article} onChange={(e) => setEditingLaw({...editingLaw, article: e.target.value})} />
            <Input placeholder="Title" value={editingLaw.title} onChange={(e) => setEditingLaw({...editingLaw, title: e.target.value})} />
            <Select value={editingLaw.category} onValueChange={(val) => setEditingLaw({...editingLaw, category: val})}>
              <SelectTrigger><SelectValue placeholder="Book" /></SelectTrigger>
              <SelectContent>
                {BOOKS.filter(b => b.value !== 'all').map((book) => (
                  <SelectItem key={book.value} value={book.value}>{book.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Input placeholder="Tags (comma separated)" value={editingLaw.tags} onChange={(e) => setEditingLaw({...editingLaw, tags: e.target.value})} />
            <textarea placeholder="Content" value={editingLaw.content} onChange={(e) => setEditingLaw({...editingLaw, content: e.target.value})} className="textarea-field" />
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
            <Input placeholder="Article Number (e.g., Art. 1)" value={newLaw.article} onChange={(e) => setNewLaw({...newLaw, article: e.target.value})} />
            <Input placeholder="Title" value={newLaw.title} onChange={(e) => setNewLaw({...newLaw, title: e.target.value})} />
            <Select value={newLaw.category} onValueChange={(val) => setNewLaw({...newLaw, category: val})}>
              <SelectTrigger><SelectValue placeholder="Book" /></SelectTrigger>
              <SelectContent>
                {BOOKS.filter(b => b.value !== 'all').map((book) => (
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
              <p className="bulk-desc">Select individual checkboxes from the list below or clear everything.</p>
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
                onChange={(e) => setSearchQuery(e.target.value)}
                className="search-input"
              />
            </div>
            <Select value={selectedBook} onValueChange={(val) => { setSelectedBook(val); setCurrentPage(1); }}>
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
          {sortedLaws.length > 0 ? (
            <>
              <div className="flex items-center justify-between mb-3 text-sm text-muted-foreground">
                <span>
                  Showing {((clampedPage - 1) * LAWS_PER_PAGE) + 1}–{Math.min(clampedPage * LAWS_PER_PAGE, sortedLaws.length)} of {sortedLaws.length} articles
                </span>
                <span>Page {clampedPage} of {totalPages}</span>
              </div>

              <div className="law-list">
                {paginatedLaws.map((law) => (
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
                            <span className="law-category-label">
                              {BOOKS.find(b => b.value === law.category)?.label || law.category}
                            </span>
                          </div>
                        </div>
                        <div className="law-badges">
                          {expandedId === law.id
                            ? <ChevronUp className="icon-4 text-muted-foreground" />
                            : <ChevronDown className="icon-4 text-muted-foreground" />}
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
                              {law.tags.map((tag, idx) => (
                                <span key={idx} className="law-tag">{tag}</span>
                              ))}
                            </div>
                          </div>
                          <div className="law-footer">
                            <span className="law-category-badge">
                              {BOOKS.find(b => b.value === law.category)?.label || law.category}
                            </span>
                            <div className="law-meta">
                              {isStaff && (
                                <button
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    setEditingLaw({ ...law, tags: Array.isArray(law.tags) ? law.tags.join(', ') : law.tags });
                                    setShowEditForm(true); setShowAddForm(false); setShowDeleteForm(false);
                                    window.scrollTo({ top: 0, behavior: 'smooth' });
                                  }}
                                  className="btn-edit-law"
                                >
                                  Edit Law
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

              {/* Pagination Controls */}
              {totalPages > 1 && (
                <div className="flex items-center justify-center gap-2 mt-6 pt-4 border-t flex-wrap">
                  <button onClick={() => goToPage(clampedPage - 1)} disabled={clampedPage === 1} className="p-2 rounded-md border hover:bg-muted disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                    <ChevronLeft className="h-4 w-4" />
                  </button>

                  {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => {
                    const showPage = page === 1 || page === totalPages || Math.abs(page - clampedPage) <= 1;
                    const showEllipsisBefore = page === clampedPage - 2 && clampedPage > 3;
                    const showEllipsisAfter = page === clampedPage + 2 && clampedPage < totalPages - 2;
                    if (showEllipsisBefore) return <span key={`eb-${page}`} className="px-1 text-muted-foreground">…</span>;
                    if (showEllipsisAfter) return <span key={`ea-${page}`} className="px-1 text-muted-foreground">…</span>;
                    if (!showPage) return null;
                    return (
                      <button key={page} onClick={() => goToPage(page)}
                        className={`min-w-[36px] h-9 px-3 rounded-md border text-sm font-medium transition-colors ${clampedPage === page ? 'bg-primary text-primary-foreground border-primary' : 'hover:bg-muted'}`}>
                        {page}
                      </button>
                    );
                  })}

                  {/* Direct page jump */}
                  <div className="flex items-center gap-1 ml-2">
                    <span className="text-xs text-muted-foreground">Go to</span>
                    <input
                      type="number" min={1} max={totalPages}
                      value={pageInput}
                      onChange={(e) => setPageInput(e.target.value)}
                      onKeyDown={handlePageInputKeyDown}
                      onBlur={handlePageInputBlur}
                      placeholder="pg"
                      className="w-14 h-9 px-2 text-sm text-center border rounded-md focus:outline-none focus:ring-2 focus:ring-primary bg-background"
                    />
                  </div>

                  <button onClick={() => goToPage(clampedPage + 1)} disabled={clampedPage === totalPages} className="p-2 rounded-md border hover:bg-muted disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                    <ChevronRight className="h-4 w-4" />
                  </button>
                </div>
              )}
            </>
          ) : (
            <div className="empty-state" data-testid="empty-knowledge">
              <BookOpen className="empty-state-icon" />
              <p className="text-muted-foreground">
                {searchQuery ? `No results found for "${searchQuery}"` : 'No legal articles found'}
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};