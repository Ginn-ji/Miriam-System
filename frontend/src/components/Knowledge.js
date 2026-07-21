import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader } from './ui/card';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { BookOpen, Search, ChevronDown, ChevronUp, Calendar, Tag, Settings } from 'lucide-react';
import apiClient from '../api/apiClient';
import { toast } from 'sonner';

export const AdminSettingsControl = () => {
  const [chatLimit, setChatLimit] = useState(5);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    const fetchLimit = async () => {
      try {
        const response = await apiClient.get('/settings/chat-limit');
        setChatLimit(response.data.limit);
      } catch (error) {
        console.error("Failed to load settings:", error);
      }
    };
    fetchLimit();
  }, []);

  const handleSaveLimit = async () => {
    setIsSaving(true);
    try {
      await apiClient.post('/settings/chat-limit', { 
        new_limit: chatLimit 
      });
      toast.success(`Chat response limit updated to ${chatLimit}`);
    } catch (error) {
      toast.error('Failed to update system limit');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <Card className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)] border-primary/20 mb-6">
      <CardContent className="pt-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 text-primary rounded-md">
            <Settings className="h-5 w-5" />
          </div>
          <div>
            <h3 className="font-semibold font-serif text-gray-900">System Configuration</h3>
            <p className="text-xs text-muted-foreground">Manage how many laws the AI retrieves per chat.</p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <label className="text-sm font-medium text-gray-700">Max Results:</label>
          <input 
            type="number" 
            min="1" 
            max="10" 
            value={chatLimit}
            onChange={(e) => setChatLimit(parseInt(e.target.value) || 1)}
            className="w-16 p-1 border rounded-md text-center text-sm"
          />
          <button 
            onClick={handleSaveLimit}
            disabled={isSaving}
            className="px-3 py-1.5 bg-primary text-primary-foreground text-xs rounded-md hover:bg-primary/90 transition-colors disabled:opacity-50"
          >
            {isSaving ? 'Saving...' : 'Save Rule'}
          </button>
        </div>
      </CardContent>
    </Card>
  );
};

export const Knowledge = ({ user }) => {
  const { t } = useLanguage();
  const [laws, setLaws] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedLanguage, setSelectedLanguage] = useState('all');
  const [expandedId, setExpandedId] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showDeleteForm, setShowDeleteForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [uploadFile, setUploadFile] = useState(null);
  
  // Bulk selection state variables
  const [selectedIds, setSelectedIds] = useState([]);
  
  const [newAdmin, setNewAdmin] = useState({ username: '', password: '' });
  
  const [newLaw, setNewLaw] = useState({
    article: '',
    title: '',
    category: 'Civil Law',
    content: '',
    tags: '',
    language: 'en'
  });
  
  const [editingLaw, setEditingLaw] = useState(null);

  const lawFileInputRef = useRef(null);

  useEffect(() => {
    const triggerSearch = async () => {
      try {
        const params = {};
        if (selectedCategory !== 'all') params.category = selectedCategory;
        if (selectedLanguage !== 'all') params.language = selectedLanguage;
        if (searchQuery) params.q = searchQuery;
        
        const response = await apiClient.get('/legal-knowledge', { params });
        setLaws(response.data.laws || []);
      } catch (error) {
        console.error('🚨 SEARCH ERROR:', error);
      }
    };

    const delayDebounceFn = setTimeout(() => {
      triggerSearch();
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [searchQuery, selectedCategory, selectedLanguage]);

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

  const toggleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const handleCreateAdmin = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        username: newAdmin.username,
        password: newAdmin.password,
        role: 'admin', 
        current_user_role: user?.role 
      };

      await apiClient.post('/users/register', payload);
      toast.success('New Admin account successfully created!');
      setNewAdmin({ username: '', password: '' }); 
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to create admin');
    }
  };

  const handleAddLaw = async () => {
    if (!newLaw.title) {
      toast.error('Please enter a title');
      return;
    }
    try {
      if (uploadFile) {
        const formData = new FormData();
        formData.append('file', uploadFile);
        formData.append('title', newLaw.title);
        formData.append('category', newLaw.category);
        formData.append('tags', newLaw.tags);
        formData.append('language', newLaw.language);
        await apiClient.post('/legal-knowledge/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      } else {
        if (!newLaw.content) {
          toast.error('Please enter content or upload a file');
          return;
        }
        await apiClient.post('/legal-knowledge', {
          ...newLaw,
          tags: newLaw.tags.split(',').map(t => t.trim()).filter(t => t)
        });
      }
      setShowAddForm(false);
      setUploadFile(null);
      setNewLaw({ article: '', title: '', category: 'Civil Law', content: '', tags: '', language: 'en' });
      fetchLaws();
      toast.success('Legal article added successfully!');
    } catch (error) {
      console.error('Error adding law:', error);
      toast.error('Failed to add legal article');
    }
  };

  const handleUpdateLaw = async () => {
    if (!editingLaw.title) {
      toast.error('Please enter a title');
      return;
    }
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
      console.error('Error updating law:', error);
      toast.error('Failed to update legal article');
    }
  };

  // Bulk check handler
  const handleSelectCheckbox = (id) => {
    setSelectedIds(prev => 
      prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]
    );
  };

  // Bulk delete execution
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

  // Delete all execution
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

  const categories = ['all', 'Civil Law', 'Labor Law', 'Criminal Law', 'Family Law', 'Privacy Law'];

  const sortedLaws = [...laws].sort((a, b) => {
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

  return (
    <div className="space-y-6" data-testid="knowledge-page">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-serif font-bold tracking-tight text-primary" data-testid="knowledge-title">
            {t('knowledge')}
          </h1>
          <p className="text-muted-foreground mt-1">Browse Philippine legal articles and statutes</p>
        </div>
        {user?.role === 'admin' && (
          <div className="flex items-center gap-2">
            <button
              onClick={() => { setShowAddForm(!showAddForm); setShowDeleteForm(false); setShowEditForm(false); }}
              className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-sm text-sm font-medium hover:bg-primary/90 transition-colors"
            >
              {showAddForm ? 'Cancel' : '+ Add Law'}
            </button>
            <button
              onClick={() => { setShowDeleteForm(!showDeleteForm); setShowAddForm(false); setShowEditForm(false); }}
              className="flex items-center gap-2 px-4 py-2 bg-destructive text-destructive-foreground rounded-sm text-sm font-medium hover:bg-destructive/90 transition-colors"
            >
              {showDeleteForm ? 'Cancel' : '🗑 Delete Law'}
            </button>
          </div>
        )}
      </div>

      {user?.role === 'admin' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <AdminSettingsControl />
          
          <Card className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)] border-primary/20 mb-6">
            <CardContent className="pt-6">
              <h3 className="font-serif font-semibold text-primary mb-4">Create New Admin Account</h3>
              <form onSubmit={handleCreateAdmin} className="flex flex-col sm:flex-row gap-3">
                <Input 
                  placeholder="Username" 
                  value={newAdmin.username}
                  onChange={(e) => setNewAdmin({...newAdmin, username: e.target.value})}
                  required
                />
                <Input 
                  type="password"
                  placeholder="Password" 
                  value={newAdmin.password}
                  onChange={(e) => setNewAdmin({...newAdmin, password: e.target.value})}
                  required
                />
                <button 
                  type="submit" 
                  className="px-4 py-2 bg-primary text-primary-foreground rounded-sm text-sm hover:bg-primary/90 whitespace-nowrap"
                >
                  Create Admin
                </button>
              </form>
            </CardContent>
          </Card>
        </div>
      )}

      {showEditForm && user?.role === 'admin' && editingLaw && (
        <Card className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)] border-amber-500/30">
          <CardContent className="pt-6 space-y-3">
            <h3 className="font-serif font-semibold text-amber-600">Edit Legal Article</h3>
            
            <Input
              placeholder="Article Number (e.g., Art. 1)"
              value={editingLaw.article}
              onChange={(e) => setEditingLaw({...editingLaw, article: e.target.value})}
            />
            <Input
              placeholder="Title (e.g. Declaration of Policy)"
              value={editingLaw.title}
              onChange={(e) => setEditingLaw({...editingLaw, title: e.target.value})}
            />
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <Select value={editingLaw.category} onValueChange={(val) => setEditingLaw({...editingLaw, category: val})}>
                <SelectTrigger>
                  <SelectValue placeholder="Category" />
                </SelectTrigger>
                <SelectContent>
                  {categories.filter(c => c !== 'all').map((cat) => (
                    <SelectItem key={cat} value={cat}>{cat}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Select value={editingLaw.language} onValueChange={(val) => setEditingLaw({...editingLaw, language: val})}>
                <SelectTrigger>
                  <SelectValue placeholder="Language" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="en">English</SelectItem>
                  <SelectItem value="tl">Tagalog</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Input
              placeholder="Tags (comma separated)"
              value={editingLaw.tags}
              onChange={(e) => setEditingLaw({...editingLaw, tags: e.target.value})}
            />
            <textarea
              placeholder="Content"
              value={editingLaw.content}
              onChange={(e) => setEditingLaw({...editingLaw, content: e.target.value})}
              className="w-full min-h-[150px] p-2 text-sm border rounded-sm bg-background resize-none"
            />
            
            <div className="flex gap-2 pt-1">
              <button
                onClick={handleUpdateLaw}
                className="px-4 py-2 bg-amber-600 text-white rounded-sm text-sm hover:bg-amber-700"
              >
                Save Changes
              </button>
              <button
                onClick={() => {
                  setShowEditForm(false);
                  setEditingLaw(null);
                }}
                className="px-4 py-2 bg-muted text-muted-foreground rounded-sm text-sm hover:bg-muted/80"
              >
                Cancel
              </button>
            </div>
          </CardContent>
        </Card>
      )}

      {showAddForm && user?.role === 'admin' && (
        <Card className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)]">
           <CardContent className="pt-6 space-y-3">
            <h3 className="font-serif font-semibold">Add New Legal Article</h3>
            
            <Input
              placeholder="Article Number (e.g., Art. 1)"
              value={newLaw.article}
              onChange={(e) => setNewLaw({...newLaw, article: e.target.value})}
            />
            <Input
              placeholder="Title (e.g. Declaration of Policy)"
              value={newLaw.title}
              onChange={(e) => setNewLaw({...newLaw, title: e.target.value})}
            />
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <Select value={newLaw.category} onValueChange={(val) => setNewLaw({...newLaw, category: val})}>
                <SelectTrigger>
                  <SelectValue placeholder="Category" />
                </SelectTrigger>
                <SelectContent>
                  {categories.filter(c => c !== 'all').map((cat) => (
                    <SelectItem key={cat} value={cat}>{cat}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Select value={newLaw.language} onValueChange={(val) => setNewLaw({...newLaw, language: val})}>
                <SelectTrigger>
                  <SelectValue placeholder="Language" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="en">English</SelectItem>
                  <SelectItem value="tl">Tagalog</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Input
              placeholder="Tags (comma separated e.g. civil law, rights, duties)"
              value={newLaw.tags}
              onChange={(e) => setNewLaw({...newLaw, tags: e.target.value})}
            />
            {!uploadFile ? (
              <>
                <textarea
                  placeholder="Content (or upload a PDF/text file below)"
                  value={newLaw.content}
                  onChange={(e) => setNewLaw({...newLaw, content: e.target.value})}
                  className="w-full min-h-[100px] p-2 text-sm border rounded-sm bg-background resize-none"
                />
                <div className="border-2 border-dashed rounded-sm p-3 text-center">
                  <input
                    type="file"
                    hidden
                    ref={lawFileInputRef}
                    accept=".pdf,.txt"
                    onChange={(e) => {
                      setUploadFile(e.target.files[0]);
                      setNewLaw({...newLaw, content: ''});
                    }}
                  />
                  <p className="text-xs text-muted-foreground mb-2">
                    Or upload a PDF/text file instead of typing
                  </p>
                  <button
                    onClick={() => lawFileInputRef.current.click()}
                    className="px-3 py-1 bg-muted rounded-sm text-xs hover:bg-muted/80"
                  >
                    Choose File (.pdf or .txt)
                  </button>
                </div>
              </>
            ) : (
              <div className="border rounded-sm p-3 flex items-center justify-between">
                <span className="text-sm text-primary">📎 {uploadFile.name}</span>
                <button
                  onClick={() => setUploadFile(null)}
                  className="text-xs text-destructive hover:underline"
                >
                  Remove
                </button>
              </div>
            )}
            <div className="flex gap-2 pt-1">
              <button
                onClick={handleAddLaw}
                className="px-4 py-2 bg-primary text-primary-foreground rounded-sm text-sm hover:bg-primary/90"
              >
                Save
              </button>
              <button
                onClick={() => {
                  setShowAddForm(false);
                  setUploadFile(null);
                  setNewLaw({ article: '', title: '', category: 'Civil Law', content: '', tags: '', language: 'en' });
                }}
                className="px-4 py-2 bg-muted text-muted-foreground rounded-sm text-sm hover:bg-muted/80"
              >
                Cancel
              </button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* NEW BULK & MASS DELETE ACTION BAR */}
      {showDeleteForm && user?.role === 'admin' && (
        <Card className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)] border-destructive/20 bg-destructive/5">
          <CardContent className="pt-6 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
              <h3 className="font-serif font-semibold text-destructive">Bulk Management & Deletion</h3>
              <p className="text-xs text-muted-foreground">Select individual checkboxes from the list below or clear everything.</p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={handleBulkDelete}
                disabled={selectedIds.length === 0}
                className="px-4 py-2 bg-destructive text-destructive-foreground rounded-sm text-sm hover:bg-destructive/90 disabled:opacity-50"
              >
                Delete Selected ({selectedIds.length})
              </button>
              <button
                onClick={handleDeleteAll}
                className="px-4 py-2 bg-black text-white rounded-sm text-sm hover:bg-gray-800"
              >
                Delete All Laws
              </button>
            </div>
          </CardContent>
        </Card>
      )}

      <Card className="shadow-[0_1px_3px_rgba(0,0,0,0.12),0_1px_2px_rgba(0,0,0,0.24)]">
        <CardHeader>
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 flex items-center gap-2">
              <Search className="h-5 w-5 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search legal knowledge..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm"
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
          {sortedLaws.length > 0 ? (
            <div className="space-y-3">
              {sortedLaws.map((law) => (
                <div
                  key={law.id}
                  className="rounded-sm border hover:bg-muted/30 transition-colors flex items-center px-4"
                  data-testid="law-item"
                >
                  {/* Checkbox enabled dynamically when Delete mode is active */}
                  {user?.role === 'admin' && showDeleteForm && (
                    <input 
                      type="checkbox" 
                      checked={selectedIds.includes(law.id)}
                      onChange={() => handleSelectCheckbox(law.id)}
                      className="mr-3 h-4 w-4 accent-primary cursor-pointer"
                    />
                  )}

                  <div className="flex-1">
                    <div
                      className="flex items-center justify-between py-4 cursor-pointer"
                      onClick={() => toggleExpand(law.id)}
                    >
                      <div className="flex items-center gap-3">
                        <BookOpen className="h-4 w-4 text-primary flex-shrink-0" />
                        <div>
                          <h3 className="font-serif font-semibold text-base">{law.title}</h3>
                          <span className="text-xs text-muted-foreground">{law.category}</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="legal-badge text-xs">{law.language}</span>
                        {expandedId === law.id
                          ? <ChevronUp className="h-4 w-4 text-muted-foreground" />
                          : <ChevronDown className="h-4 w-4 text-muted-foreground" />
                        }
                      </div>
                    </div>

                    {expandedId === law.id && (
                      <div className="pb-4 border-t pt-3 space-y-3">
                        <div>
                          <p className="text-xs font-medium text-muted-foreground mb-1">Content</p>
                          <p className="text-sm leading-relaxed">{law.content}</p>
                        </div>
                        <div>
                          <div className="flex items-center gap-1 mb-1">
                            <Tag className="h-3 w-3 text-muted-foreground" />
                            <p className="text-xs font-medium text-muted-foreground">Tags</p>
                          </div>
                          <div className="flex flex-wrap gap-2">
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
                        <div className="flex items-center justify-between pt-1">
                          <span className="px-2 py-1 rounded-sm bg-primary/10 text-primary text-xs font-medium">
                            {law.category}
                          </span>
                          
                          <div className="flex items-center gap-3">
                            {user?.role === 'admin' && (
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  setEditingLaw({
                                    ...law,
                                    tags: Array.isArray(law.tags) ? law.tags.join(', ') : law.tags
                                  });
                                  setShowEditForm(true);
                                  setShowAddForm(false);
                                  setShowDeleteForm(false);
                                  window.scrollTo({ top: 0, behavior: 'smooth' });
                                }}
                                className="px-3 py-1 bg-amber-100 text-amber-800 rounded-sm text-xs hover:bg-amber-200 transition-colors font-medium"
                              >
                                Edit Law
                              </button>
                            )}
                            <div className="flex items-center gap-1 text-xs text-muted-foreground">
                              <Calendar className="h-3 w-3" />
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