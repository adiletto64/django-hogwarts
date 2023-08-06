import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Django Hogwarts",
  description: "A set of utilities and CLI tools to improve and accelerate Django development",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Docs', link: '/installation' },
    ],

    sidebar: [
      {
        text: 'getting started',
        items: [
          {'text': 'installation', link: '/installation'}
        ]
      },
      {
        text: 'urls',
        items: [
          { text: 'Auto urls resolving', link: '/auto_urls' },
          { text: 'Auto urls generation', link: '/gen_urls' },
          { text: 'Conventions', link: '/conventions' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/adiletto64/django_hogwarts' }
    ]
  }
})
