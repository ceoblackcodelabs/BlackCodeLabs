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
