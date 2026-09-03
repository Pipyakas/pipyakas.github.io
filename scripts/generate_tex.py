#!/usr/bin/env python3
"""Generate resume.tex from resume.json data."""

import argparse
import json
import os
import re


def format_date(date_str, locale="en"):
    """Convert ISO date to readable format."""
    if date_str in ("Present", "Hiện tại"):
        return "Present" if locale == "en" else "Hiện tại"
    try:
        parts = date_str.split("-")
        months_en = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        months_vi = ["01", "02", "03", "04", "05", "06",
                     "07", "08", "09", "10", "11", "12"]
        if locale == "vi":
            return f"{months_vi[int(parts[1]) - 1]}/{parts[0]}"
        month = months_en[int(parts[1]) - 1]
        year = parts[0]
        return f"{month} {year}"
    except (IndexError, ValueError):
        return date_str


def escape_latex(text):
    """Escape LaTeX special characters in text."""
    if not isinstance(text, str):
        return text
    escape_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}'
    }
    pattern = re.compile('|'.join(re.escape(k) for k in sorted(escape_chars.keys(), key=lambda x: -len(x))))
    return pattern.sub(lambda m: escape_chars[m.group(0)], text)


def generate_tex(locale="en"):
    """Read resume_{locale}.json and generate resume_{locale}.tex with filled data."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    suffix = "" if locale == "en" else f"_{locale}"
    json_path = os.path.join(root_dir, "resume", f"resume{suffix}.json")
    template_path = os.path.join(root_dir, "resume", "resume.tex.template")
    tex_path = os.path.join(root_dir, "resume", f"resume{suffix}.tex")

    with open(json_path, "r") as f:
        data = json.load(f)

    with open(template_path, "r") as f:
        template = f.read()

    # Basics
    basics = data.get("basics", {})
    template = template.replace("VAR_NAME", escape_latex(basics.get("name", "")))
    template = template.replace("VAR_PHONE", escape_latex(basics.get("phone", "")))
    template = template.replace("VAR_EMAIL", basics.get("email", ""))
    template = template.replace("VAR_URL", basics.get("url", ""))
    template = template.replace("VAR_SUMMARY", escape_latex(basics.get("summary", "")))
    location = basics.get("location", {})
    template = template.replace("VAR_LOCATION", escape_latex(location.get("address", "")))

    # Education
    edu = data.get("education", [])
    if edu:
        edu_item = edu[0]
        template = template.replace("VAR_EDU_INSTITUTION", escape_latex(edu_item.get("institution", "")))
        start = escape_latex(format_date(edu_item.get("startDate", ""), locale))
        end = escape_latex(format_date(edu_item.get("endDate", ""), locale))
        template = template.replace("VAR_EDU_DATES", f"{start} -- {end}")
        template = template.replace("VAR_EDU_DEGREE", escape_latex(edu_item.get("studyType", "")))
        template = template.replace("VAR_EDU_AREA", escape_latex(edu_item.get("area", "")))

    # Work
    work = data.get("work", [])
    if work:
        work_item = work[0]
        template = template.replace("VAR_WORK_NAME", escape_latex(work_item.get("name", "")))
        start = escape_latex(format_date(work_item.get("startDate", ""), locale))
        end = escape_latex(format_date(work_item.get("endDate", ""), locale))
        template = template.replace("VAR_WORK_DATES", f"{start} -- {end}")
        template = template.replace("VAR_WORK_POSITION", escape_latex(work_item.get("position", "")))
        highlights = work_item.get("highlights", [])
        highlights_tex = "\n".join(f"        \\resumeItem{{{escape_latex(h)}}}" for h in highlights)
        template = template.replace("VAR_WORK_HIGHLIGHTS", highlights_tex)

    # Skills
    skills = data.get("skills", [])
    skills_parts = []
    for skill in skills:
        name = escape_latex(skill.get("name", ""))
        keywords = ", ".join(escape_latex(k) for k in skill.get("keywords", []))
        skills_parts.append(f"\\textbf{{{name}:}} {keywords}")
    skills_tex = " \\\\ ".join(skills_parts)
    template = template.replace("VAR_SKILLS", skills_tex)

    with open(tex_path, "w") as f:
        f.write(template)
    print(f"Generated {tex_path} from {json_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", choices=["en", "vi", "all"], default="all", help="Which locale to generate")
    args = parser.parse_args()
    locales = ["en", "vi"] if args.locale == "all" else [args.locale]
    for loc in locales:
        generate_tex(loc)
