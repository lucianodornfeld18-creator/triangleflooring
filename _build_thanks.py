#!/usr/bin/env python3
"""Build a /thanks/ page that form submissions redirect to after success."""
import sys
sys.path.insert(0, '/home/claude/triangle')
from _gen import *

PATH = "/thanks/"
TITLE = "Thank You — Quote Request Received | Triangle Flooring"
DESC = "Thanks for reaching out to Triangle Flooring. We'll respond within 24 hours with your free written quote."

bc_items = [("Home","/"),("Thank You", None)]
bc_schema = render_breadcrumb_schema(bc_items)

content = f"""{page_head(TITLE, DESC, PATH)}
<style>
.thanks-wrap{{min-height:60vh;display:flex;align-items:center;justify-content:center;padding:5rem 20px 4rem;background:linear-gradient(135deg,var(--navy-light) 0%,#fff 60%)}}
.thanks-card{{max-width:640px;text-align:center;background:#fff;padding:3.5rem 2.5rem;border-radius:20px;box-shadow:var(--shadow-lg);border:1px solid var(--gray-border)}}
.thanks-icon{{width:88px;height:88px;background:linear-gradient(135deg,var(--success),#0EA46F);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 1.6rem}}
.thanks-icon svg{{width:48px;height:48px;color:#fff}}
.thanks-card h1{{color:var(--navy);font-size:2rem;margin-bottom:.7rem}}
.thanks-card .lead{{font-size:1.1rem;color:var(--gray);margin-bottom:2rem;line-height:1.6}}
.thanks-actions{{display:flex;gap:.9rem;justify-content:center;flex-wrap:wrap;margin-bottom:2rem}}
.thanks-actions a{{padding:13px 26px;border-radius:50px;font-family:var(--font-head);font-weight:600;font-size:.95rem;text-decoration:none;display:inline-flex;align-items:center;gap:8px}}
.thanks-actions .btn-call{{background:var(--orange);color:#fff;box-shadow:0 6px 20px rgba(224,122,43,.35)}}
.thanks-actions .btn-call:hover{{background:var(--orange-dark);transform:translateY(-2px);color:#fff}}
.thanks-actions .btn-wa{{background:var(--whatsapp);color:#fff}}
.thanks-actions .btn-wa:hover{{background:#1FB955;transform:translateY(-2px);color:#fff}}
.thanks-actions .btn-back{{background:transparent;color:var(--navy);border:2px solid var(--navy)}}
.thanks-actions .btn-back:hover{{background:var(--navy);color:#fff}}
.thanks-next{{padding-top:2rem;border-top:1px dashed var(--gray-border);text-align:left}}
.thanks-next h3{{font-size:1rem;color:var(--navy);margin-bottom:.8rem;text-align:center;font-family:var(--font-head)}}
.thanks-next ul{{list-style:none;max-width:480px;margin:0 auto}}
.thanks-next li{{padding:.6rem 0;display:flex;gap:.7rem;align-items:flex-start;font-size:.94rem;color:var(--text)}}
.thanks-next li::before{{content:"→";color:var(--cerulean);font-weight:700;flex-shrink:0;margin-top:1px}}
@media(max-width:560px){{
  .thanks-card{{padding:2.5rem 1.5rem}}
  .thanks-card h1{{font-size:1.6rem}}
}}
</style>
{header()}

<main class="thanks-wrap">
  <div class="thanks-card">
    <div class="thanks-icon">
      <svg fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg>
    </div>
    <h1>Thanks — we got it!</h1>
    <p class="lead">Your quote request is in. We&rsquo;ll review the details and respond within <strong>24 hours</strong> with a written, itemized estimate. No spam, no pressure.</p>

    <div class="thanks-actions">
      <a href="tel:+19414026861" class="btn-call">📞 Call Us Now</a>
      <a href="https://wa.me/19414026861?text=Hi%20Triangle%20Flooring%2C%20I%20just%20submitted%20a%20quote%20request." target="_blank" rel="noopener" class="btn-wa">💬 WhatsApp</a>
      <a href="/" class="btn-back">← Back to Site</a>
    </div>

    <div class="thanks-next">
      <h3>What happens next</h3>
      <ul>
        <li>We&rsquo;ll review your project details and any photos within 24 hours.</li>
        <li>If we need clarification, we&rsquo;ll text or email you first — no surprise calls.</li>
        <li>Your written, itemized quote arrives by email. Same crew that quotes does the install.</li>
        <li>Need it faster? Call us directly at (941) 402-6861 — we answer Mon&ndash;Sat 7&nbsp;AM&ndash;7&nbsp;PM.</li>
      </ul>
    </div>
  </div>
</main>

{footer()}
{whatsapp_float()}

<script type="application/ld+json">{json.dumps(bc_schema)}</script>
<!-- noindex meta tag — don't index this page -->
<script>document.head.insertAdjacentHTML('beforeend','<meta name="robots" content="noindex,nofollow">');</script>

{menu_script()}
</body>
</html>"""

import os
out = f"{OUT_DIR}/thanks/index.html"
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as f: f.write(content)
print(f"✓ /thanks/ ({len(content)//1024}KB)")
