# django-lite-cms-core

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Django CI run test](https://github.com/christianwgd/django-lite-cms-core/actions/workflows/django-test.yml/badge.svg)](https://github.com/christianwgd/django-lite-cms-core/actions/workflows/django-test.yml)
[![codecov](https://codecov.io/gh/christianwgd/django-lite-cms-core/graph/badge.svg?token=azVWLmIFmg)](https://codecov.io/gh/christianwgd/django-lite-cms-core)

Some lightweight core classes for a cms based on django inspired by 
[Mezzanine](https://github.com/stephenmcd/mezzanine) CMS. 

Mezzanine is a complete CMS System and may be too complex for 
some apps that would only like to add some CMS functionality.

What's in there?

- Base class with
  - Properties: title, publish_date, expiry_date
  - Status model (currently DRAFT and PUBLISHED)
  - Manager with "published" query, based on status and date fields
- Mixins
  - SluggedMixin with unique slugs
  - TimeStampedMixin with created and changed properties
  - AdminOrderMixin based on django-admin-sortable2
  - ContentFieldMixin based on django-tinymce4
- Search functionality
- Admin edit links in frontend

# Todo

- Docs (wip)
- ...

# Outlook

There will come some more add ons for this lib:

- A hirachical page model with menus
- A blog app
- ...
