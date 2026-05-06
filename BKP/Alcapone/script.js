// carousel-form.js - Event Data, Carousel Logic & Booking Form
// EVENTS DATA (4 max, images from unsplash/placeholder but stylish club theme)
const eventsData = [
  {
    title: "DJ KALONDE · AFRO HOUSE",
    date: "Fri, June 13 · 10PM",
    location: "Main Floor",
    img: "https://images.unsplash.com/photo-1571266028243-3716f02d2f1b?w=600&auto=format"
  },
  {
    title: "AMAPIANO TAKEOVER: DJ ZURI",
    date: "Sat, June 21 · 11PM",
    location: "Rooftop Lounge",
    img: "https://images.unsplash.com/photo-1571945153237-4929e783af4a?w=600&auto=format"
  },
  {
    title: "HIP HOP LEGENDARY · DJ MADD",
    date: "Fri, June 27 · 10:30PM",
    location: "Al Capone Arena",
    img: "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=600&auto=format"
  },
  {
    title: "LATIN & REGGAETON NIGHT",
    date: "Sat, July 5 · 11PM",
    location: "Garden City Terrace",
    img: "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=600&auto=format"
  }
];

// Build carousel
const track = document.getElementById('carouselTrack');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const dotsContainer = document.getElementById('carouselDots');

let currentIndex = 0;
let cards = [];

function buildCarousel() {
  if (!track) return;
  track.innerHTML = '';
  eventsData.forEach((event, idx) => {
    const card = document.createElement('div');
    card.classList.add('event-card');
    card.innerHTML = `
      <div class="event-img" style="background-image: url('${event.img}'); background-size: cover;"></div>
      <div class="event-info">
        <h4>${event.title}</h4>
        <p><i class="far fa-calendar-alt"></i> ${event.date}</p>
        <p><i class="fas fa-map-marker-alt"></i> ${event.location}</p>
      </div>
    `;
    track.appendChild(card);
  });
  cards = Array.from(document.querySelectorAll('.event-card'));
  updateCarousel();
  createDots();
}

function updateCarousel() {
  if (!track || cards.length === 0) return;
  const cardWidth = cards[0].offsetWidth + 32; // gap 2rem = 32px
  const shift = currentIndex * cardWidth;
  track.style.transform = `translateX(-${shift}px)`;
  updateDots();
}

function createDots() {
  if (!dotsContainer) return;
  dotsContainer.innerHTML = '';
  eventsData.forEach((_, idx) => {
    const dot = document.createElement('div');
    dot.classList.add('dot');
    if (idx === currentIndex) dot.classList.add('active');
    dot.addEventListener('click', () => {
      currentIndex = idx;
      updateCarousel();
    });
    dotsContainer.appendChild(dot);
  });
}

function updateDots() {
  const dots = document.querySelectorAll('.dot');
  dots.forEach((dot, idx) => {
    if (idx === currentIndex) dot.classList.add('active');
    else dot.classList.remove('active');
  });
}

function nextSlide() {
  if (cards.length === 0) return;
  const maxIndex = Math.max(0, cards.length - 1);
  if (currentIndex < maxIndex) {
    currentIndex++;
    updateCarousel();
  } else if (currentIndex === maxIndex && cards.length > 1) {
    // optional infinite but we just loop? but to keep elegance, let's loop smooth
    currentIndex = 0;
    updateCarousel();
  } else {
    currentIndex = 0;
    updateCarousel();
  }
}

function prevSlide() {
  if (cards.length === 0) return;
  if (currentIndex > 0) {
    currentIndex--;
    updateCarousel();
  } else {
    currentIndex = cards.length - 1;
    updateCarousel();
  }
}

if (prevBtn && nextBtn) {
  prevBtn.addEventListener('click', prevSlide);
  nextBtn.addEventListener('click', nextSlide);
  window.addEventListener('resize', () => {
    updateCarousel();
  });
}

// Booking Form handler
const form = document.getElementById('bookingForm');
if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const date = document.getElementById('date').value;
    const guests = document.getElementById('guests').value;

    if (!name || !email || !phone || !date) {
      alert('❌ Please fill all required fields to secure your notorious night.');
      return;
    }
    if (!email.includes('@')) {
      alert('❌ Enter a valid email address.');
      return;
    }
    // simulation success
    alert(`✅ ${name}, your reservation for ${guests} guests on ${date} is received! 🥂\nWe'll contact you soon at ${phone}. Notorious Nights await!`);
    form.reset();
  });
}

// Additional dynamic: make sure carousel loads after dom
document.addEventListener('DOMContentLoaded', () => {
  buildCarousel();
  // also add initial image lazy?
  // extra glow effect on hover
  const sideImg = document.querySelector('.side-image');
  if (sideImg) {
    // preload image style already set inline in CSS (unsplash)
  }
});