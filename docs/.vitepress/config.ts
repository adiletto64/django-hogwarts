import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Django Hogwarts",
  description: "A set of utilities and CLI tools to improve and accelerate Django development",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Docs', link: '/autourl' },
    ],

    sidebar: [
      {
        text: 'Features',
        items: [
          { text: 'Auto urls resolving', link: '/autourl' },
          { text: 'Auto urls generation', link: '/gen_urls' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/adiletto64/django_hogwarts' }
    ]
  }
})
