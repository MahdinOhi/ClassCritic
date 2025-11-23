// ClassCritic - Frontend JavaScript

// Word Counter for Review Description
document.addEventListener('DOMContentLoaded', function() {
    const descriptionField = document.getElementById('review-description');
    const wordCounterDiv = document.getElementById('word-counter');
    
    if (descriptionField && wordCounterDiv) {
        descriptionField.addEventListener('input', function() {
            const text = this.value.trim();
            const wordCount = text ? text.split(/\s+/).length : 0;
            
            wordCounterDiv.textContent = `${wordCount} / 100 words`;
            
            if (wordCount >= 100) {
                wordCounterDiv.classList.add('valid');
                wordCounterDiv.classList.remove('invalid');
            } else {
                wordCounterDiv.classList.add('invalid');
                wordCounterDiv.classList.remove('valid');
            }
        });
    }
    
    // Points Slider Display
    const pointsSlider = document.getElementById('points-slider');
    const pointsDisplay = document.getElementById('points-display');
    
    if (pointsSlider && pointsDisplay) {
        pointsSlider.addEventListener('input', function() {
            pointsDisplay.textContent = this.value;
        });
    }
    
    // OTP Input Auto-focus
    const otpInput = document.querySelector('input[name="otp"]');
    if (otpInput) {
        otpInput.focus();
    }
    
    // Smooth Scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Auto-dismiss messages after 5 seconds
    setTimeout(function() {
        const messages = document.querySelectorAll('.alert');
        messages.forEach(function(message) {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        });
    }, 5000);
});
