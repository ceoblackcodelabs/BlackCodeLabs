// script.js

// Loading Animation
window.addEventListener('load', function() {
    const loading = document.getElementById('loading');
    setTimeout(() => {
        loading.classList.add('hidden');
    }, 800);
});

// Mobile Navigation Toggle
const mobileToggle = document.getElementById('mobileToggle');
const navLinks = document.getElementById('navLinks');

if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        mobileToggle.innerHTML = navLinks.classList.contains('active') 
            ? '<i class="fas fa-times"></i>' 
            : '<i class="fas fa-bars"></i>';
    });
    
    // Close mobile menu when clicking a link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            mobileToggle.innerHTML = '<i class="fas fa-bars"></i>';
        });
    });
}

// Header scroll effect
const header = document.getElementById('header');
if (header) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
}

// Animated Statistics Counter
function animateCounter(elementId, finalValue, suffix = '', duration = 2000) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    let startValue = 0;
    const increment = finalValue / (duration / 16);
    const timer = setInterval(() => {
        startValue += increment;
        if (startValue >= finalValue) {
            if (suffix === '%') {
                element.textContent = finalValue.toFixed(1) + suffix;
            } else {
                element.textContent = finalValue.toLocaleString() + suffix;
            }
            clearInterval(timer);
        } else {
            if (suffix === '%') {
                element.textContent = startValue.toFixed(1) + suffix;
            } else {
                element.textContent = Math.floor(startValue).toLocaleString() + suffix;
            }
        }
    }, 16);
}

// Initialize counters when in viewport
const observerOptions = {
    threshold: 0.5
};

const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateCounter('stat1', 1250);
            animateCounter('stat2', 8.2, '%');
            animateCounter('stat3', 324);
            animateCounter('stat4', 27500);
            statsObserver.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe hero stats section
const heroStats = document.querySelector('.hero-stats');
if (heroStats) {
    statsObserver.observe(heroStats);
}

// Forex Ticker Data
const forexPairs = [
    { pair: "EUR/USD", price: "1.0894", change: "+0.0024" },
    { pair: "GBP/USD", price: "1.2541", change: "+0.0018" },
    { pair: "USD/JPY", price: "138.62", change: "-0.24" },
    { pair: "AUD/USD", price: "0.6678", change: "-0.0012" },
    { pair: "USD/CAD", price: "1.3521", change: "+0.0015" },
    { pair: "NZD/USD", price: "0.6234", change: "-0.0008" },
    { pair: "USD/CHF", price: "0.8942", change: "-0.0010" },
    { pair: "XAU/USD", price: "1978.42", change: "+12.56" },
    { pair: "BTC/USD", price: "27350", change: "+420" },
    { pair: "ETH/USD", price: "1850", change: "+32" }
];

// Create ticker items
function initTicker() {
    const ticker = document.getElementById('forexTicker');
    if (!ticker) return;
    
    // Clear existing content
    ticker.innerHTML = '';
    
    // Duplicate items for seamless looping
    [...forexPairs, ...forexPairs].forEach(pair => {
        const tickerItem = document.createElement('div');
        tickerItem.className = 'ticker-item';
        
        const changeValue = parseFloat(pair.change);
        const changeClass = changeValue >= 0 ? 'positive' : 'negative';
        
        tickerItem.innerHTML = `
            <span class="ticker-pair">${pair.pair}</span>
            <span class="ticker-price">${pair.price}</span>
            <span class="ticker-change ${changeClass}">${pair.change}</span>
        `;
        
        ticker.appendChild(tickerItem);
    });
}

// Update ticker prices randomly
function updateTickerPrices() {
    const tickerItems = document.querySelectorAll('.ticker-item');
    
    tickerItems.forEach(item => {
        const priceElement = item.querySelector('.ticker-price');
        const changeElement = item.querySelector('.ticker-change');
        
        if (priceElement && changeElement) {
            const currentPrice = parseFloat(priceElement.textContent);
            const change = (Math.random() - 0.5) * 0.01;
            const newPrice = currentPrice + change;
            
            priceElement.textContent = newPrice.toFixed(4);
            
            // Update change with new random value
            const newChange = (Math.random() - 0.5) * 0.005;
            const changeClass = newChange >= 0 ? 'positive' : 'negative';
            
            changeElement.textContent = (newChange >= 0 ? '+' : '') + newChange.toFixed(4);
            changeElement.className = `ticker-change ${changeClass}`;
        }
    });
}

// Create animated chart
function createAnimatedChart() {
    const chart = document.getElementById('liveChart');
    if (!chart) return;
    
    // Create SVG element
    const svgNS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("viewBox", "0 0 500 300");
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "100%");
    
    // Create chart line
    const path = document.createElementNS(svgNS, "path");
    const points = generateChartPoints();
    path.setAttribute("d", pointsToPath(points));
    path.setAttribute("stroke", "#d4af37");
    path.setAttribute("stroke-width", "2");
    path.setAttribute("fill", "none");
    path.setAttribute("class", "chart-line");
    path.style.strokeDasharray = "1000";
    path.style.strokeDashoffset = "1000";
    path.style.transition = "stroke-dashoffset 3s ease-in-out";
    
    svg.appendChild(path);
    chart.appendChild(svg);
    
    // Animate the line drawing
    setTimeout(() => {
        path.style.strokeDashoffset = "0";
    }, 500);
    
    // Create gradient effect
    const defs = document.createElementNS(svgNS, "defs");
    const gradient = document.createElementNS(svgNS, "linearGradient");
    gradient.setAttribute("id", "chartGradient");
    gradient.setAttribute("x1", "0%");
    gradient.setAttribute("y1", "0%");
    gradient.setAttribute("x2", "0%");
    gradient.setAttribute("y2", "100%");
    
    const stop1 = document.createElementNS(svgNS, "stop");
    stop1.setAttribute("offset", "0%");
    stop1.setAttribute("stop-color", "rgba(212, 175, 55, 0.3)");
    
    const stop2 = document.createElementNS(svgNS, "stop");
    stop2.setAttribute("offset", "100%");
    stop2.setAttribute("stop-color", "rgba(212, 175, 55, 0)");
    
    gradient.appendChild(stop1);
    gradient.appendChild(stop2);
    defs.appendChild(gradient);
    svg.appendChild(defs);
    
    // Create area under the line
    const areaPath = document.createElementNS(svgNS, "path");
    areaPath.setAttribute("d", pointsToAreaPath(points));
    areaPath.setAttribute("fill", "url(#chartGradient)");
    svg.insertBefore(areaPath, path);
}

function generateChartPoints() {
    const points = [];
    const pointCount = 20;
    let currentY = 150;
    
    for (let i = 0; i < pointCount; i++) {
        const x = (i / (pointCount - 1)) * 500;
        // Random walk for price simulation
        currentY += (Math.random() - 0.5) * 40;
        // Keep within bounds
        currentY = Math.max(50, Math.min(250, currentY));
        points.push({ x, y: currentY });
    }
    
    return points;
}

function pointsToPath(points) {
    if (points.length === 0) return "";
    
    let path = `M ${points[0].x} ${points[0].y}`;
    
    for (let i = 1; i < points.length; i++) {
        const prev = points[i - 1];
        const curr = points[i];
        
        // Create smooth curve
        const cp1x = prev.x + (curr.x - prev.x) / 3;
        const cp1y = prev.y;
        const cp2x = curr.x - (curr.x - prev.x) / 3;
        const cp2y = curr.y;
        
        path += ` C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${curr.x} ${curr.y}`;
    }
    
    return path;
}

function pointsToAreaPath(points) {
    if (points.length === 0) return "";
    
    let path = `M ${points[0].x} ${points[0].y}`;
    
    for (let i = 1; i < points.length; i++) {
        const prev = points[i - 1];
        const curr = points[i];
        
        const cp1x = prev.x + (curr.x - prev.x) / 3;
        const cp1y = prev.y;
        const cp2x = curr.x - (curr.x - prev.x) / 3;
        const cp2y = curr.y;
        
        path += ` C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${curr.x} ${curr.y}`;
    }
    
    // Close the path to create area
    path += ` L ${points[points.length - 1].x} 300`;
    path += ` L ${points[0].x} 300`;
    path += " Z";
    
    return path;
}

// Contact Form Submission
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form values
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const interest = document.getElementById('interest').value;
        
        // Simple validation
        if (!name || !email || !interest) {
            alert('Please fill in all required fields.');
            return;
        }
        
        // Simulate form submission
        const submitBtn = contactForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        submitBtn.disabled = true;
        
        setTimeout(() => {
            alert(`Thank you ${name}! Your inquiry about ${getInterestText(interest)} has been received. We'll contact you at ${email} within 24 hours.`);
            contactForm.reset();
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }, 1500);
    });
}

function getInterestText(value) {
    const interests = {
        'vip-pro': 'VIP Pro Trader Program',
        'vip-elite': 'VIP Elite Program',
        'vip-master': 'Master Class Program',
        'partnership': 'Business Partnership',
        'general': 'General Inquiry'
    };
    
    return interests[value] || 'your selected program';
}

// Modal functionality
const loginModal = document.getElementById('login-modal');
const loginBtn = document.querySelector('.login-btn');
const modalClose = document.querySelector('.modal-close');

if (loginBtn && loginModal) {
    loginBtn.addEventListener('click', function(e) {
        e.preventDefault();
        loginModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
}

if (modalClose && loginModal) {
    modalClose.addEventListener('click', function() {
        loginModal.classList.remove('active');
        document.body.style.overflow = '';
    });
}

// Close modal when clicking outside
window.addEventListener('click', function(e) {
    if (loginModal && e.target === loginModal) {
        loginModal.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// Newsletter form submission
const newsletterForms = document.querySelectorAll('.newsletter-form');
newsletterForms.forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const emailInput = form.querySelector('input[type="email"]');
        const email = emailInput.value;
        
        if (!email) {
            alert('Please enter your email address.');
            return;
        }
        
        // Simulate subscription
        emailInput.value = '';
        alert('Thank you for subscribing to our newsletter!');
    });
});

// Timeframe switching for chart
const timeframes = document.querySelectorAll('.timeframe');
timeframes.forEach(timeframe => {
    timeframe.addEventListener('click', function() {
        timeframes.forEach(tf => tf.classList.remove('active'));
        this.classList.add('active');
        
        // In a real app, this would update the chart data
        console.log(`Switched to ${this.textContent} timeframe`);
    });
});

// Blog and Events Page Functionality
function initBlogPage() {
    // Category filtering
    const categoryBtns = document.querySelectorAll('.category-btn');
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            categoryBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            const category = this.dataset.category || 'all';
            filterBlogPosts(category);
        });
    });
    
    // Search functionality
    const blogSearch = document.querySelector('.blog-search');
    if (blogSearch) {
        const searchInput = blogSearch.querySelector('input');
        const searchBtn = blogSearch.querySelector('button');
        
        searchBtn.addEventListener('click', function() {
            searchBlogPosts(searchInput.value);
        });
        
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchBlogPosts(searchInput.value);
            }
        });
    }
}

function filterBlogPosts(category) {
    const posts = document.querySelectorAll('.blog-post-card');
    
    posts.forEach(post => {
        const postCategory = post.dataset.category;
        
        if (category === 'all' || postCategory === category) {
            post.style.display = 'block';
            setTimeout(() => {
                post.style.opacity = '1';
                post.style.transform = 'translateY(0)';
            }, 10);
        } else {
            post.style.opacity = '0';
            post.style.transform = 'translateY(20px)';
            setTimeout(() => {
                post.style.display = 'none';
            }, 300);
        }
    });
}

function searchBlogPosts(query) {
    const posts = document.querySelectorAll('.blog-post-card');
    const lowercaseQuery = query.toLowerCase();
    
    posts.forEach(post => {
        const title = post.querySelector('.post-title').textContent.toLowerCase();
        const excerpt = post.querySelector('.post-excerpt').textContent.toLowerCase();
        
        if (title.includes(lowercaseQuery) || excerpt.includes(lowercaseQuery)) {
            post.style.display = 'block';
            setTimeout(() => {
                post.style.opacity = '1';
                post.style.transform = 'translateY(0)';
            }, 10);
        } else {
            post.style.opacity = '0';
            post.style.transform = 'translateY(20px)';
            setTimeout(() => {
                post.style.display = 'none';
            }, 300);
        }
    });
}

function initEventsPage() {
    // Event filtering
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            const filter = this.dataset.filter || 'all';
            filterEvents(filter);
        });
    });
}

function filterEvents(filter) {
    const events = document.querySelectorAll('.event-card');
    
    events.forEach(event => {
        const eventType = event.dataset.type;
        
        if (filter === 'all' || eventType === filter) {
            event.style.display = 'block';
            setTimeout(() => {
                event.style.opacity = '1';
                event.style.transform = 'translateY(0)';
            }, 10);
        } else {
            event.style.opacity = '0';
            event.style.transform = 'translateY(20px)';
            setTimeout(() => {
                event.style.display = 'none';
            }, 300);
        }
    });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            const headerHeight = header ? header.offsetHeight : 80;
            const targetPosition = targetElement.offsetTop - headerHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initTicker();
    createAnimatedChart();
    
    // Check which page we're on and initialize accordingly
    if (document.querySelector('.blog-content')) {
        initBlogPage();
    }
    
    if (document.querySelector('.events-content')) {
        initEventsPage();
    }
    
    // Update ticker prices every 5 seconds
    setInterval(updateTickerPrices, 5000);
    
    // Update chart animation periodically
    setInterval(() => {
        const chart = document.getElementById('liveChart');
        if (chart) {
            chart.innerHTML = '';
            createAnimatedChart();
        }
    }, 10000);
});