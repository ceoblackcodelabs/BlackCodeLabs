/**
 * forms.js — lightweight client-side validation for the Registration
 * and Contact forms. There is no backend yet, so on success we build
 * a pre-filled WhatsApp message to the school's number and open it —
 * this keeps the forms fully functional on static GitHub Pages.
 * Swap `handleSubmit` for a real fetch() POST once an API exists.
 */
(function () {
  "use strict";

  function validateField(field) {
    const group = field.closest(".form-group");
    if (!group) return true;
    let valid = field.checkValidity();

    // basic Kenyan-style phone sanity check (digits, +, spaces only, 9+ digits)
    if (valid && field.type === "tel" && field.value.trim()) {
      const digits = field.value.replace(/[^\d]/g, "");
      valid = digits.length >= 9;
    }

    group.classList.toggle("invalid", !valid);
    return valid;
  }

  function validateForm(form) {
    let allValid = true;
    form.querySelectorAll("input[required], select[required], textarea[required]").forEach((field) => {
      if (!validateField(field)) allValid = false;
    });
    return allValid;
  }

  function buildWhatsAppMessage(form, kind) {
    const data = new FormData(form);
    const get = (name) => (data.get(name) || "").toString().trim();

    let lines = [];
    if (kind === "register") {
      lines = [
        `Hi Heltz, I'd like to register for a course.`,
        `Name: ${get("firstName")} ${get("lastName")}`,
        `Phone: ${get("phone")}`,
        `Email: ${get("email") || "-"}`,
        `Class: ${get("courseClass")}`,
        `Preferred Start Date: ${get("startDate") || "-"}`,
        `Branch: ${get("branch")}`,
      ];
    } else {
      lines = [
        `Hi Heltz, I have a question.`,
        `Name: ${get("name")}`,
        `Email: ${get("email") || "-"}`,
        `Phone: ${get("phone") || "-"}`,
        `Branch: ${get("branch") || "-"}`,
        `Message: ${get("message")}`,
      ];
    }
    return encodeURIComponent(lines.join("\n"));
  }

  function initForm(form) {
    const kind = form.dataset.form;
    const status = form.querySelector(".form-status");

    form.querySelectorAll("input, select, textarea").forEach((field) => {
      field.addEventListener("blur", () => validateField(field));
    });

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!validateForm(form)) {
        const firstInvalid = form.querySelector(".form-group.invalid input, .form-group.invalid select, .form-group.invalid textarea");
        firstInvalid?.focus();
        return;
      }

      const msg = buildWhatsAppMessage(form, kind);
      const waHref = `${window.HELTZ_DATA.business.whatsappHref}?text=${msg}`;

      if (status) {
        status.textContent = "Thanks! Opening WhatsApp so you can send this straight to our team…";
        status.classList.add("show");
      }

      window.open(waHref, "_blank", "noopener");
      form.reset();
      setTimeout(() => {
        form.querySelectorAll(".form-group.invalid").forEach((g) => g.classList.remove("invalid"));
      }, 300);
    });
  }

  document.querySelectorAll("form[data-form]").forEach(initForm);
})();
