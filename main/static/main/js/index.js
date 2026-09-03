/* ==========================================================================
   EVERGREEN HANDS — SCRIPT.JS
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {

  /* ------------------------------------------------------------------ */
  /* MOBILE NAVIGATION                                                   */
  /* ------------------------------------------------------------------ */
  var navToggle = document.getElementById('nav-toggle');
  var primaryNav = document.getElementById('primary-navigation');

  if (navToggle && primaryNav) {
    navToggle.addEventListener('click', function () {
      var isOpen = primaryNav.classList.toggle('is-open');
      navToggle.classList.toggle('is-active');
      navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    primaryNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        primaryNav.classList.remove('is-open');
        navToggle.classList.remove('is-active');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* DONATION AMOUNT SELECTOR                                            */
  /* One-time donation only. Exactly one preset amount (or "Other") is   */
  /* selected at a time. Selected value is written to the hidden input   */
  /* #donation-amount so it can be read by a Django form/view later.     */
  /* ------------------------------------------------------------------ */
  var amountGroup = document.getElementById('donation-amount-group');
  var amountHiddenInput = document.getElementById('donation-amount');
  var customAmountWrap = document.getElementById('donation-custom-amount-wrap');
  var customAmountInput = document.getElementById('donation-amount-custom');

  if (amountGroup && amountHiddenInput) {
    var amountButtons = amountGroup.querySelectorAll('.donation-amount-btn');

    amountButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        // Clear selected state from every button first, so only one is
        // ever marked selected at a time.
        amountButtons.forEach(function (btn) {
          btn.classList.remove('donation-amount-btn--selected');
          btn.removeAttribute('aria-pressed');
        });

        button.classList.add('donation-amount-btn--selected');
        button.setAttribute('aria-pressed', 'true');

        var selectedAmount = button.getAttribute('data-amount');

        if (selectedAmount === 'other') {
          customAmountWrap.hidden = false;
          customAmountInput.focus();
          amountHiddenInput.value = customAmountInput.value || '';
        } else {
          customAmountWrap.hidden = true;
          amountHiddenInput.value = selectedAmount;
        }
      });
    });

    if (customAmountInput) {
      customAmountInput.addEventListener('input', function () {
        amountHiddenInput.value = customAmountInput.value;
      });
    }
  }

  /* ------------------------------------------------------------------ */
  /* FORM SUBMISSION GUARDS                                              */
  /* These forms aren't wired to a backend yet — prevented from          */
  /* reloading the page until Django views are connected.                */
  /* ------------------------------------------------------------------ */
  ['donation-form', 'contact-form', 'newsletter-form'].forEach(function (formId) {
    var form = document.getElementById(formId);
    if (form) {
      form.addEventListener('submit', function (event) {
        event.preventDefault();
        // TODO: connect to Django view / endpoint.
      });
    }
  });

  /* ------------------------------------------------------------------ */
  /* SCROLL ANIMATIONS                                                    */
  /* Subtle fade/slide reveals using Intersection Observer. Each element  */
  /* animates once, then stops being observed (no repeat on re-scroll).  */
  /* Respects prefers-reduced-motion via the CSS media query as well.    */
  /* ------------------------------------------------------------------ */
  var animatedEls = document.querySelectorAll('[data-animate]');

  if (animatedEls.length && 'IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var el = entry.target;
          var delay = el.getAttribute('data-animate-delay');

          if (delay) {
            el.style.transitionDelay = delay + 'ms';
          }

          el.classList.add('is-visible');
          obs.unobserve(el);
        }
      });
    }, {
      threshold: 0.15,
      rootMargin: '0px 0px -40px 0px'
    });

    animatedEls.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    // Fallback for browsers without IntersectionObserver support:
    // just show everything immediately.
    animatedEls.forEach(function (el) {
      el.classList.add('is-visible');
    });
  }

});