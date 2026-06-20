# Visitor Management System (Django Admin)

A minimal visitor management system using only Django's built-in admin
interface — no custom frontend needed.

## Models

- **Visitor** — the person checking in (name, phone, email, company, ID proof, photo)
- **Host** — the staff member being visited (name, department, designation, contact info)
- **Visit** — a single visit record linking Visitor + Host, with check-in/check-out
  timestamps, purpose, status, and badge number

## Admin Features

- **Visitors**: searchable/filterable by name, phone, email, company
- **Hosts**: searchable by name/department, active/inactive filter
- **Visits**: filter by status/purpose/host/date, search by visitor or badge
  number, date-drill-down navigation, and a bulk **"Check out selected
  visits now"** action for fast front-desk checkout

---

## Run locally

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open http://127.0.0.1:8000/ (redirects to `/admin/`).

---

## Deploy for free on Render

[Render](https://render.com) offers a free web service tier and a free
PostgreSQL database (free for 90 days, renewable). No credit card required
to start.

### Step 1 — Push this project to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
```

Create a new repo on GitHub (github.com/new), then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### Step 2 — Deploy via Render Blueprint (one click, recommended)

This project includes a `render.yaml` file that auto-configures everything
(web service + free Postgres database + environment variables).

1. Go to https://dashboard.render.com/
2. Sign in (GitHub login is easiest)
3. Click **New** → **Blueprint**
4. Connect your GitHub account and select this repo
5. Render reads `render.yaml` and shows you the plan: one web service +
   one free Postgres database. Click **Apply**.
6. Wait for the build to finish (~2-5 minutes). Render will run `build.sh`
   automatically, which installs dependencies, runs `collectstatic`, and
   runs `migrate`.

### Step 3 — Create your admin login

Once deployed, open the **Shell** tab for your web service in the Render
dashboard and run:

```bash
python manage.py createsuperuser
```

Follow the prompts, then visit `https://your-app-name.onrender.com/admin/`
and log in.

### Manual setup (if you don't want to use the Blueprint)

If you'd rather configure things by hand instead of using `render.yaml`:

1. **New** → **PostgreSQL** → pick the **Free** plan → create it. Copy the
   **Internal Database URL**.
2. **New** → **Web Service** → connect your repo.
   - Runtime: Python 3
   - Build Command: `./build.sh`
   - Start Command: `gunicorn visitor_management.wsgi:application`
   - Plan: Free
3. Under **Environment**, add:
   - `SECRET_KEY` → any long random string
   - `DEBUG` → `False`
   - `DATABASE_URL` → paste the Internal Database URL from step 1
4. Deploy, then open the Shell tab and run `python manage.py createsuperuser`.

---

## Important notes about the free tier

- **Spin-down**: Render's free web services sleep after 15 minutes of
  inactivity. The next visit will take 30-60 seconds to wake back up. This
  is normal on the free tier, not a bug.
- **Ephemeral filesystem**: Anything written to disk (like visitor photo
  uploads via the `photo` field) is **wiped on every redeploy or restart**.
  The database itself is safe (it's a separate Postgres service), but
  uploaded photo *files* are not. For real persistent photo storage, swap
  `MEDIA_ROOT` for a cloud storage backend like
  [Cloudinary](https://cloudinary.com) (has a free tier) using
  `django-cloudinary-storage`. Ask if you'd like this wired up.
- **Free Postgres expiry**: Render's free Postgres databases expire after
  90 days. You'll get an email warning beforehand; you can create a fresh
  one and re-point `DATABASE_URL`, or upgrade to a paid plan to keep it
  permanently.

## Typical workflow

1. Add Hosts once (your staff directory).
2. When someone arrives, add/select a Visitor and create a Visit
   (auto-stamps check-in time).
3. When they leave, select their Visit row in the admin list and run the
   "Check out selected visits now" action (or set check_out_time manually).
