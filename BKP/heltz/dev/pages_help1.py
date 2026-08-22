# -*- coding: utf-8 -*-
"""Help Center: Prices / Payment Options / Registration page bodies."""

PRICES_BODY = """
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="index.html">Home</a><span>/</span><a href="#">Help Center</a><span>/</span><span>Prices</span></div>
    <h1>Prices</h1>
    <p>Heltz Driving School offers driving lessons according to the NTSA new driving curriculum. Rates below do not include amounts payable directly to NTSA.</p>
  </div>
</section>
<div class="hazard-strip"></div>

<section class="section">
  <div class="container">
    <div class="help-tabs">
      <a class="help-tab active" href="prices.html">Prices</a>
      <a class="help-tab" href="payment-options.html">Payment Options</a>
      <a class="help-tab" href="register.html">Registration</a>
      <a class="help-tab" href="faq.html">FAQ</a>
    </div>
    <div class="price-tables-grid" data-price-tables></div>
    <div class="section-foot">
      <a class="btn btn-amber" href="register.html">Enroll Now</a>
    </div>
  </div>
</section>
"""

PAYMENT_OPTIONS_BODY = """
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="index.html">Home</a><span>/</span><a href="#">Help Center</a><span>/</span><span>Payment Options</span></div>
    <h1>Payment Options</h1>
    <p>Heltz does not accept cash payments. Choose M-Pesa or bank deposit below.</p>
  </div>
</section>
<div class="hazard-strip"></div>

<section class="section">
  <div class="container">
    <div class="help-tabs">
      <a class="help-tab" href="prices.html">Prices</a>
      <a class="help-tab active" href="payment-options.html">Payment Options</a>
      <a class="help-tab" href="register.html">Registration</a>
      <a class="help-tab" href="faq.html">FAQ</a>
    </div>

    <div class="feature-grid" style="grid-template-columns:repeat(2,1fr);align-items:start;">
      <div class="card payment-method-card" data-animate>
        <div class="payment-method-head">
          <div class="service-icon" style="background:#25D366;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="#fff"><path d="M17.5 14.4c-.3-.1-1.7-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.5-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6.1-.1.3-.3.4-.5.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5C10.1 9 9.5 7.6 9.2 7c-.1-.5-.3-.4-.5-.4h-.5c-.2 0-.5.1-.7.3-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 5 4.3.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.5-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3ZM12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2Z"/></svg>
          </div>
          <h3 style="margin:0;">Pay Via M-Pesa</h3>
        </div>
        <div class="step-list">
          <div class="step-item"><div class="step-num"></div><p>Go to <b>M-PESA</b> on your phone</p></div>
          <div class="step-item"><div class="step-num"></div><p>Select <b>Lipa na M-PESA</b></p></div>
          <div class="step-item"><div class="step-num"></div><p>Choose the <b>Buy Goods</b> option</p></div>
          <div class="step-item"><div class="step-num"></div><p>Enter Till Number <b>656 867</b>, then click <b>OK</b></p></div>
          <div class="step-item"><div class="step-num"></div><p>Enter your M-PESA PIN, then click <b>OK</b></p></div>
          <div class="step-item"><div class="step-num"></div><p>You'll receive a confirmation SMS from M-Pesa</p></div>
        </div>
      </div>

      <div class="card payment-method-card" data-animate>
        <div class="payment-method-head">
          <div class="service-icon" style="background:var(--c-forest);">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M4 21V10M20 21V10M2 10l10-6 10 6M6 10v11M10 10v11M14 10v11M18 10v11"/></svg>
          </div>
          <h3 style="margin:0;">Pay Via Bank</h3>
        </div>
        <div class="bank-detail-list">
          <div><span>Bank</span><span>Equity Bank Limited</span></div>
          <div><span>Account Name</span><span>Heltz Institute of Advanced Driving</span></div>
          <div><span>Branch</span><span>Tom Mboya</span></div>
          <div><span>Account No.</span><span>0120 2786 60225</span></div>
        </div>
        <p class="form-note">Drop the payment receipt at the school's accounts office at any branch to confirm your payment.</p>
      </div>
    </div>

    <div class="section-foot">
      <a class="btn btn-amber" href="register.html">Enroll Now</a>
    </div>
  </div>
</section>
"""

REGISTER_BODY = """
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="index.html">Home</a><span>/</span><a href="#">Help Center</a><span>/</span><span>Registration</span></div>
    <h1>Registration</h1>
    <p>Enquire about our classes — fill in the form below and we'll get back to you.</p>
  </div>
</section>
<div class="hazard-strip"></div>

<section class="section">
  <div class="container">
    <div class="help-tabs">
      <a class="help-tab" href="prices.html">Prices</a>
      <a class="help-tab" href="payment-options.html">Payment Options</a>
      <a class="help-tab active" href="register.html">Registration</a>
      <a class="help-tab" href="faq.html">FAQ</a>
    </div>

    <div class="contact-grid">
      <div data-animate>
        <p class="eyebrow">Before You Register</p>
        <h2>What You'll Need</h2>
        <p class="lede" style="margin-top:1rem;">Driving requirements at Heltz are simple:</p>
        <ul style="margin-top:1rem;padding-left:1.2rem;list-style:disc;color:var(--c-steel);display:grid;gap:.7rem;">
          <li>You must be 18 years of age or above</li>
          <li>A valid national identity card (ID)</li>
          <li>Only one licence class can be studied at a time, per NTSA rules</li>
        </ul>
        <p class="form-note" style="margin-top:1.5rem;">Payment is by M-Pesa or bank deposit only — no cash is accepted. See <a href="payment-options.html" style="text-decoration:underline;">Payment Options</a> for details.</p>
      </div>

      <form class="card form-card" data-form="register" data-animate novalidate>
        <p class="eyebrow">Enquire About Our Classes</p>
        <div class="form-row">
          <div class="form-group">
            <label for="r-first">First Name</label>
            <input id="r-first" name="firstName" type="text" required>
            <span class="form-error">Please enter your first name.</span>
          </div>
          <div class="form-group">
            <label for="r-last">Last Name</label>
            <input id="r-last" name="lastName" type="text" required>
            <span class="form-error">Please enter your last name.</span>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="r-phone">Phone Number</label>
            <input id="r-phone" name="phone" type="tel" required>
            <span class="form-error">Please enter a valid phone number.</span>
          </div>
          <div class="form-group">
            <label for="r-email">Email</label>
            <input id="r-email" name="email" type="email">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="r-class">Select Class</label>
            <select id="r-class" name="courseClass" required>
              <option value="">-Select Class-</option>
              <option>Class A – Motorbikes</option>
              <option>Class B – Cars</option>
              <option>Class C – Trucks</option>
              <option>Class D – Vans</option>
              <option>VIP Course – Class B All Inclusive</option>
            </select>
            <span class="form-error">Please choose a class.</span>
          </div>
          <div class="form-group">
            <label for="r-date">Preferred Start Date</label>
            <input id="r-date" name="startDate" type="date">
          </div>
        </div>
        <div class="form-group">
          <label for="r-branch">Select Branch</label>
          <select id="r-branch" name="branch" required></select>
          <span class="form-error">Please choose a branch.</span>
        </div>
        <button type="submit" class="btn btn-amber btn-block">Submit</button>
        <p class="form-status"></p>
        <p class="form-note">We'll open WhatsApp with your details pre-filled so you can send your enquiry straight to our team.</p>
      </form>
    </div>
  </div>
</section>

<script>
  document.addEventListener('DOMContentLoaded', function () {
    var sel = document.getElementById('r-branch');
    if (!sel || !window.HELTZ_DATA) return;
    sel.innerHTML = '<option value="">-Select Branch-</option>' +
      window.HELTZ_DATA.branches.map(function (b) {
        return '<option>' + b.name + (b.isHQ ? ' (Head Office)' : '') + ' — ' + b.location + '</option>';
      }).join('');
  });
</script>
"""
