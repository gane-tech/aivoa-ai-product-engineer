const API = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

async function call(path, options = {}) {
  const res = await fetch(`${API}${path}`, { headers: { 'Content-Type': 'application/json', ...(options.headers || {}) }, ...options });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || 'Request failed');
  return data;
}

export const api = {
  extract: (text) => call('/ai/extract', { method: 'POST', body: JSON.stringify({ text }) }),
  extractFile: async (file) => { const form = new FormData(); form.append('file', file); const res = await fetch(`${API}/ai/extract-file`, { method: 'POST', body: form }); const data = await res.json(); if (!res.ok) throw new Error(data.detail || 'File extraction failed'); return data; },
  pipeline: (text) => call('/ai/pipeline', { method: 'POST', body: JSON.stringify({ text }) }),
  risk: (data) => call('/ai/risk', { method: 'POST', body: JSON.stringify({ data }) }),
  completeness: (data) => call('/ai/completeness', { method: 'POST', body: JSON.stringify({ data }) }),
  rootCause: (data) => call('/ai/root-cause', { method: 'POST', body: JSON.stringify({ data }) }),
  duplicate: (data) => call('/ai/duplicate', { method: 'POST', body: JSON.stringify({ data }) }),
  save: (data) => call('/complaints', { method: 'POST', body: JSON.stringify(data) })
};
