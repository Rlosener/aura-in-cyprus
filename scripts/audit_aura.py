#!/usr/bin/env python3
"""Static acceptance checks for the Aura In Cyprus localization and brand layer."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PAGE_COUNT = 36
REQUIRED_LOGOS = (
    ROOT / "assets/img/aura-logo.svg",
    ROOT / "assets/img/aura-logo-on-dark.svg",
    ROOT / "assets/img/aura-logo-white.svg",
)
FORBIDDEN_SOURCE_PATTERNS = {
    "eski marka": re.compile(r"\b(?:Piller|Pillar)(?:-html)?\b", re.I),
    "eski dil kodu": re.compile(r'lang="zxx"', re.I),
    "demo konum": re.compile(r"New York|Bangladesh|Dhaka|Academic Way", re.I),
    "demo iletişim": re.compile(
        r"infomail|examplemail|agency\.com|gmail\.com|[+]00\s*\(|[+]\(00\)|[+]011\s*\(",
        re.I,
    ),
    "dolar fiyatı": re.compile(r"\$\s*[0-9]"),
    "kırık çevrilmiş ikon yolu": re.compile(r"assets/img/icon/m²"),
}
ENGLISH_UI = re.compile(
    r"\b(?:"
    r"What are you looking for|Single Property|Strategy Services|Explore Benefits|"
    r"Browse Now|Default Sorting|Sort by|Back To Home|View All Services?|"
    r"View All Amenities|View All Reviews|Contact With Agent|Features & amenities|"
    r"Cancel Preloader|Color Switcher|Read More|View More|Subscribe Now|"
    r"Shopping cart|Featured Houses|Quick Links|All Rights Reserved"
    r")\b",
    re.I,
)


class AssetAndTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[str] = []
        self.visible_values: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.skip_depth += 1
        values = dict(attrs)
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.references.append(value)
        if not self.skip_depth:
            for attribute in ("alt", "placeholder", "aria-label", "title"):
                value = values.get(attribute)
                if value:
                    self.visible_values.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip_depth and data.strip():
            self.visible_values.append(" ".join(data.split()))


def local_target(reference: str) -> Path | None:
    clean = reference.split("#", 1)[0].split("?", 1)[0]
    if not clean or clean.startswith(
        ("http:", "https:", "mailto:", "tel:", "javascript:", "//", "data:")
    ):
        return None
    return ROOT / clean.lstrip("/")


def main() -> int:
    errors: list[str] = []
    pages = sorted(ROOT.glob("*.html"))
    if len(pages) != EXPECTED_PAGE_COUNT:
        errors.append(f"HTML sayfa sayısı {len(pages)}; beklenen {EXPECTED_PAGE_COUNT}.")

    for logo in REQUIRED_LOGOS:
        if not logo.is_file() or logo.stat().st_size < 1000:
            errors.append(f"Aura logo varlığı eksik veya boş: {logo.relative_to(ROOT)}")

    theme = ROOT / "assets/css/aura-theme.css"
    if not theme.is_file():
        errors.append("Aura tema dosyası bulunamadı: assets/css/aura-theme.css")
    else:
        theme_source = theme.read_text(encoding="utf-8", errors="ignore")
        for color in ("#2b485b", "#60a6b7"):
            if color not in theme_source.lower():
                errors.append(f"Aura ana rengi tema dosyasında bulunamadı: {color}")
        if theme_source.count("{") != theme_source.count("}"):
            errors.append("Aura tema dosyasında CSS blok dengesi bozuk.")

    for page in pages:
        source = page.read_text(encoding="utf-8", errors="ignore")
        source_without_icon_names = re.sub(r"assets/img/icon/sqft2?\.svg", "", source, flags=re.I)
        required_fragments = (
            'lang="tr"',
            "| Aura In Cyprus</title>",
            '<meta name="author" content="Aura In Cyprus">',
            'content="#2b485b"',
            'href="assets/css/aura-theme.css"',
            "aura-site",
            'aria-label="Aura In Cyprus yükleniyor"',
        )
        for fragment in required_fragments:
            if fragment not in source:
                errors.append(f"{page.name}: zorunlu marka/dil parçası eksik: {fragment}")

        for label, pattern in FORBIDDEN_SOURCE_PATTERNS.items():
            match = pattern.search(source_without_icon_names)
            if match:
                errors.append(f"{page.name}: {label} bulundu: {match.group(0)!r}")

        parser = AssetAndTextParser()
        parser.feed(source)
        for value in parser.visible_values:
            if re.search(r"\bsqft\b|ft²", value, re.I):
                errors.append(f"{page.name}: görünür eski ölçü birimi: {value!r}")
            match = ENGLISH_UI.search(value)
            if match:
                errors.append(f"{page.name}: çevrilmemiş görünür metin: {value!r}")
        for reference in parser.references:
            target = local_target(reference)
            if target is not None and not target.exists():
                errors.append(f"{page.name}: yerel bağlantı/varlık bulunamadı: {reference}")

    mailer = (ROOT / "mail.php").read_text(encoding="utf-8", errors="ignore")
    if "AURA_CONTACT_EMAIL" not in mailer:
        errors.append("mail.php, AURA_CONTACT_EMAIL ortam değişkenini kullanmıyor.")
    if "yourmail@" in mailer.lower():
        errors.append("mail.php içinde demo alıcı e-postası kaldı.")

    if errors:
        print("Aura statik kabul denetimi başarısız:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Aura statik kabul denetimi başarılı: "
        f"{len(pages)} sayfa, Türkçe UI/metadata, marka renkleri, logolar ve yerel bağlantılar doğrulandı."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
