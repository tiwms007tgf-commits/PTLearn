// Confetti effect for level up
function createConfetti() {
    for (let i = 0; i < 30; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.delay = Math.random() * 0.5 + 's';
        confetti.style.backgroundColor = ['#667eea', '#764ba2', '#f44336', '#4caf50'][Math.floor(Math.random() * 4)];
        document.body.appendChild(confetti);
        
        setTimeout(() => confetti.remove(), 3000);
    }
}

// Add CSS for confetti
const style = document.createElement('style');
style.textContent = `
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        pointer-events: none;
        animation: confetti-fall 3s ease-out forwards;
        z-index: 9999;
    }
    
    @keyframes confetti-fall {
        to {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// XP animation
function animateXPGain(amount) {
    const xpDisplay = document.querySelector('.xp-display');
    if (xpDisplay) {
        xpDisplay.style.animation = 'none';
        setTimeout(() => {
            xpDisplay.style.animation = 'pulse 0.5s ease';
        }, 10);
    }
}

// Pulse animation
const pulseStyle = document.createElement('style');
pulseStyle.textContent = `
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
`;
document.head.appendChild(pulseStyle);