import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Provider, useDispatch, useSelector } from 'react-redux';
import { api } from './api';
import { store, updateField, hydrate, patchUI, clearUI, reset } from './store';
import './styles.css';

const fields = [
  ['complaint_source', 'Complaint Source', 'select'], ['customer_name', 'Customer Name', 'input'], ['product_name', 'Product Name', 'input'],
  ['product_strength', 'Product Strength', 'input'], ['batch_number', 'Batch / Lot Number', 'input'], ['manufacturing_date', 'Manufacturing Date', 'input'],
  ['expiry_date', 'Expiry Date', 'input'], ['complaint_details', 'Complaint Details', 'textarea'], ['patient_or_consumer', 'Alleged Patient / Consumer', 'textarea'],
  ['initial_assessment', 'Initial Assessment', 'textarea'], ['priority', 'Priority', 'select']
];

function App() {
  const dispatch = useDispatch();
  const complaint = useSelector(s => s.complaint);
  const ui = useSelector(s => s.ui);
  const [assistantText, setAssistantText] = useState(`Customer reports that Paracetamol 500 mg tablets from batch PCM-25A014 had visible tablet discoloration. The distributor received three complaints from adult consumers. One consumer reported nausea but no hospitalization. Product was stored at controlled room temperature.`);

  const set = (key, value) => dispatch(updateField({ key, value }));
  const startAI = async () => {
    dispatch(patchUI({ loading: true, error: '', message: 'AI assistant is extracting complaint information…' }));
    try {
      const data = await api.pipeline(assistantText);
      dispatch(hydrate(data.extracted));
      dispatch(patchUI({ loading: false, extracted: data.extracted, risk: data.risk, completeness: data.completeness, message: 'Complaint extracted and assessed successfully.' }));
    } catch (e) { dispatch(patchUI({ loading: false, error: e.message })); }
  };
  const assess = async () => {
    dispatch(patchUI({ loading: true, error: '', message: 'Running AI assessment…' }));
    try {
      const [risk, completeness, rootCause] = await Promise.all([api.risk(complaint), api.completeness(complaint), api.rootCause(complaint)]);
      dispatch(patchUI({ loading: false, risk, completeness, rootCause, message: 'AI assessment updated.' }));
    } catch (e) { dispatch(patchUI({ loading: false, error: e.message })); }
  };
  const save = async () => {
    dispatch(patchUI({ loading: true, error: '', message: 'Saving complaint…' }));
    try { const saved = await api.save(complaint); dispatch(patchUI({ loading: false, savedId: saved.id, message: `Complaint #${saved.id} saved successfully.` })); }
    catch (e) { dispatch(patchUI({ loading: false, error: e.message })); }
  };
  const onFile = async (file) => {
    if (!file) return;
    dispatch(patchUI({ loading: true, message: `Reading ${file.name}…`, error: '' }));
    try {
      if (file.name.toLowerCase().endsWith('.txt') || file.name.toLowerCase().endsWith('.eml')) {
        const text = await file.text();
        setAssistantText(text.slice(0, 12000));
        dispatch(patchUI({ loading: false, message: 'Document loaded. Click Analyze Complaint to extract fields.' }));
      } else {
        const extracted = await api.extractFile(file);
        dispatch(hydrate(extracted));
        dispatch(patchUI({ loading: false, extracted, message: `${file.name} parsed and fields extracted.` }));
      }
    } catch (e) { dispatch(patchUI({ loading: false, error: e.message })); }
  };

  return <div className="app-shell">
    <header className="topbar"><div className="brand"><div className="brand-mark">A</div><div><div className="brand-name">AIVOA</div><div className="brand-sub">Complaint Operations Console</div></div></div><div className="top-actions"><span className="status-dot"/> AI service ready <span className="badge">Round 1 Demo</span></div></header>
    <main className="content">
      <div className="page-head"><div><h1>Log Customer Complaint</h1><p>AI-Powered Customer Complaint Management for pharmaceutical quality teams.</p></div><span className="triage-badge">{complaint.status}</span></div>
      <div className="grid">
        <section className="card form-card">
          <div className="section-title"><span>1</span><div><h2>Complaint Information</h2><p>Capture traceability and complaint details.</p></div></div>
          <div className="form-grid">
            {fields.map(([key,label,type]) => <label key={key} className={type === 'textarea' ? 'full' : ''}><span>{label}</span>{type === 'select' ? <select value={complaint[key]} onChange={e=>set(key,e.target.value)}>{key==='complaint_source' ? ['Customer Email','Phone','Distributor','Field Complaint','Regulatory Authority'].map(x=><option key={x}>{x}</option>) : ['Low','Medium','High','Critical'].map(x=><option key={x}>{x}</option>)}</select> : type==='textarea' ? <textarea value={complaint[key]} onChange={e=>set(key,e.target.value)} rows={key==='complaint_details'?5:3}/> : <input value={complaint[key]} onChange={e=>set(key,e.target.value)} />}</label>)}
          </div>
          <div className="actions"><button className="secondary" onClick={()=>{dispatch(reset());dispatch(clearUI())}}>Reset Form</button><button className="primary" onClick={save}>Save Complaint</button></div>
        </section>
        <aside className="card assistant-card">
          <div className="assistant-head"><div className="spark">✦</div><div><h2>AI Complaint Intake Assistant</h2><p>Extract facts, triage risk, and identify gaps.</p></div></div>
          <div className="dropzone" onDragOver={e=>e.preventDefault()} onDrop={e=>{e.preventDefault(); onFile(e.dataTransfer.files?.[0])}}><input id="file" type="file" accept=".txt,.eml,.pdf,.doc,.docx" hidden onChange={e=>onFile(e.target.files?.[0])}/><div className="upload-icon">⇧</div><div>Drag & drop complaint document</div><small>or <label htmlFor="file" className="link">click to browse</label></small></div>
          <div className="or">OR</div>
          <textarea className="assistant-input" value={assistantText} onChange={e=>setAssistantText(e.target.value)} rows={8} placeholder="Paste complaint text or email here…"/>
          <button className="primary wide" onClick={startAI} disabled={ui.loading}>{ui.loading ? 'Analyzing…' : 'Analyze Complaint'}</button>
          {ui.message && <div className="notice success">✓ {ui.message}</div>}
          {ui.error && <div className="notice error">⚠ {ui.error}</div>}
          <div className="results">
            <h3>AI Assessment</h3>
            {ui.risk ? <div className="risk-box"><div><span className="mini-label">Risk</span><strong>{ui.risk.risk_level}</strong></div><div className="score">{ui.risk.score}<span>/100</span></div></div> : <div className="empty">Run analysis to see risk assessment.</div>}
            {ui.completeness && <div className="completeness"><div><span>Completeness</span><strong>{ui.completeness.score}%</strong></div><div className="progress"><span style={{width:`${ui.completeness.score}%`}}/></div>{ui.completeness.missing_fields.length>0 && <small>Missing: {ui.completeness.missing_fields.join(', ')}</small>}</div>}
            <button className="secondary wide" onClick={assess}>Refresh Full AI Assessment</button>
            {ui.rootCause && <div className="ai-list"><h4>Root Cause / CAPA</h4><ul>{ui.rootCause.capa_recommendations.slice(0,3).map(x=><li key={x}>{x}</li>)}</ul></div>}
          </div>
        </aside>
      </div>
    </main>
    <footer>Built for AIVOA Round 1 • FastAPI + React/Redux + LangGraph + Gemini</footer>
  </div>;
}

createRoot(document.getElementById('root')).render(<Provider store={store}><App/></Provider>);
