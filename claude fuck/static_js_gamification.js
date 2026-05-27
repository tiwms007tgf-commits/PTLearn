/**
 * static/js/gamification.js
 * Gamification features: XP animations, level ups, achievements
 */

class Gamification {
  /**
   * Show floating XP gain text
   */
  static showXPGain(amount, x, y) {
    const xpElement = document.createElement('div');
    xpElement.className = 'xp-gain';
    xpElement.textContent = `+${amount} XP`;
    xpElement.style.left = `${x}px`;
    xpElement.style.top = `${y}px`;
    
    document.body.appendChild(xpElement);
    
    setTimeout(() => {
      xpElement.remove();
    }, 1500);
  }

  /**
   * Show XP gain from element click
   */
  static showXPFromElement(amount, element) {
    const rect = element.getBoundingClientRect();
    const x = rect.left + rect.width / 2;
    const y = rect.top;
    this.showXPGain(amount, x, y);
  }

  /**
   * Animate progress bar
   */
  static animateProgressBar(element, percentage) {
    if (!element) return;
    
    const bar = element.querySelector('.progress-bar');
    if (!bar) return;
    
    bar.style.transition = 'width 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
    bar.style.width = `${Math.min(percentage, 100)}%`;
  }

  /**
   * Show level up modal with animation
   */
  static showLevelUpModal(level, xp) {
    Modal.openLevelUp(level, xp);
    this.createConfetti();
  }

  /**
   * Create confetti animation
   */
  static createConfetti() {
    const colors = ['#6366f1', '#818cf8', '#10b981', '#f59e0b', '#ef4444'];
    
    for (let i = 0; i < 30; i++) {
      const confetti = document.createElement('div');
      confetti.className = 'level-up-confetti';
      confetti.innerHTML = ['🎉', '⭐', '🚀', '✨', '🏆'][Math.floor(Math.random() * 5)];
      confetti.style.left = Math.random() * window.innerWidth + 'px';
      confetti.style.top = '-50px';
      confetti.style.fontSize = '24px';
      confetti.style.opacity = '1';
      
      document.body.appendChild(confetti);
      
      setTimeout(() => {
        confetti.remove();
      }, 2000);
    }
  }

  /**
   * Update XP bar smoothly
   */
  static updateXPBar(currentXP, totalXP) {
    const percentage = (currentXP / totalXP) * 100;
    const bars = document.querySelectorAll('[data-xp-bar]');
    
    bars.forEach(bar => {
      this.animateProgressBar(bar, percentage);
    });
  }

  /**
   * Show achievement unlock
   */
  static showAchievementUnlock(title, icon, description) {
    const notification = document.createElement('div');
    notification.className = 'achievement-notification animate-slide-in';
    notification.innerHTML = `
      <div class="achievement-notification-content">
        <div class="achievement-icon" style="font-size: 48px;">${icon}</div>
        <div class="achievement-text">
          <h4>Achievement Unlocked!</h4>
          <p class="achievement-title">${title}</p>
          <p class="achievement-description">${description}</p>
        </div>
      </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.style.animation = 'slideInRight 0.4s ease-out reverse';
      setTimeout(() => notification.remove(), 400);
    }, 4000);
  }

  /**
   * Animate streak counter
   */
  static animateStreak(element, newStreak) {
    if (!element) return;
    
    element.classList.add('animate-bounce');
    const oldValue = parseInt(element.textContent);
    
    // Animate number increment
    for (let i = oldValue; i <= newStreak; i++) {
      setTimeout(() => {
        element.textContent = i;
      }, (i - oldValue) * 30);
    }
    
    setTimeout(() => {
      element.classList.remove('animate-bounce');
    }, 600);
  }

  /**
   * Show quiz result with animation
   */
  static showQuizResult(score, passed) {
    const resultElement = document.querySelector('[data-quiz-result]');
    if (!resultElement) return;
    
    const scoreText = resultElement.querySelector('.score-number');
    const statusBadge = resultElement.querySelector('[data-status-badge]');
    
    if (scoreText) {
      scoreText.classList.add('animate-scale-in');
      this.animateScoreCounter(scoreText, score);
    }
    
    if (statusBadge) {
      statusBadge.textContent = passed ? '✓ Passed' : '✗ Try Again';
      statusBadge.className = `badge ${passed ? 'badge-success' : 'badge-warning'}`;
      statusBadge.classList.add('animate-slide-in');
    }
  }

  /**
   * Animate score counter
   */
  static animateScoreCounter(element, finalScore) {
    let current = 0;
    const increment = Math.ceil(finalScore / 30);
    
    const timer = setInterval(() => {
      current += increment;
      if (current >= finalScore) {
        current = finalScore;
        clearInterval(timer);
      }
      element.textContent = current + '%';
    }, 20);
  }

  /**
   * Create particle effect
   */
  static createParticles(x, y, count = 10, type = 'xp') {
    const symbols = {
      'xp': '✨',
      'level': '⭐',
      'achievement': '🏆'
    };
    
    for (let i = 0; i < count; i++) {
      const particle = document.createElement('div');
      particle.textContent = symbols[type];
      particle.style.position = 'fixed';
      particle.style.left = x + 'px';
      particle.style.top = y + 'px';
      particle.style.fontSize = '20px';
      particle.style.pointerEvents = 'none';
      particle.style.zIndex = '9999';
      
      document.body.appendChild(particle);
      
      // Random direction
      const angle = (Math.PI * 2 * i) / count;
      const velocity = 2 + Math.random() * 3;
      const vx = Math.cos(angle) * velocity;
      const vy = Math.sin(angle) * velocity;
      
      let opacity = 1;
      let offsetX = 0;
      let offsetY = 0;
      
      const animate = () => {
        offsetX += vx;
        offsetY += vy;
        opacity -= 0.03;
        
        particle.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
        particle.style.opacity = opacity;
        
        if (opacity > 0) {
          requestAnimationFrame(animate);
        } else {
          particle.remove();
        }
      };
      
      animate();
    }
  }

  /**
   * Initialize gamification listeners
   */
  static init() {
    // Listen for quiz submissions
    document.addEventListener('quizSubmitted', (e) => {
      const { score, passed, xp } = e.detail;
      if (xp > 0) {
        this.showXPGain(xp, window.innerWidth / 2, window.innerHeight / 2);
        this.createParticles(window.innerWidth / 2, window.innerHeight / 2);
      }
    });

    // Listen for level ups
    document.addEventListener('levelUp', (e) => {
      const { level, xp } = e.detail;
      this.showLevelUpModal(level, xp);
    });

    // Listen for achievement unlocks
    document.addEventListener('achievementUnlock', (e) => {
      const { title, icon, description } = e.detail;
      this.showAchievementUnlock(title, icon, description);
    });
  }

  /**
   * Emit custom events
   */
  static emitQuizSubmitted(score, passed, xp) {
    document.dispatchEvent(new CustomEvent('quizSubmitted', {
      detail: { score, passed, xp }
    }));
  }

  static emitLevelUp(level, xp) {
    document.dispatchEvent(new CustomEvent('levelUp', {
      detail: { level, xp }
    }));
  }

  static emitAchievementUnlock(title, icon, description) {
    document.dispatchEvent(new CustomEvent('achievementUnlock', {
      detail: { title, icon, description }
    }));
  }
}

// Close level up modal
function closeLevelUpModal() {
  Modal.close('levelUpModal');
}

// Initialize gamification on page load
document.addEventListener('DOMContentLoaded', () => {
  Gamification.init();
});

// Export
window.Gamification = Gamification;

// Add styles dynamically
const style = document.createElement('style');
style.textContent = `
  .achievement-notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: var(--spacing-lg);
    box-shadow: var(--shadow-lg);
    z-index: 10000;
    max-width: 400px;
  }

  .achievement-notification-content {
    display: flex;
    gap: var(--spacing-lg);
    align-items: center;
  }

  .achievement-icon {
    flex-shrink: 0;
    animation: bounce 0.6s ease-out;
  }

  .achievement-text h4 {
    color: var(--accent-primary);
    font-size: var(--text-sm);
    margin: 0;
  }

  .achievement-title {
    font-weight: 700;
    margin: var(--spacing-sm) 0 0 0;
  }

  .achievement-description {
    font-size: var(--text-sm);
    color: var(--text-tertiary);
    margin: var(--spacing-xs) 0 0 0;
  }

  @media (max-width: 640px) {
    .achievement-notification {
      top: auto;
      bottom: 20px;
      left: 20px;
      right: 20px;
      max-width: none;
    }
  }
`;
document.head.appendChild(style);