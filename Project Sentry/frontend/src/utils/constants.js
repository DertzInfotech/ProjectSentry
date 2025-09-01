// Application constants

export const VIEWS = {
  DASHBOARD: 'dashboard',
  UPLOAD: 'upload', 
  ISSUES: 'issues',
  VIEWER: 'viewer'
};

export const PROJECT_STATUS = {
  PROCESSING: 'Processing',
  COMPLETED: 'Completed',
  ERROR: 'Error',
  PENDING: 'Pending'
};

export const ISSUE_SEVERITY = {
  CRITICAL: 'critical',
  WARNING: 'warning',
  INFO: 'info'
};

export const HEALTH_SCORE_RANGES = {
  EXCELLENT: { min: 90, max: 100, label: 'Excellent', color: '#38a169' },
  GOOD: { min: 80, max: 89, label: 'Good', color: '#38a169' },
  FAIR: { min: 70, max: 79, label: 'Fair', color: '#ed8936' },
  POOR: { min: 0, max: 69, label: 'Poor', color: '#e53e3e' }
};

export const FILE_TYPES = {
  IFC: {
    extensions: ['.ifc', '.IFC'],
    mimeTypes: ['application/octet-stream'],
    maxSize: 500 * 1024 * 1024 // 500MB
  }
};

export const API_ENDPOINTS = {
  HEALTH: '/health',
  PROJECTS: '/projects',
  UPLOAD: '/upload',
  DASHBOARD: '/dashboard',
  ISSUES: '/issues'
};

export const NAVIGATION_ITEMS = [
  { id: VIEWS.DASHBOARD, label: 'Dashboard', icon: 'fas fa-chart-line' },
  { id: VIEWS.UPLOAD, label: 'Upload', icon: 'fas fa-cloud-upload-alt' },
  { id: VIEWS.ISSUES, label: 'Issues', icon: 'fas fa-exclamation-triangle' },
  { id: VIEWS.VIEWER, label: 'Viewer', icon: 'fas fa-cube' }
];

export default {
  VIEWS,
  PROJECT_STATUS,
  ISSUE_SEVERITY,
  HEALTH_SCORE_RANGES,
  FILE_TYPES,
  API_ENDPOINTS,
  NAVIGATION_ITEMS
};