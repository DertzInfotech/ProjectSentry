import { HEALTH_SCORE_RANGES } from './constants';

// Format file size
export const formatFileSize = (bytes) => {
  if (!bytes || bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

// Format date to readable format
export const formatDate = (dateString) => {
  if (!dateString) return 'Unknown';

  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now - date);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  if (diffDays === 1) return 'Today';
  if (diffDays === 2) return 'Yesterday';
  if (diffDays <= 7) return `${diffDays} days ago`;
  if (diffDays <= 30) return `${Math.ceil(diffDays / 7)} weeks ago`;

  return date.toLocaleDateString();
};

// Format relative time (for activity feeds)
export const formatRelativeTime = (dateString) => {
  if (!dateString) return 'Unknown';

  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now - date);
  const diffMinutes = Math.ceil(diffTime / (1000 * 60));
  const diffHours = Math.ceil(diffTime / (1000 * 60 * 60));
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  if (diffMinutes < 60) return `${diffMinutes}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;

  return formatDate(dateString);
};

// Get health score information (color, label, etc.)
export const getHealthScoreInfo = (score) => {
  if (typeof score !== 'number') return HEALTH_SCORE_RANGES.POOR;

  for (const range of Object.values(HEALTH_SCORE_RANGES)) {
    if (score >= range.min && score <= range.max) {
      return range;
    }
  }
  return HEALTH_SCORE_RANGES.POOR;
};

// Get severity color for issues
export const getSeverityColor = (severity) => {
  const colors = {
    critical: '#e53e3e',
    warning: '#ed8936', 
    info: '#3182ce'
  };
  return colors[severity] || colors.info;
};

// Validate file type
export const validateFileType = (file) => {
  if (!file || !file.name) return false;

  const validExtensions = ['.ifc', '.IFC'];
  const extension = '.' + file.name.split('.').pop();
  return validExtensions.includes(extension);
};

// Validate file size
export const validateFileSize = (file, maxSizeInBytes = 500 * 1024 * 1024) => {
  if (!file || !file.size) return false;
  return file.size <= maxSizeInBytes;
};

// Generate unique ID
export const generateId = () => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
};

// Debounce function for search/filtering
export const debounce = (func, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

// Truncate text with ellipsis
export const truncateText = (text, maxLength = 50) => {
  if (!text || typeof text !== 'string') return '';
  if (text.length <= maxLength) return text;
  return text.substr(0, maxLength).trim() + '...';
};

// Calculate percentage
export const calculatePercentage = (value, total) => {
  if (!total || total === 0) return 0;
  return Math.round((value / total) * 100);
};

// Format number with thousands separator
export const formatNumber = (num) => {
  if (!num && num !== 0) return '0';
  return num.toLocaleString();
};

// Check if mobile device
export const isMobile = () => {
  return window.innerWidth <= 768;
};

// Check if touch device
export const isTouchDevice = () => {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
};

// Get browser info
export const getBrowserInfo = () => {
  const ua = navigator.userAgent;
  const browser = {
    name: 'Unknown',
    version: 'Unknown'
  };

  if (ua.includes('Chrome')) {
    browser.name = 'Chrome';
    browser.version = ua.match(/Chrome\/([0-9.]+)/)?.[1] || 'Unknown';
  } else if (ua.includes('Firefox')) {
    browser.name = 'Firefox';
    browser.version = ua.match(/Firefox\/([0-9.]+)/)?.[1] || 'Unknown';
  } else if (ua.includes('Safari')) {
    browser.name = 'Safari';
    browser.version = ua.match(/Version\/([0-9.]+)/)?.[1] || 'Unknown';
  }

  return browser;
};

// Export all functions as default
export default {
  formatFileSize,
  formatDate,
  formatRelativeTime,
  getHealthScoreInfo,
  getSeverityColor,
  validateFileType,
  validateFileSize,
  generateId,
  debounce,
  truncateText,
  calculatePercentage,
  formatNumber,
  isMobile,
  isTouchDevice,
  getBrowserInfo
};