import React, { useState, useEffect } from 'react';
import { Card, CardContent } from './ui/card';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Settings, Users, ShieldAlert, ShieldCheck, ShieldPlus, Gauge, Trash2, ClipboardList } from 'lucide-react';
import apiClient from '../api/apiClient';
import { toast } from 'sonner';

// ==================== 1. SETTINGS CONTROL ====================
const AdminSettingsControl = () => {
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
      await apiClient.post('/settings/chat-limit', { new_limit: chatLimit });
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
            type="number" min="1" max="10" value={chatLimit}
            onChange={(e) => setChatLimit(parseInt(e.target.value) || 1)}
            className="settings-input"
          />
          <button onClick={handleSaveLimit} disabled={isSaving} className="btn-save">
            {isSaving ? 'Saving...' : 'Save'}
          </button>
        </div>
      </CardContent>
    </Card>
  );
};

// ==================== 2. USER MANAGEMENT ====================
const UserManagementControl = ({ currentUser }) => {
  const [userList, setUserList]       = useState([]);
  const [registerStep, setRegisterStep] = useState(0);
  const [newAccount, setNewAccount]   = useState({ username: '', email: '', password: '', role: 'admin' });
  const [registerCode, setRegisterCode] = useState('');
  const [loading, setLoading]         = useState(false);
  const isSuperAdmin = currentUser?.role === 'super_admin';

  const fetchUsers = async () => {
    try {
      const response = await apiClient.get('/users', { params: { requester_id: currentUser?.id } });
      setUserList(response.data.users || []);
    } catch (err) {
      console.error("Failed to fetch users:", err);
    }
  };

  useEffect(() => {
    if (currentUser?.role === 'super_admin' || currentUser?.role === 'admin') {
      fetchUsers();
    }
  }, [currentUser]);

  const getErrorMessage = (err, defaultMessage) => {
    const detail = err.response?.data?.detail;
    if (Array.isArray(detail)) return detail.map(e => `${e.loc[e.loc.length - 1]}: ${e.msg}`).join(', ');
    if (typeof detail === 'string') return detail;
    return defaultMessage;
  };

  const handleRequestCreation = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = { ...newAccount, current_user_role: currentUser?.role };
      await apiClient.post('/users/register', payload);
      toast.success(`Verification code sent to ${newAccount.email}`);
      setRegisterStep(1);
    } catch (err) {
      toast.error(getErrorMessage(err, 'Failed to request account creation'));
    }
    setLoading(false);
  };

  const handleVerifyCreation = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await apiClient.post('/users/register/verify', { email: newAccount.email, code: registerCode });
      toast.success(`New ${newAccount.role} account created successfully!`);
      setNewAccount({ username: '', email: '', password: '', role: 'admin' });
      setRegisterCode('');
      setRegisterStep(0);
      fetchUsers();
    } catch (err) {
      toast.error(getErrorMessage(err, 'Verification failed. Invalid code.'));
    }
    setLoading(false);
  };

  const handleRoleChange = async (targetId, newRole) => {
    try {
      await apiClient.put(`/users/${targetId}/role`, { requester_id: currentUser?.id, new_role: newRole });
      toast.success("User role updated successfully");
      fetchUsers();
    } catch (err) {
      toast.error(getErrorMessage(err, "Failed to update role"));
    }
  };

  const roleBadgeClass = (role) => {
    if (role === 'super_admin') return 'role-badge role-badge--super-admin';
    if (role === 'admin') return 'role-badge role-badge--admin';
    return 'role-badge role-badge--user';
  };

  return (
    <div className="panel-grid">
      {isSuperAdmin && (
        <Card className="panel-card">
          <CardContent className="pt-6">
            <div className="panel-header">
              <ShieldPlus className="icon-5 text-primary" />
              <h3 className="panel-title">Create Admin Account</h3>
            </div>
            {registerStep === 0 ? (
              <form onSubmit={handleRequestCreation} className="form-stack">
                <Input placeholder="Username" value={newAccount.username} onChange={(e) => setNewAccount({...newAccount, username: e.target.value})} required />
                <Input type="email" placeholder="Admin Email Address" value={newAccount.email} onChange={(e) => setNewAccount({...newAccount, email: e.target.value})} required />
                <Input type="password" placeholder="Password (8 chars + special)" value={newAccount.password} onChange={(e) => setNewAccount({...newAccount, password: e.target.value})} required />
                <Select value={newAccount.role} onValueChange={(val) => setNewAccount({...newAccount, role: val})}>
                  <SelectTrigger><SelectValue placeholder="Assign Role" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="admin">Admin</SelectItem>
                    <SelectItem value="super_admin">Super Admin</SelectItem>
                  </SelectContent>
                </Select>
                <button type="submit" className="btn-primary-block" disabled={loading}>{loading ? 'Sending Code...' : 'Send Verification Code'}</button>
              </form>
            ) : (
              <form onSubmit={handleVerifyCreation} className="form-stack">
                <p className="text-sm text-center text-muted-foreground mb-2">Enter the 6-digit code sent to <strong>{newAccount.email}</strong></p>
                <Input type="text" placeholder="123456" maxLength={6} value={registerCode} onChange={(e) => setRegisterCode(e.target.value)} required className="text-center tracking-widest text-lg" />
                <button type="submit" className="btn-primary-block" disabled={loading}>Verify & Create Account</button>
                <button type="button" className="btn-muted w-full mt-2" onClick={() => setRegisterStep(0)}>Cancel</button>
              </form>
            )}
          </CardContent>
        </Card>
      )}

      <Card className={isSuperAdmin ? "panel-card-wide" : "panel-card-wide col-span-full"}>
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
                      {u.role === 'super_admin' ? <ShieldAlert className="icon-4 text-destructive" /> : u.role === 'admin' ? <ShieldCheck className="icon-4 text-primary" /> : <div className="role-icon-dot" />}
                      {u.username} {u.id === currentUser?.id && <span className="user-you-tag">(You)</span>}
                    </td>
                    <td><span className={roleBadgeClass(u.role)}>{u.role}</span></td>
                    <td className="text-right">
                      {u.id !== currentUser?.id ? (
                        isSuperAdmin ? (
                          <select value={u.role} onChange={(e) => handleRoleChange(u.id, e.target.value)} className="role-select">
                            <option value="user">User</option>
                            <option value="admin">Admin</option>
                            <option value="super_admin">Super Admin</option>
                          </select>
                        ) : (
                          <span className="text-sm text-muted-foreground">View Only</span>
                        )
                      ) : <span className="owner-tag">Owner</span>}
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

// ==================== 3. METRICS EVALUATION ====================
const MetricsEvaluationControl = ({ currentUser }) => {
  const emptyDraft = { query: '', expected_article: '' };
  const [draft, setDraft]       = useState(emptyDraft);
  const [testCases, setTestCases] = useState([]);
  const [results, setResults]   = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const [fetching, setFetching] = useState(true);

  useEffect(() => {
    fetchTestCases();
  }, []);

  const fetchTestCases = async () => {
    try {
      const response = await apiClient.get('/admin/metrics/test-cases');
      // Keep the real backend test_id as-is — it's the only thing ever sent
      // back to the server (delete, evaluate). The "#" row number shown in
      // the table is purely cosmetic and computed at render time instead,
      // so it can never be confused with — or accidentally overwrite — a
      // real identifier.
      setTestCases(response.data.test_cases || []);
    } catch (err) {
      toast.error("Failed to load test cases from database.");
    } finally {
      setFetching(false);
    }
  };

  const handleAddTestCase = async (e) => {
    e.preventDefault();
    if (!draft.query || !draft.expected_article) return toast.error('Please provide both a query and the expected article');
    // A random id here avoids collisions entirely — deriving it from
    // testCases.length meant two different real records could both end up
    // with the same id as items were added and removed over time.
    const nextId = `T-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`;
    const payload = { test_id: nextId, query: draft.query, expected_article: draft.expected_article };
    try {
      await apiClient.post('/admin/metrics/test-cases', payload);
      setDraft(emptyDraft);
      toast.success('Test case saved to cloud database.');
      await fetchTestCases(); 
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save test case.');
    }
  };

  const handleRemoveTestCase = async (tc) => {
    try {
      await apiClient.delete(`/admin/metrics/test-cases/${tc.test_id}`);
      toast.success('Test case removed.');
      await fetchTestCases();   // always trust the server's copy after a mutation
    } catch (err) {
      if (err.response?.status === 404) {
        // Already gone server-side (stale local state) — resync instead of
        // leaving a ghost row the user can never successfully delete.
        toast.error('That test case was already removed. Refreshing the list.');
        await fetchTestCases();
      } else {
        toast.error('Failed to delete test case.');
      }
    }
  };

  const handleRunEvaluation = async () => {
    if (testCases.length === 0) return toast.error('Add at least one test case first');
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
            <p className="settings-desc">Test queries and expected articles saved to cloud. IDs are assigned automatically.</p>
          </div>
        </div>

        <form onSubmit={handleAddTestCase} className="flex gap-2 mb-6">
          <input type="text" placeholder="Query" value={draft.query} onChange={(e) => setDraft({...draft, query: e.target.value})} className="flex-[2] border p-2 text-sm rounded-sm" required />
          <input type="text" placeholder="Expected Article" value={draft.expected_article} onChange={(e) => setDraft({...draft, expected_article: e.target.value})} className="flex-[2] border p-2 text-sm rounded-sm" required />
          <button type="submit" className="bg-[#1e293b] text-white px-4 py-2 text-sm font-medium">+ Add</button>
        </form>

        <div className="border rounded-sm overflow-hidden mb-4">
          <table className="w-full text-left text-sm">
            <thead className="bg-gray-100 text-gray-600 text-xs uppercase font-bold border-b">
              <tr>
                <th className="p-3 w-16">#</th>
                <th className="p-3">Query</th>
                <th className="p-3">Expected Article</th>
                <th className="p-3 text-right">Remove</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {testCases.map((tc, i) => (
                <tr key={tc.test_id} className="hover:bg-gray-50">
                  <td className="p-3 font-semibold">{i + 1}</td>
                  <td className="p-3">{tc.query}</td>
                  <td className="p-3">{tc.expected_article}</td>
                  <td className="p-3 text-right">
                    <button type="button" onClick={() => handleRemoveTestCase(tc)} className="text-red-500 hover:text-red-700">
                      <Trash2 className="h-4 w-4 inline" />
                    </button>
                  </td>
                </tr>
              ))}
              {testCases.length === 0 && (
                <tr><td colSpan="4" className="p-4 text-center text-gray-500 italic">No test cases configured.</td></tr>
              )}
            </tbody>
          </table>
        </div>

        <button onClick={handleRunEvaluation} disabled={isRunning || testCases.length === 0} className="bg-[#1e293b] text-white px-6 py-2 text-sm font-bold rounded-sm mb-6 disabled:opacity-50">
          {isRunning ? 'Running...' : 'Run Evaluation'}
        </button>

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
                    <th className="p-3">ID</th>
                    <th className="p-3">Query</th>
                    <th className="p-3">Ground Truth</th>
                    <th className="p-3">Retrieved (top 3)</th>
                    <th className="p-3">Relevant?</th>
                    <th className="p-3">Hit Rank</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {results.results_matrix.map((row) => (
                    <tr key={row.test_id} className="hover:bg-gray-50">
                      <td className="p-3 font-semibold">{row.test_id}</td>
                      <td className="p-3">{row.query}</td>
                      <td className="p-3">{row.ground_truth}</td>
                      <td className="p-3">{row.retrieved_laws.join(', ') || '—'}</td>
                      <td className="p-3 font-medium">
                        <span className={row.is_relevant.includes('0/') ? 'text-red-500' : 'text-emerald-600'}>{row.is_relevant}</span>
                      </td>
                      <td className="p-3">{row.hit_rank}</td>
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

// ==================== 4. ACTIVITY LOG ====================
const ActivityLogControl = () => {
  const [logs, setLogs]       = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await apiClient.get('/admin/activity-log');
        setLogs(res.data.logs || []);
      } catch (_) { /* non-critical */ }
      finally { setLoading(false); }
    };
    fetchLogs();
  }, []);

  const actionColor = (action = '') => {
    if (action.startsWith('ADD'))    return 'text-emerald-700 bg-emerald-50 border border-emerald-200';
    if (action.startsWith('EDIT'))   return 'text-amber-700 bg-amber-50 border border-amber-200';
    if (action.startsWith('DELETE')) return 'text-red-700 bg-red-50 border border-red-200';
    return 'text-slate-700 bg-slate-50 border border-slate-200';
  };

  return (
    <Card className="metrics-card">
      <CardContent className="pt-6">
        <div className="panel-header mb-4">
          {/* ✅ Using ClipboardList icon — no conflict with browser History API */}
          <ClipboardList className="icon-5 text-primary" />
          <div>
            <h3 className="panel-title">Article Change Log</h3>
            <p className="settings-desc">Record of who added, edited, or deleted Labor Code articles.</p>
          </div>
        </div>

        {loading ? (
          <p className="text-sm text-muted-foreground">Loading log...</p>
        ) : logs.length === 0 ? (
          <p className="text-sm text-muted-foreground italic">No activity recorded yet.</p>
        ) : (
          <div className="border rounded-sm overflow-hidden">
            <table className="w-full text-left text-sm">
              <thead className="bg-gray-100 text-gray-600 text-xs uppercase font-bold border-b">
                <tr>
                  <th className="p-3">Admin</th>
                  <th className="p-3">Action</th>
                  <th className="p-3">Article</th>
                  <th className="p-3 whitespace-nowrap">Date & Time</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {logs.map((log, idx) => (
                  <tr key={idx} className="hover:bg-gray-50">
                    <td className="p-3 font-medium">{log.admin_username}</td>
                    <td className="p-3">
                      <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${actionColor(log.action)}`}>
                        {log.action}
                      </span>
                    </td>
                    <td className="p-3 text-gray-700 max-w-[200px] truncate" title={log.article_title}>
                      {log.article_title}
                    </td>
                    <td className="p-3 text-xs text-muted-foreground whitespace-nowrap">
                      {new Date(log.timestamp).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

// ==================== MAIN ADMIN DASHBOARD COMPONENT ====================
export const AdminDashboard = ({ user }) => {
  return (
    <div className="space-y-6">
      <div className="page-header">
        <div>
          <h1 className="page-title">Admin Dashboard</h1>
          <p className="page-subtitle">Manage system settings, users, and IR metrics</p>
        </div>
      </div>
      <AdminSettingsControl />
      <UserManagementControl currentUser={user} />
      <MetricsEvaluationControl currentUser={user} />
      <ActivityLogControl />
    </div>
  );
};