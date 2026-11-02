# Radiant Karats

![Radiant Karats on a desktop, a tablet and a phone](docs/mockup.webp)

Radiant Karats is a ring collection website built with Django. Anyone can
browse the rings, search them by name, filter them by style and sort them by
price. People with an
account add their own rings, with a photo, the style, the metal, the gemstone
and a price. Only the person who added a ring, or the site owner, can edit or
delete it. In the Christmas season, snow falls on the home page.

**Live site:** [radiant-karats-9aa02d050439.herokuapp.com](https://radiant-karats-9aa02d050439.herokuapp.com/)

**Repository:** [github.com/Krishna2414/radiant-karats](https://github.com/Krishna2414/radiant-karats)

**Project board:** [GitHub Projects](https://github.com/users/Krishna2414/projects/11)

## Contents

- [User experience (UX)](#user-experience-ux)
  - [Strategy](#strategy)
  - [Scope](#scope)
  - [User stories](#user-stories)
  - [Structure](#structure)
  - [Skeleton: wireframes](#skeleton-wireframes)
  - [Surface: design](#surface-design)
- [Database](#database)
- [Features](#features)
  - [Existing features](#existing-features)
  - [Tablet and mobile view](#tablet-and-mobile-view)
  - [Future features](#future-features)
- [Agile methodology](#agile-methodology)
- [Technologies used](#technologies-used)
- [Testing](#testing)
  - [Automated tests](#automated-tests)
  - [Code validation](#code-validation)
  - [PageSpeed Insights and Lighthouse](#pagespeed-insights-and-lighthouse)
  - [Accessibility](#accessibility)
  - [Responsiveness](#responsiveness)
  - [Browser testing](#browser-testing)
  - [Testing the user stories](#testing-the-user-stories)
  - [Testing the ring picture and the snow](#testing-the-ring-picture-and-the-snow)
  - [Defensive testing](#defensive-testing)
  - [Links](#links)
  - [Bugs](#bugs)
- [Deployment](#deployment)
- [AI tools](#ai-tools)
- [Credits](#credits)

## User experience (UX)

### Strategy

**The idea.** One place to share and find rings, where every ring shows the
same clear details: a photo, the style, the metal, the gemstone and the price.

**Research.** Before planning, I looked at where people find rings online
today, including my own shop at [radiantkarats.com](https://radiantkarats.com)
and on Etsy.

| Where | What works well | What's missing |
| --- | --- | --- |
| Jewellery shop websites | Every ring has photos, a price, and its metal and stone. Shoppers can usually filter and sort the rings. | Only the shop can add rings. |
| Pinterest and Instagram | Lots of ring ideas, and anyone can share their own. | The details are missing or buried in captions, and you can't filter by style or sort by price. |

Radiant Karats takes the clear details and the filters of a shop, and lets
anyone add their own rings, as on a social site.

**Who it's for:**

- People looking for ring ideas, for example for an engagement, a wedding or
  a gift.
- Makers, collectors and small jewellers who want to show their own rings.
- The site owner, who looks after the collection and removes anything
  unsuitable.

**External user's goal:** browse rings easily, and add and look after my own
rings.

**Site owner's goal:** a growing collection of rings with complete details,
where nobody can change anyone else's rings.

### Scope

The project was planned with MoSCoW priorities. Every must-have and
should-have story is built, and so is one could-have: search by name (US17).

| Priority | Features | Stories |
| --- | --- | --- |
| Must have | Register, log in and log out; see who is logged in; browse every ring; a page for each ring; add, edit and delete my own rings, with a photo; nobody else can change my rings; the site owner can manage every ring; works on any screen | US01 to US11 |
| Should have | The newest rings on the home page; My rings; filter by style; sort by price; custom 404 and 403 pages | US12 to US16 |
| Could have | Search by name (built); favourite rings (built) | US17 and US18 |
| Won't have this time | Made-to-order rings; buying rings online | US19 and US20 |

**Kept out on purpose.** My facilitator advised me to keep this project
simple: no shop or checkout (showing a price is fine) and no made-to-order
customisation, and to list both as future features instead.

### User stories

Each user story is an issue in the repository, with its acceptance criteria,
its tasks and a MoSCoW label. Every story is tested against its acceptance
criteria in [Testing the user stories](#testing-the-user-stories).

| Issue | User story | Priority |
| --- | --- | --- |
| [#1](https://github.com/Krishna2414/radiant-karats/issues/1) | As a visitor, I can register an account so that I can add my own rings. | Must have |
| [#2](https://github.com/Krishna2414/radiant-karats/issues/2) | As a registered user, I can log in and log out so that only I can use my account. | Must have |
| [#3](https://github.com/Krishna2414/radiant-karats/issues/3) | As a user, I can see whether I'm logged in, and as whom, so that I know which account I'm using. | Must have |
| [#4](https://github.com/Krishna2414/radiant-karats/issues/4) | As a visitor, I can browse every ring so that I can find rings I like. | Must have |
| [#5](https://github.com/Krishna2414/radiant-karats/issues/5) | As a visitor, I can open a ring's own page so that I can see all its details. | Must have |
| [#6](https://github.com/Krishna2414/radiant-karats/issues/6) | As a signed-in user, I can add a ring with a photo so that other people can see it. | Must have |
| [#7](https://github.com/Krishna2414/radiant-karats/issues/7) | As a ring's owner, I can edit my ring so that I can fix mistakes or add a photo. | Must have |
| [#8](https://github.com/Krishna2414/radiant-karats/issues/8) | As a ring's owner, I can delete my ring so that I can remove rings I no longer want. | Must have |
| [#9](https://github.com/Krishna2414/radiant-karats/issues/9) | As a ring's owner, I can trust that nobody else can change my rings so that they stay as I made them. | Must have |
| [#10](https://github.com/Krishna2414/radiant-karats/issues/10) | As the site owner, I can edit or delete any ring so that I can remove anything unsuitable. | Must have |
| [#11](https://github.com/Krishna2414/radiant-karats/issues/11) | As a visitor, I can use the site on a phone, tablet or computer so that I can browse anywhere. | Must have |
| [#12](https://github.com/Krishna2414/radiant-karats/issues/12) | As a visitor, I can see the newest rings on the home page so that I can see what's new. | Should have |
| [#13](https://github.com/Krishna2414/radiant-karats/issues/13) | As a signed-in user, I can see only the rings I added so that I can manage them in one place. | Should have |
| [#14](https://github.com/Krishna2414/radiant-karats/issues/14) | As a visitor, I can filter the rings by style so that I only see the styles I like. | Should have |
| [#15](https://github.com/Krishna2414/radiant-karats/issues/15) | As a visitor, I can sort the rings by price so that I can find rings in my budget. | Should have |
| [#16](https://github.com/Krishna2414/radiant-karats/issues/16) | As a visitor, I can see a helpful page when a link is broken or not allowed so that I can find my way back. | Should have |
| [#17](https://github.com/Krishna2414/radiant-karats/issues/17) | As a visitor, I can search the rings by name so that I can find a ring quickly. | Could have |
| [#18](https://github.com/Krishna2414/radiant-karats/issues/18) | As a signed-in user, I can save rings I like so that I can find them again. | Could have |
| [#19](https://github.com/Krishna2414/radiant-karats/issues/19) | As a customer, I can choose the metal, stone and size of a ring made for me so that I get exactly the ring I want. | Won't have |
| [#20](https://github.com/Krishna2414/radiant-karats/issues/20) | As a customer, I can pay for a ring on the site so that I don't need to visit a shop. | Won't have |

### Structure

**Site map.** The navbar is on every page, and it only shows the links each
person can use. White boxes are open to everyone; gold boxes need an
account, and the Django admin is for staff only.

```mermaid
flowchart TD
    nav["Navbar, on every page"]
    nav --> home["Home"]
    nav --> all["All rings"]
    nav --> add["Add a ring"]
    nav --> mine["My rings"]
    nav --> acc["Register, log in, log out"]
    nav --> admin["Django admin (staff)"]
    home --> ring["Ring page"]
    all --> ring
    mine --> ring
    add -- "saved" --> ring
    ring -- "owner or staff" --> edit["Edit ring"]
    ring -- "owner or staff" --> del["Delete box or page"]
    edit -- "saved" --> ring
    del -- "deleted" --> mine
    classDef page fill:#faf7f2,stroke:#1c2430,color:#1c2430
    classDef owner fill:#f1e8da,stroke:#7d5f12,color:#1c2430
    class nav,home,all,ring,acc page
    class add,mine,edit,del,admin owner
```

**Who can use each page.**

| Page | Address | Visitors | Signed-in users | Site owner (staff) |
| --- | --- | :---: | :---: | :---: |
| Home | `/` | Yes | Yes | Yes |
| All rings | `/rings/` | Yes | Yes | Yes |
| Ring page | `/rings/<slug>/` | Yes | Yes | Yes |
| Register, Log in | `/accounts/signup/`, `/accounts/login/` | Yes | | |
| Add a ring | `/rings/add/` | Sent to log in | Yes | Yes |
| My rings | `/rings/mine/` | Sent to log in | Yes | Yes |
| Favourites | `/rings/favourites/` | Sent to log in | Yes | Yes |
| Edit or delete a ring | `/rings/<slug>/edit/`, `/rings/<slug>/delete/` | Sent to log in | Their own rings only | Any ring |
| Log out | `/accounts/logout/` | | Yes | Yes |
| Django admin | `/admin/` | | | Yes |

**CRUD and user feedback.** Every change to the data shows a message, and
deleting always asks first.

| | What the user does | Who | What they see afterwards |
| --- | --- | --- | --- |
| Create | Fills in the Add a ring form | Signed-in users | The new ring's page and "Evening Star has been added." |
| Create, with a mistake | Sends the form with a mistake | Signed-in users | The form again, the reason under the field, and "Please check the form for errors." |
| Read | Browses All rings, opens a ring, opens My rings | Everyone (My rings needs an account) | How many rings there are, or a message when there are none |
| Update | Edits a ring and saves | The owner, and staff | The ring's page and "Evening Star has been updated." |
| Delete | Clicks Delete ring, then confirms | The owner, and staff | "Delete Evening Star?" first, then My rings and "Evening Star has been deleted." |

**Defensive design.**

- Pages that need an account send visitors to log in, then back to the page
  they wanted.
- Edit and Delete only show for the ring's owner and staff. Anyone else who
  types the address sees a 403 page.
- Deleting always asks first, and only the form button (a POST) can delete.
  Opening the delete address shows a confirm page.
- The form refuses a stone-set style with no gemstone, a price under £1, a
  photo over 5 MB and files Cloudinary can't read. The database also refuses
  a price of 0 or less.
- The All rings page ignores style and sort values it doesn't know, such as
  `?style=banana`, instead of failing.
- Every form has a CSRF token.

### Skeleton: wireframes

Wireframes of each page at desktop and phone sizes. The numbered notes
explain what each part does, including the phone menu, the Style menu, the
delete box and the form errors.

<details open>
<summary>Home page</summary>

![Home page wireframe](docs/wireframes/home-my-rings-style.svg)
</details>

<details>
<summary>All rings, with the Style menu open</summary>

![All rings wireframe](docs/wireframes/all-rings.webp)
</details>

<details>
<summary>Ring page, with the delete box open</summary>

![Ring page wireframe](docs/wireframes/ring-page.webp)
</details>

<details>
<summary>Add a ring and Edit a ring, with form errors</summary>

![Ring form wireframe](docs/wireframes/ring-form.webp)
</details>

<details>
<summary>My rings</summary>

![My rings wireframe](docs/wireframes/my-rings.webp)
</details>

<details>
<summary>Register, log in and log out</summary>

![Account pages wireframe](docs/wireframes/accounts.webp)
</details>

<details>
<summary>404 and 403 pages</summary>

![Error pages wireframe](docs/wireframes/error-pages.webp)
</details>

### Surface: design

**Colour scheme.** Deep ink and gold, like a jewellery box: calm, smart and
easy to read. Gold is the colour of the metal itself, and the dark ink gives
it strong contrast.

![The six colours of the site](docs/palette.webp)

| Colour | Hex | Used for | Contrast |
| --- | --- | --- | --- |
| Ink | `#1c2430` | Text, navbar, footer, dark buttons | 14.6:1 on ivory |
| Gold | `#d4af37` | Gold buttons, the brand name, highlights on dark backgrounds | 7.4:1 with ink |
| Dark gold | `#7d5f12` | Links, prices and small headings on light backgrounds | 5.6:1 on ivory, 4.9:1 on champagne |
| Ivory | `#faf7f2` | Page background | |
| Champagne | `#f1e8da` | Behind ring pictures, and boxes | 12.9:1 with ink |
| Grey | `#5b6370` | Secondary text | 5.7:1 on ivory |

Every text colour pair meets WCAG AA (4.5:1 or more). Bright gold on ivory is
only 2.0:1, so small gold text on light backgrounds uses the dark gold.
Bootstrap's own grey is 4.4:1 on ivory, just under the limit, so the site
uses a slightly darker grey.

The home page hero is lit like a jewellery display: a soft radial gradient
from `#3a4860` behind the ring picture to `#2e3641`. Measured where the text
sits, from 320px to 1920px wide, the small gold text is at least 5.0:1, the
gold word in the heading at least 4.5:1 and the white text at least 7.2:1.

**Typography.** Headings use
[Cormorant Garamond](https://fonts.google.com/specimen/Cormorant+Garamond),
an elegant serif that suits jewellery. Body text uses
[Lato](https://fonts.google.com/specimen/Lato), which stays easy to read at
small sizes. Both come from Google Fonts, with Georgia and Arial as
fallbacks.

**Imagery.** Until a ring has a photo, it shows a drawing of its style:
solitaire, halo, trilogy, eternity or band. The drawings are SVG files, so
they stay sharp at any size. Photos are stored on Cloudinary, which sends
them as WebP or AVIF to browsers that support it, at a quality that keeps the
file small (`f_auto` and `q_auto`).

On laptops and desktops, a drawing of a gold solitaire ring fills the right of
the home page hero, on the gradient's light spot. It's decoration, so it's a
CSS background: screen readers skip it, and phones and tablets, which don't
show it, never download it. From 1 November to 6 January, small snowflakes
fall behind the hero text and the ring (see [Christmas snow](#christmas-snow)).

**Layout.** The same patterns repeat on every page so the site is easy to
learn: ring cards where the whole card is a link, gold buttons for the main
action, ink buttons for the next step, outlined buttons for "Cancel" and
"Keep it", and red for deleting. Messages always appear at the top of the
page.

## Database

The live site uses PostgreSQL. The tests, and local set-ups without a
`DATABASE_URL`, use SQLite. Ring is the custom model; User is Django's
built-in user model, used by django-allauth.

![Entity relationship diagram: one User adds zero or many Rings](docs/erd.webp)

| Ring field | Type | Rules |
| --- | --- | --- |
| `owner` | ForeignKey to User | Set to the signed-in user when the ring is added. Deleting a user deletes their rings (`CASCADE`). `user.rings` lists a user's rings. |
| `name` | CharField(100) | Required |
| `slug` | SlugField(120), unique | The ring's address, made from its name when it's first saved. It can't be edited. |
| `style` | CharField with choices | Solitaire, Halo, Trilogy, Eternity or Band |
| `metal` | CharField with choices | Yellow gold, White gold, Rose gold, Platinum or Sterling silver |
| `gemstone` | CharField with choices | Diamond, Lab-grown diamond, Moissanite, Sapphire, Emerald, Ruby or No gemstone (the default) |
| `price` | DecimalField(8, 2) | £1 or more. A database `CHECK` constraint refuses 0 or less. |
| `description` | TextField | Required |
| `image` | CloudinaryField | Optional. Until a photo is uploaded, the ring shows a drawing of its style. |
| `created_on`, `updated_on` | DateTimeField | Filled in automatically. Rings are listed newest first. |

**How Ring differs from the walkthrough.** The Codestar blog's Post model is
a blog post: a title, an author, the content and a draft or published status.
Ring has its own choices for style, metal and gemstone, a price with a
validator and a database constraint, a Cloudinary photo with a drawing as a
fallback, an ownership rule, and an address made from its name that keeps
clear of the site's own addresses.

**Custom logic:**

- `make_unique_slug()` makes an address from the name. It renames "add" and
  "mine", which `/rings/add/` and `/rings/mine/` use, and loops to add a
  number (`aurora-2`, `aurora-3`) until no other ring has the address.
- `can_be_changed_by(user)` holds the ownership rule in one place: visitors
  can't change a ring; its owner and staff can. The views and the templates
  both use it.
- `photo_url` builds the Cloudinary address with `f_auto` and `q_auto`, or
  returns nothing so the page shows the drawing. `alt_text` describes the
  photo, for example "The Heirloom, a platinum halo ring".
- `RingForm.clean()` checks that solitaire, halo, trilogy and eternity rings
  have a gemstone. `PhotoField` refuses photos over 5 MB, and turns a failed
  upload into a message under the field.
- `RingList` only accepts the styles and sort orders it knows. Rings with the
  same price stay newest first, so they never swap places between pages.

## Features

The screenshots were taken on the live site on 2 November 2026, in the
Christmas season, so snow is falling on the home page. Three of them come
from a copy of the site running the same code, so that no test accounts had
to be made on the live site: the 403 page, the register form with a mistake,
and My rings with no rings yet.

### Existing features

#### Navigation and login state

The navbar is on every page. It shows who is signed in ("Signed in as
KK1424"), and only the links that person can use: visitors see Log in and
Register, signed-in users see Add a ring, My rings, Favourites and Log out,
and staff also see Admin. The current page is underlined. On phones and
tablets the links fold into a menu button, shown open in [Tablet and mobile
view](#tablet-and-mobile-view). *Stories US01 to US03, US10 and US11.*

![The navbar for a visitor and for the site owner](docs/screenshots/navbar-states.webp)

A signed-in user who isn't staff sees the same links as the site owner,
without Admin.

#### Home page

A short introduction, the three newest rings and a button to see them all.
On laptops and desktops, a picture of a gold ring sits beside the
introduction; on phones and tablets the introduction has the full width. The
box at the bottom asks visitors to create an account; signed-in users see Add
a ring instead. With no rings yet, the page says "No rings yet. Be the first
to add one!" *Story US12.*

![Home page](docs/screenshots/home.webp)

#### Christmas snow

From 1 November to 6 January, snow falls behind the hero text and the ring
picture, and a snowdrift in the page colour finishes off the hero. The dates
come from `show_christmas_effect()` in `views.py`, and two automated tests
check the first and last days. The snow is made with CSS only, so the site
still has no custom JavaScript.

Moving pictures must be easy to stop (WCAG 2.2.2), so a **Pause the snow**
switch sits in the corner of the hero. It works with a mouse, a tap or the
keyboard (Tab to it, then Space), and turns gold while the snow is paused.
People who turn off animations in their device settings see no falling snow
at all. The snow is decoration only, so screen readers skip it.

| Snow on a laptop | Snow on a phone |
| :---: | :---: |
| <img src="docs/screenshots/christmas-snow.webp" alt="Snow falling on the home page, with the Pause the snow switch in the corner" width="560"> | <img src="docs/screenshots/christmas-snow-phone.webp" alt="Snow falling on the home page on a phone" width="200"> |

The switch while the snow is paused, with the keyboard focus outline:

<img src="docs/screenshots/christmas-paused.webp" alt="The Pause the snow switch turned gold, with a gold focus outline" width="316">

#### All rings

Every ring as a card with its photo or drawing, name, style, metal and price.
The whole card is a link to the ring's page. There are nine rings to a page,
with Previous and Next links, and a count of the rings. *Story US04.*

![All rings](docs/screenshots/all-rings.webp)

#### Search by name

The Search by name box on All rings finds every ring whose name contains the
words typed, in capitals or not. It works together with the Style and Sort
menus, the count says how many rings match, and the search stays in the box
and in the page links. When nothing matches, a message and a Show all rings
button appear. *Story US17.*

| Searching for "marquise" | Nothing matches "sapphire" |
| --- | --- |
| ![Two rings match marquise](docs/screenshots/search.webp) | ![No rings match sapphire](docs/screenshots/search-none.webp) |

#### Filter by style and sort by price

The Style menu shows one style at a time, and the Sort menu orders the rings
newest first or by price. The count says how many rings match, and the
choices stay set when you change page. When no ring matches, a message and a
Show all rings button appear. *Stories US14 and US15.*

| Eternity rings, highest price first | No rings in the chosen style |
| --- | --- |
| ![Eternity rings sorted by price](docs/screenshots/filter-sort.webp) | ![No trilogy rings yet](docs/screenshots/filter-none.webp) |

#### Ring page

The photo (or a drawing of the style), the price, style, metal, gemstone, who
added the ring and when, and its description. The breadcrumb leads back to
All rings. The ring's owner and staff also see Edit ring and Delete ring.
*Story US05.*

![Ring page](docs/screenshots/ring-page.webp)

#### Add a ring

Signed-in users add a ring with a name, style, metal, gemstone, price,
description and an optional photo. Style, metal and gemstone are dropdowns,
so only real choices can be picked. Photos (JPG, PNG or WebP, under 5 MB)
are uploaded to Cloudinary. Mistakes are explained under the field, and a
message confirms when the ring is added. In the screenshots, Evening Star was
added without a photo, so its page shows the solitaire drawing. *Story US06.*

| The empty form | The form with mistakes | The new ring and its message |
| --- | --- | --- |
| ![Add a ring form](docs/screenshots/add-ring.webp) | ![Form with errors](docs/screenshots/form-errors.webp) | ![Ring added](docs/screenshots/ring-added.webp) |

#### Edit a ring

The same form, filled in with the ring's details. Leaving the photo empty
keeps the old one. A message confirms the change. *Stories US07 and US10.*

| The edit form | The ring after saving |
| --- | --- |
| ![Edit form](docs/screenshots/edit-ring.webp) | ![Ring updated](docs/screenshots/ring-updated.webp) |

#### Delete a ring

Delete ring opens a box that asks "Delete Evening Star?" first. Keep it
closes the box; Delete ring deletes the ring and goes back to My rings with a
message. The Delete buttons on My rings open a confirm page that does the
same, and so does the delete address if JavaScript is off. *Story US08.*

| The delete box | The confirm page | After deleting |
| --- | --- | --- |
| ![Delete box](docs/screenshots/delete-modal.webp) | ![Confirm page](docs/screenshots/delete-confirm.webp) | ![Ring deleted](docs/screenshots/ring-deleted.webp) |

#### My rings

Only the rings the signed-in user added, newest first, each with Edit and
Delete buttons. With no rings yet, a message and an Add your first ring
button appear. *Story US13.*

| My rings | No rings yet |
| --- | --- |
| ![My rings](docs/screenshots/my-rings.webp) | ![My rings with no rings](docs/screenshots/my-rings-empty.webp) |

#### Favourites

Signed-in users can save any ring to their Favourites list and return to it
later. The button changes between Save to favourites and Remove from
favourites, and the list shows the saved rings most recently added first.
*Story US18.*

| Save to favourites on the ring page | Favourites page |
| --- | --- |
| ![Save to favourites on the ring page](docs/screenshots/favourites-ring.png) | ![Your saved rings on the Favourites page](docs/screenshots/favourites-page.png) |

#### Accounts

Register, log in and log out use django-allauth, styled to match the site.
Registering needs a username and a password typed twice; the email is
optional. Logging out asks first. *Stories US01 and US02.*

| Register | Log in |
| --- | --- |
| ![Register page](docs/screenshots/register.webp) | ![Log in page](docs/screenshots/login.webp) |
| **A mistake on the form** | **Log out** |
| ![Passwords that don't match](docs/screenshots/register-error.webp) | ![Log out page](docs/screenshots/logout.webp) |

#### Messages

A message at the top of the page confirms every change, and each one can be
closed:

- "Successfully signed in as KK1424." after logging in or registering
- "You have signed out." after logging out
- "Evening Star has been added.", "has been updated." and "has been deleted."
- "Please check the form for errors." in red, with the reason under each field

![Message after adding a ring](docs/screenshots/message.webp)

#### Permissions and the 403 page

Nobody can change someone else's ring. Other users don't see the Edit and
Delete buttons, and if they type the address, they get a 403 page with links
back. Visitors are sent to log in. *Stories US09 and US16.*

![403 page](docs/screenshots/403.webp)

#### 404 page

A broken link, or a ring that has been deleted, shows a 404 page in the
site's style, with links to the home page and the rings. *Story US16.*

![404 page](docs/screenshots/404.webp)

#### The site owner

Staff see Edit and Delete on every ring, and an Admin link in the navbar. The
Django admin lists every ring, with filters for style, metal and gemstone,
and a search by name, description or owner. *Story US10.* The admin follows
the browser's light or dark setting; this screenshot was taken in dark mode.

![Rings in the Django admin](docs/screenshots/admin.webp)

#### Accessibility

- A "Skip to main content" link, landmarks (header, nav, main, footer) and
  one `h1` on each page.
- A clear focus outline on links, buttons and form fields.
- Labels on every form field, and alt text on every image.
- Hidden text on repeated buttons, so screen readers hear the ring's name
  too, such as "Edit 2 CT Emerald Cut Diamond Ring with Pave Band", rather
  than just "Edit".
- The delete box is a labelled dialog. It traps the focus, and Escape closes
  it.
- Colour pairs that meet WCAG AA, and form text at 16px, so phones don't
  zoom in.
- Decorative pictures, the ring in the hero and the snow, are hidden from
  screen readers.
- The snow has a Pause the snow switch, and doesn't fall at all for people
  who turn off animations (WCAG 2.2.2 Pause, Stop, Hide).

#### Footer

The footer links to [radiantkarats.com](https://radiantkarats.com), which
opens in a new tab.

### Tablet and mobile view

Every page works from 320px wide. The menu folds into a button, the cards
stack, and the forms fill the screen. The ring picture in the home page hero
only shows from 992px wide, so on phones and tablets the introduction has the
full width.

| Home | All rings | Ring page |
| :---: | :---: | :---: |
| <img src="docs/screenshots/home-phone.webp" alt="Home page on a phone" width="250"> | <img src="docs/screenshots/all-rings-phone.webp" alt="All rings on a phone" width="250"> | <img src="docs/screenshots/ring-page-phone.webp" alt="Ring page on a phone, scrolled to the details" width="250"> |

| Add a ring, with a mistake | My rings | Menu open |
| :---: | :---: | :---: |
| <img src="docs/screenshots/form-phone.webp" alt="The form on a phone" width="250"> | <img src="docs/screenshots/my-rings-phone.webp" alt="My rings on a phone" width="250"> | <img src="docs/screenshots/menu-phone.webp" alt="The menu open on a phone" width="250"> |

| All rings on a tablet | Ring page on a tablet |
| :---: | :---: |
| <img src="docs/screenshots/all-rings-tablet.webp" alt="All rings on a tablet" width="380"> | <img src="docs/screenshots/ring-page-tablet.webp" alt="Ring page on a tablet" width="380"> |

### Future features

- **Made-to-order rings** (US19): customers choose the metal, stone and size
  of a ring to be made for them, and the site owner sends a quote.
- **A shop** (US20): a basket and online payments, for example with Stripe.
- **More photos** for each ring, shown as a small gallery.
- **More filters**, such as metal, gemstone and a price range.
- **Tidying up Cloudinary**: delete a ring's old photo when it's replaced, or
  when the ring is deleted.
- **Email**: confirm new accounts by email, and reset a forgotten password.
- **More seasonal themes**, such as Valentine's Day, using the same date
  check as the Christmas snow.

## Agile methodology

I planned and tracked the work on a
[GitHub Projects board](https://github.com/users/Krishna2414/projects/11) with
the columns Todo, In Progress and Done.

- **User stories as issues.** Each user story is an issue with acceptance
  criteria and tasks as checkboxes, so it's clear when a story is done.
- **MoSCoW labels.** Each issue has a `must-have`, `should-have`,
  `could-have` or `won't-have` label. Must-haves were built first, then the
  should-haves.
- **Small steps.** Each story moved from Todo to In Progress to Done as I
  built and tested it. Search by name (US17), a could-have, was built at the
  end. Favourites (US18) and the won't-haves stay in Todo as future features.
- **Commits.** I committed after every step, with a message that says what
  changed, for example "Let signed-in users add a ring (#6)". The issue number
  links the commit to its story.

I worked in three short iterations:

| Iteration | Dates | What was done |
| --- | --- | --- |
| 1. Set-up | 14 to 19 October | The Django project and Heroku settings, accounts with allauth (US01 to US03), the site styles, and the Ring model with Cloudinary photos |
| 2. The ring pages | 19 to 27 October | All rings and ring pages (US04, US05), add, edit and delete (US06 to US08), permissions and the 403 page (US09, US10), phones (US11), the newest rings (US12), My rings (US13), filter and sort (US14, US15), and the 404 page (US16) |
| 3. Testing, documentation and finishing touches | From 28 October | Validation, Lighthouse, accessibility and screen-size checks, this README, the ring picture in the home page hero, a seasonal effect (the Christmas snow), and search by name (US17) |

## Technologies used

**Languages:** Python 3.12, HTML5 and CSS3. There's no custom JavaScript:
Bootstrap's own script opens the phone menu and the delete box, and closes
the messages.

**Frameworks and libraries:**

| Name | Version | Used for |
| --- | --- | --- |
| [Django](https://www.djangoproject.com/) | 4.2 | The web framework |
| [django-allauth](https://docs.allauth.org/) | 0.57 | Registering, logging in and logging out |
| [django-crispy-forms](https://django-crispy-forms.readthedocs.io/) and [crispy-bootstrap5](https://github.com/django-crispy-forms/crispy-bootstrap5) | 2.5 and 0.7 | Bootstrap styling for the forms |
| [Bootstrap](https://getbootstrap.com/) | 5.3 | The grid, navbar, cards, modal and form styles |
| [Cloudinary](https://cloudinary.com/) (`cloudinary`) | 1.36 | Storing and sending ring photos |
| [Gunicorn](https://gunicorn.org/) | 23.0 | The web server on Heroku |
| [WhiteNoise](https://whitenoise.readthedocs.io/) | 5.3 | Serving the CSS and images on Heroku |
| [dj-database-url](https://github.com/jazzband/dj-database-url) and [psycopg2](https://www.psycopg.org/) | 0.5 and 2.9 | Connecting to PostgreSQL |

**Programs and services:** Git, GitHub, GitHub Projects, VS Code, Heroku,
Code Institute's PostgreSQL database, Cloudinary, Google Fonts, Chrome
DevTools, Lighthouse, PageSpeed Insights, the W3C Markup Validation Service
and CSS Validation Service, flake8, and Claude (an AI assistant, see
[AI tools](#ai-tools)).

## Testing

### Automated tests

There are 85 automated tests in `rings/tests.py`, written with Django's
`TestCase`. They use SQLite, because the Code Institute database doesn't let
Django create the separate database tests need. Photo uploads are faked with
`unittest.mock`, so the tests never upload anything to Cloudinary.

Run them with:

```
python manage.py test
```

```
Found 85 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....................................................................................
----------------------------------------------------------------------
Ran 85 tests in 23.652s

OK
```

| Test class | Tests | What it checks |
| --- | ---: | --- |
| `HomePageTests` | 6 | The three newest rings, the message when there are none, the links to All rings and to each ring, and the Christmas snow showing only from 1 November to 6 January |
| `RingModelTests` | 2 | Slugs made from the name, and different slugs for rings with the same name |
| `RingListTests` | 6 | The cards' details, drawings for rings without a photo, nine rings a page, the empty message and the navbar link |
| `RingDetailTests` | 7 | Every detail on the ring page, the photo or the drawing, who added it and when, and the 404 page for a missing ring |
| `RingFormTests` | 5 | The optional photo, a gemstone for stone-set styles, bands without a gemstone, the £1 minimum and the 5 MB limit |
| `RingCreateTests` | 7 | Visitors sent to log in, the Add a ring link, adding with and without a photo, upload errors and form mistakes |
| `RingEditTests` | 10 | Who can edit, the filled-in form, saving with a message, staff editing, and keeping or replacing the photo |
| `MyRingsTests` | 4 | Logging in first, the navbar link, only my rings with Edit and Delete, and the empty message |
| `RingDeleteTests` | 7 | Who sees Delete, the confirm page, visitors and other users refused, deleting with a message, and staff deleting |
| `RingSafetyTests` | 3 | No Edit or Delete for other users, the 403 page, and visitors sent to log in |
| `SiteOwnerTests` | 3 | Staff buttons on every ring, the Admin link for staff only, and the admin's filters and search |
| `AnyDeviceTests` | 3 | The viewport tag, the folding navbar and the number keypad for the price |
| `StyleFilterTests` | 6 | The Style menu, one style at a time, the count, the no-match message, unknown styles and page links |
| `SortTests` | 6 | The three sort orders, newest first by default, unknown values and keeping the choices across pages |
| `SearchTests` | 7 | The search box, part of a name in any case, search and style together, the message when nothing matches, a search of only spaces, the search kept in the box and the page links, and a search shown as text, not run as code |
| `ErrorPageTests` | 3 | The custom 404 and 403 pages, with links back, in the site's style |
| **Total** | **85** | **All pass** |

### Code validation

**HTML.** Every page of the live site was checked with the
[W3C Markup Validation Service](https://validator.w3.org/nu/) (the Nu Html
Checker, version 26.11.1) on 2 November 2026: **no errors or warnings on any
page**. Pages anyone can open were checked by address (Check by address), and
the 404 page by address with "Check error pages" turned on. Pages behind the
login were checked by pasting their source (Check by text input), with the
CSRF token's value taken out first, because it's a secret that belongs to my
logged-in session. The 403 page can only be reached with a second account, so
it was checked on the copy of the site instead (Nu Html Checker 26.10.12),
also with no errors or warnings.

| Home (by address) | All rings (by address) |
| :---: | :---: |
| <img src="docs/validation/html-home.webp" alt="W3C result for the home page: no errors or warnings" width="420"> | <img src="docs/validation/html-all-rings.webp" alt="W3C result for All rings: no errors or warnings" width="420"> |
| **A search, `/rings/?q=marquise` (by address)** | **Ring page (by address)** |
| <img src="docs/validation/html-search.webp" alt="W3C result for a search: no errors or warnings" width="420"> | <img src="docs/validation/html-ring-page.webp" alt="W3C result for a ring page: no errors or warnings" width="420"> |
| **Register (by address)** | **Log in (by address)** |
| <img src="docs/validation/html-register.webp" alt="W3C result for Register: no errors or warnings" width="420"> | <img src="docs/validation/html-login.webp" alt="W3C result for Log in: no errors or warnings" width="420"> |
| **404 page (by address, error pages on)** | **My rings (text input)** |
| <img src="docs/validation/html-404.webp" alt="W3C result for the 404 page: no errors or warnings" width="420"> | <img src="docs/validation/html-my-rings.webp" alt="W3C result for My rings: no errors or warnings" width="420"> |
| **Add a ring (text input)** | **The form with mistakes (text input)** |
| <img src="docs/validation/html-add-ring.webp" alt="W3C result for Add a ring: no errors or warnings" width="420"> | <img src="docs/validation/html-form-errors.webp" alt="W3C result for the form with mistakes: no errors or warnings" width="420"> |
| **Edit ring (text input)** | **Delete confirm page (text input)** |
| <img src="docs/validation/html-edit-ring.webp" alt="W3C result for Edit ring: no errors or warnings" width="420"> | <img src="docs/validation/html-delete-confirm.webp" alt="W3C result for the delete confirm page: no errors or warnings" width="420"> |
| **Ring page as its owner, with the delete box (text input)** | **Log out (text input)** |
| <img src="docs/validation/html-ring-page-owner.webp" alt="W3C result for the owner's ring page with the delete box: no errors or warnings" width="420"> | <img src="docs/validation/html-logout.webp" alt="W3C result for Log out: no errors or warnings" width="420"> |

**CSS.** `static/css/style.css` was checked by address with the
[W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) (CSS level
3 + SVG): **no errors**. It shows 13 warnings, all the same: "Due to their
dynamic nature, CSS variables are currently not statically checked." That's
the validator saying it can't check colours written as CSS variables, such as
`var(--rk-gold)`; it isn't a mistake in the CSS. Bootstrap's CSS comes from a
CDN and isn't my code, so it wasn't checked.

<img src="docs/validation/css.webp" alt="W3C CSS Validator: Congratulations! No Error Found." width="420">


**Python.** Every Python file passes **flake8 with no problems** (flake8 7.4,
which runs pycodestyle, the PEP 8 checker the
[Code Institute Python Linter](https://pep8ci.herokuapp.com/) uses, and
pyflakes). Lines are 79 characters or fewer. Django's migration files are
left out, because Django writes them. The settings are in `.flake8`.

**JavaScript.** There's no custom JavaScript to check with JSHint: the menu,
the delete box and the closing messages use Bootstrap's own script.

### PageSpeed Insights and Lighthouse

[PageSpeed Insights](https://pagespeed.web.dev/) runs Lighthouse on Google's
servers. It was run on the live site on 2 November 2026 for the three pages
anyone can open: the home page, All rings and a ring page.

| Page | Device | Performance | Accessibility | Best practices | SEO |
| --- | --- | ---: | ---: | ---: | ---: |
| Home | Mobile | 99 | 100 | 100 | 100 |
| Home | Desktop | 100 | 100 | 100 | 100 |
| All rings | Mobile | 96 | 100 | 100 | 100 |
| All rings | Desktop | 100 | 100 | 100 | 100 |
| Ring page | Mobile | 75 | 100 | 100 | 100 |
| Ring page | Desktop | 100 | 100 | 100 | 100 |

| | Mobile | Desktop |
| --- | :---: | :---: |
| **Home** | <img src="docs/pagespeed/home-mobile.webp" alt="PageSpeed Insights for the home page on mobile: 99, 100, 100, 100" width="380"> | <img src="docs/pagespeed/home-desktop.webp" alt="PageSpeed Insights for the home page on desktop: 100, 100, 100, 100" width="380"> |
| **All rings** | <img src="docs/pagespeed/all-rings-mobile.webp" alt="PageSpeed Insights for All rings on mobile: 96, 100, 100, 100" width="380"> | <img src="docs/pagespeed/all-rings-desktop.webp" alt="PageSpeed Insights for All rings on desktop: 100, 100, 100, 100" width="380"> |
| **Ring page** | <img src="docs/pagespeed/ring-page-mobile.webp" alt="PageSpeed Insights for a ring page on mobile: 75, 100, 100, 100" width="380"> | <img src="docs/pagespeed/ring-page-desktop.webp" alt="PageSpeed Insights for a ring page on desktop: 100, 100, 100, 100" width="380"> |

**Why the ring page scores 75 on phones.** The photo has no set height, so
the page is first drawn without it, and the name, price and details jump down
when the photo arrives. PageSpeed Insights measured a Cumulative Layout Shift
of 0.476 (0.1 or less counts as good). On desktops the photo sits beside the
details, so nothing moves (0.008) and the score is 100. The fix is in
[Known issues](#bugs).

PageSpeed Insights also suggested removing the Bootstrap CSS the site doesn't
use (about 31 KB) and loading the CSS without holding up the first paint
(about 0.13 seconds). Both are ideas for later.

**Signed-in pages.** PageSpeed Insights can't log in, so Add a ring and My
rings were checked with Lighthouse 12.2.1 in Chromium 141, logged in, on a copy
of the site running the way it runs on Heroku: DEBUG off and static files
served by WhiteNoise.

| Page | Device | Performance | Accessibility | Best practices | SEO |
| --- | --- | ---: | ---: | ---: | ---: |
| Add a ring | Mobile | 94 | 100 | 100 | 100 |
| Add a ring | Desktop | 100 | 100 | 100 | 100 |
| My rings | Mobile | 95 | 100 | 100 | 100 |
| My rings | Desktop | 100 | 100 | 100 | 100 |

### Accessibility

- **axe-core 4.10.2** checked 24 page states with its WCAG 2.0, 2.1 and 2.2
  A and AA rules, including the open phone menu, the open delete box, the
  form with errors, and the home page with the Christmas snow on a laptop, on
  a phone and with animations turned off. It found **no problems**.
- **PageSpeed Insights** scores 100 for accessibility on every page it
  checked on the live site, on mobile and desktop, and Lighthouse scores 100
  on the signed-in pages.
- **Colour contrast:** every text colour pair meets WCAG AA. The lowest is
  dark gold on champagne at 4.9:1. The full table is in
  [Surface: design](#surface-design).
- **Keyboard:** the first Tab press shows "Skip to main content", and Enter
  moves to the page's content. Links, buttons and form fields show a clear
  focus outline. The delete box opens with Enter, keeps the focus inside, and
  closes with Escape.
- **Moving content:** after the skip link, the first Tab press reaches the
  Pause the snow switch, which shows a gold focus outline. Space stops all 50
  snow animations, and pressing the switch again starts them. With "Reduce
  motion" turned on, no snow falls and the switch is hidden.

### Responsiveness

Every page was checked in the browser at 320, 375, 768, 1024 and 1440 pixels
wide: 17 pages and page states, plus the open phone menu, the open delete box
and the form with errors on a 320px phone. That's 88 checks, and nothing
scrolls sideways in any of them.

| Width | Menu | Ring cards per row | Result |
| --- | --- | :---: | --- |
| 320px (small phone) | Folded into a button | 1 | Nothing scrolls sideways |
| 375px (phone) | Folded into a button | 1 | Nothing scrolls sideways |
| 768px (tablet) | Folded into a button | 2 | Nothing scrolls sideways |
| 1024px (laptop) | Full navbar | 3 | Nothing scrolls sideways |
| 1440px (desktop) | Full navbar | 3 | Nothing scrolls sideways |

A ring with a 77-letter name and a long web address in its description also
wraps neatly, without pushing the page sideways. Form fields use 16px text,
so iPhones don't zoom in, and the price box is set to open a number keypad
on phones.

### Browser testing

| Browser | Device | Result |
| --- | --- | --- |
| Chrome (Chromium 141) | Desktop | Every page and feature works |
| Chrome (Chromium 141), device mode | Phone and tablet sizes | Every page and feature works |
| Chrome on Windows, the live site | Desktop, phone and tablet sizes | Every page and feature works; the screenshots in this README were taken there |

The site only uses standard HTML and CSS and Bootstrap 5.3, which supports
the latest versions of Chrome, Edge, Firefox and Safari on desktops and
phones.

### Testing the user stories

Each user story was tested in the browser against its acceptance criteria,
on a copy of the site with sample rings and test accounts (amy, ben and a
staff account). The main stories were then checked again on the live site,
where the screenshots come from.

| Story | Test | Expected result | Result |
| --- | --- | --- | --- |
| US01 Register | Logged out, click Register in the navbar | A form asking for a username, an optional email and the password twice | Pass |
| US01 Register | Type two different passwords and submit | "You must type the same password each time." under the second password, and no account is made | Pass |
| US01 Register | Register with a new username and matching passwords | Signed in, on the home page, with "Successfully signed in as newuser." | Pass |
| US02 Log in and out | Log in with a correct username and password | The home page, with "Successfully signed in as amy." | Pass |
| US02 Log in and out | Log in with a wrong password | "The username and/or password you specified are not correct." and still logged out | Pass |
| US02 Log in and out | Click Log out | "Are you sure you want to log out?" first; after Log out, the home page with "You have signed out." | Pass |
| US03 Login state | Look at the navbar logged out, signed in and as staff | Log in and Register; then "Signed in as amy" and Log out; staff also see Admin | Pass |
| US04 Browse | Open All rings | A card for each ring with its photo or drawing, name, style, metal and price, and "12 rings" | Pass |
| US04 Browse | With 12 rings, look at the bottom of the page | Nine rings, "Page 1 of 2" and Next; page 2 has three rings and Previous | Pass |
| US04 Browse | Open All rings with no rings in the database | "No rings yet. When people add rings, you'll see them here." | Pass |
| US05 Ring page | Click a ring card | The ring's page with its photo, name, price, style, metal, gemstone, description, who added it and when | Pass |
| US05 Ring page | Open a ring without a photo | A drawing of its style instead | Pass |
| US05 Ring page | Open `/rings/no-such-ring/` | The 404 page | Pass |
| US06 Add a ring | Logged out, look at the navbar, then open `/rings/add/` | No Add a ring link; sent to log in, then back to the form after logging in | Pass |
| US06 Add a ring | Add a solitaire ring with "No gemstone" and a price of 0.50 | "Solitaire rings need a gemstone. Choose one, or change the style to Band." and "Ensure this value is greater than or equal to 1.00." under the fields, "Please check the form for errors." at the top, and no ring added | Pass |
| US06 Add a ring | Fix the mistakes, add a photo and submit | The new ring's page with its photo and "Evening Star has been added." | Pass |
| US06 Add a ring | Add a ring without a photo | It shows a drawing of its style | Pass |
| US07 Edit | Open my own ring, then someone else's | Edit ring on mine only | Pass |
| US07 Edit | Click Edit ring | The form, filled in with the ring's details | Pass |
| US07 Edit | Change the price to 750 and save, leaving the photo empty | The ring's page with "Evening Star has been updated.", the new price and the same photo | Pass |
| US08 Delete | Click Delete ring, then Keep it | The box closes and the ring is still there | Pass |
| US08 Delete | Click Delete ring, then Delete ring in the box | My rings, with "Evening Star has been deleted." | Pass |
| US08 Delete | Open the ring's `/delete/` address | A confirm page; nothing is deleted until the button is pressed | Pass |
| US09 Keep my rings safe | As another user, open my ring | No Edit or Delete buttons | Pass |
| US09 Keep my rings safe | As another user, type `/rings/aurora/edit/` or `/rings/aurora/delete/` | The 403 page | Pass |
| US09 Keep my rings safe | Logged out, type the same addresses | Sent to log in | Pass |
| US10 Site owner | As staff, open someone else's ring | Edit ring and Delete ring show | Pass |
| US10 Site owner | As staff, edit and then delete someone else's ring | "Little Star has been updated."; then All rings with "Little Star has been deleted." | Pass |
| US10 Site owner | As staff, click Admin, then Rings | Every ring, filters for style, metal and gemstone, and a search box | Pass |
| US11 Any device | Open every page at 320, 375, 768, 1024 and 1440px | The menu folds on phones and tablets, the cards stack, and nothing scrolls sideways | Pass |
| US11 Any device | Look at the price box on a phone-sized screen | It's set to open a number keypad (`inputmode="decimal"`) | Pass |
| US12 Newest rings | Open the home page | The three newest rings, newest first | Pass |
| US12 Newest rings | Click See all rings | All rings | Pass |
| US12 Newest rings | Open the home page with no rings in the database | "No rings yet. Be the first to add one!" | Pass |
| US13 My rings | Look at the navbar logged out, then signed in | My rings only when signed in | Pass |
| US13 My rings | Open My rings | Only my rings, each with Edit and Delete | Pass |
| US13 My rings | Open My rings with a new account | "You haven't added any rings yet." and Add your first ring | Pass |
| US14 Filter | Choose Halo and click Apply | Only halo rings, and "2 rings in the halo style" | Pass |
| US14 Filter | Choose a style with no rings | "No eternity rings yet." and Show all rings, which shows every ring again | Pass |
| US14 Filter | Type `?style=banana` in the address | Every ring, as if no style was chosen | Pass |
| US15 Sort | Choose Price: low to high, then high to low | The rings in price order each way | Pass |
| US15 Sort | Choose a sort order, click Apply, then click Next | Page 2 keeps the sort order, and the style when one is chosen | Pass |
| US15 Sort | Type `?sort=cheapest` in the address | Newest first, as if no order was chosen | Pass |
| US16 Error pages | Open `/rings/no-such-ring/` | The custom 404 page, with links to the home page and the rings | Pass |
| US16 Error pages | Try to edit someone else's ring | The custom 403 page, with links to the rings and My rings | Pass |
| US16 Error pages | Compare both pages with the rest of the site | The same navbar, footer, fonts and colours | Pass |
| US17 Search | Type "marquise" in Search by name and click Apply | The two marquise rings, and "2 rings matching "marquise"" | Pass |
| US17 Search | Search for "sapphire" | "No rings match "sapphire"." and Show all rings, which shows every ring again | Pass |
| US17 Search | Search in capitals, or with a style chosen (automated tests) | The same rings in any case; with a style, only the rings of that style that match | Pass |
| US17 Search | Search, then click Next (automated test) | Page 2 keeps the search, the style and the sort order | Pass |

### Testing the ring picture and the snow

| Test | Expected result | Result |
| --- | --- | --- |
| Open the home page on a laptop or desktop (992px or wider) | The gold ring picture on the right of the hero, clear of the text at every width | Pass |
| Open the home page on a phone or tablet (under 992px) | No ring picture, and the introduction has the full width | Pass |
| Make the browser's text bigger, then open the home page on a laptop | The ring picture hides on narrower screens instead of sitting behind the words | Pass |
| Open the home page between 1 November and 6 January | Snow falls behind the text and the ring, with a Pause the snow switch in the corner | Pass |
| Tab to the switch, then press Space | A gold focus outline round the switch, the switch turns gold, and the snow stops | Pass |
| Click the switch again | The snow starts again | Pass |
| Turn on "Reduce motion" in the device settings | No falling snow and no switch; the snowdrift stays | Pass |
| Open the home page on 31 October or 7 January | No snow and no switch (automated test) | Pass |

### Defensive testing

| What was tried | Expected result | Result |
| --- | --- | --- |
| A visitor opens `/rings/add/`, `/rings/mine/` or a ring's edit or delete address | Sent to log in, then back to that page | Pass |
| Another user sends a POST straight to the edit or delete address of my ring | 403, and the ring isn't changed | Pass |
| A form is sent without its CSRF token | 403 Forbidden, nothing saved | Pass |
| A price of 0, -5 or "abc" is sent straight to the server | "Ensure this value is greater than or equal to 1.00." or "Enter a number." | Pass |
| A photo over 5 MB | "Please choose a photo smaller than 5 MB." | Pass |
| A file Cloudinary can't read | "That file couldn't be uploaded. Please choose a JPG, PNG or WebP photo." (automated test) | Pass |
| `<script>` typed into a description | Shown as plain text, and the script doesn't run | Pass |
| A ring called "Add" | Its address is `/rings/add-ring/`, and `/rings/add/` is still the form | Pass |
| Two rings with the same name | Each gets its own address, such as `aurora-2` (automated test) | Pass |
| A page number that doesn't exist, `/rings/?page=99` | The custom 404 page | Pass |
| Visiting `/accounts/logout/` without pressing the button | Still logged in | Pass |
| `<script>` typed into the search box | Shown as plain text in the box and in the message, and the script doesn't run (automated test) | Pass |
| A search of only spaces | Every ring, as if nothing was typed (automated test) | Pass |

### Links

Every internal link on the main pages was followed as a visitor, as a
signed-in user and as staff: 58 links, all working. Each kind of link was
also checked in the browser:

| Link | Expected | Result |
| --- | --- | --- |
| Brand name in the navbar | The home page | Pass |
| Home, All rings, Add a ring and My rings in the navbar | The right page, with its link underlined | Pass |
| Admin in the navbar (staff only) | The Django admin | Pass |
| Log in, Register and Log out | The right account page | Pass |
| "Create an account" and "Log in" links on the account pages | The other account page | Pass |
| Explore the collection | Scrolls down to the latest rings | Pass |
| See all rings, Show all rings, Browse rings | All rings | Pass |
| Any ring card | That ring's page | Pass |
| Breadcrumb on a ring page | All rings | Pass |
| Edit ring, Cancel | The edit form; Cancel goes back to the ring, or to All rings when adding | Pass |
| Previous and Next | The next or previous page, keeping the style and sort | Pass |
| Buttons on the 403 and 404 pages | The home page, All rings or My rings | Pass |
| radiantkarats.com in the footer | Opens in a new tab | Pass |

### Bugs

**Fixed:**

| Bug | Cause | Fix |
| --- | --- | --- |
| `python manage.py migrate` stopped with "No module named 'cloudinary'", then "No module named 'dj_database_url'" | The packages weren't installed in the virtual environment | Installed them and updated `requirements.txt` |
| On phones, a long ring name, username or link pushed the page sideways and hid the card's price | Long words with no spaces don't wrap by default | Added `overflow-wrap: anywhere` to the body |
| The HTML validator reported an error on the delete box | It had `aria-labelledby` but no role | Added `role="dialog"` |
| The keyboard focus outline disappeared on the page links | Bootstrap's `.page-link:focus` removes the outline | Added a `:focus-visible` outline |
| After the whole card became a link, clicking almost anywhere on the page opened a ring | Bootstrap's stretched link fills the nearest positioned parent | Added `position: relative` to `.ring-card` |
| On phones, the Edit and Delete buttons on My rings overlapped the next card | The cards were set to the full height of their column | Made each column a flex column |
| The alt text and the gemstone message said "a eternity ring" | The style name was put after "a" | Reworded them to "Eternity ring drawing" and "Eternity rings need a gemstone." |
| flake8 reported E303 "too many blank lines" in `views.py` | Extra blank lines and spaces at the end of the file after pasting new code | Removed them |
| From 2 November, two ring pictures would have sat on top of each other in the hero | An earlier try had put the same picture on an empty `hero-note` box as well as on the hero | Removed the `hero-note` box from `index.html`, so only one ring is drawn |

**Known issues:**

- When a ring's photo is replaced, or the ring is deleted, the old photo stays
  in Cloudinary. It doesn't show anywhere on the site. Deleting it is a future
  feature.
- The photo is uploaded while the form is being checked. If the form then has
  another mistake, such as a missing gemstone, the photo has to be chosen
  again, and the first upload stays unused in Cloudinary.
- On phones, the ring page jumps when the photo loads: the photo has no set
  height, so the name, price and details move down once it arrives.
  PageSpeed Insights measured a Cumulative Layout Shift of 0.476, which
  brings the ring page's mobile Performance score down to 75. The fix is to
  keep the photo's space before it loads, for example with
  `aspect-ratio: 1 / 1` and `object-fit: contain` on the photo. On a copy of
  the site, with the photo slowed down on purpose, that brought the layout
  shift from 0.316 to 0.

## Deployment

### Before you start

You need accounts with [GitHub](https://github.com/),
[Heroku](https://www.heroku.com/) and [Cloudinary](https://cloudinary.com/)
(the free plan is enough), and a PostgreSQL database URL, for example from
Code Institute's database tool.

### Fork or clone the repository

- **Fork:** on the [repository](https://github.com/Krishna2414/radiant-karats),
  click **Fork** to make your own copy on GitHub.
- **Clone:** click **Code**, copy the address, and in a terminal run:

  ```
  git clone https://github.com/Krishna2414/radiant-karats.git
  cd radiant-karats
  ```

### Run it on your own computer

1. Make a virtual environment with Python 3.12 and install the packages.
   On Windows (PowerShell):

   ```
   py -3.12 -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

   On a Mac, use `python3.12 -m venv .venv` and `source .venv/bin/activate`.

2. Copy `env_template.py` to a new file called `env.py`, next to
   `manage.py`, and put in your own values. `env.py` is in `.gitignore`, so it
   never reaches GitHub. To use SQLite on your computer, delete the
   `DATABASE_URL` line. To make a secret key, run:

   ```
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

3. Set up the database, make an admin account and start the site:

   ```
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

   Then open http://127.0.0.1:8000/. A superuser is also staff, so it can
   manage every ring.

4. Run the tests with `python manage.py test`.

### Deploy to Heroku

1. In Heroku, choose **New > Create new app**, give it a name and pick the
   Europe region.
2. In Cloudinary, open the dashboard and copy the **API environment
   variable**. Copy only the part that starts with `cloudinary://`, without
   `CLOUDINARY_URL=` in front.
3. In Heroku, open **Settings > Reveal Config Vars** and add:

   | Key | Value |
   | --- | --- |
   | `DATABASE_URL` | Your PostgreSQL database URL |
   | `SECRET_KEY` | A long random string, different from your local one |
   | `CLOUDINARY_URL` | Your Cloudinary API environment variable |

   Don't add `DEBUG`. Without it, DEBUG stays off on the live site.
4. Check that these files are in the repository. Heroku reads them:
   - `requirements.txt`: the Python packages to install.
   - `.python-version`: the Python version (3.12).
   - `Procfile`: `web: gunicorn radiant_karats.wsgi` starts the site, and
     `release: python manage.py migrate --noinput` updates the database on
     every deploy.
5. On the **Deploy** tab, choose **GitHub**, find the repository and click
   **Connect**. Under **Manual deploy**, choose the `main` branch and click
   **Deploy Branch**. Heroku installs the packages, collects the static
   files (WhiteNoise serves them), and runs the migrations.
6. Make the site owner's account: open **More > Run console** and run
   `python manage.py createsuperuser`. You can also run it on your own
   computer with the live `DATABASE_URL` in `env.py`.
7. Click **Open app** and check the site. Open a page that doesn't exist: the
   custom 404 page, not Django's yellow error page, shows that DEBUG is off.

To deploy new commits, click **Deploy Branch** again, or turn on **Enable
Automatic Deploys**.

### Keeping secrets safe

- The secret key, the database URL and the Cloudinary URL only come from
  environment variables, never from the code.
- `env.py` is listed in `.gitignore`, so it's never committed.
- DEBUG is only on when the `DEBUG` variable is exactly `True`, so the live
  site runs with it off.
- `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` only allow Heroku, Code
  Institute's IDE and my own computer.

## AI tools

I used Claude, Anthropic's AI assistant, throughout this project. This is how
I used it, and what I learned.

**Debugging.** When something broke, I sent Claude the error message or a
screenshot, and it explained the cause before the fix. For example, it found
that `migrate` failed because packages were missing from my virtual
environment, that flake8's E303 error came from blank lines I'd pasted at the
end of `views.py`, and that long ring names pushed the page sideways on
phones. Most fixes were small, but I wouldn't have found some of the causes
quickly on my own.

**Performance and user experience.** AI suggested many of the details that
make the site faster and easier to use: Cloudinary sending photos as WebP
(`f_auto` and `q_auto`), lazy-loading the card images, colours that pass
contrast checks, a number keypad for the price on phones, whole cards as
links, a confirmation before deleting, and keeping the filter and sort when
changing page.

## Credits

### Code

- Code Institute's Codestar blog walkthrough: the project set-up, accounts
  with allauth, Cloudinary and deployment to Heroku.
- [Django documentation](https://docs.djangoproject.com/en/4.2/): class-based
  views and pagination, forms and validation, model constraints, custom
  error pages and testing.
- [django-allauth documentation](https://docs.allauth.org/): account settings
  and template overrides.
- [Bootstrap 5.3 documentation](https://getbootstrap.com/docs/5.3/): the
  navbar, cards, stretched link, modal, pagination and grid.
- [Cloudinary documentation](https://cloudinary.com/documentation/django_integration):
  photo uploads, and `f_auto` and `q_auto` for smaller images.
- [MDN Web Docs](https://developer.mozilla.org/): `overflow-wrap`,
  `inputmode`, `animation-play-state` and `prefers-reduced-motion`.
- [W3C, Understanding WCAG 2.2: Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html):
  why the snow needs a way to stop it.
- Claude (Anthropic): help with the code, the tests and this README, as
  described in [AI tools](#ai-tools).

### Content

- The text on the site was written for this project.
- The rings in the screenshots are the rings on the live site, added
  through the site's Add a ring form.

### Media

- The ring drawings, the gold ring in the home page hero, the snowflake and
  the favicon are SVG files made with Claude for this project.
- The ring photos on the live site were uploaded through the Add a ring form
  and are stored on Cloudinary.
- The wireframes, the ERD, the colour palette and the mockup were made with
  Claude for this README.
- Fonts: [Cormorant Garamond](https://fonts.google.com/specimen/Cormorant+Garamond)
  and [Lato](https://fonts.google.com/specimen/Lato), from Google Fonts.

### Acknowledgements

- Tim, my Code Institute facilitator, for his advice on keeping the project
  simple and focused.