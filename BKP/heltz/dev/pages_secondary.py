# -*- coding: utf-8 -*-
"""Courses / Branches / About page bodies."""

COURSES_BODY = """
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="index.html">Home</a><span>/</span><span>Courses</span></div>
    <h1>Courses</h1>
    <p>Heltz Driving School offers driving lessons according to the NTSA new driving curriculum — Class A (Motorbikes), Class B (Cars), Class C (Trucks) and Class D (Vans).</p>
  </div>
</section>
<div class="hazard-strip"></div>

<section class="section">
  <div class="container">
    <div class="filter-row" data-course-filter></div>
    <div class="courses-grid" data-courses-full></div>
  </div>
</section>

<section class="section" style="background:var(--c-paper-alt);">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Theoretical Lessons</p>
      <h2>What Every Student Learns</h2>
      <p class="lede">While driving on the road, there are laws and principles that govern road users. Our instructors pass this knowledge down to every joining student, to make them responsible, competent and confident drivers.</p>
    </div>
    <div class="feature-grid" style="grid-template-columns:repeat(2,1fr);">
      <div class="card feature-card">
        <h3>Theory Covers</h3>
        <ul style="margin-top:1rem;padding-left:1.2rem;list-style:disc;color:var(--c-steel);display:grid;gap:.6rem;">
          <li>Maneuvering easily on a modern town board</li>
          <li>Understanding rules and regulations of Kenyan roads</li>
          <li>How traffic is controlled on the roads</li>
          <li>Categories of road users</li>
        </ul>
      </div>
      <div class="card feature-card">
        <h3>Other Benefits</h3>
        <ul style="margin-top:1rem;padding-left:1.2rem;list-style:disc;color:var(--c-steel);display:grid;gap:.6rem;">
          <li>Basic Mechanics</li>
          <li>First Aid</li>
          <li>Assessment Test</li>
          <li>Car Hire</li>
          <li>Driving Test</li>
          <li>Certificate of Competency</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="cta-banner">
      <div>
        <p class="eyebrow" style="color:rgba(246,244,238,.75);">On Request, Extra Fee</p>
        <h2>Extra Prestige Services</h2>
        <p style="color:rgba(246,244,238,.85);margin-top:.8rem;max-width:48ch;">Special request for a lady instructor, door-to-door pick and drop, and unlimited theory lessons — available on request.</p>
      </div>
      <a class="btn btn-amber" href="register.html">Enroll Now</a>
    </div>
  </div>
</section>
"""

BRANCHES_BODY = """
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="index.html">Home</a><span>/</span><span>Branches</span></div>
    <h1>Branches</h1>
    <p>Heltz Driving School is located across Nairobi, with 13 branches widely distributed throughout the city — find the one closest to you.</p>
  </div>
</section>
<div class="hazard-strip"></div>

<section class="section">
  <div class="container">
    <div class="map-embed">
      <iframe data-field="mapembed" loading="lazy" title="Heltz Driving Academy branches map"></iframe>
    </div>
    <div class="branches-grid" data-branches-full></div>
  </div>
</section>

<section class="section" style="background:var(--c-paper-alt);padding-top:0;">
  <div class="container">
    <div class="cta-banner" data-animate>
      <h2>Not Sure Which Branch Is Closest?</h2>
      <div class="hero-cta-row">
        <a class="btn btn-amber" href="#" data-field="whatsapp-href" target="_blank" rel="noopener">Ask On WhatsApp</a>
        <a class="btn btn-outline" style="color:#fff;" href="register.html">Register Now</a>
      </div>
    </div>
  </div>
</section>
"""

ABOUT_BODY = """
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="index.html">Home</a><span>/</span><span>About Heltz</span></div>
    <h1>About Us</h1>
    <p>Smart Drivers Start Here. Let's Get You On The Road.</p>
  </div>
</section>
<div class="hazard-strip"></div>

<section class="section">
  <div class="container">
    <div class="about-grid">
      <div class="about-copy" data-animate>
        <p class="eyebrow">Who We Are</p>
        <h2>35+ Years Of Responsible Driving Instruction</h2>
        <p class="lede">For over 35 years, Heltz Driving Academy has earned a reputation for responsible and competent driving instruction throughout Nairobi.</p>
        <p>Our professional and friendly local driving instructors ensure all our students experience a relaxed, positive and encouraging environment as they start to learn to drive — and for those who join our refresher courses to improve their driving skills.</p>
        <div class="about-quick-stats">
          <div class="quick-stat"><b>35+</b><span>Years Experience</span></div>
          <div class="quick-stat"><b>13</b><span>Nairobi Branches</span></div>
          <div class="quick-stat"><b>4</b><span>Licence Classes</span></div>
        </div>
      </div>
      <div class="about-media" data-animate>
        <img src="https://heltzdrivingschool.com/wp-content/uploads/2024/02/WhatsApp-Image-2024-02-16-at-09.23.52.jpeg" alt="Heltz Driving Academy student on Class A motorbike" loading="lazy">
        <div class="about-badge"><b>NTSA</b><span>Approved Curriculum</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--c-paper-alt);">
  <div class="container">
    <div class="section-head center">
      <p class="eyebrow" style="justify-content:center;">Why Heltz</p>
      <h2>Why Students Choose Heltz</h2>
    </div>
    <div class="feature-grid" data-why></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="feature-grid" style="grid-template-columns:repeat(2,1fr);">
      <div class="card feature-card" data-animate>
        <h3>Become An Instructor</h3>
        <p style="color:var(--c-steel);margin-top:.8rem;">Get a buzz from teaching? Kick-start a rewarding career with tailor-made training options to suit your needs.</p>
        <a class="btn btn-outline" href="contact.html" style="margin-top:1.4rem;">Click Here</a>
      </div>
      <div class="card feature-card" data-animate>
        <h3>Improve Your Driving</h3>
        <p style="color:var(--c-steel);margin-top:.8rem;">Whether recently passed or more experienced, we'll help you become a more confident, safety-savvy driver.</p>
        <a class="btn btn-outline" href="courses.html" style="margin-top:1.4rem;">Train With Us</a>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--c-paper-alt);">
  <div class="container">
    <div class="section-head center">
      <p class="eyebrow" style="justify-content:center;">Getting Started</p>
      <h2>How It Works</h2>
    </div>
    <div class="steps-row" data-journey></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="cta-banner" data-animate>
      <h2>Smart Drivers Start Here! Let's Get You On The Road.</h2>
      <a class="btn btn-amber" href="register.html">Enroll Now</a>
    </div>
  </div>
</section>
"""
