"""Seeds SEO-focused blog posts aimed at Kenyan search intent.

Safe to re-run: posts are matched by slug and never overwritten.
Usage: python manage.py seed_kenya_posts [--author USERNAME]
"""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from Blogs.models import Category, Post


def html(*blocks):
    # post_detail renders body|safe|linebreaks, so no raw newlines between tags.
    return "".join(blocks)


POSTS = [
    dict(
        slug="how-much-does-a-website-cost-in-kenya",
        title="How Much Does a Website Cost in Kenya? (2026 Pricing Guide)",
        category="Web Development",
        excerpt="A plain-English breakdown of what websites, web apps and mobile apps cost in Kenya in KES, what drives the price, and how to avoid paying twice.",
        read_minutes=6, featured=True, days_ago=1,
        body=html(
            "<p>If you have searched \"how much does a website cost in Kenya\", you have probably seen quotes from KES 5,000 to KES 500,000 for what looks like the same thing. The gap is real, and it comes from what is actually being built.</p>",
            "<h2>Typical price ranges in Kenya</h2>",
            "<ul>",
            "<li><strong>Business website (up to ~8 pages):</strong> roughly KES 45,000 and up for a custom-designed, fast, SEO-ready site.</li>",
            "<li><strong>Custom web platform or online store with M-Pesa:</strong> roughly KES 150,000 and up.</li>",
            "<li><strong>Mobile app (iOS + Android) with a backend:</strong> roughly KES 450,000 and up.</li>",
            "<li><strong>Enterprise systems:</strong> scoped per project.</li>",
            "</ul>",
            "<p>These are the starting points we publish on our <a href=\"/pricing/\">pricing page</a>. Your fixed quote depends on scope.</p>",
            "<h2>What drives the price</h2>",
            "<ol>",
            "<li><strong>Features, not pages.</strong> A brochure site is cheap. Logins, payments, bookings, dashboards and notifications are where the effort goes.</li>",
            "<li><strong>Integrations.</strong> M-Pesa Daraja, SMS, email, maps and accounting tools each add design, build and testing time.</li>",
            "<li><strong>Design.</strong> A template is cheaper than a custom design built around your brand and customers.</li>",
            "<li><strong>Who builds it.</strong> A freelancer, an agency and an in-house hire price risk, speed and accountability differently.</li>",
            "</ol>",
            "<h2>The cheap website trap</h2>",
            "<p>A KES 8,000 site is usually a reused template with no SEO setup, no security hardening and nobody to call when it breaks. Many businesses end up rebuilding within a year, so they pay twice. Ask what you own at the end: source code, hosting access and domain should all be yours.</p>",
            "<h2>Project price vs. monthly maintenance</h2>",
            "<p>Building and maintaining are separate costs. You pay once to build, and optionally a monthly fee afterwards for hosting care, backups, security updates and small changes. Be wary of any quote that charges you monthly just to get the project built.</p>",
            "<h2>Costs people forget</h2>",
            "<ul>",
            "<li>Domain (renewed yearly) and hosting.</li>",
            "<li>Payment gateway and SMS fees, which are charged by the provider.</li>",
            "<li>Content: photos, copywriting, product data.</li>",
            "</ul>",
            "<h2>How to get an accurate quote</h2>",
            "<p>Write down what the site must do for your customers, list the systems it must connect to, and share two or three sites you like. With that, any serious developer can give you a fixed written quote. <a href=\"/contact/\">Talk to BlackCodeLabs</a> for a free consultation.</p>",
        ),
    ),
    dict(
        slug="mpesa-daraja-stk-push-integration-guide",
        title="M-Pesa Daraja STK Push Integration: A Practical Guide for Kenyan Businesses",
        category="API Engineering",
        excerpt="How an M-Pesa STK Push payment actually works end to end, what you need from Safaricom, and the mistakes that cause failed or duplicated payments.",
        read_minutes=7, featured=False, days_ago=3,
        body=html(
            "<p>Accepting M-Pesa inside your own website or app is one of the highest-value integrations you can build in Kenya. Customers get a prompt on their phone, enter their PIN, and your system confirms the payment automatically. Here is how it works with Safaricom's Daraja API.</p>",
            "<h2>What you need before you start</h2>",
            "<ul>",
            "<li>A Safaricom Daraja developer account and an app (sandbox first).</li>",
            "<li>A Paybill or Till number for production, plus your Lipa na M-Pesa passkey.</li>",
            "<li>A public HTTPS callback URL that Safaricom can reach.</li>",
            "</ul>",
            "<h2>The flow in four steps</h2>",
            "<ol>",
            "<li><strong>Get an access token</strong> using your consumer key and secret via the OAuth endpoint (client credentials).</li>",
            "<li><strong>Send the STK Push request</strong> to the processrequest endpoint.</li>",
            "<li><strong>Customer approves</strong> the prompt on their phone.</li>",
            "<li><strong>Safaricom calls your callback URL</strong> with the result, and you update the order.</li>",
            "</ol>",
            "<h2>The request</h2>",
            "<p>The password is the Base64 of <code>ShortCode + Passkey + Timestamp</code>, and the timestamp is formatted <code>YYYYMMDDHHMMSS</code>.</p>",
            "<pre><code>POST /mpesa/stkpush/v1/processrequest&#10;{&#10;  \"BusinessShortCode\": \"174379\",&#10;  \"Password\": \"&lt;base64(shortcode+passkey+timestamp)&gt;\",&#10;  \"Timestamp\": \"20260101120000\",&#10;  \"TransactionType\": \"CustomerPayBillOnline\",&#10;  \"Amount\": 1,&#10;  \"PartyA\": \"2547XXXXXXXX\",&#10;  \"PartyB\": \"174379\",&#10;  \"PhoneNumber\": \"2547XXXXXXXX\",&#10;  \"CallBackURL\": \"https://yourdomain.com/mpesa/callback/\",&#10;  \"AccountReference\": \"ORDER-1001\",&#10;  \"TransactionDesc\": \"Payment\"&#10;}</code></pre>",
            "<p>Use <code>CustomerBuyGoodsOnline</code> for a Till number. Phone numbers must be in the <code>2547XXXXXXXX</code> format, not <code>07XX</code>.</p>",
            "<h2>Handling the callback</h2>",
            "<p>The callback contains a <code>ResultCode</code>. A value of <code>0</code> means success and includes the M-Pesa receipt number. Anything else is a failure or cancellation. Store the <code>CheckoutRequestID</code> when you send the request so you can match the callback to the right order.</p>",
            "<h2>Mistakes that cost money</h2>",
            "<ul>",
            "<li><strong>Trusting the browser.</strong> Only mark an order paid from the verified server callback, never from a page redirect.</li>",
            "<li><strong>No idempotency.</strong> Callbacks can arrive more than once. Make updates safe to repeat.</li>",
            "<li><strong>Hardcoded secrets.</strong> Keep keys and passkeys in environment variables.</li>",
            "<li><strong>No fallback.</strong> If the callback never arrives, query the transaction status so no paid order is left pending.</li>",
            "</ul>",
            "<p>BlackCodeLabs builds M-Pesa Daraja integrations on Django for shops, ticketing and booking platforms. <a href=\"/contact/\">Get in touch</a> if you want it done right the first time.</p>",
        ),
    ),
    dict(
        slug="how-to-choose-a-software-development-company-in-kenya",
        title="How to Choose a Software Development Company in Kenya: 9 Questions to Ask",
        category="Business & Strategy",
        excerpt="Before you sign with a developer or agency, ask these nine questions. They separate teams that ship reliable software from those that disappear after payment.",
        read_minutes=6, featured=False, days_ago=6,
        body=html(
            "<p>Hiring the wrong developer is expensive: lost months, a half-built product and sometimes no access to your own code. Use these questions to vet any software company in Kenya, including us.</p>",
            "<h2>1. Can I see live work?</h2>",
            "<p>Ask for links to real, running projects, not just screenshots. Open them on your phone. Check speed and whether they work properly.</p>",
            "<h2>2. Who will actually build my project?</h2>",
            "<p>Some agencies sell with senior people and hand work to juniors or subcontractors. Ask who writes the code and who you will talk to weekly.</p>",
            "<h2>3. Will I own the code and the accounts?</h2>",
            "<p>The answer must be yes: source code, domain, hosting and databases in your name. Get it in writing as an IP transfer clause.</p>",
            "<h2>4. How is the price structured?</h2>",
            "<p>Look for a fixed written quote with milestones, for example 50% to start and 50% on delivery. Be careful with vague hourly estimates and with monthly fees just to build.</p>",
            "<h2>5. What is the timeline?</h2>",
            "<p>A credible team gives dated milestones. A typical business site takes 1-2 weeks, a custom platform 4-8 weeks and a mobile app 8-16 weeks.</p>",
            "<h2>6. Can you integrate M-Pesa and local services?</h2>",
            "<p>If you sell in Kenya, you need Daraja, SMS and maybe KRA or accounting integrations. Ask for an example.</p>",
            "<h2>7. How do you handle security and backups?</h2>",
            "<p>Ask about HTTPS, access control, backups and how they respond to vulnerabilities.</p>",
            "<h2>8. What happens after launch?</h2>",
            "<p>Software needs updates. Ask what a maintenance plan includes, what it costs, and whether you can cancel.</p>",
            "<h2>9. How will we communicate?</h2>",
            "<p>Weekly demos and one clear contact beat silence followed by a surprise. Agree on channels such as WhatsApp and email up front.</p>",
            "<h2>Red flags</h2>",
            "<ul><li>Prices far below everyone else, with no breakdown.</li><li>No portfolio you can verify.</li><li>Refusal to hand over source code.</li><li>Pressure to pay everything upfront.</li></ul>",
            "<p>Want to see how we answer these? Review our <a href=\"/portfolio/\">portfolio</a> and <a href=\"/pricing/\">pricing</a>, then <a href=\"/contact/\">book a free consultation</a>.</p>",
        ),
    ),
    dict(
        slug="website-vs-web-app-vs-mobile-app-for-your-kenyan-business",
        title="Website, Web App or Mobile App? What Your Kenyan Business Actually Needs",
        category="Software Development",
        excerpt="Not every business needs an app. Here is a simple way to decide between a website, a web application and a mobile app, and what each one costs to run.",
        read_minutes=5, featured=False, days_ago=9,
        body=html(
            "<p>\"We need an app\" is the most common thing founders tell us, and often the wrong first step. The right choice depends on what your customers need to do.</p>",
            "<h2>A website is enough when...</h2>",
            "<p>You mainly need to be found on Google, explain your services, build trust and collect enquiries via a form or WhatsApp. Clinics, law firms, schools, restaurants and consultants often start here.</p>",
            "<h2>You need a web application when...</h2>",
            "<p>Users must log in, pay, book, track orders or manage data. Examples: an online store with M-Pesa, a booking system, a school portal, a voting or ticketing platform. A web app runs in any browser, so there is nothing to install, which suits Kenya well where phone storage and data costs matter.</p>",
            "<h2>You need a mobile app when...</h2>",
            "<ul>",
            "<li>You need push notifications, offline use or device features like the camera and GPS.</li>",
            "<li>Customers use your product daily, such as delivery, fintech or fitness.</li>",
            "<li>You are building a product, not just supporting a business.</li>",
            "</ul>",
            "<h2>A smart path for most startups</h2>",
            "<ol>",
            "<li>Launch a fast, SEO-ready website to start getting customers.</li>",
            "<li>Add a web platform for the features that make money.</li>",
            "<li>Build the mobile app once real usage proves the need.</li>",
            "</ol>",
            "<p>With Django for the backend and React Native for mobile, the API you build for the web platform can be reused for the app, which saves cost later.</p>",
            "<h2>What about running costs?</h2>",
            "<p>Every option has hosting, domain and updates. Mobile apps add app-store fees and OS updates. Plan for an optional monthly maintenance plan from the start.</p>",
            "<p>Not sure which fits? <a href=\"/contact/\">Tell us what you want to achieve</a> and we will recommend the simplest option that works.</p>",
        ),
    ),
    dict(
        slug="why-your-website-needs-a-maintenance-plan",
        title="Why Your Website Needs a Maintenance Plan (and What It Should Include)",
        category="Software Development",
        excerpt="Launching is the start, not the finish. Here is what website maintenance covers, why skipping it gets expensive, and how to tell a good plan from a bad one.",
        read_minutes=5, featured=False, days_ago=12,
        body=html(
            "<p>Many owners treat a website like a printed brochure: build it once and forget it. But software ages. Dependencies need patches, certificates expire and hosting servers need attention.</p>",
            "<h2>What maintenance should cover</h2>",
            "<ul>",
            "<li><strong>Security updates</strong> for the framework and its packages.</li>",
            "<li><strong>Backups</strong> that are tested, stored off the server and restorable.</li>",
            "<li><strong>Uptime monitoring</strong> so you hear about downtime before customers do.</li>",
            "<li><strong>Bug fixes</strong> when something breaks, such as a payment error after a provider change.</li>",
            "<li><strong>Performance checks</strong> for speed, which affects both conversions and Google rankings.</li>",
            "<li><strong>A set number of hours</strong> for small content and feature changes.</li>",
            "</ul>",
            "<h2>What skipping it costs</h2>",
            "<p>Outdated software is the most common way sites get hacked. Recovering a compromised or crashed site, with no backup, usually costs far more than a year of maintenance. A slow or broken site also quietly loses customers.</p>",
            "<h2>Maintenance is separate from the build</h2>",
            "<p>A fair structure is a one-time project price to build, plus an optional monthly fee afterwards. At BlackCodeLabs our care plans start from KES 3,500 per month for a website, and you can cancel with 30 days' notice. See the details on the <a href=\"/pricing/\">pricing page</a>.</p>",
            "<h2>How to judge a plan</h2>",
            "<ol>",
            "<li>It lists exactly what is included and how many hours you get.</li>",
            "<li>It states response times.</li>",
            "<li>There is no long lock-in contract.</li>",
            "<li>You keep ownership and access to everything.</li>",
            "</ol>",
            "<p>Questions about keeping your site healthy? <a href=\"/contact/\">Contact us</a> for a quick review.</p>",
        ),
    ),
    dict(
        slug="ssl-certificates-in-kenya-how-to-choose-a-provider",
        title="SSL Certificates in Kenya (2026): How to Choose a Provider and What to Pay",
        category="Security & Bug Bounty",
        excerpt="Free or paid, DV or OV? A plain-English guide to choosing an SSL certificate provider in Kenya: what each type is for, what to ask before you buy, and why shorter 2026 lifespans make auto-renewal essential.",
        read_minutes=9, featured=False, days_ago=0,
        body=html(
            "<p>Open a website without a valid SSL certificate and the browser warns you it is “Not secure”. For a Kenyan business that is a lost customer: nobody types an M-Pesa number, a card number or even an email address into a page their browser is warning them about. Search engines also treat HTTPS as the baseline, and the Data Protection Act, 2019 expects you to protect the personal data your forms collect.</p>",
            "<p>The good news is that SSL is cheap, and often free. The difficulty is choosing: free or paid, which type, and who to buy from. This guide covers each question in plain English.</p>",

            "<h2>What an SSL certificate actually does</h2>",
            "<p>An SSL (technically TLS) certificate does two jobs. It <strong>encrypts</strong> the connection between your visitor and your server so nobody on the café Wi-Fi can read what is sent, and it <strong>proves identity</strong>, so the visitor knows the site really belongs to the domain in the address bar. The padlock and the <code>https://</code> prefix are the visible result.</p>",
            "<p>One point surprises many people: <strong>the encryption is the same strength whatever you pay</strong>. A free certificate and a KES 30,000 one encrypt equally well. What the money buys is the level of identity checking, a warranty, support and convenience.</p>",

            "<h2>The certificate types, and who needs which</h2>",
            "<div class=\"tbl\"><table>",
            "<tr><th>Type</th><th>What is checked</th><th>Best for</th><th>Issued in</th></tr>",
            "<tr><td><strong>DV</strong> (Domain Validation)</td><td>That you control the domain</td><td>Blogs, brochure sites, most small businesses and online shops</td><td>Minutes</td></tr>",
            "<tr><td><strong>OV</strong> (Organisation Validation)</td><td>The domain plus your registered company</td><td>Companies that want customers to see the organisation behind the site</td><td>1 to 3 days</td></tr>",
            "<tr><td><strong>EV</strong> (Extended Validation)</td><td>Strict legal and operational checks</td><td>Banks, fintech and regulated businesses</td><td>Several days</td></tr>",
            "<tr><td><strong>Wildcard</strong></td><td>Covers every subdomain, such as <code>*.yourdomain.co.ke</code></td><td>Sites with many subdomains (shop., app., mail.)</td><td>Same as DV or OV</td></tr>",
            "<tr><td><strong>Multi-domain</strong> (SAN)</td><td>Several different domain names on one certificate</td><td>A company with a few separate sites</td><td>Same as DV or OV</td></tr>",
            "</table></div>",
            "<p><strong>A note on EV.</strong> It used to turn the address bar green with your company name. Browsers removed that display years ago, so today an EV certificate brings little visible benefit to ordinary visitors. Pay for it only if a regulator, bank or partner requires it.</p>",

            "<h2>Free or paid SSL?</h2>",
            "<p><strong>Free is fine for most sites.</strong> Let's Encrypt, ZeroSSL and the certificate Cloudflare provides are all trusted by every major browser. If your host installs and renews one automatically, a brochure site, blog or small shop has no need to pay.</p>",
            "<p><strong>Paid makes sense when</strong> you need an OV or EV certificate, you want a warranty or insurance against a certificate-related loss, your payment partner or tender asks for a named business certificate, or you simply prefer a provider that installs it, monitors it and answers the phone when something breaks. You are paying for the service wrapped around the certificate, so judge the provider, not the padlock.</p>",

            "<h2>The 2026 change that matters: certificates now expire much sooner</h2>",
            "<p>Until recently a certificate could last 398 days. The browser and certificate-authority industry has agreed to shorten this in steps, as <a href=\"https://www.ssl.com/article/ssl-certificate-validity-changes-what-you-need-to-know/\" rel=\"noopener\" target=\"_blank\">SSL.com</a> and others have explained:</p>",
            "<ul><li><strong>From 15 March 2026:</strong> a maximum of 200 days (already in force).</li><li><strong>From 15 March 2027:</strong> a maximum of 100 days.</li><li><strong>From 15 March 2029:</strong> a maximum of 47 days.</li></ul>",
            "<p>This applies to every publicly trusted certificate, free or paid. In practice it means <strong>renewing by hand once a year is ending</strong>. Soon you would be doing it several times a year, and one forgotten renewal takes your site offline with a full-page browser warning. Whoever you buy from, automatic renewal is now close to essential.</p>",

            "<h2>How to choose a provider in Kenya: a checklist</h2>",
            "<p>Before you pay anyone, ask these questions:</p>",
            "<ol>",
            "<li><strong>What is the total price in KES?</strong> Ask for the all-in figure including VAT, and the price at renewal, which is sometimes higher than year one. Be wary of dollar prices that move with the exchange rate.</li>",
            "<li><strong>Can I pay by M-Pesa?</strong> Local payment options save you the card-and-forex headache and give you a proper receipt.</li>",
            "<li><strong>Do you install it for me?</strong> Installation is where many people get stuck. A provider that does it for you, on your hosting, is worth a small premium.</li>",
            "<li><strong>Is renewal automatic, and who is alerted if it fails?</strong> With the shorter lifespans above, this matters more than the brand on the certificate.</li>",
            "<li><strong>How is OV or EV validation handled?</strong> Ask what documents are needed and how long it normally takes, so you are not surprised on launch day.</li>",
            "<li><strong>Who can I reach, and how?</strong> Local support by phone or WhatsApp during business hours beats a ticket system in another time zone.</li>",
            "<li><strong>Which certificate authority is behind it?</strong> Sectigo, DigiCert, GlobalSign and Let's Encrypt are all trusted by every mainstream browser and phone. You rarely need to chase a famous brand for DV certificates.</li>",
            "<li><strong>Is reissue free, and what is the refund policy?</strong> You will need to reissue if you change servers or lose a key.</li>",
            "<li><strong>Will the account be in my name?</strong> The certificate and its login should belong to you, not to a freelancer who may disappear.</li>",
            "</ol>",

            "<h2>Where to get your certificate</h2>",
            "<div class=\"tbl\"><table>",
            "<tr><th>Source</th><th>Good because</th><th>Watch out for</th></tr>",
            "<tr><td><strong>Your hosting company</strong></td><td>Often included free, installed and renewed automatically (for example through cPanel AutoSSL)</td><td>Usually DV only; check what happens if you move host</td></tr>",
            "<tr><td><strong>A local reseller or web agency</strong></td><td>Prices in KES, M-Pesa, hands-on installation and local support</td><td>Compare the all-in price and confirm renewal is handled</td></tr>",
            "<tr><td><strong>The certificate authority directly</strong></td><td>Widest choice, including OV and EV</td><td>Dollar billing, and you do the validation and installation yourself</td></tr>",
            "<tr><td><strong>Cloudflare</strong></td><td>Free, automatic, and adds a CDN and firewall</td><td>Set the encryption mode to Full (strict), or traffic between Cloudflare and your server stays weak</td></tr>",
            "</table></div>",

            "<h2>Installing it without stress</h2>",
            "<ol>",
            "<li><strong>On shared hosting,</strong> switch on AutoSSL or Let's Encrypt in the control panel. For a paid certificate, generate a CSR, submit it, complete the validation and paste in the certificate files, or ask your provider to do it.</li>",
            "<li><strong>On your own server (VPS),</strong> use Certbot, which obtains and renews Let's Encrypt certificates automatically.</li>",
            "<li><strong>Force HTTPS.</strong> Redirect all <code>http://</code> traffic to <code>https://</code>, on both the bare domain and <code>www</code>.</li>",
            "<li><strong>Fix mixed content.</strong> Images, scripts or fonts still loaded over <code>http://</code> break the padlock. Update them.</li>",
            "<li><strong>Update the rest.</strong> Point your canonical URLs, sitemap, Google Search Console property and payment callbacks (such as your M-Pesa callback URL) to the <code>https://</code> address.</li>",
            "<li><strong>Test it.</strong> Run your domain through the free <a href=\"https://www.ssllabs.com/ssltest/\" rel=\"noopener\" target=\"_blank\">SSL Labs test</a> and look for a clean A grade.</li>",
            "</ol>",
            "<p>If your site runs on Django, also turn on <code>SECURE_SSL_REDIRECT</code>, <code>SESSION_COOKIE_SECURE</code> and <code>CSRF_COOKIE_SECURE</code> once HTTPS works, and consider HSTS.</p>",

            "<h2>Seven mistakes to avoid</h2>",
            "<ul>",
            "<li><strong>Letting it expire.</strong> The most common one. Set automatic renewal and a calendar reminder as a backstop.</li>",
            "<li><strong>Covering only one hostname.</strong> A certificate for <code>www.example.co.ke</code> does not automatically cover <code>example.co.ke</code>. Confirm both are included.</li>",
            "<li><strong>Buying a wildcard you do not need.</strong> If you have one or two subdomains, two ordinary certificates are cheaper.</li>",
            "<li><strong>Paying for EV out of habit.</strong> See the note above: visitors no longer see the difference.</li>",
            "<li><strong>Ignoring mixed content.</strong> The certificate is valid but the page still shows a warning.</li>",
            "<li><strong>Skipping the intermediate certificate.</strong> A missing chain works on your laptop and fails on some phones. SSL Labs will flag it.</li>",
            "<li><strong>Not owning the account.</strong> If a former developer holds the login, you cannot renew when it matters.</li>",
            "</ul>",

            "<h2>Frequently asked questions</h2>",
            "<h3>Is a free SSL certificate safe?</h3>",
            "<p>Yes. The encryption is the same as on paid certificates, and the certificate authorities behind the free ones are trusted by all mainstream browsers. What free certificates do not offer is organisation-level validation, a warranty or a support desk.</p>",
            "<h3>Do I need SSL if my site does not take payments?</h3>",
            "<p>Yes. Any form, login or contact page handles personal data, browsers flag non-HTTPS sites as “Not secure”, and HTTPS is a basic search-ranking signal.</p>",
            "<h3>How long does it take to get one?</h3>",
            "<p>A DV certificate is usually issued within minutes of proving you control the domain. OV takes a day or more and EV longer, depending on how quickly you provide your documents.</p>",
            "<h3>What happens if mine expires?</h3>",
            "<p>Visitors see a full-page browser warning and most will leave. Search engines and payment callbacks may also fail. Renewing and reinstalling restores the site immediately, which is why automatic renewal is worth setting up.</p>",
            "<h3>Can I move my certificate to another host?</h3>",
            "<p>Yes, if you have the private key, or you can simply reissue it, which is normally free. Free auto-renewing certificates are re-created on the new host in minutes.</p>",

            "<h2>The bottom line</h2>",
            "<p>For most Kenyan small businesses the right answer is simple: use a free, automatically renewing DV certificate installed properly, force HTTPS, and monitor it. Step up to a paid OV certificate when your business, your customers or a partner needs to see the company behind the site. Choose the provider on installation, renewal and support, not on the logo.</p>",
            "<p>BlackCodeLabs sets up HTTPS, redirects and renewal monitoring on every site we build, and our <a href=\"/pricing/\">maintenance plans</a> include certificate renewal reminders so a lapsed padlock never reaches your customers. If your site is showing “Not secure” or you want a second pair of eyes on your setup, <a href=\"/contact/\">talk to us</a> for a free check.</p>",
        ),
    ),
]


class Command(BaseCommand):
    help = "Seed SEO-focused blog posts for Kenyan search intent (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument("--author", help="Username to publish as (default: first superuser)")

    def handle(self, *args, **opts):
        User = get_user_model()
        if opts.get("author"):
            author = User.objects.filter(**{User.USERNAME_FIELD: opts["author"]}).first()
        else:
            author = User.objects.filter(is_superuser=True).order_by("pk").first()
        if not author:
            raise CommandError("No author found. Create a superuser or pass --author.")

        now = timezone.now()
        created = 0
        for p in POSTS:
            if Post.objects.filter(slug=p["slug"]).exists():
                self.stdout.write(f"skip (exists): {p['slug']}")
                continue
            cat, _ = Category.objects.get_or_create(name=p["category"])
            Post.objects.create(
                slug=p["slug"], title=p["title"], category=cat, author=author,
                excerpt=p["excerpt"], body=p["body"], read_minutes=p["read_minutes"],
                featured=p["featured"], status="published",
                published_at=now - timedelta(days=p["days_ago"]),
            )
            created += 1
            self.stdout.write(self.style.SUCCESS(f"created: {p['slug']}"))
        self.stdout.write(self.style.SUCCESS(f"Done. {created} new post(s)."))
