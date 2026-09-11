import { configureStore, createSlice } from '@reduxjs/toolkit';

const initialComplaint = {
  complaint_source: 'Customer Email', customer_name: '', product_name: '', product_strength: '', batch_number: '',
  manufacturing_date: '', expiry_date: '', complaint_details: '', patient_or_consumer: '', initial_assessment: '', priority: 'Medium', status: 'Pending Triage'
};

const complaintSlice = createSlice({
  name: 'complaint', initialState: initialComplaint,
  reducers: {
    updateField: (state, action) => { state[action.payload.key] = action.payload.value; },
    hydrate: (state, action) => Object.assign(state, action.payload),
    reset: () => ({ ...initialComplaint })
  }
});

const uiSlice = createSlice({
  name: 'ui', initialState: { loading: false, message: '', error: '', extracted: null, risk: null, completeness: null, rootCause: null, savedId: null },
  reducers: {
    patchUI: (state, action) => Object.assign(state, action.payload),
    clearUI: () => ({ loading: false, message: '', error: '', extracted: null, risk: null, completeness: null, rootCause: null, savedId: null })
  }
});

export const { updateField, hydrate, reset } = complaintSlice.actions;
export const { patchUI, clearUI } = uiSlice.actions;
export const store = configureStore({ reducer: { complaint: complaintSlice.reducer, ui: uiSlice.reducer } });
