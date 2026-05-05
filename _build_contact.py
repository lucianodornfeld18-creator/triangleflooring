#!/usr/bin/env python3
"""Generate /contact/index.html"""
import sys, json
sys.path.insert(0, '/home/claude/triangle')
from _gen import *

PATH = "/contact/"
TITLE = "Contact Triangle Flooring | Free Quote in Bradenton FL"
DESC = "Contact Triangle Flooring for a free flooring estimate. Call (941) 402-6861, WhatsApp, or email. Serving Bradenton, Sarasota & Tampa Bay. 24h response."

bc_items = [("Home", "/"), ("Contact", None)]
bc_schema = render_breadcrumb_schema([(n,u) for n,u in bc_items])

contact_schema = {
  "@context":"https://schema.org",
  "@type":"ContactPage",
  "url":f"https://{DOMAIN}/contact/",
  "name":"Contact Triangle Flooring",
  "description":DESC,
  "mainEntity":{"@id":f"https://{DOMAIN}/#organization"}
}

extra_css = """
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:2.5rem;align-items:start;max-width:1100px;margin:0 auto}
.contact-card{background:#fff;border-radius:18px;padding:2rem;box-shadow:var(--shadow);border:1px solid var(--gray-border)}
.contact-card h2{font-size:1.5rem;margin-bottom:.5rem}
.contact-card>p{color:var(--gray);margin-bottom:1.5rem}
.contact-method{display:flex;gap:14px;padding:1.1rem 0;border-bottom:1px solid var(--gray-border);align-items:flex-start}
.contact-method:last-child{border-bottom:none}
.contact-method-icon{width:42px;height:42px;background:var(--navy-light);border-radius:50%;display:grid;place-items:center;color:var(--navy);flex-shrink:0}
.contact-method-icon svg{width:18px;height:18px}
.contact-method strong{font-family:var(--font-head);font-size:1rem;color:var(--text);display:block;margin-bottom:2px}
.contact-method a{color:var(--cerulean);font-weight:600;font-size:1.05rem}
.contact-method span{font-size:.85rem;color:var(--gray);display:block;margin-top:2px}
.form-group{margin-bottom:1.1rem}
.form-group label{display:block;font-family:var(--font-head);font-weight:600;font-size:.88rem;color:var(--text);margin-bottom:.4rem}
.form-group input,.form-group select,.form-group textarea{width:100%;padding:11px 14px;border:1.5px solid var(--gray-border);border-radius:10px;font-family:var(--font-body);font-size:.95rem;color:var(--text);transition:all var(--transition);background:#fff}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{outline:none;border-color:var(--cerulean);box-shadow:0 0 0 3px rgba(46,141,217,.12)}
.form-group textarea{resize:vertical;min-height:100px;font-family:var(--font-body)}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.hours-list{list-style:none;padding:0}
.hours-list li{display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px dashed var(--gray-border);font-size:.94rem}
.hours-list li:last-child{border-bottom:none}
.hours-list strong{font-family:var(--font-head);color:var(--text);font-weight:600}
.hours-list span{color:var(--gray)}
.map-wrap{margin-top:2rem;border-radius:18px;overflow:hidden;box-shadow:var(--shadow);height:380px;border:1px solid var(--gray-border)}
.map-wrap iframe{width:100%;height:100%;border:0;display:block}
@media(max-width:880px){.contact-grid{grid-template-columns:1fr;gap:2rem}.form-row{grid-template-columns:1fr}}
"""

content = f"""{page_head(TITLE, DESC, PATH)}
<style>{extra_css}</style>
{header()}
{breadcrumbs(bc_items)}

<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Get In Touch</span>
    <h1>Free Estimate <span>Within 24 Hours</span></h1>
    <p>Call, text, WhatsApp, or fill out the form below — whichever works best. We respond same-day, 7 days a week.</p>
  </div>
</section>

<section style="background:var(--gray-light)">
  <div class="container">
    <div class="contact-grid">
      <div class="contact-card">
        <h2>Talk to Us</h2>
        <p>The fastest way to a free quote — pick whichever channel you prefer.</p>
        <div class="contact-method">
          <div class="contact-method-icon"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg></div>
          <div><strong>Call or Text</strong><a href="tel:{PHONE}">{PHONE_DISPLAY}</a><span>Mon–Sun, 7 AM – 8 PM</span></div>
        </div>
        <div class="contact-method">
          <div class="contact-method-icon" style="background:#DCFCE7;color:#15803D"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.71.306 1.263.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347"/></svg></div>
          <div><strong>WhatsApp</strong><a href="https://wa.me/19414026861?text=Hi%20Triangle%20Flooring%2C%20I%27d%20like%20a%20free%20flooring%20estimate." target="_blank" rel="noopener">{PHONE_DISPLAY}</a><span>Reply within 1 hour during business hours</span></div>
        </div>
        <div class="contact-method">
          <div class="contact-method-icon"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></div>
          <div><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a><span>Best for project details &amp; photos</span></div>
        </div>
        <div class="contact-method">
          <div class="contact-method-icon"><svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg></div>
          <div><strong>Visit Us</strong><span style="color:var(--text);font-weight:500">8737 Royal Acacia Ave<br>Palmetto, FL 34221</span><span>By appointment only</span></div>
        </div>

        <h3 style="margin:1.8rem 0 .8rem;font-size:1.1rem">Business Hours</h3>
        <ul class="hours-list">
          <li><strong>Monday – Friday</strong><span>7:00 AM – 8:00 PM</span></li>
          <li><strong>Saturday</strong><span>7:00 AM – 8:00 PM</span></li>
          <li><strong>Sunday</strong><span>7:00 AM – 8:00 PM</span></li>
        </ul>
      </div>

      <div class="contact-card">
        <h2>Request a Free Quote</h2>
        <p>Tell us about your project — we'll respond within 24 hours with a no-obligation written estimate.</p>
        <form action="https://api.web3forms.com/submit" method="POST">
          <input type="hidden" name="access_key" value="d811c86f-d17c-4768-baaa-e6f55aceeb57">
          <input type="hidden" name="subject" value="New Quote Request — Triangle Flooring">
          <input type="hidden" name="from_name" value="Triangle Flooring Website">
          <input type="hidden" name="redirect" value="https://triangle-floor.com/thanks/">
          <input type="checkbox" name="botcheck" style="display:none" tabindex="-1" autocomplete="off">
          <div class="form-row">
            <div class="form-group"><label for="name">Name *</label><input type="text" id="name" name="name" required autocomplete="name"></div>
            <div class="form-group"><label for="phone">Phone *</label><input type="tel" id="phone" name="phone" required autocomplete="tel"></div>
          </div>
          <div class="form-group"><label for="email">Email</label><input type="email" id="email" name="email" autocomplete="email"></div>
          <div class="form-row">
            <div class="form-group"><label for="city">City</label><input type="text" id="city" name="city" placeholder="Bradenton, Sarasota..." autocomplete="address-level2"></div>
            <div class="form-group"><label for="service">Service Needed</label>
              <select id="service" name="service">
                <option value="">— Select —</option>
                <option>Hardwood Flooring</option>
                <option>Luxury Vinyl Plank (LVP)</option>
                <option>Tile Installation</option>
                <option>Laminate Flooring</option>
                <option>Stair Treads</option>
                <option>Repair / Replacement</option>
                <option>Multiple / Not Sure</option>
              </select>
            </div>
          </div>
          <div class="form-group"><label for="sqft">Approx. Square Footage (optional)</label><input type="text" id="sqft" name="sqft" placeholder="e.g. 1,200 sqft"></div>
          <div class="form-group"><label for="message">Project Details</label><textarea id="message" name="message" placeholder="Tell us about your project — rooms, timeline, any specific products in mind..."></textarea></div>
          <button type="submit" class="btn btn-primary" style="width:100%;font-size:1rem">Send My Request →</button>
          <p style="font-size:.78rem;color:var(--gray);text-align:center;margin-top:.85rem">By submitting, you agree to be contacted about your project. We never spam.</p>
        </form>
        <p style="font-size:.85rem;color:var(--gray);text-align:center;margin-top:1.4rem;padding-top:1.4rem;border-top:1px dashed var(--gray-border)">Form not working? Email us directly at <a href="mailto:trianglefloor@gmail.com?subject=Free%20Flooring%20Quote%20Request" style="color:var(--cerulean);font-weight:600">trianglefloor@gmail.com</a> or call <a href="tel:+19414026861" style="color:var(--cerulean);font-weight:600">(941) 402-6861</a>.</p>
      </div>
    </div>

    <div class="map-wrap" style="margin-top:3rem;max-width:1100px;margin-left:auto;margin-right:auto">
      <iframe loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=8737+Royal+Acacia+Ave,+Palmetto,+FL+34221&t=&z=13&ie=UTF8&iwloc=&output=embed" title="Triangle Flooring location map" allowfullscreen></iframe>
    </div>

  </div>
</section>

{final_cta()}
{footer()}
{whatsapp_float()}

<script type="application/ld+json">{json.dumps(bc_schema)}</script>
<script type="application/ld+json">{json.dumps(contact_schema)}</script>

{menu_script()}
</body>
</html>"""

with open(f"{OUT_DIR}/contact/index.html", "w") as f:
    f.write(content)
print(f"✓ /contact/index.html ({len(content)//1024} KB)")
