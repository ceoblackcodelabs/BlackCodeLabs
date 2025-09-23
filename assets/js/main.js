// Main JavaScript for BlackCodeLabs
document.addEventListener('DOMContentLoaded', function() {
    // Initialize everything when DOM is loaded
    initSpace();
    initScrollAnimations();
    initNavigation();
    initStatistics();
    initHeaderScroll();
    initNewsletter();
    initLoadingAnimation();
});

// Space Scene Initialization
let scene, camera, renderer, stars;

function initSpace() {
    if (document.getElementById('space-container')) {
        // Scene setup
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('space-container').appendChild(renderer.domElement);
        
        // Create stars
        const starGeometry = new THREE.BufferGeometry();
        const starVertices = [];
        for (let i = 0; i < 10000; i++) {
            const x = (Math.random() - 0.5) * 2000;
            const y = (Math.random() - 0.5) * 2000;
            const z = (Math.random() - 0.5) * 2000;
            starVertices.push(x, y, z);
        }
        starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));
        const starMaterial = new THREE.PointsMaterial({ 
            color: 0xffffff, 
            size: 1.2,
            sizeAttenuation: true
        });
        stars = new THREE.Points(starGeometry, starMaterial);
        scene.add(stars);
        
        // Set camera position
        camera.position.z = 100;
        
        // Animation loop
        animateSpace();
        
        // Handle window resize
        window.addEventListener('resize', onWindowResize);
    }
}

function animateSpace() {
    requestAnimationFrame(animateSpace);
    stars.rotation.x += 0.0005;
    stars.rotation.y += 0.0005;
    renderer.render(scene, camera);
}

function onWindowResize() {
    if (camera && renderer) {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

// Header Scroll Effect
function initHeaderScroll() {
    window.addEventListener('scroll', function() {
        const header = document.querySelector('header');
        if (window.scrollY > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        updateNavigation();
    });
}

// Scroll Animations
function initScrollAnimations() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                
                // Animate statistics if in view
                if (entry.target.classList.contains('statistics')) {
                    animateStatistics();
                }
            }
        });
    }, observerOptions);
    
    // Observe elements
    document.querySelectorAll('.feature-card, .service-card, .value-card').forEach(card => {
        observer.observe(card);
    });
}

// Navigation Dots
function initNavigation() {
    const sections = document.querySelectorAll('section[id]');
    const dots = document.querySelectorAll('.nav-dot');
    
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            if (sections[index]) {
                sections[index].scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

function updateNavigation() {
    const sections = document.querySelectorAll('section[id]');
    const dots = document.querySelectorAll('.nav-dot');
    
    let currentSection = '';
    const scrollPos = window.scrollY + 200;
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
            currentSection = section.getAttribute('id');
        }
    });
    
    dots.forEach(dot => {
        dot.classList.remove('active');
        if (dot.getAttribute('data-section').toLowerCase() === currentSection) {
            dot.classList.add('active');
        }
    });
}

// Statistics Counter
function initStatistics() {
    // Will be animated when section comes into view
}

function animateStatistics() {
    const stat1 = document.getElementById('stat1');
    const stat2 = document.getElementById('stat2');
    const stat3 = document.getElementById('stat3');
    const stat4 = document.getElementById('stat4');
    
    if (!stat1 || stat1.textContent !== '0') return; // Prevent re-animation
    
    const targetValues = [150, 380, 98, 45];
    const duration = 3000;
    const interval = 20;
    
    const counters = [stat1, stat2, stat3, stat4];
    
    counters.forEach((counter, index) => {
        let current = 0;
        const increment = targetValues[index] / (duration / interval);
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= targetValues[index]) {
                clearInterval(timer);
                current = targetValues[index];
            }
            
            if (index === 2) { // Percentage
                counter.textContent = Math.round(current) + '%';
            } else {
                counter.textContent = Math.round(current);
            }
        }, interval);
    });
}

// Newsletter Form
function initNewsletter() {
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input').value;
            
            // Simple validation
            if (!email || !email.includes('@')) {
                showNotification('Please enter a valid email address.', 'error');
                return;
            }
            
            // Simulate submission
            showNotification('Thank you for subscribing to our newsletter!', 'success');
            this.querySelector('input').value = '';
        });
    }
}

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">&times;</button>
    `;
    
    // Add styles if not exists
    if (!document.querySelector('#notification-styles')) {
        const styles = document.createElement('style');
        styles.id = 'notification-styles';
        styles.textContent = `
            .notification {
                position: fixed;
                top: 100px;
                right: 30px;
                padding: 15px 20px;
                border-radius: 10px;
                color: white;
                z-index: 10000;
                display: flex;
                align-items: center;
                gap: 15px;
                max-width: 400px;
                animation: slideIn 0.3s ease;
            }
            .notification.success { background: var(--success-green); }
            .notification.error { background: var(--warning-orange); }
            .notification button { 
                background: none; 
                border: none; 
                color: white; 
                font-size: 20px;
                cursor: pointer;
            }
            @keyframes slideIn {
                from { transform: translateX(100%); }
                to { transform: translateX(0); }
            }
        `;
        document.head.appendChild(styles);
    }
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Loading Animation
function initLoadingAnimation() {
    const loading = document.querySelector('.loading');
    if (loading) {
        // Simulate loading time
        setTimeout(() => {
            loading.classList.add('hidden');
        }, 2000);
    }
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// CTA Button Handler
document.querySelectorAll('.cta-button').forEach(button => {
    button.addEventListener('click', function() {
        // Scroll to contact section or show contact modal
        const contactSection = document.getElementById('contact');
        if (contactSection) {
            contactSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            window.location.href = 'contact.html';
        }
    });
});