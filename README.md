# SPIN USM Bubble Run — Streamlit edition

An English event site managed through GitHub. No database, paid disk, or
website admin password is needed. The original recruitment poster is preserved.
The main button opens https://forms.gle/ToiAGNVwjLzkHAJq9.
All eight future sections start as Coming soon.

## Deploy

1. Create a GitHub repository and upload the CONTENTS of this folder.
   streamlit_app.py, content.json and requirements.txt must be at the root;
   images/poster.png must remain inside images/.
2. Open https://share.streamlit.io/ and sign in with GitHub.
3. Select Create app and choose your repository, branch (usually main),
   and main file path: streamlit_app.py.
4. Select Python 3.12 in Advanced settings if a version choice is offered.
5. Deploy. Community Cloud installs requirements.txt.
6. Configure the app's sharing setting so your intended audience can view it.
   Test the public link in a signed-out/private browser window before sharing.
   A private GitHub repository and a public app are different settings.
7. Keep the .streamlit/config.toml file for the dark theme. GitHub web upload
   may skip hidden folders; create this file manually if necessary.

No Render configuration should be uploaded with this project.
No website has been deployed by creating this ZIP.

## Edit content on GitHub

Edit content.json, then Commit changes to the SAME branch connected to the app.
Community Cloud updates the application from that branch. Wait for the update
to complete, then refresh your browser. This is not an instant database update.

- poster.file: image path, e.g. images/poster.png
- poster.visible: true displays the poster; false hides it.
- poster.caption / poster.alt: update these when changing poster purpose.
- registration_url: the main application link.
- registration_label / category: update when the main campaign changes.
- announcements: list of objects with date, title, body; top items appear first.
- sections.KEY.published: false shows Coming soon; true shows your content.
- sections.KEY.body: text (use \n inside a string for a line break).
- sections.KEY.images: list of paths inside images/.
- sections.KEY.link: optional https:// URL; run_registration uses a distinct URL.
- updated: optional display text, for example 13 November 2026.
  This is an editorial label, not an automatically recorded timestamp.

Available section keys:
schedule, route, tshirt, medal, posters, photos, faq, run_registration.

You can publish multiple images in the posters/photos sections.
Published sections require text, images or a link. FAQ uses plain text;
you can include several questions and answers separated by \n\n.
Blank registration_url hides the main registration buttons.
Taking down a poster does not delete it from the repository or Git history.
Repository images are public if the repository is public. Do not include
personal registration records, passwords, or private documents.

## Upload a new poster

Upload a PNG, JPG or WebP to images/, then change poster.file in content.json
to the exact case-sensitive path. Commit both changes. A new filename is
recommended. Update alt text, caption, category and links where appropriate.
Do not rename a JPG extension to PNG. Each image should be under 10 MB;
optimize large photo galleries to keep page loads reasonable.

## Local preview (optional)

Requires Python 3.11+ and internet for initial dependency installation.
Open PowerShell in this folder and run:
powershell -NoProfile -ExecutionPolicy Bypass -File .\Start.ps1

Or:
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py

The default local address is http://localhost:8501.
Ctrl+C stops the server. Cloud visitors do not depend on this local server.
Before committing, optional content validation:
python site_content.py

## Updating and troubleshooting

The app re-reads deployed content every 30 seconds in an active browser session.
This interval does NOT make GitHub deploys instantaneous. Cloud sync or a
redeploy must finish first. If necessary refresh the browser after deployment.
For invalid JSON or missing images, the app shows a neutral notice; an existing
session may retain its last valid page. Check the Cloud logs, fix the file,
and commit again. Do not assume malformed changes have published.
JSON needs double quotes, true/false without quotes, and no trailing commas.
Content should be English if you want the site to remain fully English.

This edition has no /admin page and does not accept browser uploads.
Content is retained in GitHub, so runtime filesystem resets do not erase it.
Community Cloud free hosting is subject to its current resource and inactivity
limits. The site is not designed as a payment or registration-record system.
The Google Form handles applications separately.
Python code changes are needed only for new layout/behavior beyond the
provided sections.

Official documentation:
https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app
