import React, { useState, useEffect } from 'react';
import { Card, CardContent } from './ui/card';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Settings, Users, ShieldAlert, ShieldCheck, ShieldPlus, Gauge, Trash2 } from 'lucide-react';
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
  const [userList, setUserList] = useState([]);
  const [registerStep, setRegisterStep] = useState(0);
  const [newAccount, setNewAccount] = useState({ username: '', email: '', password: '', role: 'admin' });
  const [registerCode, setRegisterCode] = useState('');
  const [loading, setLoading] = useState(false);
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
  // ── No test_id in draft anymore — auto-assigned ────────────
  const emptyDraft = { query: '', expected_article: '' };
  const [draft, setDraft] = useState(emptyDraft);
  const [testCases, setTestCases] = useState([]);
  const [results, setResults] = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const [fetching, setFetching] = useState(true);

  useEffect(() => {
    const fetchTestCases = async () => {
      try {
        const response = await apiClient.get('/admin/metrics/test-cases');
        // Normalize IDs to T1, T2... on load regardless of stored IDs
        const normalized = (response.data.test_cases || []).map((tc, i) => ({
          ...tc,
          _backendId: tc.test_id, // keep original for deletion
          test_id: `T${i + 1}`,
        }));
        setTestCases(normalized);
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
    if (!draft.query || !draft.expected_article) return toast.error('Please provide both a query and the expected article');
    // Auto-assign next sequential ID
    const nextId = `T${testCases.length + 1}`;
    const payload = { test_id: nextId, query: draft.query, expected_article: draft.expected_article };
    try {
      await apiClient.post('/admin/metrics/test-cases', payload);
      setTestCases([...testCases, { ...payload, _backendId: nextId }]);
      setDraft(emptyDraft);
      toast.success('Test case saved to cloud database.');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save test case.');
    }
  };

  const handleRemoveTestCase = async (tc) => {
    try {
      // Delete using backend ID
      await apiClient.delete(`/admin/metrics/test-cases/${tc._backendId || tc.test_id}`);
      // Remove from local array and renumber sequentially
      const remaining = testCases.filter((t) => t.test_id !== tc.test_id);
      const renumbered = remaining.map((t, i) => ({
        ...t,
        test_id: `T${i + 1}`,
      }));
      setTestCases(renumbered);
      toast.success('Test case removed.');
    } catch (err) {
      toast.error('Failed to delete test case.');
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

        {/* ── Form — no Test ID field ── */}
        <form onSubmit={handleAddTestCase} className="flex gap-2 mb-6">
          <input
            type="text"
            placeholder="Query"
            value={draft.query}
            onChange={(e) => setDraft({...draft, query: e.target.value})}
            className="metrics-input-wide"
            required
          />
          <input
            type="text"
            placeholder="Expected Article"
            value={draft.expected_article}
            onChange={(e) => setDraft({...draft, expected_article: e.target.value})}
            className="metrics-input-wide"
            required
          />
          <button type="submit" className="metrics-btn-dark">+ Add</button>
        </form>

        <div className="metrics-table-wrap">
          <table className="metrics-table">
            <thead className="metrics-thead">
              <tr>
                <th className="metrics-th w-16">#</th>
                <th className="metrics-th">Query</th>
                <th className="metrics-th">Expected Article</th>
                <th className="metrics-th text-right">Remove</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {testCases.map((tc) => (
                <tr key={tc.test_id} className="metrics-tr">
                  <td className="metrics-td-bold">{tc.test_id}</td>
                  <td className="metrics-td">{tc.query}</td>
                  <td className="metrics-td">{tc.expected_article}</td>
                  <td className="metrics-td text-right">
                    <button
                      type="button"
                      onClick={() => handleRemoveTestCase(tc)}
                      className="metrics-btn-remove"
                    >
                      <Trash2 className="h-4 w-4 inline" />
                    </button>
                  </td>
                </tr>
              ))}
              {testCases.length === 0 && (
                <tr>
                  <td colSpan="4" className="p-4 text-center text-gray-500 italic">No test cases configured.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <button
          onClick={handleRunEvaluation}
          disabled={isRunning || testCases.length === 0}
          className="metrics-btn-execute"
        >
          {isRunning ? 'Running...' : 'Run Evaluation'}
        </button>

        {results && (
          <div className="metrics-results">
            <div className="metrics-summary-grid">
              {[
                ['Precision', results.summary.macro_precision],
                ['Recall', results.summary.macro_recall],
                ['F1 Score', results.summary.f1_score],
                ['MRR', results.summary.mrr],
                ['Tested', results.summary.total_tested],
              ].map(([label, value]) => (
                <div key={label} className="metrics-summary-card">
                  <p className="metrics-summary-label">{label}</p>
                  <p className="metrics-summary-value">{value}</p>
                </div>
              ))}
            </div>
            <div className="metrics-result-wrap">
              <table className="metrics-table">
                <thead className="metrics-thead">
                  <tr>
                    <th className="metrics-th">ID</th>
                    <th className="metrics-th">Query</th>
                    <th className="metrics-th">Ground Truth</th>
                    <th className="metrics-th">Retrieved (top 3)</th>
                    <th className="metrics-th">Relevant?</th>
                    <th className="metrics-th">Hit Rank</th>
                  </tr>
                </thead>
                <tbody className="divide-y">
                  {results.results_matrix.map((row) => (
                    <tr key={row.test_id} className="metrics-tr">
                      <td className="metrics-td-bold">{row.test_id}</td>
                      <td className="metrics-td">{row.query}</td>
                      <td className="metrics-td">{row.ground_truth}</td>
                      <td className="metrics-td">{row.retrieved_laws.join(', ') || '—'}</td>
                      <td className="metrics-td font-medium">
                        <span className={row.is_relevant.includes('0/') ? 'text-red-500' : 'text-emerald-600'}>
                          {row.is_relevant}
                        </span>
                      </td>
                      <td className="metrics-td">{row.hit_rank}</td>
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
    </div>
  );
};