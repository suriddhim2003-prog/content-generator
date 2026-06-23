"""
Social Media Content Generator — AI-powered caption & post generator.
Demo project #2 for AI automation freelancing.
"""

import json
import os
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

PLATFORMS = {
    "instagram": {"name": "Instagram", "icon": "📸", "max_chars": 2200, "hashtags": True, "emoji_heavy": True},
    "twitter": {"name": "Twitter / X", "icon": "🐦", "max_chars": 280, "hashtags": True, "emoji_heavy": False},
    "linkedin": {"name": "LinkedIn", "icon": "💼", "max_chars": 3000, "hashtags": True, "emoji_heavy": False},
    "whatsapp": {"name": "WhatsApp Status", "icon": "💬", "max_chars": 700, "hashtags": False, "emoji_heavy": True},
}

TONES = ["Professional", "Casual & Fun", "Inspirational", "Urgent/FOMO", "Storytelling"]

TEMPLATES = {
    "instagram": {
        "Professional": [
            "Introducing {product} — designed for those who demand quality.\n\n{benefit}\n\nAvailable now. Link in bio.\n\n{hashtags}",
            "What sets {product} apart?\n\n✅ {feature1}\n✅ {feature2}\n✅ {feature3}\n\nExperience the difference. DM us to know more.\n\n{hashtags}",
            "Your search for {category} ends here.\n\n{product} delivers {benefit}.\n\nTap the link in bio to get started.\n\n{hashtags}",
        ],
        "Casual & Fun": [
            "POV: You just discovered {product} and your life changed 😍\n\n{benefit}\n\nWho else needs this? Tag them! 👇\n\n{hashtags}",
            "Not gonna lie… {product} hits different 🔥\n\n{benefit}\n\nGrab yours before everyone else does!\n\n{hashtags}",
            "Tell me you love {category} without telling me you love {category} 😏\n\nUs: *shows {product}*\n\n{hashtags}",
        ],
        "Inspirational": [
            "Every great journey starts with one step.\n\nOurs started with {product}.\n\n{benefit}\n\nWhat's your next step? 🌟\n\n{hashtags}",
            "Dream big. Start small. But start NOW.\n\n{product} was built for dreamers who do.\n\n{benefit}\n\n{hashtags}",
            "They said it couldn't be done. We built {product} anyway.\n\n{benefit}\n\nYour turn. 💪\n\n{hashtags}",
        ],
        "Urgent/FOMO": [
            "⚡ FLASH DROP ⚡\n\n{product} is HERE — but not for long.\n\n{benefit}\n\n🔗 Link in bio. Don't sleep on this.\n\n{hashtags}",
            "🚨 Only a few left!\n\n{product} is selling FAST.\n\n{benefit}\n\nGrab yours NOW before it's gone → Link in bio\n\n{hashtags}",
            "48 HOURS ONLY 🕐\n\n{product} at a price you won't believe.\n\n{benefit}\n\nDon't miss out. Link in bio!\n\n{hashtags}",
        ],
        "Storytelling": [
            "6 months ago, we had an idea.\n\nWhat if {category} could be {benefit}?\n\nToday, {product} is that idea — alive.\n\nSwipe to see the journey →\n\n{hashtags}",
            "The story behind {product}:\n\nIt started with a problem — {category} was broken.\nSo we fixed it.\n\n{benefit}\n\nThis is just the beginning.\n\n{hashtags}",
            "\"Why did you create {product}?\"\n\nBecause {category} deserved better.\nBecause {benefit}.\nBecause you asked for it.\n\nHere it is. 🙌\n\n{hashtags}",
        ],
    },
    "twitter": {
        "Professional": [
            "Introducing {product} — {benefit}.\n\nLearn more 👇\n{hashtags}",
            "{product} is here.\n\n{feature1}. {feature2}. {feature3}.\n\nThe future of {category}.\n{hashtags}",
            "Why {product}?\n\nBecause {benefit}.\n\nSimple as that.\n{hashtags}",
        ],
        "Casual & Fun": [
            "{product} just dropped and honestly? It's a vibe 🔥\n\n{benefit}\n{hashtags}",
            "Me before {product}: 😐\nMe after {product}: 😎\n\n{hashtags}",
            "hot take: {product} is the best thing to happen to {category} this year\n\n{hashtags}",
        ],
        "Inspirational": [
            "Build something people love.\n\nThat's why we made {product}.\n\n{benefit} ✨\n{hashtags}",
            "The best time to start was yesterday. The next best time? Right now.\n\n{product} — {benefit}.\n{hashtags}",
            "Small steps, big dreams.\n\n{product} is our step. What's yours?\n{hashtags}",
        ],
        "Urgent/FOMO": [
            "🚨 {product} is LIVE.\n\nFirst 50 customers get early access.\n\n{benefit}\n\nDon't wait.\n{hashtags}",
            "This won't last ⏰\n\n{product} — {benefit}.\n\nAct now.\n{hashtags}",
            "Last chance to grab {product} at launch price.\n\n{benefit}\n\nGoing, going… 🔥\n{hashtags}",
        ],
        "Storytelling": [
            "We spent 6 months on {product}.\n\nWhy? Because {category} needed {benefit}.\n\nThread 🧵👇\n{hashtags}",
            "The problem: {category} was stuck.\nThe solution: {product}.\nThe result: {benefit}.\n\n{hashtags}",
            "1/ How we built {product}:\n\nIt started with a question — what if {benefit}?\n\n{hashtags}",
        ],
    },
    "linkedin": {
        "Professional": [
            "Excited to announce the launch of {product}.\n\n{benefit}\n\nIn a market full of {category} options, we focused on what matters most — delivering real value.\n\nKey highlights:\n→ {feature1}\n→ {feature2}\n→ {feature3}\n\nWould love to hear your thoughts.\n\n{hashtags}",
            "The {category} landscape is evolving.\n\n{product} represents our answer to the changing needs of modern businesses.\n\n{benefit}\n\nLet's connect if you're working in this space.\n\n{hashtags}",
            "After months of development, {product} is ready.\n\nOur mission: {benefit}\n\nKey differentiators:\n• {feature1}\n• {feature2}\n• {feature3}\n\nOpen to feedback and conversations.\n\n{hashtags}",
        ],
        "Casual & Fun": [
            "So… we built a thing. 😄\n\nIt's called {product}, and it's our take on making {category} actually enjoyable.\n\n{benefit}\n\nCheck it out and let me know what you think!\n\n{hashtags}",
            "Monday motivation: Launch the thing.\n\n{product} is live! 🚀\n\n{benefit}\n\nGrateful for the journey. Excited for what's next.\n\n{hashtags}",
            "Not every launch needs a TED talk.\n\nSo here's the short version:\n\n{product} → {benefit}\n\nThat's it. That's the post.\n\n{hashtags}",
        ],
        "Inspirational": [
            "Every innovation starts with frustration.\n\nWe were frustrated with {category}. So we built {product}.\n\n{benefit}\n\nIf you're building something too — keep going. The world needs what you're creating.\n\n{hashtags}",
            "\"The best way to predict the future is to create it.\"\n\n{product} is our contribution to the future of {category}.\n\n{benefit}\n\nWhat are you creating?\n\n{hashtags}",
            "3 things I learned building {product}:\n\n1. {category} has more room for innovation than people think\n2. {benefit} matters more than features\n3. Showing up consistently beats perfection\n\nWhat's your biggest lesson from building?\n\n{hashtags}",
        ],
        "Urgent/FOMO": [
            "🔔 Big announcement:\n\n{product} is officially live — and our early-bird pricing ends this week.\n\n{benefit}\n\nIf you're in {category}, this is worth a look.\n\nLink in comments 👇\n\n{hashtags}",
            "We're opening up {product} to the first 100 users.\n\n{benefit}\n\nIf {category} is part of your work, DM me for early access.\n\n{hashtags}",
            "Time-sensitive: {product} launch pricing ends Friday.\n\n{benefit}\n\nWe built this for professionals in {category} who want results, not complexity.\n\nDetails in comments.\n\n{hashtags}",
        ],
        "Storytelling": [
            "1 year ago, I had a conversation that changed everything.\n\nA colleague asked: \"Why is {category} still so painful?\"\n\nI didn't have a good answer. So I built one.\n\n{product} — {benefit}.\n\nThe journey from idea to launch taught me more than any MBA could.\n\nHere's what I'd tell my past self:\n→ Start before you're ready\n→ Talk to users, not investors\n→ Ship fast, improve faster\n\n{hashtags}",
            "From napkin sketch to launch day.\n\nThe {product} story:\n\nProblem: {category} needed {benefit}\nSolution: We built it\nResult: Better than we imagined\n\nGrateful for every person who believed in this vision.\n\n{hashtags}",
            "Behind every product is a team that refused to give up.\n\n{product} took longer than planned. Cost more than budgeted. Required more patience than expected.\n\nBut today, it's live. And it delivers {benefit}.\n\nTo every founder in the trenches — keep building.\n\n{hashtags}",
        ],
    },
    "whatsapp": {
        "Professional": [
            "🔔 New Launch!\n\n*{product}*\n\n{benefit}\n\nReply to know more or visit our website.",
            "Hi! 👋\n\nCheck out *{product}* — {benefit}.\n\nFor orders/inquiries, reply here.",
            "📢 *{product}* is now available!\n\n{benefit}\n\nMessage us for pricing & details.",
        ],
        "Casual & Fun": [
            "Guess what's NEW! 🎉\n\n*{product}*\n\n{benefit}\n\nReply 'YES' if you want details! 😊",
            "Hey! 👋 Something exciting just dropped!\n\n*{product}* — {benefit}\n\nForward this to someone who needs it! 💫",
            "🔥 *{product}* is HERE!\n\n{benefit}\n\nDon't miss out — reply to grab yours!",
        ],
        "Inspirational": [
            "✨ New beginnings start with better choices.\n\n*{product}* — {benefit}\n\nTake the first step today. Reply to know more.",
            "💡 What if {category} could be simpler?\n\n*{product}* makes it happen.\n\n{benefit}\n\nMessage us to learn more.",
            "🌟 *{product}*\n\n{benefit}\n\nBecause you deserve the best in {category}.\n\nReply for details!",
        ],
        "Urgent/FOMO": [
            "⚡ LIMITED OFFER ⚡\n\n*{product}*\n\n{benefit}\n\n⏰ Offer valid till tonight only!\n\nReply NOW to order!",
            "🚨 *{product}* — Almost SOLD OUT!\n\n{benefit}\n\nDon't wait — reply to book yours!",
            "🔥 LAST CHANCE!\n\n*{product}* at special price!\n\n{benefit}\n\nReply 'ORDER' before it's gone!",
        ],
        "Storytelling": [
            "You know what's funny?\n\nWe created *{product}* because WE needed it first.\n\n{benefit}\n\nNow it's yours too. Reply to check it out! 😊",
            "A small idea became something big.\n\n*{product}* — {benefit}\n\nOur journey started with {category}. Where will yours start?\n\nReply to know more.",
            "Every product has a story.\n\n*{product}* was born from a simple wish: {benefit}.\n\nWant to be part of the story? Reply! ✨",
        ],
    },
}


def extract_details(product: str, description: str):
    words = (product + " " + description).lower().split()

    categories = {
        "food": ["food", "restaurant", "cafe", "snack", "meal", "cook", "kitchen", "recipe", "biryani", "cake", "sweet", "chocolate"],
        "fashion": ["fashion", "clothing", "wear", "dress", "shirt", "shoe", "style", "boutique", "designer", "saree", "kurta", "jeans"],
        "beauty": ["beauty", "skin", "hair", "salon", "cosmetic", "cream", "serum", "glow", "makeup", "facial", "parlour"],
        "tech": ["tech", "app", "software", "digital", "phone", "laptop", "gadget", "device", "smart", "ai", "automation", "saas"],
        "fitness": ["fitness", "gym", "health", "workout", "yoga", "protein", "supplement", "weight", "exercise", "training"],
        "education": ["education", "course", "learn", "class", "coaching", "tutor", "study", "ielts", "english", "skill", "training"],
        "home": ["home", "decor", "furniture", "interior", "kitchen", "appliance", "cleaning", "garden"],
        "business": ["business", "service", "consulting", "agency", "marketing", "freelance", "startup", "company"],
    }

    category = "business"
    for cat, keywords in categories.items():
        if any(w in words for w in keywords):
            category = cat
            break

    desc_parts = description.split(".") if description else [product]
    features = []
    for part in desc_parts[:3]:
        part = part.strip()
        if part and len(part) > 3:
            features.append(part)
    while len(features) < 3:
        features.append(f"Premium quality {category} solution")

    benefit = features[0] if features else f"The best in {category}"

    hashtag_bank = {
        "food": ["#Foodie", "#FoodLover", "#Yummy", "#HomeMade", "#FoodBusiness", "#Delicious", "#InstaFood"],
        "fashion": ["#Fashion", "#Style", "#OOTD", "#FashionBusiness", "#Trending", "#NewCollection", "#Wear"],
        "beauty": ["#Beauty", "#Skincare", "#GlowUp", "#BeautyBusiness", "#SelfCare", "#NaturalBeauty"],
        "tech": ["#Tech", "#Innovation", "#AI", "#Digital", "#StartupLife", "#SaaS", "#TechBusiness"],
        "fitness": ["#Fitness", "#Health", "#FitLife", "#GymLife", "#Wellness", "#HealthyLiving"],
        "education": ["#Education", "#Learning", "#OnlineCourse", "#SkillUp", "#EdTech", "#StudyWithMe"],
        "home": ["#HomeDecor", "#InteriorDesign", "#HomeBusiness", "#Lifestyle", "#HomeGoals"],
        "business": ["#Business", "#Entrepreneur", "#SmallBusiness", "#Growth", "#Startup", "#Success"],
    }

    tags = hashtag_bank.get(category, hashtag_bank["business"])
    selected_tags = random.sample(tags, min(5, len(tags)))
    selected_tags.append(f"#{product.replace(' ', '')}")
    hashtags = " ".join(selected_tags)

    return {
        "product": product,
        "category": category,
        "benefit": benefit,
        "feature1": features[0],
        "feature2": features[1],
        "feature3": features[2],
        "hashtags": hashtags,
    }


def generate_content(product: str, description: str, platforms: list, tones: list):
    details = extract_details(product, description)
    results = {}

    for platform in platforms:
        results[platform] = {}
        for tone in tones:
            pool = TEMPLATES.get(platform, {}).get(tone, [])
            if pool:
                template = random.choice(pool)
                post = template.format(**details)
                results[platform][tone] = {
                    "text": post,
                    "chars": len(post),
                    "max_chars": PLATFORMS[platform]["max_chars"],
                    "platform_name": PLATFORMS[platform]["name"],
                    "platform_icon": PLATFORMS[platform]["icon"],
                }

    return results


@app.route("/")
def index():
    return render_template("index.html", platforms=PLATFORMS, tones=TONES)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    product = data.get("product", "").strip()
    description = data.get("description", "").strip()
    platforms = data.get("platforms", ["instagram"])
    tones = data.get("tones", ["Casual & Fun"])

    if not product:
        return jsonify({"error": "Product name is required"}), 400

    results = generate_content(product, description, platforms, tones)
    return jsonify(results)


if __name__ == "__main__":
    print("\n  Social Media Content Generator")
    print("  Open http://localhost:5051 in your browser\n")
    app.run(host="127.0.0.1", port=5051, debug=True)
