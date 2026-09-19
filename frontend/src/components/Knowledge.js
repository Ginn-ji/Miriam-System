import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Card, CardContent, CardHeader } from './ui/card';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { BookOpen, Search, ChevronDown, ChevronUp, Calendar, Tag, Settings, Users, ShieldAlert, ShieldCheck, ShieldPlus, Gauge, Plus, Trash2 } from 'lucide-react';
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
    <Card className="settings-card">
      <CardContent className="settings-card-body">
        <div className="settings-info">
          <div className="settings-icon-wrap">
            <Settings className="icon-5" />
          </div>
          <div>
            <h3 className="settings-title">Laws Retrieved</h3>
            <p className="settings-desc">Manage how many laws the AI retrieves per chat.</p>
          </div>
        </div>
        
        <div className="settings-control">
          <label className="settings-label">Max Results:</label>
          <input 
            type="number" 
            min="1" 
            max="10" 
            value={chatLimit}
            onChange={(e) => setChatLimit(parseInt(e.target.value) || 1)}
            className="settings-input"
          />
          <button 
            onClick={handleSaveLimit}
            disabled={isSaving}
            className="btn-save"
          >
            {isSaving ? 'Saving...' : 'Save'}
          </button>
        </div>
      </CardContent>
    </Card>
  );
};

// ==================== SUPER ADMIN USER MANAGEMENT PANEL ====================
export const UserManagementControl = ({ currentUser }) => {
  const [userList, setUserList] = useState([]);
  const [newAccount, setNewAccount] = useState({ username: '', password: '', role: 'admin' });
  const [loading, setLoading] = useState(false);

  const fetchUsers = async () => {
    try {
      const response = await apiClient.get('/users', {
        params: { requester_id: currentUser?.id }
      });
      setUserList(response.data.users || []);
    } catch (err) {
      console.error("Failed to fetch users:", err);
    }
  };

  useEffect(() => {
    if (currentUser?.role === 'super_admin') {
      fetchUsers();
    }
  }, [currentUser]);

  const handleCreateAccount = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        username: newAccount.username,
        password: newAccount.password,
        role: newAccount.role,
        current_user_role: currentUser?.role 
      };

      await apiClient.post('/users/register', payload);
      toast.success(`New ${newAccount.role} account created!`);
      setNewAccount({ username: '', password: '', role: 'admin' });
      fetchUsers();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to create account');
    }
  };

  const handleRoleChange = async (targetId, newRole) => {
    try {
      await apiClient.put(`/users/${targetId}/role`, {
        requester_id: currentUser?.id,
        new_role: newRole
      });
      toast.success("User role updated successfully");
      fetchUsers();
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to update role");
    }
  };

  const roleBadgeClass = (role) => {
    if (role === 'super_admin') return 'role-badge role-badge--super-admin';
    if (role === 'admin') return 'role-badge role-badge--admin';
    return 'role-badge role-badge--user';
  };

  return (
    <div className="panel-grid">
      {/* Create Account Form */}
      <Card className="panel-card">
        <CardContent className="pt-6">
          <div className="panel-header">
            <ShieldPlus className="icon-5 text-primary" />
            <h3 className="panel-title">Create Admin Account</h3>
          </div>
          <form onSubmit={handleCreateAccount} className="form-stack">
            <Input 
              placeholder="Username" 
              value={newAccount.username}
              onChange={(e) => setNewAccount({...newAccount, username: e.target.value})}
              required
            />
            <Input 
              type="password"
              placeholder="Password" 
              value={newAccount.password}
              onChange={(e) => setNewAccount({...newAccount, password: e.target.value})}
              required
            />
            <Select 
              value={newAccount.role} 
              onValueChange={(val) => setNewAccount({...newAccount, role: val})}
            >
              <SelectTrigger>
                <SelectValue placeholder="Assign Role" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="admin">Admin</SelectItem>
                <SelectItem value="super_admin">Super Admin</SelectItem>
              </SelectContent>
            </Select>
            <button 
              type="submit" 
              className="btn-primary-block"
            >
              Create Account
            </button>
          </form>
        </CardContent>
      </Card>

      {/* User Roster Table */}
      <Card className="panel-card-wide">
        <CardContent className="pt-6">
          <div className="panel-header">
            <Users className="icon-5 text-primary" />
            <h3 className="panel-title">User Management & Permissions</h3>
          </div>
          <div className="table-wrap">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Username</th>
                  <th>Current Role</th>
                  <th className="text-right">Change Role</th>
                </tr>
              </thead>
              <tbody>
                {userList.map((u) => (
                  <tr key={u.id} className="hover:bg-muted/40 transition-colors">
                    <td className="user-name-cell">
                      {u.role === 'super_admin' ? (
                        <ShieldAlert className="icon-4 text-destructive" />
                      ) : u.role === 'admin' ? (
                        <ShieldCheck className="icon-4 text-primary" />
                      ) : (
                        <div className="role-icon-dot" />
                      )}
                      {u.username}
                      {u.id === currentUser?.id && <span className="user-you-tag">(You)</span>}
                    </td>
                    <td>
                      <span className={roleBadgeClass(u.role)}>
                        {u.role}
                      </span>
                    </td>
                    <td className="text-right">
                      {u.id !== currentUser?.id ? (
                        <select
                          value={u.role}
                          onChange={(e) => handleRoleChange(u.id, e.target.value)}
                          className="role-select"
                        >
                          <option value="user">User</option>
                          <option value="admin">Admin</option>
                          <option value="super_admin">Super Admin</option>
                        </select>
                      ) : (
                        <span className="owner-tag">Owner</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// ==================== ADMIN-ONLY: MANUAL SEARCH METRICS EVALUATION (CLOUD) ====================
export const MetricsEvaluationControl = ({ currentUser }) => {
  const emptyDraft = { test_id: '', query: '', expected_article: '' };
  const [draft, setDraft] = useState(emptyDraft);
  const [testCases, setTestCases] = useState([]);
  const [results, setResults] = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const [fetching, setFetching] = useState(true);

  // Load Test Cases from the cloud on mount
  useEffect(() => {
    const fetchTestCases = async () => {
      try {
        const response = await apiClient.get('/admin/metrics/test-cases');
        setTestCases(response.data.test_cases || []);
      } catch (err) {
        toast.error("Failed to load test cases from database.");
      } finally {
        setFetching(false);
      }
    };
    fetchTestCases();
  }, []);

  const handleAddTestCase = async (e) => {
    e.preventDefault();
    if (!draft.query || !draft.expected_article) {
      toast.error('Please provide both a query and the expected article');
      return;
    }
    const autoId = draft.test_id || `T${testCases.length + 1}`;
    const payload = { test_id: autoId, query: draft.query, expected_article: draft.expected_article };
    
    try {
      await apiClient.post('/admin/metrics/test-cases', payload);
      setTestCases([...testCases, payload]);
      setDraft(emptyDraft);
      toast.success('Test case saved to cloud database.');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save test case.');
    }
  };

  const handleRemoveTestCase = async (testId) => {
    try {
      await apiClient.delete(`/admin/metrics/test-cases/${testId}`);
      setTestCases(testCases.filter(tc => tc.test_id !== testId));
      toast.success('Test case removed.');
    } catch (err) {
      toast.error('Failed to delete test case.');
    }
  };

  const handleRunEvaluation = async () => {
    if (testCases.length === 0) {
      toast.error('Add at least one test case first');
      return;
    }
    setIsRunning(true);
    try {
      const response = await apiClient.post(
        '/admin/metrics/evaluate',
        { test_cases: testCases },
        { params: { requester_id: currentUser?.id } }
      );
      setResults(response.data);
      toast.success('Evaluation complete');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to run evaluation');
    } finally {
      setIsRunning(false);
    }
  };

  if (fetching) return <div className="text-sm text-muted-foreground p-4">Loading evaluation matrix...</div>;

  return (
    <Card className="metrics-card">
      <CardContent className="pt-6">
        <div className="panel-header mb-6">
          <Gauge className="icon-5 text-primary" />
          <div>
            <h3 className="panel-title">Search Metrics Evaluation</h3>
            <p className="settings-desc">
              Test queries and their expected articles are saved to the cloud for team collaboration.
            </p>
          </div>
        </div>

        {/* Form Row matching the screenshot layout */}
        <form onSubmit={handleAddTestCase} className="flex gap-2 mb-6">
          <input 
            type="text" 
            placeholder="Test ID (optional)" 
            value={draft.test_id} 
            onChange={(e) => setDraft({...draft, test_id: e.target.value})} 
            className="flex-1 border p-2 text-sm rounded-sm focus:outline-primary" 
          />
          <input 
            type="text" 
            placeholder="Query" 
            value={draft.query} 
            onChange={(e) => setDraft({...draft, query: e.target.value})} 
            className="flex-[2] border p-2 text-sm rounded-sm focus:outline-primary" 
            required 
          />
          <input 
            type="text" 
            placeholder="Expected Article (e.g., Art. 82)" 
            value={draft.expected_article} 
            onChange={(e) => setDraft({...draft, expected_article: e.target.value})} 
            className="flex-[2] border p-2 text-sm rounded-sm focus:outline-primary" 
            required 
          />
          <button type="submit" className="bg-[#1e293b] text-white px-4 py-2 text-sm font-medium hover:bg-slate-800 transition">
            + Add Test Case
          </button>
        </form>

        {/* Queue Table matching the screenshot layout */}
        <div className="border rounded-sm overflow-hidden mb-4">
          <table className="w-full text-left text-sm">
            <thead className="bg-gray-100 text-gray-600 text-xs uppercase font-bold border-b">
              <tr>
                <th className="p-3">Test ID</th>
                <th className="p-3">Query</th>
                <th className="p-3">Expected Article</th>
                <th className="p-3 text-right">Remove</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {testCases.map((tc) => (
                <tr key={tc.test_id} className="hover:bg-gray-50">
                  <td className="p-3 text-gray-700">{tc.test_id}</td>
                  <td className="p-3 text-gray-700">{tc.query}</td>
                  <td className="p-3 text-gray-700">{tc.expected_article}</td>
                  <td className="p-3 text-right">
                    <button type="button" onClick={() => handleRemoveTestCase(tc.test_id)} className="text-red-500 hover:text-red-700">
                      <Trash2 className="h-4 w-4 inline" />
                    </button>
                  </td>
                </tr>
              ))}
              {testCases.length === 0 && (
                <tr><td colSpan="4" className="p-4 text-center text-gray-500 italic">No test cases configured yet.</td></tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Execution Button aligned below the table */}
        <button 
          onClick={handleRunEvaluation} 
          disabled={isRunning || testCases.length === 0} 
          className="bg-[#1e293b] text-white px-6 py-2 text-sm font-bold rounded-sm mb-6 hover:bg-slate-800 disabled:opacity-50"
        >
          {isRunning ? 'Running Evaluation...' : 'Run Evaluation'}
        </button>

        {/* Results Matrix Block */}
        {results && (
          <div className="metrics-results">
            <div className="summary-grid">
              {[
                ['Precision', results.summary.macro_precision],
                ['Recall', results.summary.macro_recall],
                ['F1 Score', results.summary.f1_score],
                ['MRR', results.summary.mrr],
                ['Tested', results.summary.total_tested],
              ].map(([label, value]) => (
                <div key={label} className="summary-tile border p-4 text-center bg-white rounded-sm">
                  <p className="text-xs text-gray-500 uppercase">{label}</p>
                  <p className="text-xl font-bold mt-1 text-slate-800">{value}</p>
                </div>
              ))}
            </div>

            <div className="table-wrap-tall mt-4 border rounded-sm overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-gray-100 text-gray-600 uppercase border-b">
                  <tr>
                    <th className="p-3">Test ID</th>
                    <th className="p-3">Query</th>
                    <th className="p-3">Ground Truth</th>
                    <th className="p-3">Retrieved (top 3)</th>
                    <th className="p-3">Relevant?</th>
                    <th className="p-3">Hit Rank</th>
                    <th className="p-3">Precision@K</th>
                    <th className="p-3">Recall</th>
                    <th className="p-3">RR</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {results.results_matrix.map((row) => (
                    <tr key={row.test_id} className="hover:bg-gray-50 transition-colors">
                      <td className="p-3 font-semibold text-gray-700">{row.test_id}</td>
                      <td className="p-3 text-gray-800">{row.query}</td>
                      <td className="p-3 text-gray-800">{row.ground_truth}</td>
                      <td className="p-3 text-gray-600">{row.retrieved_laws.join(', ') || '—'}</td>
                      <td className="p-3 font-medium">
                        <span className={row.is_relevant.includes('0/') ? 'text-red-500' : 'text-emerald-600'}>
                          {row.is_relevant}
                        </span>
                      </td>
                      <td className="p-3 text-gray-800">{row.hit_rank}</td>
                      <td className="p-3 text-gray-800">{row.precision_k}</td>
                      <td className="p-3 text-gray-800">{row.recall}</td>
                      <td className="p-3 text-gray-800">{row.reciprocal_rank}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

// ==================== MAIN KNOWLEDGE COMPONENT ====================
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

  const isStaff = user?.role === 'admin' || user?.role === 'super_admin';
  const isSuperAdmin = user?.role === 'super_admin';

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

  const handleSelectCheckbox = (id) => {
    setSelectedIds(prev => 
      prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]
    );
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
      <div className="page-header">
        <div>
          <h1 className="page-title" data-testid="knowledge-title">
            {t('knowledge')}
          </h1>
          <p className="page-subtitle">Browse Philippine legal articles and statutes</p>
        </div>

        {/* Both Admin and Super Admin can manage articles */}
        {isStaff && (
          <div className="header-actions">
            <button
              onClick={() => { setShowAddForm(!showAddForm); setShowDeleteForm(false); setShowEditForm(false); }}
              className="btn-header-primary"
            >
              {showAddForm ? 'Cancel' : '+ Add Law'}
            </button>
            <button
              onClick={() => { setShowDeleteForm(!showDeleteForm); setShowAddForm(false); setShowEditForm(false); }}
              className="btn-header-destructive"
            >
              {showDeleteForm ? 'Cancel' : '🗑 Delete Law'}
            </button>
          </div>
        )}
      </div>

      {/* SYSTEM CONFIGURATION */}
      {isStaff && <AdminSettingsControl />}

      {/* SUPER ADMIN ONLY: User Management & Admin Creator */}
      {isSuperAdmin && <UserManagementControl currentUser={user} />}

      {/* ADMIN PANEL ONLY: Manual Search Metrics Evaluation */}
      {isStaff && <MetricsEvaluationControl currentUser={user} />}

      {/* EDIT FORM */}
      {showEditForm && isStaff && editingLaw && (
        <Card className="edit-card">
          <CardContent className="pt-6 space-y-3">
            <h3 className="edit-card-title">Edit Legal Article</h3>
            
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
            
            <div className="form-grid-2">
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
              className="textarea-field"
            />
            
            <div className="form-actions">
              <button
                onClick={handleUpdateLaw}
                className="btn-amber"
              >
                Save Changes
              </button>
              <button
                onClick={() => {
                  setShowEditForm(false);
                  setEditingLaw(null);
                }}
                className="btn-muted"
              >
                Cancel
              </button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* ADD LAW FORM */}
      {showAddForm && isStaff && (
        <Card className="card-elevated">
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
            
            <div className="form-grid-2">
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
                  className="textarea-field-sm"
                />
                <div className="upload-dropzone">
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
                  <p className="upload-hint">
                    Or upload a PDF/text file instead of typing
                  </p>
                  <button
                    onClick={() => lawFileInputRef.current.click()}
                    className="btn-choose-file"
                  >
                    Choose File (.pdf or .txt)
                  </button>
                </div>
              </>
            ) : (
              <div className="upload-file-row">
                <span className="upload-file-name">📎 {uploadFile.name}</span>
                <button
                  onClick={() => setUploadFile(null)}
                  className="link-remove"
                >
                  Remove
                </button>
              </div>
            )}
            <div className="form-actions">
              <button
                onClick={handleAddLaw}
                className="btn-save-law"
              >
                Save
              </button>
              <button
                onClick={() => {
                  setShowAddForm(false);
                  setUploadFile(null);
                  setNewLaw({ article: '', title: '', category: 'Civil Law', content: '', tags: '', language: 'en' });
                }}
                className="btn-muted"
              >
                Cancel
              </button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* BULK & MASS DELETE ACTION BAR */}
      {showDeleteForm && isStaff && (
        <Card className="bulk-bar">
          <CardContent className="bulk-bar-body">
            <div>
              <h3 className="bulk-title">Article Deletion</h3>
              <p className="bulk-desc">Select individual checkboxes from the list below or clear everything.</p>
            </div>
            <div className="bulk-actions">
              <button
                onClick={handleBulkDelete}
                disabled={selectedIds.length === 0}
                className="btn-delete-selected"
              >
                Delete Selected ({selectedIds.length})
              </button>
              <button
                onClick={handleDeleteAll}
                className="btn-delete-all"
              >
                Delete All Laws
              </button>
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
                placeholder="Search legal knowledge..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="search-input"
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
            <div className="law-list">
              {sortedLaws.map((law) => (
                <div
                  key={law.id}
                  className="law-item"
                  data-testid="law-item"
                >
                  {isStaff && showDeleteForm && (
                    <input 
                      type="checkbox" 
                      checked={selectedIds.includes(law.id)}
                      onChange={() => handleSelectCheckbox(law.id)}
                      className="law-checkbox"
                    />
                  )}

                  <div className="flex-1">
                    <div
                      className="law-row"
                      onClick={() => toggleExpand(law.id)}
                    >
                      <div className="law-title-group">
                        <BookOpen className="icon-4 text-primary flex-shrink-0" />
                        <div>
                          <h3 className="law-title">{law.title}</h3>
                          <span className="law-category-label">{law.category}</span>
                        </div>
                      </div>
                      <div className="law-badges">
                        <span className="legal-badge text-xs">{law.language}</span>
                        {expandedId === law.id
                          ? <ChevronUp className="icon-4 text-muted-foreground" />
                          : <ChevronDown className="icon-4 text-muted-foreground" />
                        }
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
                              <span
                                key={idx}
                                className="law-tag"
                              >
                                {tag}
                              </span>
                            ))}
                          </div>
                        </div>
                        <div className="law-footer">
                          <span className="law-category-badge">
                            {law.category}
                          </span>
                          
                          <div className="law-meta">
                            {isStaff && (
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
          ) : (
            <div className="empty-state" data-testid="empty-knowledge">
              <BookOpen className="empty-state-icon" />
              <p className="text-muted-foreground">No legal articles found</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};