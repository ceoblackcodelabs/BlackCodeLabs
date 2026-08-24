from django.utils import timezone
from django.db import migrations


CATEGORIES = [
    "Engineering",
    "Product",
    "Case Studies",
    "Industry Notes",
]

POSTS = [
    dict(
        title="Why We Chose Django for Client Projects in 2026",
        category="Engineering",
        excerpt="A look at why Django keeps winning on client work: speed of delivery, a mature admin, and an ecosystem that doesn't fight you.",
        body=(
            "<p>Every few months a client asks why we default to Django instead of the framework "
            "of the week. The honest answer: it lets us ship reliable software fast, and reliability "
            "compounds — a project that's still easy to maintain a year later saves everyone money.</p>"
            "<p>Django's admin alone routinely replaces weeks of internal-tooling work. Pair that with "
            "a mature ORM, a security team that takes CVEs seriously, and a package ecosystem that's "
            "survived a decade of churn, and it's a pragmatic default for almost any client engagement.</p>"
            "<p>That doesn't mean we reach for it blindly — a real-time chat app or a heavy data-science "
            "pipeline pulls in different tools. But for the majority of web platforms and internal tools "
            "we build, Django remains the fastest path from kickoff call to production.</p>"
        ),
        featured=True,
        read_minutes=5,
        days_ago=2,
    ),
    dict(
        title="From Kickoff to Launch: How We Scope a Client Project",
        category="Product",
        excerpt="A behind-the-scenes look at how we turn a first call into a shipped product — without scope creep eating the timeline.",
        body=(
            "<p>Every project starts the same way: a conversation about the problem, not the solution. "
            "We resist jumping straight to tech stack decisions until we understand what success actually "
            "looks like for the client.</p>"
            "<p>From there we break the build into milestones small enough to demo every week. Clients see "
            "progress constantly, which means scope drift gets caught early instead of at the end.</p>"
            "<p>The result is a predictable delivery process — fewer surprises for the client, fewer late "
            "nights for us.</p>"
        ),
        featured=False,
        read_minutes=4,
        days_ago=6,
    ),
    dict(
        title="Building VoteHub: A Real-Time Voting Platform on M-Pesa",
        category="Case Studies",
        excerpt="How we built a live award-show voting platform with M-Pesa payments, digital ticketing, and zero downtime on show night.",
        body=(
            "<p>When BCL Production came to us needing a platform to run live nominee voting for their "
            "annual awards show, the brief was simple: it has to work, live, in front of thousands of "
            "voters, with real money moving through M-Pesa.</p>"
            "<p>We built the vote-counting logic to be idempotent from day one — duplicate payment "
            "callbacks are a certainty at that scale, not an edge case. Combined with aggressive caching "
            "on the leaderboard and a queue-backed STK push integration, the platform held up through the "
            "entire show without a hiccup.</p>"
            "<p>Read more about the build in our portfolio.</p>"
        ),
        featured=False,
        read_minutes=6,
        days_ago=12,
    ),
    dict(
        title="The Tools We Actually Use in 2026",
        category="Industry Notes",
        excerpt="No sponsorships, no hype — just the tools sitting open on our machines every day this year.",
        body=(
            "<p>Every year the tooling landscape shifts a little, and every year we get asked what's "
            "actually in our stack versus what's just trending on social media. Here's the honest list.</p>"
            "<p>For backend work, Django and PostgreSQL remain the default. For anything real-time, we "
            "reach for FastAPI with WebSockets. On the frontend, React still wins for client dashboards, "
            "while React Native covers mobile when a project doesn't need fully native performance.</p>"
            "<p>Tooling opinions age fast — we'll revisit this list again next year.</p>"
        ),
        featured=False,
        read_minutes=3,
        days_ago=20,
    ),
]


def seed(apps, schema_editor):
    Category = apps.get_model("Blogs", "Category")
    Post = apps.get_model("Blogs", "Post")
    Comment = apps.get_model("Blogs", "Comment")
    User = apps.get_model("auth", "User")

    # Clear out any previously seeded off-brand content (e.g. campus/institutional
    # sample data from an earlier seed command) so the blog matches the site theme.
    Comment.objects.all().delete()
    Post.objects.all().delete()
    Category.objects.all().delete()

    author = User.objects.filter(is_superuser=True).order_by("id").first()
    if not author:
        author = User.objects.order_by("id").first()
    if not author:
        # No users at all yet — nothing safe to author posts with; leave blog empty.
        return

    cat_objs = {}
    for name in CATEGORIES:
        from django.utils.text import slugify
        cat_objs[name] = Category.objects.create(name=name, slug=slugify(name))

    from django.utils.text import slugify
    for data in POSTS:
        base_slug = slugify(data["title"])[:200] or "post"
        Post.objects.create(
            title=data["title"],
            slug=base_slug,
            category=cat_objs[data["category"]],
            author=author,
            excerpt=data["excerpt"],
            body=data["body"],
            featured=data["featured"],
            status="published",
            read_minutes=data["read_minutes"],
            published_at=timezone.now() - timezone.timedelta(days=data["days_ago"]),
        )


def unseed(apps, schema_editor):
    Category = apps.get_model("Blogs", "Category")
    Post = apps.get_model("Blogs", "Post")
    Post.objects.filter(title__in=[p["title"] for p in POSTS]).delete()
    Category.objects.filter(name__in=CATEGORIES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("Blogs", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
