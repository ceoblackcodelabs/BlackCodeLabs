# -*- coding: utf-8 -*-
"""Homepage body content."""

INDEX_BODY = """
<!-- HERO -->
<section class="hero" data-hero aria-label="Featured highlights">
  <div class="hero-track"></div>
  <div class="hero-controls">
    <div class="hero-dots"></div>
    <div class="hero-arrows">
      <button class="hero-arrow prev" aria-label="Previous slide">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
      </button>
      <button class="hero-arrow next" aria-label="Next slide">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      </button>
    </div>
  </div>
</section>

<!-- STATS -->
<section class="stats-strip">
  <div class="container">
    <div class="stats-grid" data-stats></div>
  </div>
</section>

<div class="hazard-strip thin"></div>

<!-- ABOUT -->
<section class="section" id="about">
  <div class="container">
    <div class="about-grid">
      <div class="about-copy" data-animate>
        <p class="eyebrow">About Heltz</p>
        <h2>Enhancing Driving Competence &amp; Confidence</h2>
        <p class="lede">For over 35 years, Heltz Driving Academy has earned a reputation for responsible and competent driving instruction throughout Nairobi.</p>
        <p>Our professional and friendly local driving instructors ensure every student experiences a relaxed, positive and encouraging environment — whether they're learning to drive for the first time or sharpening their skills in one of our refresher courses.</p>
        <div class="about-quick-stats">
          <div class="quick-stat"><b>35+</b><span>Years Experience</span></div>
          <div class="quick-stat"><b>13</b><span>Nairobi Branches</span></div>
          <div class="quick-stat"><b>4</b><span>Licence Classes</span></div>
        </div>
        <div class="about-cta">
          <a class="btn btn-amber" href="register.html">Enroll Today</a>
          <a class="btn btn-outline" href="about.html">More About Us</a>
        </div>
      </div>
      <div class="about-media" data-animate>
        <img src="https://heltzdrivingschool.com/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-21-at-12.31.47.jpeg" alt="Heltz Driving Academy instructor with student" loading="lazy">
        <div class="about-badge">
          <b>35+</b>
          <span>Years Teaching Nairobi To Drive</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- WHY HELTZ -->
<section class="section" style="background:var(--c-paper-alt);">
  <div class="container">
    <div class="section-head center">
      <p class="eyebrow" style="justify-content:center;">Why Choose Us</p>
      <h2>Why Heltz Driving School</h2>
    </div>
    <div class="feature-grid" data-why></div>
  </div>
</section>

<!-- SERVICES -->
<section class="section">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">What We Offer</p>
      <h2>Our Services</h2>
      <p class="lede">Practical and theoretical instruction across every licence class, plus refresher and professional-driver programmes.</p>
    </div>
    <div class="services-grid" data-services></div>
  </div>
</section>

<!-- COURSES PREVIEW -->
<section class="section" style="background:var(--c-paper-alt);">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">NTSA Curriculum</p>
      <h2>Practical Driving Courses</h2>
      <p class="lede">Heltz offers driving lessons according to the NTSA new driving curriculum, across four licence classes.</p>
    </div>
    <div class="courses-grid" data-courses-preview></div>
    <div class="section-foot">
      <a class="btn btn-outline" href="courses.html">View All Courses</a>
    </div>
  </div>
</section>

<!-- FLEET -->
<section class="section">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Our Fleet</p>
      <h2>Learn On Well-Kept Vehicles</h2>
      <p class="lede">Training vehicles across every class we teach — from motorbikes to PSV vans.</p>
    </div>
  </div>
  <div class="fleet-viewport" data-fleet>
    <div class="fleet-track"></div>
  </div>
</section>

<!-- TESTIMONIALS (hides itself when there is no data) -->
<section class="section" data-testimonials-section style="background:var(--c-ink);color:var(--c-paper);">
  <div class="container">
    <div class="section-head center">
      <p class="eyebrow" style="justify-content:center;">Student Voices</p>
      <h2 style="color:#fff;">What Our Students Say</h2>
    </div>
    <div class="testimonial-track-wrap">
      <div class="testimonial-track" data-testimonials></div>
    </div>
  </div>
</section>

<!-- GALLERY PREVIEW -->
<section class="section">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Life At Heltz</p>
      <h2>Gallery</h2>
    </div>
    <div class="gallery-grid" data-gallery="preview"></div>
    <div class="section-foot">
      <a class="btn btn-outline" href="gallery.html">View Full Gallery</a>
    </div>
  </div>
</section>

<!-- BRANCHES PREVIEW -->
<section class="section" style="background:var(--c-paper-alt);">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">13 Locations</p>
      <h2>Find A Branch Near You</h2>
      <p class="lede">Heltz Driving School is located across Nairobi, with branches widely distributed throughout the city.</p>
    </div>
    <div class="branches-grid" data-branches-preview></div>
    <div class="section-foot">
      <a class="btn btn-outline" href="branches.html">View All Branches</a>
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section class="section">
  <div class="container">
    <div class="section-head center">
      <p class="eyebrow" style="justify-content:center;">Getting Started</p>
      <h2>How It Works</h2>
    </div>
    <div class="steps-row" data-journey></div>
  </div>
</section>

<!-- CTA BANNER -->
<section class="section" style="padding-top:0;">
  <div class="container">
    <div class="cta-banner" data-animate>
      <h2>Smart Drivers Start Here. Let's Get You On The Road.</h2>
      <div class="hero-cta-row">
        <a class="btn btn-amber" href="register.html">Enroll Now</a>
        <a class="btn btn-outline" style="color:#fff;" href="#" data-field="whatsapp-href" target="_blank" rel="noopener">Chat On WhatsApp</a>
      </div>
    </div>
  </div>
</section>

<!-- CONTACT -->
<section class="section" id="contact" style="background:var(--c-paper-alt);">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Get In Touch</p>
      <h2>Contact Heltz</h2>
      <p class="lede">Questions about a course, a branch, or how to register? Reach us any of these ways.</p>
    </div>
    <div class="contact-grid">
      <div data-animate>
        <div class="contact-info-list">
          <div class="contact-info-item">
            <div class="contact-info-icon"><svg class="icon-16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg></div>
            <div><h4>Address</h4><p data-field="address">1st Floor, City Square Sheikh House, Tom Mboya Street, Nairobi, Kenya</p></div>
          </div>
          <div class="contact-info-item">
            <div class="contact-info-icon"><svg class="icon-16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg></div>
            <div><h4>Call Us</h4><a href="#" data-field="phone-href"><span data-field="phone">+254 743 552541</span></a></div>
          </div>
          <div class="contact-info-item">
            <div class="contact-info-icon"><svg class="icon-16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 6c0-1.1-.9-2-2-2H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6Z"/><path d="m2 7 10 6 10-6"/></svg></div>
            <div><h4>Email</h4><a href="#" data-field="email-href"><span data-field="email">heltzdrivingschool@gmail.com</span></a></div>
          </div>
          <div class="contact-info-item">
            <div class="contact-info-icon"><svg class="icon-16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg></div>
            <div><h4>Hours</h4><p>Weekdays: <span data-field="hours-weekday">7:00 AM – 7:00 PM</span><br>Saturday: <span data-field="hours-saturday">7:00 AM – 3:00 PM</span></p></div>
          </div>
        </div>
        <div class="contact-social">
          <a href="#" data-field="facebook" target="_blank" rel="noopener" aria-label="Facebook"><svg class="icon-16" viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.4h-1.2c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12Z"/></svg></a>
          <a href="#" data-field="twitter" target="_blank" rel="noopener" aria-label="Twitter"><svg class="icon-16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.9 3H21l-6.5 7.4L22.2 21h-6.9l-5.4-6.7L3.6 21H1.4l7-8-7.7-10h7l4.9 6.2L18.9 3Zm-1.2 16h1.9L7.4 5H5.4l12.3 14Z"/></svg></a>
          <a href="#" data-field="instagram" target="_blank" rel="noopener" aria-label="Instagram"><svg class="icon-16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/></svg></a>
          <a href="#" data-field="tiktok" target="_blank" rel="noopener" aria-label="TikTok"><svg class="icon-16" viewBox="0 0 24 24" fill="currentColor"><path d="M16.7 2h-3.3v14.2a2.6 2.6 0 1 1-2.6-2.6c.2 0 .5 0 .7.1V10.4a6 6 0 1 0 5.2 6V8.6c1.2.9 2.6 1.4 4.1 1.4V6.7A5 5 0 0 1 16.7 2Z"/></svg></a>
        </div>
      </div>
      <form class="card form-card" data-form="contact" data-animate novalidate>
        <div class="form-row">
          <div class="form-group">
            <label for="c-name">Full Name</label>
            <input id="c-name" name="name" type="text" required>
            <span class="form-error">Please enter your name.</span>
          </div>
          <div class="form-group">
            <label for="c-phone">Phone Number</label>
            <input id="c-phone" name="phone" type="tel" required>
            <span class="form-error">Please enter a valid phone number.</span>
          </div>
        </div>
        <div class="form-group">
          <label for="c-email">Email Address</label>
          <input id="c-email" name="email" type="email">
        </div>
        <div class="form-group">
          <label for="c-branch">Nearest Branch</label>
          <select id="c-branch" name="branch"></select>
        </div>
        <div class="form-group">
          <label for="c-message">Message</label>
          <textarea id="c-message" name="message" required></textarea>
          <span class="form-error">Tell us what you'd like help with.</span>
        </div>
        <button type="submit" class="btn btn-amber btn-block">Send Message</button>
        <p class="form-status"></p>
        <p class="form-note">We'll open WhatsApp with your message pre-filled so you can send it straight to our team.</p>
      </form>
    </div>
    <div class="map-embed" style="margin-top:3rem;">
      <iframe data-field="mapembed" loading="lazy" title="Heltz Driving Academy map"></iframe>
    </div>
  </div>
</section>

<script>
  // Populate the branch <select> on the contact form from shared data
  document.addEventListener('DOMContentLoaded', function () {
    var sel = document.getElementById('c-branch');
    if (!sel || !window.HELTZ_DATA) return;
    sel.innerHTML = '<option value="">Select a branch</option>' +
      window.HELTZ_DATA.branches.map(function (b) { return '<option>' + b.name + '</option>'; }).join('');
  });
</script>
"""
