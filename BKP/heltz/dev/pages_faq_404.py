# -*- coding: utf-8 -*-
"""FAQ / 404 page bodies."""

FAQ_BODY = """
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="index.html">Home</a><span>/</span><a href="#">Help Center</a><span>/</span><span>FAQ</span></div>
    <h1>Frequently Asked Questions</h1>
    <p>Answers to the questions we hear most often from Heltz students.</p>
  </div>
</section>
<div class="hazard-strip"></div>

<section class="section">
  <div class="container">
    <div class="help-tabs">
      <a class="help-tab" href="prices.html">Prices</a>
      <a class="help-tab" href="payment-options.html">Payment Options</a>
      <a class="help-tab" href="register.html">Registration</a>
      <a class="help-tab active" href="faq.html">FAQ</a>
    </div>

    <div class="faq-search">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
      <input type="search" placeholder="Search questions…" data-faq-search aria-label="Search FAQs">
    </div>

    <div class="faq-list" data-faq></div>

    <div class="cta-banner" style="margin-top:3rem;" data-animate>
      <h2>Still Have A Question?</h2>
      <a class="btn btn-amber" href="#" data-field="whatsapp-href" target="_blank" rel="noopener">Ask Us On WhatsApp</a>
    </div>
  </div>
</section>
"""

NOT_FOUND_BODY = """
<section class="error-page">
  <div class="plate" style="margin-bottom:1.5rem;">Wrong Turn</div>
  <div class="code">404</div>
  <h2 style="margin-top:1rem;">This Road Doesn't Lead Anywhere</h2>
  <p class="lede" style="margin:1rem auto 2rem;">The page you're looking for has moved or doesn't exist. Let's get you back on route.</p>
  <div class="hero-cta-row" style="justify-content:center;">
    <a class="btn btn-amber" href="index.html">Back To Home</a>
    <a class="btn btn-outline" href="courses.html">View Courses</a>
  </div>
</section>
"""
