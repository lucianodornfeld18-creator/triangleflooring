// Cloudflare Pages Function: /wa-lead
// Receives a lead (JSON) from the site forms via sendBeacon, then:
//   1. notifies the owner on WhatsApp through CallMeBot, and
//   2. emails the lead through Resend (independent of Web3Forms), when configured.
// Both run server-side, so no API key appears in page source and the calls are not
// subject to the page Content-Security-Policy.
//
// Environment variables (Cloudflare Pages -> Settings -> Environment variables):
//   CALLMEBOT_APIKEY, CALLMEBOT_PHONE  - optional, override the fallback literals below
//   RESEND_API_KEY                     - enables the email channel (no key = skipped)
//   LEAD_TO                            - comma-separated recipients (default: trianglefloor@gmail.com)
//   LEAD_BCC                           - optional comma-separated hidden copies (agency)
//   LEAD_FROM                          - sender on a Resend-verified domain
//                                        (default: "Triangle Flooring Website <leads@triangle-floor.com>")

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

    // Email channel (Resend). Skipped silently when RESEND_API_KEY is not set.
    if (context.env.RESEND_API_KEY && lines.length > 1) {
      const split = (v) => String(v || "").split(",").map((x) => x.trim()).filter(Boolean);
      const to = split(context.env.LEAD_TO);
      const bcc = split(context.env.LEAD_BCC);
      const from = context.env.LEAD_FROM || "Triangle Flooring Website <leads@triangle-floor.com>";
      const name = (d.name == null ? "" : String(d.name)).trim() || "Website visitor";
      const service = (d.service == null ? "" : String(d.service)).trim();
      const city = (d.city == null ? "" : String(d.city)).trim();
      const leadEmail = (d.email == null ? "" : String(d.email)).trim();
      const page = context.request.headers.get("referer") || "";
      const when = new Date().toLocaleString("en-US", { timeZone: "America/New_York" });
      const subject = "New lead: " + name
        + (service ? " - " + service : "")
        + (city ? " (" + city + ")" : "")
        + " - " + when;
      const body = lines.slice(1).join("\n")
        + "\n\nPage: " + page
        + "\nReceived: " + when + " (Florida time)"
        + "\n\nSent by the triangle-floor.com lead notifier.";
      const payload = {
        from: from,
        to: to.length ? to : ["trianglefloor@gmail.com"],
        subject: subject,
        text: body,
      };
      if (bcc.length) payload.bcc = bcc;
      if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(leadEmail)) payload.reply_to = leadEmail;
      context.waitUntil(fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + context.env.RESEND_API_KEY,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      }).catch(() => {}));
    }

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
