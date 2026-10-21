# Anvaya — static site (v4)

Deploy dist/ as-is on Vercel. Pages: index, about, weddings, milestones, corporate, contact.
All 28 photographs are in dist/img/ (web JPEGs). 2K originals in the separate photos zip.

## Fill in before launch (search build.py for these)
PHONE_TEL  = "+1XXXXXXXXXX"   -> the Call button
WHATSAPP   = "1XXXXXXXXXX"    -> the WhatsApp button
SITE       = canonical domain once it moves off vercel.app
[Phone] [Email] [@instagram] placeholders in footer/contact; testimonials (4).
Add img/logo-dark.webp and img/favicon.png from the old site.

## Forms
Contact form and the Book-a-conversation modal show confirmations only. Both store nothing server-side.
Wire the submit handlers in src/main.js (search "enquiry" and "bkform") to Formspree, a Vercel function,
or Calendly/Cal.com for the booking step. Then `python3 build.py` from the parent folder to rebuild.

## SEO
Each page has a keyword title, meta description, OG tags, canonical, and JSON-LD (LocalBusiness/EventPlanner,
areaServed cities, service catalog; FAQPage on weddings).
