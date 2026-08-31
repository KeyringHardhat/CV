#!/usr/bin/env python3
"""Build the lightweight static CV website from the shared CV data."""
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "_data" / "cv.json"
OUTPUT = ROOT / "index.html"


def text(value):
    return html.escape(str(value))


def key(value):
    return "_".join(value.lower().replace("&", " ").split())


def roles(items):
    rendered = []
    for index, role in enumerate(items):
        achievements = "".join(
            f'<li><strong>{text(key(item["label"]))}:</strong> {text(item["detail"])}</li>'
            for item in role["achievements"]
        )
        current = '<span class="status">Current</span>' if index == 0 else ''
        rendered.append(f'''<article class="role">
  <p class="role__period"><span class="record-label">entry_{index + 1:02d}</span>{text(role["period"])}</p>
  <div class="role__content">
    <div class="role__heading"><h3>{text(role["title"])} {current}</h3><p>{text(role["company"])}</p></div>
    <ul>{achievements}</ul>
  </div>
</article>''')
    return "\n".join(rendered)


def projects(items):
    return "\n".join(
        f'''<article class="project-card">
  <p class="project-card__number">0{index}</p>
  <h3>{text(project["name"])}</h3>
  <p>{text(project["description"])}</p>
  <ul>{"".join(f"<li>{text(outcome)}</li>" for outcome in project["outcomes"])}</ul>
</article>'''
        for index, project in enumerate(items, start=1)
    )


def skills(items):
    return "\n".join(
        f'<article><h3>{text(key(skill["name"]))}:</h3><p>{text(skill["detail"])}</p></article>'
        for skill in items
    )


def main():
    cv = json.loads(DATA.read_text())
    name, title = text(cv["name"]), text(cv["title"])
    email, linkedin = text(cv["contact"]["email"]), text(cv["contact"]["linkedin"])
    focus = "".join(f"<li>{text(item)}</li>" for item in cv["focus"])
    page = f'''<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{text(cv["summary"])}">
  <meta name="theme-color" content="#101113">
  <link rel="canonical" href="https://cv.kieron.xyz/">
  <link rel="stylesheet" href="assets/css/style.css">
  <title>{name} | {title}</title>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="site-shell">
    <header class="site-header">
      <a class="wordmark" href="#top" aria-label="{name}, top of page">~/kieron-harding<span aria-hidden="true"> $</span></a>
      <div class="header-tools"><span class="host-location">{text(cv["location"])}</span><button class="effects-toggle" type="button" aria-pressed="true" hidden>effects: on</button></div>
    </header>
    <div class="terminal">
    <div class="terminal-bar" aria-hidden="true"><span class="dot"></span><span class="dot"></span><span class="dot"></span><p>kieron - platform engineering</p></div>
    <nav class="terminal-nav" aria-label="Primary navigation"><a href="#experience">experience</a><a href="#impact">impact</a><a href="#skills">skills</a><a href="#contact">contact</a><a class="nav-download" href="assets/Kieron-Harding-CV.pdf" aria-label="Download CV PDF">cv.pdf ↓</a></nav>
    <div class="terminal-body">
    <main id="main" tabindex="-1">
      <section class="hero" id="top" aria-labelledby="intro-heading">
        <div class="boot-sequence">
          <button class="boot-replay" type="button" hidden>replay intro ↻</button>
          <div class="boot-log" aria-hidden="true">
            <p class="boot-launch"><span>$</span> <span class="boot-command">./cv --init</span></p>
            <p class="boot-step"><span>[ok]</span> profile.json loaded</p>
            <p class="boot-step"><span>[ok]</span> {len(cv["roles"])} experience entries indexed</p>
            <div class="boot-meter"><span class="boot-track"><span class="boot-fill"></span></span><span class="boot-complete">ready.</span></div>
          </div>
        </div>
        <p class="prompt" aria-hidden="true"><span class="host">kieron@platform</span><span class="path">~</span><span class="symbol">$</span><span class="typed-command">whoami</span><span class="cursor"></span></p>
        <div class="intro-grid">
        <div class="hero__content">
          <h1 id="intro-heading">{name}</h1>
          <p class="hero__title">{title}</p>
          <p class="hero__summary">{text(cv["summary"])}</p>
          <div class="hero__actions"><a class="button button--primary" href="assets/Kieron-Harding-CV.pdf">Download CV <span aria-hidden="true">↓</span></a><a class="button" href="{linkedin}" rel="me">LinkedIn <span aria-hidden="true">↗</span></a></div>
        </div>
        <aside class="hero__aside" aria-label="Core strengths"><p class="comment"># platform_focus</p><ul>{focus}</ul></aside>
        </div>
      </section>
      <section class="section" id="experience" aria-labelledby="experience-heading"><div class="section-heading"><p class="prompt" aria-hidden="true"><span class="symbol">$</span> cat experience.log --latest-first</p><h2 id="experience-heading"># experience · {len(cv["roles"])} entries · newest first</h2></div><div class="timeline">{roles(cv["roles"])}</div></section>
      <section class="section" id="impact" aria-labelledby="impact-heading"><div class="section-heading"><p class="prompt" aria-hidden="true"><span class="symbol">$</span> ls ./impact --details</p><h2 id="impact-heading"># selected impact · {len(cv["projects"])} results</h2></div><div class="project-grid">{projects(cv["projects"])}</div></section>
      <section class="section" id="skills" aria-labelledby="skills-heading"><div class="section-heading"><p class="prompt" aria-hidden="true"><span class="symbol">$</span> cat capabilities.yml</p><h2 id="skills-heading"># capabilities · {len(cv["skills"])} groups</h2></div><div class="skill-grid">{skills(cv["skills"])}</div></section>
    </main>
    <footer class="contact" id="contact" aria-label="Contact"><p class="prompt" aria-hidden="true"><span class="symbol">$</span> ./connect</p><p class="comment"># open a conversation</p><div class="contact-links"><a href="mailto:{email}">{email}</a><a href="{linkedin}">LinkedIn ↗</a></div></footer>
    </div>
    </div>
    <div class="site-footer"><p>{name} / {title}</p><p>Last updated: {text(cv["updated"])}</p></div>
  </div>
  <script src="assets/js/terminal.js" defer></script>
</body>
</html>'''
    OUTPUT.write_text(page + "\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
