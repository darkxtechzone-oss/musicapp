"""
Inatengeneza icons zote za launcher (bitmap) zenye muundo mmoja:
gradient ya zambarau (inayolingana na ile ya adaptive icon iliyopo) + alama ya "X" nyeupe.
Inaandika moja kwa moja juu ya faili za zamani (mipmap-*/ic_launcher*.webp,
drawable/ic_launcher.png, ic_launcher-playstore.png).
"""

from PIL import Image, ImageDraw

BG_TOP = (90, 44, 160)      # #5A2CA0 - sawa na adaptive icon background iliyopo
BG_BOTTOM = (44, 44, 160)   # #2C2CA0

SIZES = {
    "composeApp/src/main/res/mipmap-mdpi/ic_launcher.webp": 48,
    "composeApp/src/main/res/mipmap-mdpi/ic_launcher_round.webp": 48,
    "composeApp/src/main/res/mipmap-hdpi/ic_launcher.webp": 72,
    "composeApp/src/main/res/mipmap-hdpi/ic_launcher_round.webp": 72,
    "composeApp/src/main/res/mipmap-xhdpi/ic_launcher.webp": 96,
    "composeApp/src/main/res/mipmap-xhdpi/ic_launcher_round.webp": 96,
    "composeApp/src/main/res/mipmap-xxhdpi/ic_launcher.webp": 144,
    "composeApp/src/main/res/mipmap-xxhdpi/ic_launcher_round.webp": 144,
    "composeApp/src/main/res/mipmap-xxxhdpi/ic_launcher.webp": 192,
    "composeApp/src/main/res/mipmap-xxxhdpi/ic_launcher_round.webp": 192,
}

DRAWABLE_ICON = "composeApp/src/androidMain/res/drawable/ic_launcher.png"
PLAYSTORE_ICON = "composeApp/src/androidMain/ic_launcher-playstore.png"


def make_icon(size: int, round_mask: bool = False) -> Image.Image:
    scale = 4  # antialiasing kwa kuchora kwa ubora wa juu kisha kupunguza
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background - gradient wima kutoka juu (zambarau nyepesi) mpaka chini (giza)
    for y in range(s):
        t = y / s
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t)
        draw.line([(0, y), (s, y)], fill=(r, g, b, 255))

    # Fanya pembe ziwe za mviringo (squircle) au duara kamili
    mask = Image.new("L", (s, s), 0)
    mask_draw = ImageDraw.Draw(mask)
    if round_mask:
        mask_draw.ellipse([0, 0, s, s], fill=255)
    else:
        radius = int(s * 0.22)
        mask_draw.rounded_rectangle([0, 0, s, s], radius=radius, fill=255)
    img.putalpha(mask)

    # Alama ya "X" - pau mbili zinazokatana, nyeupe
    cx, cy = s / 2, s / 2
    arm = s * 0.30       # urefu wa kila mkono kutoka katikati
    half_w = s * 0.075   # nusu-upana wa kila pau

    import math
    def bar_points(angle_deg):
        angle = math.radians(angle_deg)
        dx, dy = math.cos(angle), math.sin(angle)
        px, py = -dy, dx  # perpendicular
        p1 = (cx - dx * arm, cy - dy * arm)
        p2 = (cx + dx * arm, cy + dy * arm)
        return [
            (p1[0] + px * half_w, p1[1] + py * half_w),
            (p1[0] - px * half_w, p1[1] - py * half_w),
            (p2[0] - px * half_w, p2[1] - py * half_w),
            (p2[0] + px * half_w, p2[1] + py * half_w),
        ]

    draw.polygon(bar_points(45), fill=(255, 255, 255, 255))
    draw.polygon(bar_points(135), fill=(255, 255, 255, 255))

    return img.resize((size, size), Image.LANCZOS)


def main():
    for path, size in SIZES.items():
        is_round = "round" in path
        icon = make_icon(size, round_mask=is_round)
        icon.save(path, format="WEBP")
        print(f"  {path} ({size}x{size})")

    # Drawable flat icon (dp size, arbitrary resolution - 192 ni salama)
    make_icon(192).save(DRAWABLE_ICON, format="PNG")
    print(f"  {DRAWABLE_ICON} (192x192)")

    # Play Store / F-Droid icon - 512x512 ni kiwango cha kawaida
    make_icon(512).save(PLAYSTORE_ICON, format="PNG")
    print(f"  {PLAYSTORE_ICON} (512x512)")


if __name__ == "__main__":
    main()
