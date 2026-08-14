// Cloudflare Pages Function: /wa-lead
// Receives a lead (JSON) from the site forms via sendBeacon, then notifies the
// owner on WhatsApp through CallMeBot — server-side, so the API key never appears
// in page source and the call is not subject to the page Content-Security-Policy.
//
// Optional (recommended) hardening: set CALLMEBOT_APIKEY and CALLMEBOT_PHONE as
// environment variables in the Cloudflare Pages dashboard to remove the fallback
// literals below from the repository entirely.

export async function onRequestPost(context) {
  try {
    const raw = await context.request.text();
    let d = {};
    try { d = JSON.parse(raw); } catch (_) { d = {}; }

    const phone = context.env.CALLMEBOT_PHONE || "+19414026861";
    const apikey = context.env.CALLMEBOT_APIKEY || "2854072";

    const fields = [
      ["name", "Nome"], ["phone", "Tel"], ["email", "Email"],
      ["city", "Cidade"], ["service", "Servico"],
      ["sqft", "Metragem"], ["message", "Detalhes"],
    ];
    const lines = ["Novo lead - Triangle Flooring"];
    for (const [k, label] of fields) {
      const v = (d[k] == null ? "" : String(d[k])).trim();
      if (v) lines.push(label + ": " + v);
    }
    const text = lines.join("\n");

    const url = "https://api.callmebot.com/whatsapp.php"
      + "?phone=" + encodeURIComponent(phone)
      + "&apikey=" + encodeURIComponent(apikey)
      + "&text=" + encodeURIComponent(text);

    // Let the CallMeBot request finish even after we return.
    context.waitUntil(fetch(url).catch(() => {}));

    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      // This is a form-processing endpoint, not a page that should be indexed.
      headers: {
        "Content-Type": "application/json",
        "X-Robots-Tag": "noindex, nofollow",
      },
    });
  } catch (e) {
    return new Response(JSON.stringify({ ok: false }), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "X-Robots-Tag": "noindex, nofollow",
      },
    });
  }
}

// Reject other methods cleanly.
export async function onRequest(context) {
  if (context.request.method === "POST") return onRequestPost(context);
  return new Response("Method Not Allowed", {
    status: 405,
    headers: { "X-Robots-Tag": "noindex, nofollow" },
  });
}
