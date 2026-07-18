/* Dentallabor Ekkert — site interactions (vanilla, no deps) */
(function () {
  "use strict";
  var d = document;

  /* ---- current year ---- */
  d.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---- cookie notice (nur technisch notwendige Speicherung → einfacher Hinweis) ---- */
  var cookie = d.getElementById("cookie");
  if (cookie) {
    var acked = false;
    try { acked = !!localStorage.getItem("gpCookieOk"); } catch (e) {}
    if (!acked) cookie.classList.add("is-shown");
    var okBtn = cookie.querySelector("[data-cookie-ok]");
    if (okBtn) okBtn.addEventListener("click", function () {
      try { localStorage.setItem("gpCookieOk", "1"); } catch (e) {}
      cookie.classList.remove("is-shown");
    });
  }

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

  /* ---- Kontaktformular → GrowPotential-Endpoint (JSON) ---- */
  d.querySelectorAll("form[data-lead]").forEach(function (form) {
    var msg = form.querySelector(".form__msg");
    var btn = form.querySelector('[type="submit"]');
    var btnText = btn ? btn.innerHTML : "";
    function showMsg(text, isError) {
      if (!msg) { alert(text); return; }
      msg.textContent = text;
      msg.className = "form__msg " + (isError ? "is-err" : "is-ok");
      msg.scrollIntoView({ behavior: "smooth", block: "center" });
    }
    function val(n) { var el = form.elements[n]; return el ? el.value : ""; }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (msg) { msg.className = "form__msg"; }
      var honey = form.elements["botcheck"];
      if (honey && honey.checked) return; // Bot → still verwerfen
      var endpoint = form.getAttribute("data-endpoint");
      var payload = {
        client: form.getAttribute("data-client"),
        name: val("name"), email: val("email"), telefon: val("telefon"),
        nachricht: val("nachricht"), seite: val("seite"), botcheck: ""
      };
      if (btn) { btn.disabled = true; btn.innerHTML = "Wird gesendet …"; }
      fetch(endpoint, {
        method: "POST",
        headers: { "content-type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(payload)
      }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (data) { return { ok: r.ok, data: data }; });
      }).then(function (res) {
        if (res.ok && res.data && res.data.ok) {
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
  });

  /* ---- scroll reveal ---- */
  var reveals = d.querySelectorAll(".reveal");
  var showAll = function () { reveals.forEach(function (el) { el.classList.add("is-in"); }); };
  var vh = window.innerHeight || 800;
  /* reveal anything already in view immediately — no flash for above-the-fold content */
  reveals.forEach(function (el) { if (el.getBoundingClientRect().top < vh * 0.98) el.classList.add("is-in"); });
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.06, rootMargin: "0px 0px -30px 0px" });
    reveals.forEach(function (el) { if (!el.classList.contains("is-in")) io.observe(el); });
    /* safety net: content is never left hidden even if the observer misfires */
    setTimeout(showAll, 1500);
    window.addEventListener("load", function () { setTimeout(showAll, 250); });
  } else {
    showAll();
  }
})();
