from django.shortcuts import render


def home(request):
    rings = [
        {
            "name": "Solstice Solitaire",
            "detail": "Oval-cut moissanite · 14k gold",
            "price": "£489",
            "image": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=900&q=85",
            "alt": "Gold solitaire ring with a bright centre stone",
            "label": "Bestseller",
        },
        {
            "name": "The Heirloom",
            "detail": "Emerald-cut diamond · Platinum",
            "price": "£1,250",
            "image": "https://images.unsplash.com/photo-1603561591411-07134e71a2a9?auto=format&fit=crop&w=900&q=85",
            "alt": "Elegant engagement ring displayed close up",
            "label": "Made to order",
        },
        {
            "name": "Golden Hour Band",
            "detail": "Textured 18k recycled gold",
            "price": "£320",
            "image": "https://images.unsplash.com/photo-1603561596112-0a132b757442?auto=format&fit=crop&w=900&q=85",
            "alt": "Minimal gold ring with a polished finish",
            "label": "New",
        },
    ]
    return render(request, "rings/index.html", {"rings": rings})
