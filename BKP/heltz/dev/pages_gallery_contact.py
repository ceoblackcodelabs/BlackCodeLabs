# -*- coding: utf-8 -*-
"""Gallery / Contact page bodies."""

GALLERY_BODY = """
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="index.html">Home</a><span>/</span><span>Gallery</span></div>
    <h1>Gallery</h1>
    <p>A look at life at Heltz Driving Academy — lessons, vehicles and branches from across Nairobi.</p>
  </div>
</section>
<div class="hazard-strip"></div>

<section class="section">
  <div class="container">
    <div class="gallery-filter" data-gallery-filter></div>
    <div class="gallery-grid" data-gallery="full"></div>
    <div class="gallery-load-more">
      <button class="btn btn-outline" data-gallery-more>Load More</button>
    </div>
  </div>
</section>
"""

CONTACT_BODY = """
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="index.html">Home</a><span>/</span><span>Contact</span></div>
    <h1>Contact</h1>
    <p>Smart Drivers Start Here. Let's Get You On The Road!</p>
  </div>
</section>
<div class="hazard-strip"></div>

<section class="section">
  <div class="container">
    <div class="map-embed">
      <iframe data-field="mapembed" loading="lazy" title="Heltz Driving Academy map"></iframe>
    </div>
    <div class="contact-grid">
      <div data-animate>
        <p class="eyebrow">Our Contact</p>
        <h2>Get In Touch</h2>
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
            <div class="contact-info-icon"><svg class="icon-16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 14.4c-.3-.1-1.7-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.5-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6"/></svg></div>
            <div><h4>WhatsApp</h4><a href="#" data-field="whatsapp-href" target="_blank" rel="noopener"><span data-field="whatsapp">+254 733 340082</span></a></div>
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
        <p class="eyebrow">Send Us A Message</p>
        <div class="form-row">
          <div class="form-group">
            <label for="ct-name">Full Name</label>
            <input id="ct-name" name="name" type="text" required>
            <span class="form-error">Please enter your name.</span>
          </div>
          <div class="form-group">
            <label for="ct-phone">Phone Number</label>
            <input id="ct-phone" name="phone" type="tel" required>
            <span class="form-error">Please enter a valid phone number.</span>
          </div>
        </div>
        <div class="form-group">
          <label for="ct-email">Email Address</label>
          <input id="ct-email" name="email" type="email">
        </div>
        <div class="form-group">
          <label for="ct-branch">Select Branch</label>
          <select id="ct-branch" name="branch"></select>
        </div>
        <div class="form-group">
          <label for="ct-message">Message</label>
          <textarea id="ct-message" name="message" required></textarea>
          <span class="form-error">Tell us what you'd like help with.</span>
        </div>
        <button type="submit" class="btn btn-amber btn-block">Send Message</button>
        <p class="form-status"></p>
        <p class="form-note">We'll open WhatsApp with your message pre-filled so you can send it straight to our team.</p>
      </form>
    </div>
  </div>
</section>

<script>
  document.addEventListener('DOMContentLoaded', function () {
    var sel = document.getElementById('ct-branch');
    if (!sel || !window.HELTZ_DATA) return;
    sel.innerHTML = '<option value="">Select a branch</option>' +
      window.HELTZ_DATA.branches.map(function (b) { return '<option>' + b.name + '</option>'; }).join('');
  });
</script>
"""
