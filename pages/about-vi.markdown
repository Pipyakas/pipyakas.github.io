---
layout: page
title: Giới thiệu
permalink: /about/vi/
toc: false
---

<div class="resume-container">
  {% assign resume = site.data.resume_vi %}

  <header class="resume-header">
    <h2>{{ resume.basics.name }}</h2>
    <p class="resume-subtitle">{{ resume.basics.label }}</p>
    <div class="resume-contact">
      <span><i class="fas fa-envelope"></i> {{ resume.basics.email }}</span>
      <span><i class="fas fa-phone"></i> {{ resume.basics.phone }}</span>
      <span><i class="fas fa-map-marker-alt"></i> {{ resume.basics.location.address }}</span>
      <span><i class="fas fa-link"></i> <a href="{{ resume.basics.url }}">{{ resume.basics.url | replace: 'https://', '' }}</a></span>
    </div>
    <p class="resume-lang-switch"><a href="/about/">English</a> · <strong>Tiếng Việt</strong></p>
  </header>

  <section class="resume-section">
    <h3>Tóm tắt</h3>
    <p>{{ resume.basics.summary }}</p>
  </section>

  <section class="resume-section">
    <h3>Kinh nghiệm làm việc</h3>
    {% for job in resume.work %}
    <div class="resume-item">
      <div class="resume-item-header">
        <span class="resume-item-title">{{ job.position }}</span>
        <span class="resume-item-date">{{ job.startDate }} — {{ job.endDate }}</span>
      </div>
      <div class="resume-item-company">{{ job.name }}</div>
      <ul class="resume-item-highlights">
        {% for highlight in job.highlights %}
        <li>{{ highlight }}</li>
        {% endfor %}
      </ul>
    </div>
    {% endfor %}
  </section>

  <section class="resume-section">
    <h3>Kỹ năng</h3>
    <div class="resume-skills">
      {% for skill in resume.skills %}
      <div class="resume-skill-group">
        <strong>{{ skill.name }}:</strong> {{ skill.keywords | join: ", " }}
      </div>
      {% endfor %}
    </div>
  </section>

  <section class="resume-section">
    <h3>Học vấn</h3>
    {% for edu in resume.education %}
    <div class="resume-item">
      <div class="resume-item-header">
        <span class="resume-item-title">{{ edu.institution }}</span>
        <span class="resume-item-date">{{ edu.startDate }} — {{ edu.endDate }}</span>
      </div>
      <div class="resume-item-degree">{{ edu.studyType }} ngành {{ edu.area }}</div>
    </div>
    {% endfor %}
  </section>

  {% if resume.languages %}
  <section class="resume-section">
    <h3>Ngôn ngữ</h3>
    <div class="resume-languages">
      {% for lang in resume.languages %}
      <div class="resume-language"><strong>{{ lang.language }}:</strong> {{ lang.fluency }}</div>
      {% endfor %}
    </div>
  </section>
  {% endif %}

  <div class="resume-pdf-section">
    <p class="resume-download">
      <a href="/assets/quy.nguyenngoc-vi.pdf" download>Tải CV (PDF)</a>
    </p>
  </div>
</div>
