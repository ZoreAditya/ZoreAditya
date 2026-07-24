#!/usr/bin/env python3
"""
Generate an animated Neofetch-style info card SVG.
"""

import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))



W = 500
H = 440          # Increased height

PAD = 20
TITLEBAR_H = 30

KEY_X = PAD
VAL_X = PAD + 105

LINE_H = 21

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"

KEY = "#ffa657"
SECTION = "#58a6ff"
GREEN = "#3fb950"
ACCENT = "#22d3ee"

# ----------------------------------------------------
# Content
# ----------------------------------------------------

ROWS = [

    ("host",),

    ("kv", "Now", "Software Engineer @ Capgemini"),
    ("kv", "Prev", "Software Engineering Intern @ Sparks Foundation"),
    ("kv", "Edu", "B.Tech ENTC, DYPIT Pune '24"),

    ("gap",),

    ("sec", "Technical Skills"),

    ("kv", "Language", "Java 8, JavaScript"),
    ("kv", "Backend", "Spring Boot, Spring Security, MySql, Postgress Sql"),
    ("kv", "ORM", "Hibernate, JPA"),
    ("kv", "Web", "HTML, REST APIs"),
    ("kv", "Tools", "Docker, Maven, Git"),
    ("kv", "Dev", "Postman, Swagger, IntelliJ"),

    ("gap",),

    ("sec", "Achievements"),

    ("bul", "Ranked #1 among 40 associates at Capgemini"),
    ("bul", "Solved 220+ LeetCode problems"),

]

# ----------------------------------------------------


def esc(text):
    return html.escape(text)


def rise(inner, idx):
    if STATIC:
        return inner

    delay = 0.15 + idx * 0.06

    return f"""
<g opacity="0" transform="translate(0,5)">
{inner}
<animate attributeName="opacity"
         from="0"
         to="1"
         begin="{delay:.2f}s"
         dur="0.4s"
         fill="freeze"/>

<animateTransform
         attributeName="transform"
         type="translate"
         from="0 5"
         to="0 0"
         begin="{delay:.2f}s"
         dur="0.4s"
         fill="freeze"
         calcMode="spline"
         keySplines="0.2 0.8 0.2 1"/>
</g>
"""


parts = []

parts.append(f"""<svg xmlns="http://www.w3.org/2000/svg"
width="{W}"
height="{H}"
viewBox="0 0 {W} {H}"
font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">

<defs>

<linearGradient id="bg"
x1="0" y1="0"
x2="0" y2="1">

<stop offset="0" stop-color="{BG2}"/>
<stop offset="1" stop-color="{BG}"/>

</linearGradient>

</defs>

<rect
width="{W}"
height="{H}"
rx="12"
fill="url(#bg)"/>

<rect
x="0.5"
y="0.5"
width="{W-1}"
height="{H-1}"
rx="12"
fill="none"
stroke="{FRAME}"/>

<line
x1="0"
y1="{TITLEBAR_H}"
x2="{W}"
y2="{TITLEBAR_H}"
stroke="{FRAME}"/>
""")

# Mac buttons

for i, color in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    cx = 20 + i * 16
    parts.append(f'<circle cx="{cx}" cy="15" r="5" fill="{color}"/>')

parts.append(
    f'''
<text
x="{W/2}"
y="19"
fill="{MUTED}"
font-size="12"
text-anchor="middle">
aditya@github: ~$ neofetch
</text>
'''
)

# --------------------------

y = TITLEBAR_H + 30

for idx, row in enumerate(ROWS):

    kind = row[0]

    if kind == "gap":
        y += LINE_H * 0.5
        continue

    if kind == "host":

        inner = f"""
<text
x="{KEY_X}"
y="{y}"
font-size="14"
font-weight="700">

<tspan fill="{GREEN}">aditya</tspan>

<tspan fill="{MUTED}">@</tspan>

<tspan fill="{ACCENT}">github</tspan>

</text>

<line
x1="{KEY_X+100}"
y1="{y-4}"
x2="{W-PAD}"
y2="{y-4}"
stroke="{FRAME}"
stroke-opacity="0.8"/>
"""

    elif kind == "sec":

        title = esc(row[1])

        inner = f"""
<text
x="{KEY_X}"
y="{y}"
fill="{SECTION}"
font-size="12.5"
font-weight="700">
— {title}
</text>

<line
x1="{KEY_X+90}"
y1="{y-4}"
x2="{W-PAD}"
y2="{y-4}"
stroke="{FRAME}"
stroke-opacity="0.8"/>
"""

    elif kind == "kv":

        key = esc(row[1])
        value = esc(row[2])

        inner = f"""
<text
x="{KEY_X}"
y="{y}"
fill="{KEY}"
font-size="12.5"
font-weight="700">
{key}
</text>

<text
x="{VAL_X}"
y="{y}"
fill="{INK}"
font-size="12.5">
{value}
</text>
"""

    elif kind == "bul":

        txt = esc(row[1])

        inner = f"""
<circle
cx="{KEY_X+3}"
cy="{y-4}"
r="2.5"
fill="{GREEN}"/>

<text
x="{KEY_X+14}"
y="{y}"
fill="{INK}"
font-size="12.5">
{txt}
</text>
"""

    parts.append(rise(inner, idx))
    y += LINE_H

parts.append("</svg>")

svg = "".join(parts)

os.makedirs(os.path.dirname(OUT), exist_ok=True)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Generated {OUT}")