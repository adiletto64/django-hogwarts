---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "Django Hogwarts"
  tagline: "Set of tools to codegen urls, views and templates!"
  image:
      src: /logo.png
      alt: "logo"
  actions:
    - theme: brand
      text: docs
      link: /installation
    - theme: alt
      text: github
      link: https://github.com/adiletto64/django_hogwarts

features:
  - icon: 🖨
    title: Urls generator and auto resolver 
    details: Generate urls.py from your views with REST-like convention
    link: "/gen_urls"
  - icon: ✏
    title: Views generator 
    details: Generate basic CRUD views from your model
    link: "/gen_views"
  - icon: 📜
    title: Generate templates from templates! 
    details: Specify basic html markup and generated forms, lists, tables from them
---

