/**
 * data.js
 * ------------------------------------------------------------------
 * Single source of truth for site content. Every renderer in
 * carousel.js / gallery.js / main.js reads from window.HELTZ_DATA.
 *
 * This is written as plain JS objects/arrays so it can be swapped
 * for `await fetch('/api/...')` later without touching the render
 * functions — each render function already accepts a data array.
 * ------------------------------------------------------------------
 */

const HELTZ_DATA = {
  business: {
    name: "Heltz Driving Academy",
    shortName: "Heltz",
    tagline: "Driving Academy",
    strapline: "Smart Drivers Start Here",
    phonePrimary: "+254 743 552541",
    phonePrimaryHref: "tel:+254743552541",
    phoneList: ["020 222 3325", "0743 552541", "0722 614473", "0722 873914"],
    whatsapp: "+254 733 340082",
    whatsappHref: "https://wa.me/254733340082",
    email: "heltzdrivingschool@gmail.com",
    emailAlt: "info@heltzdrivingschool.com",
    address: "1st Floor, City Square Sheikh House, Tom Mboya Street, Nairobi, Kenya",
    poBox: "P.O. Box 71300-006622, Nairobi",
    hours: [
      { label: "Weekdays", value: "7:00 AM – 7:00 PM" },
      { label: "Saturday", value: "7:00 AM – 3:00 PM" },
    ],
    social: {
      facebook: "https://web.facebook.com/heltzdriving",
      twitter: "https://twitter.com/heltzdriving",
      instagram: "https://www.instagram.com/heltzdriving/?hl=nl",
      tiktok: "https://www.tiktok.com/@heltzdrivingschool",
    },
    mapsEmbed:
      "https://maps.google.com/maps?q=heltz%20driving&t=m&z=11&output=embed&iwloc=near",
    brochureUrl:
      "https://heltzdrivingschool.com/wp-content/uploads/2024/03/Heltz-brochure-full-clour-2024-21-feb.pdf",
  },

  /* ------------------------------------------------------------
     HERO CAROUSEL — mixed image/video slides, database-driven.
     Swap `media` for a locally-hosted asset once you have one;
     for now these hotlink the school's own existing photography.
  ------------------------------------------------------------ */
  heroSlides: [
    {
      type: "image",
      media:
        "https://heltzdrivingschool.com/wp-content/uploads/2024/05/WhatsApp-Image-2024-05-27-at-10.22.00-1.jpeg",
      tag: "Class B · Cars",
      title: "Let's Get You On The Road",
      description:
        "Ready to start driving? 35+ years teaching Nairobi to drive safely, responsibly and with confidence.",
      ctaText: "Enroll Now",
      ctaUrl: "register.html",
    },
    {
      type: "image",
      media:
        "https://heltzdrivingschool.com/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-21-at-12.31.47.jpeg",
      tag: "NTSA Curriculum",
      title: "Trained The Right Way",
      description:
        "Every lesson follows the NTSA driving curriculum — practical, theoretical, and built around real Nairobi roads.",
      ctaText: "View Courses",
      ctaUrl: "courses.html",
    },
    {
      type: "image",
      media:
        "https://heltzdrivingschool.com/wp-content/uploads/2023/02/Class-C.jpeg",
      tag: "Classes A · B · C · D",
      title: "Motorbikes To Trucks",
      description:
        "From Class A motorbikes to Class C trucks and PSV endorsements — one academy, every licence category.",
      ctaText: "See All Classes",
      ctaUrl: "courses.html",
    },
    {
      type: "image",
      media:
        "https://heltzdrivingschool.com/wp-content/uploads/2024/02/WhatsApp-Image-2024-02-16-at-09.23.52.jpeg",
      tag: "13 Branches",
      title: "A Branch Near You",
      description:
        "Thirteen branches across Nairobi — from Tom Mboya to Westlands, Donholm to South B. Find yours.",
      ctaText: "Find A Branch",
      ctaUrl: "branches.html",
    },
  ],

  /* ------------------------------------------------------------
     STATS — only real, non-invented figures. Counters animate
     the numeric ones; the others render as static text.
  ------------------------------------------------------------ */
  stats: [
    { value: 35, suffix: "+", label: "Years Instructing Drivers" },
    { value: 13, suffix: "", label: "Branches In Nairobi" },
    { value: 4, suffix: "", label: "Licence Classes Offered" },
    { value: 6, suffix: "", label: "Days A Week Open" },
  ],

  /* ------------------------------------------------------------
     WHY HELTZ — from the homepage "Why Heltz Driving School"
  ------------------------------------------------------------ */
  whyUs: [
    {
      icon: "instructor",
      title: "Experienced Instructors",
      text: "Our instructors are attentive to every student, with training schedules structured to match each student's needs and plans.",
    },
    {
      icon: "trophy",
      title: "Great Track Record",
      text: "Heltz has successfully trained thousands of competent drivers from all over Kenya — the driving academy trusted by individuals and corporations alike.",
    },
    {
      icon: "wallet",
      title: "Affordable Rates",
      text: "We offer all our courses at a pocket-friendly rate, with flexible full-course and half-course options for every student.",
    },
  ],

  /* ------------------------------------------------------------
     SERVICES
  ------------------------------------------------------------ */
  services: [
    {
      icon: "steering-wheel",
      title: "Practical Driving Lessons",
      text: "Hands-on instruction across Class A, B, C and D vehicles, following the NTSA curriculum, one class at a time.",
    },
    {
      icon: "book",
      title: "Theoretical Lessons",
      text: "Road rules, traffic control, road-user categories and modern town-board manoeuvring taught by experienced instructors.",
    },
    {
      icon: "refresh",
      title: "Refresher Courses",
      text: "Already licensed but want to sharpen up? Minimum 5-lesson refresher packages for Class A, B, C and D drivers.",
    },
    {
      icon: "briefcase",
      title: "Corporate & PSV Training",
      text: "PSV, bus and taxi endorsements plus professional driver training for uber/taxi operators and corporate fleets.",
    },
  ],

  /* ------------------------------------------------------------
     COURSES — grouped by class, mirrors the /courses page
     Each item: { class, name, details, price, unit }
  ------------------------------------------------------------ */
  courseGroups: [
    {
      id: "class-a",
      classCode: "A",
      name: "Class A",
      category: "Motorbikes",
      image:
        "https://heltzdrivingschool.com/wp-content/uploads/2021/02/108356642_3042037272583758_1200353584466957656_o-removebg-preview.png",
      description:
        "Motorbike instruction for both personal and PSV/courier riders, taught on real Nairobi road conditions.",
      transmission: "Manual",
      items: [
        { details: "A2 (18 years) — above 50cc", price: 8000 },
        { details: "A3 (21 years) — above 100cc (PSV/Courier)", price: 6000 },
        { details: "A2/A3 — Theory & Test Only", price: 6000 },
      ],
    },
    {
      id: "class-b",
      classCode: "B",
      name: "Class B",
      category: "Cars",
      image:
        "https://heltzdrivingschool.com/wp-content/uploads/2024/05/WhatsApp-Image-2024-05-27-at-10.22.00-1.jpeg",
      description:
        "The academy's most popular course — manual or automatic car lessons for everyday driving in Nairobi.",
      transmission: "Manual / Automatic",
      items: [
        { details: "Light Manual (18 years) — Full Course", price: 15000 },
        { details: "Light Auto (18 years) — Full Course", price: 15000 },
        { details: "Light Manual — Half Course / 2 lessons", price: 7000 },
        { details: "Light Auto — Half Course / 2 lessons", price: 7000 },
      ],
    },
    {
      id: "class-c",
      classCode: "C",
      name: "Class C",
      category: "Trucks",
      image:
        "https://heltzdrivingschool.com/wp-content/uploads/2023/02/Lorry-1024x683.jpeg",
      description:
        "Light truck instruction (C1), including a combined C1 + B1 package for drivers who want both classes.",
      transmission: "Manual",
      items: [
        { details: "C1 Light Trucks (22 years)", price: 15000 },
        { details: "C1 + B1 Combination (22 years)", price: 25000 },
        { details: "C1/C — Half Course / Theory & Test / 2 lessons", price: 7000 },
      ],
    },
    {
      id: "class-d",
      classCode: "D",
      name: "Class D",
      category: "Vans & PSV",
      image:
        "https://heltzdrivingschool.com/wp-content/uploads/2024/03/WhatsApp_Image_2024-02-16_at_15.23.52-removebg-preview.png",
      description:
        "Van, bus, taxi and PSV endorsements for professional drivers — including Uber/taxi and bus/PSV categories.",
      transmission: "Manual",
      items: [
        { details: "D1 Van (22 years), up to 14-seater PSV — 4yrs experience endorsement", price: 7000 },
        { details: "D Professional (21 years), Uber/Taxi — 3yrs experience endorsement", price: 7000 },
        { details: "D1 — Bus/PSV Endorsement", price: 7000 },
        { details: "D2 — Taxi/PSV Endorsement", price: 7000 },
        { details: "D — PSV F Full Course", price: 15000 },
      ],
    },
    {
      id: "vip",
      classCode: "VIP",
      name: "VIP Course",
      category: "Class B — All Inclusive",
      image:
        "https://heltzdrivingschool.com/wp-content/uploads/2024/03/886934b4-c86f-4648-a0a8-619011180d88-removebg-preview.png",
      description:
        "The complete Class B package, all inclusive — for students who want a single fixed price, start to finish.",
      transmission: "Manual / Automatic",
      items: [{ details: "Class B — All Inclusive", price: 30000 }],
    },
  ],

  refresherRates: [
    { classCode: "A", rate: 1000 },
    { classCode: "B", rate: 1200 },
    { classCode: "C & D", rate: 1500 },
  ],

  ntsaFees: [
    { item: "Provisional Driving Licence", amount: 650 },
    { item: "Test Application Fee", amount: 1050 },
    { item: "Endorsement", amount: 600 },
    { item: "Smart Driving Card", amount: 3000 },
  ],

  courseExtras: {
    theoryCovers: [
      "Manoeuvring on a modern town board",
      "Rules and regulations of Kenyan roads",
      "How traffic is controlled on the roads",
      "Categories of road users",
    ],
    otherBenefits: [
      "Basic Mechanics",
      "First Aid",
      "Assessment Test",
      "Car Hire",
      "Driving Test",
      "Certificate of Competency",
    ],
    prestigeServices: [
      "Special request for a lady instructor",
      "Pick and drop service (door-to-door)",
      "Unlimited theory lessons",
    ],
  },

  /* ------------------------------------------------------------
     FLEET — representative vehicle images per licence class.
     Individual model names aren't published on the source site,
     so cards are labelled by class/category rather than invented
     model names.
  ------------------------------------------------------------ */
  fleet: [
    {
      name: "Class A Training Motorbike",
      category: "Motorbikes",
      transmission: "Manual",
      image:
        "https://heltzdrivingschool.com/wp-content/uploads/2022/05/WhatsApp_Image_2022-02-17_at_11.53.41_AM-removebg-preview.png",
    },
    {
      name: "Class B Training Car",
      category: "Cars",
      transmission: "Manual / Automatic",
      image:
        "https://heltzdrivingschool.com/wp-content/uploads/2023/02/WhatsApp_Image_2023-01-06_at_15.34.33-removebg-preview.png",
    },
    {
      name: "Class C Training Truck",
      category: "Trucks",
      transmission: "Manual",
      image: "https://heltzdrivingschool.com/wp-content/uploads/2023/02/Lorry-1024x683.jpeg",
    },
    {
      name: "Class D Training Van",
      category: "Vans & PSV",
      transmission: "Manual",
      image:
        "https://heltzdrivingschool.com/wp-content/uploads/2024/03/WhatsApp_Image_2024-02-16_at_15.23.52-removebg-preview.png",
    },
    {
      name: "Class B VIP Vehicle",
      category: "Cars — VIP",
      transmission: "Manual / Automatic",
      image:
        "https://heltzdrivingschool.com/wp-content/uploads/2024/03/886934b4-c86f-4648-a0a8-619011180d88-removebg-preview.png",
    },
  ],

  /* ------------------------------------------------------------
     TESTIMONIALS — intentionally empty. The source site does not
     publish any student testimonials, so none are fabricated here.
     The renderer hides the section entirely when this is empty;
     drop real testimonials in following this shape to activate it.
  ------------------------------------------------------------ */
  testimonials: [],

  /* ------------------------------------------------------------
     GALLERY — curated subset of the school's published photos
  ------------------------------------------------------------ */
  gallery: [
    { type: "image", category: "Cars", src: "https://heltzdrivingschool.com/wp-content/uploads/2024/05/WhatsApp-Image-2024-05-27-at-10.22.00-1.jpeg", alt: "Heltz driving lesson, Class B car" },
    { type: "image", category: "Cars", src: "https://heltzdrivingschool.com/wp-content/uploads/2024/05/WhatsApp-Image-2024-05-27-at-10.22.01-1.jpeg", alt: "Heltz driving lesson in progress" },
    { type: "image", category: "Trucks", src: "https://heltzdrivingschool.com/wp-content/uploads/2023/02/Lorry.jpeg", alt: "Heltz Class C truck training" },
    { type: "image", category: "Cars", src: "https://heltzdrivingschool.com/wp-content/uploads/2024/05/WhatsApp-Image-2024-05-27-at-10.22.02.jpeg", alt: "Heltz student on the road" },
    { type: "image", category: "Campus", src: "https://heltzdrivingschool.com/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-21-at-12.31.47.jpeg", alt: "Heltz Driving Academy branch" },
    { type: "image", category: "Campus", src: "https://heltzdrivingschool.com/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-21-at-12.31.49.jpeg", alt: "Heltz Driving Academy team" },
    { type: "image", category: "Campus", src: "https://heltzdrivingschool.com/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-21-at-12.31.49-1.jpeg", alt: "Heltz Driving Academy students" },
    { type: "image", category: "Cars", src: "https://heltzdrivingschool.com/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-21-at-12.31.48-1.jpeg", alt: "Heltz Class B training" },
    { type: "image", category: "Trucks", src: "https://heltzdrivingschool.com/wp-content/uploads/2023/02/Class-C.jpeg", alt: "Heltz Class C training vehicle" },
    { type: "image", category: "Campus", src: "https://heltzdrivingschool.com/wp-content/uploads/2024/02/WhatsApp-Image-2024-02-28-at-17.31.33.jpeg", alt: "Heltz Driving Academy activity" },
    { type: "image", category: "Campus", src: "https://heltzdrivingschool.com/wp-content/uploads/2024/02/WhatsApp-Image-2024-02-28-at-17.31.32-1.jpeg", alt: "Heltz Driving Academy students" },
    { type: "image", category: "Campus", src: "https://heltzdrivingschool.com/wp-content/uploads/2024/02/WhatsApp-Image-2024-02-28-at-17.31.32.jpeg", alt: "Heltz Driving Academy branch" },
    { type: "image", category: "Motorbikes", src: "https://heltzdrivingschool.com/wp-content/uploads/2024/02/WhatsApp-Image-2024-02-16-at-09.23.52.jpeg", alt: "Heltz Class A motorbike training" },
    { type: "image", category: "Vans", src: "https://heltzdrivingschool.com/wp-content/uploads/2024/02/WhatsApp-Image-2024-02-16-at-09.24.31.jpeg", alt: "Heltz Class D van training" },
    { type: "image", category: "Campus", src: "https://heltzdrivingschool.com/wp-content/uploads/2024/02/WhatsApp-Image-2024-02-16-at-15.23.51.jpeg", alt: "Heltz Driving Academy" },
    { type: "image", category: "Campus", src: "https://heltzdrivingschool.com/wp-content/uploads/2024/02/WhatsApp-Image-2024-02-16-at-15.23.52-2.jpeg", alt: "Heltz Driving Academy students" },
    { type: "image", category: "Campus", src: "https://heltzdrivingschool.com/wp-content/uploads/2023/11/WhatsApp-Image-2023-10-25-at-10.53.07.jpeg", alt: "Heltz Driving Academy" },
    { type: "image", category: "Campus", src: "https://heltzdrivingschool.com/wp-content/uploads/2023/11/WhatsApp-Image-2023-10-25-at-10.53.05.jpeg", alt: "Heltz Driving Academy" },
    { type: "image", category: "Cars", src: "https://heltzdrivingschool.com/wp-content/uploads/2023/01/WhatsApp-Image-2023-01-06-at-15.34.27.jpeg", alt: "Heltz Class B car training" },
    { type: "image", category: "Cars", src: "https://heltzdrivingschool.com/wp-content/uploads/2023/01/WhatsApp-Image-2023-01-06-at-15.34.28.jpeg", alt: "Heltz Class B car training" },
    { type: "image", category: "Cars", src: "https://heltzdrivingschool.com/wp-content/uploads/2023/01/WhatsApp-Image-2023-01-06-at-15.34.29.jpeg", alt: "Heltz Class B car training" },
    { type: "image", category: "Campus", src: "https://heltzdrivingschool.com/wp-content/uploads/2023/01/WhatsApp-Image-2023-01-04-at-10.39.33-1.jpeg", alt: "Heltz Driving Academy" },
    { type: "image", category: "Campus", src: "https://heltzdrivingschool.com/wp-content/uploads/2023/01/WhatsApp-Image-2023-01-03-at-09.15.32.jpeg", alt: "Heltz Driving Academy" },
    { type: "image", category: "Campus", src: "https://heltzdrivingschool.com/wp-content/uploads/2023/01/WhatsApp-Image-2023-01-03-at-09.15.33.jpeg", alt: "Heltz Driving Academy" },
  ],

  /* ------------------------------------------------------------
     BRANCHES
  ------------------------------------------------------------ */
  branches: [
    { name: "Tom Mboya Branch", isHQ: true, location: "1st Floor, Sheikh House, Tom Mboya Street, Nairobi CBD" },
    { name: "Harambee Avenue Branch", isHQ: false, location: "City Square Branch, 3rd Floor, Jeevan Bharati House, Harambee Avenue — Opp. Electricity House" },
    { name: "Westlands Branch", isHQ: false, location: "2nd Floor, Westlands Arcade, Chiromo Road — Next to Naivas" },
    { name: "Parklands Branch", isHQ: false, location: "Shams Residence Building, Kusi Lane, Off Third Parklands Avenue" },
    { name: "Industrial Area Branch", isHQ: false, location: "Ground Floor, Enterprise Road, Opp. Homabay Road — Next to Shell" },
    { name: "Donholm Branch", isHQ: false, location: "1st Floor, Near Roundabout, Off Outer Ring Road — Next to Naivas, Close to Caltex" },
    { name: "Embakasi Branch", isHQ: false, location: "Ground Floor, Outering Road, Pipeline — Next to Bata & Aga Khan Hospital" },
    { name: "Umoja Branch", isHQ: false, location: "Ground Floor, Maliwa Plaza, Moi Drive — Next to Peacock Stage C" },
    { name: "Ruaraka Branch", isHQ: false, location: "Ground Floor, Drive-In Estate, Near GSU Roundabout, Outering Road — Opp. Shell Petrol Station" },
    { name: "Ngara Branch", isHQ: false, location: "Bano House, Past Post Bank — Near Ngara/Thika Road Junction" },
    { name: "Utawala Branch", isHQ: false, location: "1st Floor, Next to Easymart Supermarket — Opp. Family Bank, Next to Shell Petrol Station" },
    { name: "South C Branch", isHQ: false, location: "South C Shopping Centre, Muhoho Avenue — Opp. First Community Bank, Inside Minimall, 1st Floor" },
    { name: "South B Branch", isHQ: false, location: "Likoni Road, Inside Likoni Mall, 1st Floor — Opp. Winners Chapel Church" },
  ],

  /* ------------------------------------------------------------
     FAQ
  ------------------------------------------------------------ */
  faqs: [
    {
      q: "What is the right age to earn a licence in Kenya?",
      a: "18 years and above.",
    },
    {
      q: "Is BCE still recommended as a driving curriculum?",
      a: "NTSA (National Transport and Safety Authority) introduced a new curriculum where drivers attend one class at a time for a set duration — for example, a student cannot learn Class B and Class C at the same time.",
    },
    {
      q: "Can a student attend two classes at the same time?",
      a: "No. Each student is allowed to attend one class at a time. A student attending Class B cannot attend Class C at the same time.",
    },
    {
      q: "How much will I have to pay to attain a smart driving card?",
      a: "Each driver is expected to pay KES 3,000 to NTSA. As a Heltz student, we assist you in applying for your smart driving licence according to NTSA regulations.",
    },
    {
      q: "Is Heltz Driving School all over Kenya?",
      a: "Heltz Driving School is only located within Nairobi, with branches widely distributed across the city.",
    },
    {
      q: "What are the driving requirements?",
      a: "You must be 18 years or above with a national identity card (ID).",
    },
    {
      q: "What are the payment methods at Heltz Driving School?",
      a: "Heltz does not accept cash payments. Students can pay via M-Pesa (Buy Goods, Till Number 656 867) or bank deposit to our Equity Bank account. See the Payment Options page for full details.",
    },
    {
      q: "How can I get in touch with Heltz Driving School?",
      a: "Visit any of our 13 branches within Nairobi, call us on 020 222 3325 / 0743 552541 / 0722 614473 / 0722 873914, email heltzdrivingschool@gmail.com, or reach us on Facebook, Twitter/X, Instagram and TikTok.",
    },
  ],

  /* ------------------------------------------------------------
     HOW IT WORKS / STUDENT JOURNEY
  ------------------------------------------------------------ */
  journey: [
    { title: "Register", text: "Fill in the registration form or visit any branch with your national ID to enrol in a class." },
    { title: "Pick A Branch", text: "Choose the Heltz branch nearest you from our 13 Nairobi locations." },
    { title: "Learn & Practice", text: "Attend theoretical and practical lessons for your chosen class — one class at a time, per NTSA rules." },
    { title: "Test & Get Licensed", text: "Sit your assessment and driving test, then receive your certificate of competency." },
  ],
};

// Expose globally for the render scripts
window.HELTZ_DATA = HELTZ_DATA;
