#!/usr/bin/env python3
"""One-time, structure-preserving Aura localization transform for the static template."""

from __future__ import annotations

from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = Path(
    "/Users/rlosener/Downloads/"
    "piller-real-estate-html-template-2026-08-07-06-59-30-utc/download-version"
)
LOGO_ROOT = Path("/Users/rlosener/Desktop/Aura Logo/SVG")

TRANSLATABLE_ATTRIBUTES = ("alt", "placeholder", "aria-label", "title")

PAGE_TITLES = {
    "index.html": "Ana Sayfa",
    "home-2.html": "Kuzey Kıbrıs Yatırım Projeleri",
    "home-3.html": "Haritalı Kuzey Kıbrıs İlanları",
    "home-4.html": "Premium Kuzey Kıbrıs Konutları",
    "home-5.html": "Seçili Kuzey Kıbrıs Projesi",
    "home-6.html": "Aura In Cyprus Hakkında",
    "home-7.html": "Yerel Yatırım Danışmanlığı",
    "home-8.html": "Bölgesel Kuzey Kıbrıs Portföyü",
    "home-9.html": "Yeni Nesil Kuzey Kıbrıs Konutları",
    "home-10.html": "Modern Kuzey Kıbrıs Yaşamı",
    "about.html": "Hakkımızda",
    "property.html": "Kuzey Kıbrıs Gayrimenkul İlanları",
    "property-details.html": "Gayrimenkul Detayı",
    "agency.html": "Proje Geliştiricileri",
    "agency-details.html": "Proje Geliştiricisi Detayı",
    "service.html": "Yatırım Danışmanlığı Hizmetleri",
    "service-right-sidebar.html": "Danışmanlık Hizmetleri",
    "service-details.html": "Danışmanlık Hizmeti Detayı",
    "team.html": "Yatırım Uzmanlarımız",
    "team-details.html": "Yatırım Uzmanı Profili",
    "gallery.html": "Kuzey Kıbrıs Portföy Galerisi",
    "pricing.html": "Danışmanlık Hizmet Paketleri",
    "neighborhood-guide.html": "Kuzey Kıbrıs Bölge Rehberi",
    "faq.html": "Sık Sorulan Sorular",
    "blog.html": "Kuzey Kıbrıs Yatırım Rehberi",
    "blog-grid-left-sidebar.html": "Kuzey Kıbrıs Yatırım Rehberi",
    "blog-grid-right-sidebar.html": "Kuzey Kıbrıs Yatırım Rehberi",
    "blog-details.html": "Yatırım Rehberi Detayı",
    "contact.html": "İletişim",
    "wishlist.html": "Favori Gayrimenkuller",
    "cart.html": "Gayrimenkul Karşılaştırma Listesi",
    "checkout.html": "Danışmanlık Talebi",
    "shop.html": "Kuzey Kıbrıs Yatırım Projeleri",
    "shop-details.html": "Yatırım Projesi Detayı",
    "typography.html": "Aura Tasarım Sistemi",
    "error.html": "Sayfa Bulunamadı",
}

MANUAL_TEXT = {
    "Home": "Ana Sayfa",
    "Home Real Estate": "Kuzey Kıbrıs Gayrimenkul",
    "Home Property": "Yatırım Projeleri",
    "Home Map": "Haritalı İlanlar",
    "Home Luxury": "Premium Konutlar",
    "Home Single Property": "Seçili Proje",
    "Home Single Property(v2)": "Seçili Proje Alternatifi",
    "Real Estate Company": "Aura In Cyprus",
    "Real Estate Agency": "Yatırım Danışmanlığı",
    "Real Estate Local Agency": "Yerel Danışmanlık",
    "Modern House Agency": "Modern Yaşam Portföyü",
    "Single Property": "Seçili Proje",
    "View Demo": "Sayfayı İncele",
    "About Us": "Hakkımızda",
    "Property": "Gayrimenkul",
    "Properties": "Gayrimenkuller",
    "Properties Details": "Gayrimenkul Detayı",
    "Property Details": "Gayrimenkul Detayı",
    "Agencies": "Proje Geliştiricileri",
    "Agency Details": "Geliştirici Detayı",
    "Pages": "Kurumsal",
    "Shop": "Yatırım Projeleri",
    "Shop Details": "Proje Detayı",
    "Cart Page": "Karşılaştırma Listesi",
    "Cart": "Karşılaştırma",
    "Checkout": "Danışmanlık Talebi",
    "Wishlist": "Favori İlanlar",
    "Agents Page": "Yatırım Uzmanları",
    "Agent Details": "Uzman Profili",
    "Gallery Page": "Portföy Galerisi",
    "Service Page": "Hizmetler",
    "Service with sidebar": "Danışmanlık Hizmetleri",
    "Service Details": "Hizmet Detayı",
    "Pricing Plan": "Hizmet Paketleri",
    "Neighborhood Guide": "Bölge Rehberi",
    "Faq Page": "Sık Sorulan Sorular",
    "Error Page": "Sayfa Bulunamadı",
    "Blog": "Yatırım Rehberi",
    "Blog Grid": "Yatırım Yazıları",
    "Blog Grid With Right Sidebar": "Yatırım Yazıları",
    "Blog Grid With Left Sidebar": "Yatırım Yazıları",
    "Blog Details": "Yatırım Rehberi Detayı",
    "Contact Us": "İletişim",
    "Color Switcher": "Aura Renk Sistemi",
    "Check template with your color": "Aura marka tonlarını inceleyin",
    "Or custom color..": "Özel bir ton seçin",
    "English": "Türkçe",
    "Spanish": "Türkçe",
    "Hindi": "Türkçe",
    "What are you looking for?": "Kuzey Kıbrıs'ta nasıl bir gayrimenkul arıyorsunuz?",
    "Search": "Ara",
    "Cancel Preloader": "Yüklemeyi Geç",
    "Recent Posts": "Son Yazılar",
    "Newsletter": "Yatırım Bülteni",
    "Featured Houses": "Öne Çıkan Gayrimenkuller",
    "Quick Links": "Hızlı Bağlantılar",
    "Support": "Danışmanlık",
    "Pillar Location": "Aura In Cyprus",
    "Piller Location": "Aura In Cyprus",
    "Shopping cart": "Favori İlanlar",
    "View cart": "Favorileri Gör",
    "Subtotal:": "Toplam portföy değeri:",
    "Read More": "Devamını Oku",
    "View More": "Detayları Gör",
    "Load More": "Daha Fazla Göster",
    "For Sale": "Satılık",
    "For Rent": "Kiralık",
    "Add To Favorite": "Favorilere Ekle",
    "View all img": "Tüm Görseller",
    "Location": "Konum",
    "Bedrooms": "Yatak Odası",
    "Bathrooms": "Banyo",
    "Area": "Alan",
    "Garage": "Otopark",
    "Property Type": "Gayrimenkul Türü",
    "City": "Bölge",
    "All Cities": "Tüm Bölgeler",
    "All Properties": "Tüm Gayrimenkuller",
    "Apartment": "Daire",
    "Villa": "Villa",
    "Commercial": "Ticari",
    "Copyright": "Telif Hakkı",
    ". All Rights Reserved.": ". Tüm hakları saklıdır.",
    "Social Media:": "Sosyal Medya:",
    "Submit": "Gönder",
    "Send Message": "Mesaj Gönder",
    "Subscribe Now": "Bültene Katıl",
    "Enter Email": "E-posta adresiniz",
    "Email Address": "E-posta Adresi",
    "Phone Number": "Telefon Numarası",
    "Your Name": "Adınız Soyadınız",
    "Message": "Mesajınız",
    "Previous": "Önceki",
    "Next": "Sonraki",
    "All": "Tümü",
    "Strategy Services": "Danışmanlık Hizmetleri",
    "Explore Properties": "Gayrimenkulleri Keşfet",
    "Explore Property": "Gayrimenkulü İncele",
    "Explore All Property": "Tüm Gayrimenkulleri Keşfet",
    "View All Service": "Tüm Hizmetleri Gör",
    "View All Services": "Tüm Hizmetleri Gör",
    "View All Amenities": "Tüm Olanakları Gör",
    "View All Reviews": "Tüm Değerlendirmeleri Gör",
    "Browse All Now": "Tümünü Şimdi İncele",
    "Browse Now": "Şimdi İncele",
    "Explore Benefits": "Avantajları Keşfet",
    "Contact With Agent": "Danışmanlık Talebi Oluştur",
    "Finding the Right Home or Buyer": "Doğru gayrimenkul veya alıcı eşleştirmesi",
    "Financing and Mortgage Assistance": "Finansman seçeneklerinin değerlendirilmesi",
    "Prevents overpricing and underpricing, maintaining property values.": "Bölgesel verilerle gerçekçi fiyat değerlendirmesi sunar.",
    "Helps maintain neighborhood stability and property values..": "Konum, proje ve kullanım amacını birlikte değerlendirir.",
    "Features & amenities": "Özellikler ve Olanaklar",
    "Back To Home": "Ana Sayfaya Dön",
    "Easty To Rent": "Kiralama Danışmanlığı",
    "Default Sorting": "Önerilen Sıralama",
    "Sort by popularity": "İlgiye Göre Sırala",
    "Sort by average rating": "Değerlendirmeye Göre Sırala",
    "Sort by latest": "En Yeniye Göre Sırala",
    "Sort by price: low to high": "Fiyat: Düşükten Yükseğe",
    "Sort by price: high to low": "Fiyat: Yüksekten Düşüğe",
    "Apartment for rent": "Kiralık Daire",
    "Modern Business & Innovation Center": "Karma Kullanımlı Yatırım Projesi",
    "Luxury Living Apartment Complex": "Premium Konut Projesi",
    "Premium Grade-A Office Building": "Nitelikli Ticari Gayrimenkul",
    "Eden Estate Residential Community": "Planlı Konut Yerleşimi",
    "Bringing Vision Strategy & Innovation to the Real Estate Industry": "Kuzey Kıbrıs Gayrimenkulünde Yerel Bilgi ve Stratejik Bakış",
    "customer rating": "kullanıcı değerlendirmesi",
    "customer reviews)": "kullanıcı değerlendirmesi)",
    "I have read and agree to the terms & conditions": "Şartları ve koşulları okudum, kabul ediyorum",
    "Piller": "Aura In Cyprus",
    "Pillar": "Aura In Cyprus",
}

MANUAL_ATTRIBUTES = {
    "Piller-html": "Aura In Cyprus",
    "Piller html": "Aura In Cyprus",
    "Home Image": "Kuzey Kıbrıs gayrimenkul görseli",
    "Home One": "Kuzey Kıbrıs gayrimenkul ana sayfası",
    "Home Two": "Kuzey Kıbrıs yatırım projeleri sayfası",
    "Home Three": "Haritalı gayrimenkul sayfası",
    "Home Four": "Premium konutlar sayfası",
    "Home Five": "Seçili proje sayfası",
    "Home Six": "Aura In Cyprus kurumsal sayfası",
    "Home Seven": "Yerel danışmanlık sayfası",
    "Home Eight": "Bölgesel portföy sayfası",
    "Home Nine": "Yeni nesil konutlar sayfası",
    "Home Ten": "Modern yaşam portföyü sayfası",
    "Property Image": "Kuzey Kıbrıs gayrimenkul görseli",
    "Cart Image": "Favori gayrimenkul görseli",
    "Gallery-Image": "Kuzey Kıbrıs portföy galerisi",
    "Enter Keyword": "Arama kelimesi girin",
    "Search Here": "Burada arayın",
    "Your name*": "Adınız soyadınız*",
    "Your email*": "E-posta adresiniz*",
    "Your Message *": "Mesajınız*",
    "What are you looking for?": "Kuzey Kıbrıs'ta nasıl bir gayrimenkul arıyorsunuz?",
    "Comment*": "Yorumunuz*",
    "Email": "E-posta",
}


def normalize(value: str) -> str:
    return " ".join(value.split())


def index_from_pos(text: str, line: int, offset: int) -> int:
    starts = [0]
    for match in re.finditer("\n", text):
        starts.append(match.end())
    return starts[line - 1] + offset


class StructureParser(HTMLParser):
    def __init__(self, source: str) -> None:
        super().__init__(convert_charrefs=False)
        self.source = source
        self.stack: list[tuple[str, str, str, str, str, str]] = []
        self.data_by_key: dict[tuple, list[dict]] = defaultdict(list)
        self.tags_by_key: dict[tuple, list[dict]] = defaultdict(list)
        self.line_starts = [0]
        for match in re.finditer("\n", source):
            self.line_starts.append(match.end())

    @staticmethod
    def signature(tag: str, attrs: list[tuple[str, str | None]]) -> tuple:
        values = dict(attrs)
        classes = " ".join(sorted((values.get("class") or "").split()))
        return (
            tag,
            values.get("id") or "",
            classes,
            values.get("href") or "",
            values.get("name") or "",
            values.get("type") or "",
        )

    def absolute_pos(self) -> int:
        line, offset = self.getpos()
        return self.line_starts[line - 1] + offset

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        signature = self.signature(tag, attrs)
        self.stack.append(signature)
        raw = self.get_starttag_text() or ""
        start = self.absolute_pos()
        self.tags_by_key[tuple(self.stack)].append(
            {"raw": raw, "start": start, "end": start + len(raw), "attrs": dict(attrs)}
        )

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        signature = self.signature(tag, attrs)
        key = tuple(self.stack + [signature])
        raw = self.get_starttag_text() or ""
        start = self.absolute_pos()
        self.tags_by_key[key].append(
            {"raw": raw, "start": start, "end": start + len(raw), "attrs": dict(attrs)}
        )

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                self.stack = self.stack[:index]
                return

    def handle_data(self, data: str) -> None:
        if not self.stack or self.stack[-1][0] in {"script", "style"} or not data.strip():
            return
        start = self.absolute_pos()
        self.data_by_key[tuple(self.stack)].append(
            {"raw": data, "start": start, "end": start + len(data)}
        )


def parsed(path: Path) -> StructureParser:
    source = path.read_text(encoding="utf-8", errors="ignore")
    parser = StructureParser(source)
    parser.feed(source)
    return parser


def build_global_maps(files: list[Path]) -> tuple[dict[str, str], dict[str, str]]:
    text_votes: dict[str, Counter] = defaultdict(Counter)
    attribute_votes: dict[str, Counter] = defaultdict(Counter)

    for path in files:
        reference_path = REFERENCE / path.name
        if not reference_path.exists():
            continue
        current = parsed(path)
        previous = parsed(reference_path)

        for key, current_nodes in current.data_by_key.items():
            previous_nodes = previous.data_by_key.get(key, [])
            if len(current_nodes) != len(previous_nodes):
                continue
            for source_node, target_node in zip(current_nodes, previous_nodes):
                source_value = normalize(source_node["raw"])
                target_value = normalize(target_node["raw"])
                if len(source_value) > 1 and source_value != target_value:
                    text_votes[source_value][target_value] += 1

        for key, current_tags in current.tags_by_key.items():
            previous_tags = previous.tags_by_key.get(key, [])
            if len(current_tags) != len(previous_tags):
                continue
            for source_tag, target_tag in zip(current_tags, previous_tags):
                for attribute in TRANSLATABLE_ATTRIBUTES:
                    source_value = source_tag["attrs"].get(attribute)
                    target_value = target_tag["attrs"].get(attribute)
                    if source_value and target_value and source_value != target_value:
                        attribute_votes[source_value][target_value] += 1

    text_map = {}
    for source, votes in text_votes.items():
        target, count = votes.most_common(1)[0]
        if count / sum(votes.values()) >= 0.75:
            text_map[source] = target
    text_map.update(MANUAL_TEXT)

    attribute_map = {}
    for source, votes in attribute_votes.items():
        target, count = votes.most_common(1)[0]
        if count / sum(votes.values()) >= 0.75:
            attribute_map[source] = target
    attribute_map.update(MANUAL_ATTRIBUTES)
    return text_map, attribute_map


def replace_text_nodes(source: str, text_map: dict[str, str]) -> str:
    parts = re.split(r"(<[^>]+>)", source)
    in_script = False
    in_style = False
    for index, part in enumerate(parts):
        if part.startswith("<"):
            lowered = part.lower()
            if lowered.startswith("<script"):
                in_script = True
            elif lowered.startswith("</script"):
                in_script = False
            elif lowered.startswith("<style"):
                in_style = True
            elif lowered.startswith("</style"):
                in_style = False
            continue
        if in_script or in_style or not part.strip():
            continue
        normalized = normalize(part)
        replacement = text_map.get(normalized)
        if replacement is None:
            continue
        leading = part[: len(part) - len(part.lstrip())]
        trailing = part[len(part.rstrip()) :]
        parts[index] = f"{leading}{replacement}{trailing}"
    return "".join(parts)


def replace_attributes(source: str, attribute_map: dict[str, str]) -> str:
    attr_pattern = re.compile(
        r"\b(alt|placeholder|aria-label|title|value)=(?P<quote>['\"])(?P<value>.*?)(?P=quote)",
        re.IGNORECASE,
    )

    def replace(match: re.Match) -> str:
        value = match.group("value")
        replacement = attribute_map.get(value)
        if replacement is None:
            return match.group(0)
        quote = match.group("quote")
        replacement = replacement.replace(quote, "&quot;" if quote == '"' else "&#39;")
        return f"{match.group(1)}={quote}{replacement}{quote}"

    return attr_pattern.sub(replace, source)


def apply_brand_metadata(source: str, filename: str) -> str:
    page_title = PAGE_TITLES.get(filename, "Kuzey Kıbrıs Gayrimenkul")
    full_title = f"{page_title} | Aura In Cyprus"
    description = (
        f"{page_title}: Kuzey Kıbrıs'ta doğru gayrimenkulü seçmeniz için "
        "yerel portföy, bölge bilgisi ve yatırım danışmanlığı."
    )
    keywords = (
        "Kuzey Kıbrıs gayrimenkul, KKTC emlak, Kuzey Kıbrıs yatırım, "
        "Girne satılık daire, İskele yatırım, Aura In Cyprus"
    )

    source = re.sub(r'lang="[^"]*"', 'lang="tr"', source, count=1)
    source = re.sub(r"<title>.*?</title>", f"<title>{full_title}</title>", source, count=1, flags=re.S)
    source = re.sub(
        r'<meta name="author" content="[^"]*">',
        '<meta name="author" content="Aura In Cyprus">',
        source,
        count=1,
    )
    source = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{description}">',
        source,
        count=1,
    )
    source = re.sub(
        r'<meta name="keywords" content="[^"]*">',
        f'<meta name="keywords" content="{keywords}">',
        source,
        count=1,
    )
    source = re.sub(
        r'<meta name="theme-color" content="[^"]*">',
        '<meta name="theme-color" content="#2b485b">',
        source,
        count=1,
    )
    if 'rel="icon" type="image/svg+xml"' not in source:
        source = source.replace(
            '<meta name="robots" content="INDEX,FOLLOW">',
            '<meta name="robots" content="INDEX,FOLLOW">\n'
            '    <link rel="icon" type="image/svg+xml" href="assets/img/aura-logo.svg">',
            1,
        )
    if 'assets/css/aura-theme.css' not in source:
        source = source.replace(
            '<link rel="stylesheet" href="assets/css/style.css">',
            '<link rel="stylesheet" href="assets/css/style.css">\n'
            '    <link rel="stylesheet" href="assets/css/aura-theme.css">',
            1,
        )
    def body_class(match: re.Match) -> str:
        classes = match.group(1).strip().split()
        if "aura-site" not in classes:
            classes.append("aura-site")
        classes = " ".join(classes)
        return f'<body class="{classes}">'

    source = re.sub(r'<body class="([^"]*)">', body_class, source, count=1)
    return source


def apply_business_context(source: str) -> str:
    source = source.replace("Piller-html", "Aura In Cyprus")
    source = source.replace("Pillar-html", "Aura In Cyprus")
    source = re.sub(r"\bPiller\b", "Aura In Cyprus", source, flags=re.I)
    source = re.sub(r"\bPillar\b", "Aura In Cyprus", source, flags=re.I)
    source = source.replace("$", "£")
    source = source.replace("sqft", "m²").replace("Sqft", "m²").replace("ft²", "m²")
    source = source.replace("assets/img/icon/m².svg", "assets/img/icon/sqft.svg")
    source = source.replace("assets/img/icon/m²2.svg", "assets/img/icon/sqft2.svg")
    source = source.replace("New York", "Kuzey Kıbrıs")
    source = source.replace("United States", "Kuzey Kıbrıs")
    source = source.replace("Bangladesh", "Kuzey Kıbrıs")
    source = source.replace("Dhaka", "Lefkoşa")
    source = source.replace("info@piller.com", "İletişim formu")
    source = source.replace("infomailexample@mail.com", "contact.html")
    source = source.replace("mailto:contact.html", "contact.html")
    source = re.sub(r'href="tel:[^"]+"', 'href="contact.html"', source)
    source = re.sub(
        r'<a href="mailto:(?!\?)[^"]+"([^>]*)>[^<]*</a>',
        r'<a href="contact.html"\1>İletişim formu</a>',
        source,
        flags=re.I,
    )
    source = re.sub(
        r'<a href="contact\.html"([^>]*)>\s*[+]?[0-9() -]{7,}\s*</a>',
        r'<a href="contact.html"\1>İletişim formu</a>',
        source,
        flags=re.I,
    )
    source = source.replace(">contact.html<", ">İletişim formu<")
    source = source.replace(
        "123 Academic Way City, State, 1234, Kuzey Kıbrıs City.",
        "Kuzey Kıbrıs genelinde yerel gayrimenkul danışmanlığı",
    )
    source = re.sub(
        r'href="https://www\.(facebook|twitter|linkedin|whatsapp)\.com/?"',
        'href="contact.html" aria-label="Sosyal medya bilgileri için iletişime geçin"',
        source,
    )
    source = re.sub(r'action="/submit-form"', 'action="property.html" method="get"', source)
    source = re.sub(r'action="#"([^>]*)class="search-form"', r'action="property.html" method="get"\1class="search-form"', source)
    source = source.replace('<form class="search-form">', '<form action="property.html" method="get" class="search-form">')
    source = source.replace('<form class="newsletter-form">', '<form action="contact.html" method="get" class="newsletter-form">')
    source = source.replace('<form action="#" class="newsletter-form">', '<form action="contact.html" method="get" class="newsletter-form">')
    source = re.sub(
        r'(<div class="popup-search-box[^>]*>.*?<form) action="#"',
        r'\1 action="property.html" method="get"',
        source,
        count=1,
        flags=re.S,
    )
    source = re.sub(
        r'(<div class="popup-search-box[^>]*>.*?<input type="text")(?![^>]*\bname=)',
        r'\1 name="q"',
        source,
        count=1,
        flags=re.S,
    )
    source = re.sub(
        r'<a class="th-btn radius w-100"><i class="fa-regular fa-magnifying-glass me-2"></i>\s*İlan Ara\s*</a>',
        '<button type="submit" class="th-btn radius w-100"><i class="fa-regular fa-magnifying-glass me-2"></i> İlan Ara</button>',
        source,
    )
    source = re.sub(r'<option selected="">English</option>', '<option selected="">Türkçe</option>', source)
    source = source.replace('data-color="#6240CF"', 'data-color="#2b485b"')
    source = source.replace('data-color="#068FFF"', 'data-color="#60a6b7"')
    source = source.replace('data-color="#044DBC"', 'data-color="#3c6d7e"')
    source = source.replace('data-color="#FFAF00"', 'data-color="#8bc4d0"')
    source = source.replace('data-color="#F80000"', 'data-color="#234051"')
    source = source.replace('data-color="#231E7A"', 'data-color="#75b6c4"')
    source = source.replace('id="thcolorpicker" value="#068FFF"', 'id="thcolorpicker" value="#60a6b7"')
    source = source.replace('href="/property-details"', 'href="property-details.html"')
    source = source.replace('href="testimonials.html"', 'href="about.html#testimonials"')
    source = source.replace('href="about.html text-anime-style-2"', 'href="contact.html"')

    preloader = (
        '<div class="txt-loading" role="status" aria-label="Aura In Cyprus yükleniyor">\n'
        '                <span data-text-preloader="A" class="letters-loading">A</span>\n'
        '                <span data-text-preloader="U" class="letters-loading">U</span>\n'
        '                <span data-text-preloader="R" class="letters-loading">R</span>\n'
        '                <span data-text-preloader="A" class="letters-loading">A</span>\n'
        '            </div>'
    )
    source = re.sub(r'<div class="txt-loading">.*?</div>', preloader, source, count=1, flags=re.S)
    return source


def copy_brand_assets() -> None:
    assets = ROOT / "assets" / "img"
    pairs = {
        "AURA-02.svg": ("aura-logo.svg", "logo.svg"),
        "AURA-03.svg": ("aura-logo-on-dark.svg", "logo-white.svg"),
        "AURA-04.svg": ("aura-logo-white.svg",),
    }
    for source_name, targets in pairs.items():
        source = LOGO_ROOT / source_name
        if not source.exists():
            raise FileNotFoundError(source)
        for target_name in targets:
            shutil.copyfile(source, assets / target_name)


def main() -> None:
    if not REFERENCE.exists():
        raise FileNotFoundError(f"Translation reference not found: {REFERENCE}")
    files = sorted(ROOT.glob("*.html"))
    text_map, attribute_map = build_global_maps(files)
    copy_brand_assets()

    for path in files:
        source = path.read_text(encoding="utf-8", errors="ignore")
        source = replace_text_nodes(source, text_map)
        source = replace_attributes(source, attribute_map)
        source = apply_brand_metadata(source, path.name)
        source = apply_business_context(source)
        path.write_text(source, encoding="utf-8")

    print(
        f"Aura transform complete: {len(files)} HTML pages, "
        f"{len(text_map)} text mappings, {len(attribute_map)} attribute mappings."
    )


if __name__ == "__main__":
    main()
