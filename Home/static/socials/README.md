# /socials/ assets

Drop your files here, then point the matching <img>/<video> src in
templates/Home/socials.html at them using {% load static %} + {% static %}.

- socials/img/logo.svg          -> nav + hero + footer logo (replaces the placeholder diamond SVG)
- socials/img/profile.jpg       -> About Me photo (about-photo-wrap)
- socials/video/about.mp4       -> About Me "in action" portrait video
- socials/video/reel.mp4        -> "IN MOTION" showreel (landscape)
- socials/img/services/*.jpg    -> one photo per service tab in "What I Do" (optional)

Everything else editable (services, socials links, merch products, collab
logos, testimonials, stats, impact numbers, hero taglines) lives in
Home/views.py -> SocialsPageView.get_context_data().
