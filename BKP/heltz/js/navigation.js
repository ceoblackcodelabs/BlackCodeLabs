/**
 * navigation.js — header scroll state, dropdown a11y, mobile drawer
 */
(function () {
  "use strict";

  const header = document.querySelector(".site-header");
  const onScroll = () => {
    if (!header) return;
    header.classList.toggle("scrolled", window.scrollY > 12);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---------- Desktop dropdown (Help Center) ---------- */
  const dropdowns = document.querySelectorAll(".nav-item-dropdown");
  dropdowns.forEach((dd) => {
    const trigger = dd.querySelector(".nav-link");
    if (!trigger) return;
    trigger.setAttribute("aria-expanded", "false");
    trigger.addEventListener("click", (e) => {
      e.preventDefault();
      const isOpen = dd.classList.toggle("open");
      trigger.setAttribute("aria-expanded", String(isOpen));
      dropdowns.forEach((other) => {
        if (other !== dd) {
          other.classList.remove("open");
          other.querySelector(".nav-link")?.setAttribute("aria-expanded", "false");
        }
      });
    });
  });

  document.addEventListener("click", (e) => {
    dropdowns.forEach((dd) => {
      if (!dd.contains(e.target)) {
        dd.classList.remove("open");
        dd.querySelector(".nav-link")?.setAttribute("aria-expanded", "false");
      }
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      dropdowns.forEach((dd) => {
        dd.classList.remove("open");
        dd.querySelector(".nav-link")?.setAttribute("aria-expanded", "false");
      });
    }
  });

  /* ---------- Mobile drawer ---------- */
  const hamburger = document.querySelector(".hamburger");
  const drawer = document.querySelector(".mobile-drawer");
  const drawerClose = document.querySelector(".drawer-close");
  const drawerBackdrop = document.querySelector(".drawer-backdrop");

  function openDrawer() {
    if (!drawer) return;
    drawer.classList.add("open");
    hamburger?.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
  }

  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove("open");
    hamburger?.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  }

  hamburger?.addEventListener("click", () => {
    const isOpen = drawer?.classList.contains("open");
    isOpen ? closeDrawer() : openDrawer();
  });
  drawerClose?.addEventListener("click", closeDrawer);
  drawerBackdrop?.addEventListener("click", closeDrawer);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeDrawer();
  });

  /* Close drawer when a plain link inside it is followed */
  drawer?.querySelectorAll("a[href]").forEach((a) => {
    a.addEventListener("click", closeDrawer);
  });

  /* ---------- Mobile Help Center accordion ---------- */
  document.querySelectorAll(".drawer-accordion").forEach((btn) => {
    const submenu = document.getElementById(btn.getAttribute("aria-controls"));
    btn.addEventListener("click", () => {
      const isOpen = btn.classList.toggle("open");
      btn.setAttribute("aria-expanded", String(isOpen));
      if (submenu) {
        submenu.style.maxHeight = isOpen ? submenu.scrollHeight + "px" : "0";
      }
    });
  });

  /* ---------- Mark current page as active in nav ---------- */
  const path = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".main-nav a.nav-link, .drawer-nav a").forEach((a) => {
    const href = a.getAttribute("href");
    if (href === path || (path === "index.html" && href === "./") || (path === "" && href === "index.html")) {
      a.classList.add("active");
    }
  });
})();
