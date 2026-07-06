/* Dentallabor Ekkert — site interactions (vanilla, no deps) */
(function () {
  "use strict";
  var d = document;

  /* ---- current year ---- */
  d.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---- header shadow on scroll ---- */
  var header = d.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---- mobile nav ---- */
  var burger = d.querySelector(".burger");
  var mobileNav = d.querySelector(".nav-mobile");
  if (burger && mobileNav) {
    var toggleNav = function (open) {
      var willOpen = open != null ? open : !mobileNav.classList.contains("is-open");
      mobileNav.classList.toggle("is-open", willOpen);
      burger.setAttribute("aria-expanded", willOpen ? "true" : "false");
      d.body.style.overflow = willOpen ? "hidden" : "";
    };
    burger.addEventListener("click", function () { toggleNav(); });
    mobileNav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { toggleNav(false); });
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 720) toggleNav(false);
    });
  }

  /* ---- YouTube facade (privacy: nothing loads until click) ---- */
  d.querySelectorAll(".video[data-yt]").forEach(function (box) {
    box.addEventListener("click", function () {
      if (box.dataset.loaded) return;
      box.dataset.loaded = "1";
      var id = box.getAttribute("data-yt");
      var f = d.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + id +
        "?autoplay=1&rel=0&modestbranding=1";
      f.title = box.getAttribute("data-title") || "Video";
      f.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      f.setAttribute("allowfullscreen", "");
      box.innerHTML = "";
      box.appendChild(f);
    });
  });

  /* ---- Google Maps consent loader (DSGVO) ---- */
  d.querySelectorAll(".map[data-map]").forEach(function (box) {
    var consent = box.querySelector(".map__consent");
    if (!consent) return;
    consent.addEventListener("click", function () {
      var f = d.createElement("iframe");
      f.src = box.getAttribute("data-map");
      f.title = "Standort Dentallabor Ekkert auf Google Maps";
      f.loading = "lazy";
      f.referrerPolicy = "no-referrer-when-downgrade";
      box.appendChild(f);
      consent.remove();
    });
  });

  /* ---- Web3Forms contact submit ---- */
  d.querySelectorAll("form[data-web3form]").forEach(function (form) {
    var msg = form.querySelector(".form__msg");
    var btn = form.querySelector('[type="submit"]');
    var btnText = btn ? btn.innerHTML : "";
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (msg) { msg.className = "form__msg"; }
      var key = form.querySelector('[name="access_key"]');
      // Guard: not yet configured
      if (!key || /YOUR_|PLACEHOLDER/i.test(key.value)) {
        showMsg("Das Formular ist noch nicht final verknüpft. Bitte schreiben Sie uns direkt an zahntechnik-ekkert@web.de oder rufen Sie an.", true);
        return;
      }
      if (btn) { btn.disabled = true; btn.innerHTML = "Wird gesendet …"; }
      fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { "Accept": "application/json" },
        body: new FormData(form)
      }).then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.success) {
            form.reset();
            showMsg("Vielen Dank! Ihre Anfrage ist eingegangen – ich melde mich innerhalb von 24 Stunden bei Ihnen.", false);
          } else {
            showMsg("Es ist ein Fehler aufgetreten. Bitte versuchen Sie es erneut oder schreiben Sie an zahntechnik-ekkert@web.de.", true);
          }
        }).catch(function () {
          showMsg("Verbindung fehlgeschlagen. Bitte versuchen Sie es erneut oder schreiben Sie an zahntechnik-ekkert@web.de.", true);
        }).finally(function () {
          if (btn) { btn.disabled = false; btn.innerHTML = btnText; }
        });
    });
    function showMsg(text, isError) {
      if (!msg) { alert(text); return; }
      msg.textContent = text;
      msg.className = "form__msg " + (isError ? "is-err" : "is-ok");
      msg.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });

  /* ---- scroll reveal ---- */
  var reveals = d.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }
})();
