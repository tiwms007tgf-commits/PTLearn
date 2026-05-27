/**
 * static/js/main.js
 * Main JavaScript with common utilities and DOM management
 */

// Utility Functions
class Utils {
  static async fetch(url, options = {}) {
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Fetch error:', error);
      throw error;
    }
  }

  static showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} animate-slide-in`;
    alert.textContent = message;
    
    const container = document.querySelector('.page-content') || document.body;
    container.insertBefore(alert, container.firstChild);
    
    setTimeout(() => {
      alert.style.animation = 'fadeOut 0.3s ease-out forwards';
      setTimeout(() => alert.remove(), 300);
    }, 4000);
  }

  static formatDate(date) {
    if (typeof date === 'string') {
      date = new Date(date);
    }
    
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  }

  static formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}m ${secs}s`;
  }

  static debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  static throttle(func, limit) {
    let inThrottle;
    return function(...args) {
      if (!inThrottle) {
        func.apply(this, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  }

  static createElement(tag, classes = '', innerHTML = '') {
    const element = document.createElement(tag);
    if (classes) element.className = classes;
    if (innerHTML) element.innerHTML = innerHTML;
    return element;
  }
}

// API Client
class APIClient {
  static async get(endpoint) {
    return Utils.fetch(endpoint);
  }

  static async post(endpoint, data) {
    return Utils.fetch(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  static async getDashboard() {
    return this.get('/progress/api/dashboard');
  }

  static async getLessons() {
    return this.get('/lessons/api/path');
  }

  static async getLesson(slug) {
    return this.get(`/lessons/api/${slug}`);
  }

  static async completeLesson(lessonId, code = null) {
    return this.post(`/lessons/api/${lessonId}/complete`, {
      code_attempted: code
    });
  }

  static async getQuiz(quizId) {
    return this.get(`/quizzes/api/${quizId}`);
  }

  static async submitQuiz(quizId, answers, timeSpent) {
    return this.post(`/quizzes/api/${quizId}/submit`, {
      answers,
      time_spent: timeSpent
    });
  }

  static async executeCode(code) {
    return this.post('/code-lab/api/execute', { code });
  }

  static async getAchievements() {
    return this.get('/progress/api/achievements');
  }

  static async getLeaderboard(limit = 50) {
    return this.get(`/progress/api/leaderboard?limit=${limit}`);
  }
}

// DOM Helpers
class DOM {
  static byId(id) {
    return document.getElementById(id);
  }

  static query(selector) {
    return document.querySelector(selector);
  }

  static queryAll(selector) {
    return document.querySelectorAll(selector);
  }

  static on(selector, event, handler) {
    const elements = typeof selector === 'string' 
      ? DOM.queryAll(selector) 
      : [selector];
    
    elements.forEach(el => {
      if (el) el.addEventListener(event, handler);
    });
  }

  static addClass(selector, className) {
    const elements = typeof selector === 'string' 
      ? DOM.queryAll(selector) 
      : [selector];
    
    elements.forEach(el => {
      if (el) el.classList.add(className);
    });
  }

  static removeClass(selector, className) {
    const elements = typeof selector === 'string' 
      ? DOM.queryAll(selector) 
      : [selector];
    
    elements.forEach(el => {
      if (el) el.classList.remove(className);
    });
  }

  static toggleClass(selector, className) {
    const elements = typeof selector === 'string' 
      ? DOM.queryAll(selector) 
      : [selector];
    
    elements.forEach(el => {
      if (el) el.classList.toggle(className);
    });
  }

  static setStyle(selector, styles) {
    const elements = typeof selector === 'string' 
      ? DOM.queryAll(selector) 
      : [selector];
    
    elements.forEach(el => {
      if (el) {
        Object.assign(el.style, styles);
      }
    });
  }

  static show(selector) {
    DOM.addClass(selector, 'visible');
    DOM.removeClass(selector, 'hidden');
  }

  static hide(selector) {
    DOM.addClass(selector, 'hidden');
    DOM.removeClass(selector, 'visible');
  }
}

// Modal Management
class Modal {
  static open(modalId) {
    const modal = DOM.byId(modalId);
    if (modal) {
      modal.style.display = 'flex';
      modal.classList.add('animate-fade-in');
    }
  }

  static close(modalId) {
    const modal = DOM.byId(modalId);
    if (modal) {
      modal.style.display = 'none';
    }
  }

  static openLevelUp(level, xp) {
    DOM.byId('newLevel').textContent = level;
    DOM.byId('xpGained').textContent = xp;
    Modal.open('levelUpModal');
  }
}

// Form Helpers
class Form {
  static serialize(formElement) {
    const data = new FormData(formElement);
    const obj = {};
    data.forEach((value, key) => {
      obj[key] = value;
    });
    return obj;
  }

  static validate(formElement) {
    const inputs = formElement.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
      if (!input.value.trim()) {
        input.classList.add('error');
        isValid = false;
      } else {
        input.classList.remove('error');
      }
    });

    return isValid;
  }

  static clearErrors(formElement) {
    formElement.querySelectorAll('.error').forEach(el => {
      el.classList.remove('error');
    });
  }
}

// Notification System
class Notification {
  static show(message, type = 'info', duration = 4000) {
    Utils.showAlert(message, type);
  }

  static success(message) {
    this.show(message, 'success');
  }

  static error(message) {
    this.show(message, 'error');
  }

  static warning(message) {
    this.show(message, 'warning');
  }

  static info(message) {
    this.show(message, 'info');
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  // Set theme preference label
  const isDark = document.body.classList.contains('dark-mode');
  const themeBtn = document.getElementById('themeToggle');
  if (themeBtn) {
    themeBtn.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
  }

  // Add loading state management
  window.isLoading = false;

  // Global error handler
  window.addEventListener('error', function(e) {
    console.error('Global error:', e);
    Notification.error('An unexpected error occurred');
  });

  // Network error handling
  window.addEventListener('offline', function() {
    Notification.warning('You are offline. Some features may not work.');
  });

  window.addEventListener('online', function() {
    Notification.success('You are back online!');
  });
});

// Prevent accidental page close
let isDirty = false;
window.addEventListener('beforeunload', function(e) {
  if (isDirty) {
    e.preventDefault();
    e.returnValue = '';
  }
});

// Mark page as dirty when form inputs change
document.addEventListener('change', function(e) {
  if (e.target.tagName === 'INPUT' || 
      e.target.tagName === 'TEXTAREA' || 
      e.target.tagName === 'SELECT') {
    isDirty = true;
  }
}, true);

// Mark clean when form is submitted
document.addEventListener('submit', function(e) {
  isDirty = false;
}, true);

// Export for use in other modules
window.Utils = Utils;
window.APIClient = APIClient;
window.DOM = DOM;
window.Modal = Modal;
window.Form = Form;
window.Notification = Notification;