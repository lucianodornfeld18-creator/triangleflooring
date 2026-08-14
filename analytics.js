/*
 * Triangle Flooring analytics
 *
 * This file deliberately sends no form values, URLs, phone numbers, email
 * addresses, or message text. It is safe to include once sitewide with:
 * <script defer src="/analytics.js" data-triangle-analytics="v1"></script>
 */
(function (window, document) {
  "use strict";

  var MEASUREMENT_ID = "G-7VP0F63NPC";
  var LOADED_FLAG = "__triangleAnalyticsV1Loaded";

  if (window[LOADED_FLAG]) return;
  window[LOADED_FLAG] = true;

  window.dataLayer = window.dataLayer || [];
  if (typeof window.gtag !== "function") {
    window.gtag = function () {
      window.dataLayer.push(arguments);
    };
  }

  function hasGa4Config() {
    for (var i = 0; i < window.dataLayer.length; i += 1) {
      var item = window.dataLayer[i];
      if (item && item[0] === "config" && item[1] === MEASUREMENT_ID) return true;
    }
    return false;
  }

  function hasGa4Script() {
    var scripts = document.scripts;
    for (var i = 0; i < scripts.length; i += 1) {
      var src = scripts[i].src || "";
      if (src.indexOf("googletagmanager.com/gtag/js") !== -1 && src.indexOf("id=" + MEASUREMENT_ID) !== -1) {
        return true;
      }
    }
    return false;
  }

  function hasGa4LoaderDeclaration() {
    var scripts = document.scripts;
    var expectedSource = "googletagmanager.com/gtag/js?id=" + MEASUREMENT_ID;

    for (var i = 0; i < scripts.length; i += 1) {
      if ((scripts[i].textContent || "").indexOf(expectedSource) !== -1) return true;
    }
    return false;
  }

  function loadGa4() {
    if (!hasGa4Config()) {
      window.gtag("js", new Date());
      window.gtag("config", MEASUREMENT_ID);
    }

    if (!hasGa4Script() && !hasGa4LoaderDeclaration()) {
      var tag = document.createElement("script");
      tag.async = true;
      tag.src = "https://www.googletagmanager.com/gtag/js?id=" + MEASUREMENT_ID;
      tag.setAttribute("data-triangle-ga4", "v1");
      document.head.appendChild(tag);
    }
  }

  function sendEvent(name, parameters) {
    try {
      window.gtag("event", name, parameters || {});
    } catch (_) {
      // Analytics must never interrupt a visitor action.
    }
  }

  function getClosestForm(node) {
    while (node && node !== document) {
      if (node.nodeType === 1 && node.tagName === "FORM") return node;
      node = node.parentNode;
    }
    return null;
  }

  function formPosition(form) {
    var forms = document.forms;
    for (var i = 0; i < forms.length; i += 1) {
      if (forms[i] === form) return i + 1;
    }
    return 0;
  }

  function isLeadForm(form) {
    var action = (form.getAttribute("action") || "").toLowerCase();
    return action.indexOf("web3forms") !== -1 ? "lead" : "form";
  }

  var startedForms = typeof window.WeakSet === "function" ? new window.WeakSet() : [];

  function hasStarted(form) {
    if (typeof startedForms.has === "function") return startedForms.has(form);
    return startedForms.indexOf(form) !== -1;
  }

  function markFormStarted(form) {
    if (!form || hasStarted(form)) return;

    if (typeof startedForms.add === "function") {
      startedForms.add(form);
    } else {
      startedForms.push(form);
    }

    sendEvent("form_start", {
      form_position: formPosition(form),
      form_type: isLeadForm(form)
    });
  }

  function findLink(node) {
    while (node && node !== document) {
      if (node.nodeType === 1 && node.tagName === "A" && node.hasAttribute("href")) return node;
      node = node.parentNode;
    }
    return null;
  }

  function contactMethod(link) {
    var href = (link.getAttribute("href") || "").trim();
    if (/^tel:/i.test(href)) return "phone";
    if (/^mailto:/i.test(href)) return "email";

    try {
      var url = new window.URL(href, window.location.href);
      if (url.hostname === "wa.me" || url.hostname === "www.wa.me") return "whatsapp";
    } catch (_) {
      // A malformed or non-HTTP link is not a tracked contact action.
    }

    return "";
  }

  function onFormInteraction(event) {
    markFormStarted(getClosestForm(event.target));
  }

  loadGa4();

  ["focusin", "input", "change", "pointerdown"].forEach(function (eventName) {
    document.addEventListener(eventName, onFormInteraction, true);
  });

  document.addEventListener("click", function (event) {
    var method = contactMethod(findLink(event.target));
    if (!method) return;

    sendEvent("contact_click", {
      contact_method: method,
      transport_type: "beacon"
    });
  }, true);

  var path = window.location.pathname.replace(/\/+$/, "/") || "/";
  if (path === "/thanks/") {
    sendEvent("generate_lead", { lead_source: "quote_form" });
  }
})(window, document);
