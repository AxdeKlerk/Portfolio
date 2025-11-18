## Security Error

**Bug:**  
I accidentally committed my `.env` file to **Github**, which contained my **Django** `SECRET_KEY` and **Cloudinary** API credentials. Even after adding `.env` to `.gitignore`, the secrets were still visible in the repository’s history because Git continues tracking files that were already committed before being ignored.

**Fix:**  
I permanently removed all sensitive data from Git history using the `git filter-repo` tool. The exact steps I followed were:

    git filter-repo --invert-paths --path .env

Then I force-pushed the cleaned history to overwrite the remote repository:

    git push origin main --force

After that, I confirmed `.env` was gone from **Github** but noticed that any new commits were still picking it up. I realized Git was still tracking the file locally. To stop this, I ran:

    git rm --cached .env
    git add .gitignore
    git commit -m "Remove .env from tracking and ensure it's ignored"

Next, I regenerated new secret keys and updated my `.env` file with fresh credentials:

    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

I also logged into **Cloudinary** to regenerate my API key and secret under “Account Details,” then updated the `.env` accordingly.

Finally, I verified the `.env` file was listed under “Untracked files” in `git status` and confirmed it was no longer visible on **Github**. 

To make sure my database wasn’t exposed either, I removed it too:

    git rm --cached db.sqlite3
    echo "*.sqlite3" >> .gitignore
    git add .gitignore
    git commit -m "Remove .env and database from repo tracking and update .gitignore"
    git push origin main --force

**Lesson Learned:**  
Once a file is committed to Git, simply adding it to `.gitignore` does not remove it from history. I learned that sensitive files like `.env` and `db.sqlite3` must be explicitly untracked and purged from the repository’s commit history. It’s also vital to regenerate new keys after exposure, since even deleted secrets in **Github** history can be recovered unless the history is fully rewritten. Now `.env` and `.sqlite3` are permanently ignored and my **Django** project is secure.

---

## Security Cleanup (Round 2)

**Bug:**  
After my first cleanup, my old **Django** `SECRET_KEY` and **Cloudinary** API credentials were still buried in the **Github** commit history. Even though `.env` was ignored, those earlier commits still contained sensitive data that hadn’t been completely removed. This meant anyone could technically recover the exposed keys by checking past commits.

**Fix:**  
I used `git filter-repo` again to surgically remove all traces of my `.env` file and any previous versions of `config/settings.py` that contained embedded keys. The exact commands were:

    git filter-repo --path .env --path config/settings.py --invert-paths

Then I force-pushed the cleaned history back to **Github**:

    git push origin main --force

Finally, I verified everything was gone using:

    git log -p | findstr SECRET_KEY

The only remaining line referred to the text inside my `DEBUGGING.md` entry, which was safe.  
No active keys were found in the repository or history.

**Lesson Learned:**  
Rewriting Git history is the only reliable way to permanently remove exposed secrets. Simply deleting a file or adding it to `.gitignore` doesn’t fix older commits. I now always confirm the clean state with a search before making any new commits.

---

## VS Code Configuration to Permanently Hide .env

**Bug:**  
Even after cleaning my **Github** history, **VS Code** kept showing `.env` under *Changes (U)* in the Source Control panel. When I clicked “Commit All,” it re-added the `.env` file even though it was listed in `.gitignore`. This was caused by VS Code’s new behaviour of displaying untracked files by default.

**Fix:**  
I modified my global **VS Code** `settings.json` file to permanently hide `.env` files from the Explorer, Source Control, and Search panels. This restored the older behaviour that my previous projects used.  
I opened my User Settings (JSON) and replaced the content with a single valid JSON block:

    {
        "git.untrackedChanges": "hidden",
        "files.exclude": {
            "**/.env": true
        },
        "search.exclude": {
            "**/.env": true
        }
    }

After saving and restarting VS Code, `.env` disappeared from the interface completely, but the file still existed locally and was still read by **Django**.

**Lesson Learned:**  
VS Code now shows ignored files by default, which can easily lead to accidental commits. Hiding `.env` globally prevents this without affecting functionality. I can still edit the file anytime by pressing `Ctrl + P`, typing `.env`, and pressing Enter. This setup ensures `.env` is protected both visually and technically from accidental exposure.

---

## Database Integrity Error

**Bug:**  
When I added the new `slug` field to my `Blog` model in **Django**, migrations failed with the error:  
`django.db.utils.IntegrityError: UNIQUE constraint failed: portfolio_blog.slug`.  

This happened because existing blog entries in the database had no slugs yet, and **Django** tried to insert empty strings (`""`) into a field marked as `unique=True`. Since all rows had the same empty value, the database rejected it.

**Fix:**  
I removed the `unique=True` constraint temporarily to allow the field to be added safely. Then I recreated the migration so the database schema matched the model. To confirm that the `slug` column didn’t exist before regenerating migrations, I used a **SQLite** `PRAGMA` check in the shell:

    from portfolio.models import Blog
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("PRAGMA table_info(portfolio_blog);")
    print(cursor.fetchall())

The output showed there was no `slug` column. After deleting the broken migration, I created a fresh one and ran `makemigrations` and `migrate` again. Once the `slug` column appeared in the `PRAGMA` output, I populated slugs manually:

    from portfolio.models import Blog
    from django.utils.text import slugify

    for post in Blog.objects.all():
        if not post.slug:
            post.slug = slugify(post.title)
            post.save()

After confirming that each blog post had a proper slug, I re-enabled `unique=True` and migrated again. This ensured that all future slugs remain unique while avoiding duplicate constraint errors.

**Lesson Learned:**  
Adding a `unique=True` field to a model that already contains data can cause migration errors if existing rows don’t have values. The safe approach is to first create the field without uniqueness, populate it, and only then enforce uniqueness. This two-step migration avoids data conflicts and keeps both **Django** and the database schema in sync.

---

## Deploying to Render Errors

### Runtime Error — Missing `Procfile` and `runtime.txt`

**Bug:**  
When I first attempted to deploy my **Django** portfolio project to **Render**, the build failed because the service didn’t know how to start the app or what Python version to use. The logs showed errors like `ModuleNotFoundError` and missing runtime configuration.

**Fix:**  
I created two files at the project root (same level as `manage.py`):
    `Procfile`
    `web: gunicorn config.wsgi:application`

and
    `runtime.txt`
    `python-3.12.1`

Then I committed and pushed them to **Github** so **Render** could install dependencies and start **Gunicorn** correctly.

**Lesson Learned:**  
**Render** needs both a `Procfile` and a `runtime.txt` to identify the entry point and Python version for any **Django** deployment. Without them, the app can’t start.

---

### Configuration Error — `ModuleNotFoundError: No module named 'config.settings'`

**Bug:**  
After deployment, **Render** couldn’t find my settings file, even though `config/settings.py` existed. The log showed `ModuleNotFoundError: No module named 'config.settings'`.

**Fix:**  
The issue was that **Render** wasn’t working from the correct directory. I edited the `Procfile` to include a working directory change:

    web: cd Portfolio && gunicorn config.wsgi:application

Once committed and pushed, **Render** could locate the **Django** settings module correctly and continue the build process.

**Lesson Learned:**  
When using **Render**, the service sometimes runs from a directory above your project root. Adding `cd <project-folder>` in the `Procfile` ensures **Gunicorn** starts in the right place.

---

### Configuration Error — Missing `STATICFILES_STORAGE`

**Bug:**  
After fixing the startup path, the next build failed with this error:  
`AttributeError: 'Settings' object has no attribute 'STATICFILES_STORAGE'`.

**Fix:**  
I added the missing setting to `config/settings.py`:

    STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticCloudinaryStorage'

Then I redeployed, and the error disappeared.

**Lesson Learned:**  
When using **Cloudinary**, `STATICFILES_STORAGE` must be defined so **Django** knows where to store static and media files.

---

### Configuration Error — Missing `STATIC_ROOT`

**Bug:**  
After adding **Cloudinary** storage, the build failed again with:  
`You're using the staticfiles app without having set the STATIC_ROOT setting to a filesystem path.`

**Fix:**  
I added this line to `config/settings.py` above the static URL definition:

    STATIC_ROOT = BASE_DIR / 'staticfiles'

This gave **Django** a path to collect static files into before uploading or serving.

**Lesson Learned:**  
**Django** always requires a physical path for `STATIC_ROOT`, even if you’re using a remote storage backend.

---

### Deployment Error — `DisallowedHost`

**Bug:**  
Once the app built successfully, **Render** displayed a `DisallowedHost` error on the live site because my deployment URL wasn’t listed in `ALLOWED_HOSTS`.

**Fix:**  
I updated `ALLOWED_HOSTS` in `settings.py` to include **Render**’s autogenerated domain:

    ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'portfolio-5y32.onrender.com']

After pushing the change, **Render** auto-deployed and the site became accessible.

**Lesson Learned:**  
**Django** strictly checks hostnames for security. Always add your live domain or subdomain to `ALLOWED_HOSTS` when deploying.

---

### Static File Error — 404 for `/static/...` Paths

**Bug:**  
The site loaded but none of the static images or CSS appeared. The browser console showed 404 errors for `/static/...` assets.

**Fix:**  
The issue was caused by missing *Whitenoise* configuration and a missing slash in `STATIC_URL`.  
I changed:

    STATIC_URL = 'static/'

to:

    STATIC_URL = '/static/'

Then I installed `Whitenoise`:

    pip install whitenoise

and updated `settings.py`:

- Added `'whitenoise.middleware.WhiteNoiseMiddleware'` after `'django.middleware.security.SecurityMiddleware'`
- Added:

        STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

Finally, I committed and redeployed. The static images and CSS began loading correctly.

**Lesson Learned:**  
*Whitenoise* is the simplest and most reliable way to serve static files directly from **Render** when using **Django**. It compresses and caches them automatically.

---

### Final Configuration — Hybrid Storage (Whitenoise + Cloudinary)

**Bug:**  
After switching everything to *Whitenoise*, images uploaded to **Cloudinary** through the admin were no longer accessible because **Cloudinary** handling had been fully disabled.

**Fix:**  
I used a hybrid setup in `settings.py` so *Whitenoise* served static assets and **Cloudinary** continued handling uploaded media:

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

After redeploying, both static and uploaded images appeared as expected.

**Lesson Learned:**  
For portfolio or small production sites, the ideal setup is:
- *Whitenoise* for static files (`/static/`)
- **Cloudinary** for uploaded media  
This combination keeps performance high and setup simple.

---

### Build Performance Note — Render Speed vs. **Heroku**

**Bug:**  
Deployment took significantly longer on **Render** compared to **Heroku**, especially for first-time builds.

**Fix:**  
No code fix required — this delay is caused by **Render**’s container initialization and free-tier sleep/wake behavior. Subsequent deployments and requests run faster after caching.

**Lesson Learned:**  
**Render**’s free plan trades startup speed for cost savings. Use “Manual Deploy” only when necessary, and expect first builds to take several minutes. Once cached, the system runs efficiently.

---

## Remote: Internal Server Error

**Bug:**  
I tried to push to **Github** and received:
`remote: Internal Server Error` followed by `! [remote rejected] main -> main (Internal Server Error)`. The push failed even though my remote was reachable and credentials were fine.

**Fix:**  

**What I Saw (Symptoms):**  
- Push to **Github** failed with `Internal Server Error`.  
- No local Git errors; only the remote rejected the update.

**Diagnostics (Step-by-step):**  

**Step 1 — Confirm local repo state**  
I checked the working tree and remote config to rule out local issues.
    
    git status
    git remote -v

Result: clean working tree; remote URL pointed to my repo on **Github**.

**Step 2 — Verify remote availability**  
I confirmed the remote was reachable and the branch existed.

    git ls-remote origin

Result: returned `HEAD` and `refs/heads/main` hashes successfully (so **Github** was reachable).

**Step 3 — Check local object health**  
I ran a full integrity check to ensure no corrupt local objects.

    git fsck --full

Result: no issues reported.

**Step 4 — Eliminate transient server hiccup**  
I retried a normal push:

    git push origin main

Result: same `Internal Server Error`. This suggested a branch-specific issue on **Github**, not connectivity.

**Step 5 — Control test with a new branch**  
I created and tried to push a fresh branch to see if **Github** would accept any new refs:

    git checkout -b test-push
    git push origin test-push

Result: **Github** again reported `Internal Server Error` on push; however, the branch list on the website showed that `test-push` had “recent pushes,” confirming the server was intermittently accepting refs but something about `main` remained problematic.

**Step 6 — Resolve by merging healthy history onto main via Pull Request**  
I used the web UI to create a Pull Request from `test-push` into `main`:

    (on Github website)
    base: main  ←  compare: test-push
    Create pull request → Merge pull request → Confirm

Result: `main` was updated to the good history from `test-push`.

**Step 7 — Resync local and verify push works**  
I fast-forwarded my local branch and verified pushes were clean:

    git checkout main
    git pull origin main
    git push origin main

Result: “Everything up-to-date.” Push succeeded without errors.

**Step 8 — Clean up temporary branch**  
I removed the temporary branch locally and on **Github**:

    git branch -d test-push
    git push origin --delete test-push

**Reference Commands Used:**

    git status
    git remote -v
    git ls-remote origin
    git fsck --full
    git push origin main
    git checkout -b test-push
    git push origin test-push
    # (create Pull Request: base main ← compare test-push, then merge on Github)
    git checkout main
    git pull origin main
    git push origin main
    git branch -d test-push
    git push origin --delete test-push

**Lesson Learned:**  
This error pointed to a server-side branch/reference problem on **Github**, not a local Git issue. The safest, path was: 
- verify local health, confirm remote reachability, 
- prove a clean branch can be accepted, 
- then repair `main` via a Pull Request from the healthy branch. 
  
In future, when **Github** returns `Internal Server Error` during `git push`, I’ll: 
1. verify with `git fsck --full` and `git ls-remote origin`, 
2. try a temporary branch push, and 
3. if the issue persists, use a Pull Request to replace `main` with the known-good branch, then resync locally.

---

## File Handling Error

**Bug:**  
I attempted to make the PDF version of my CV downloadable through my **Django** site using a `CloudinaryField`. The PDF either returned a 404, displayed a “Failed to load PDF document” error, or returned a **Cloudinary** 401 access error. Even when the PDF existed in my admin panel, the direct link failed to load. I also noticed that my **Cloudinary** dashboard showed the asset as “Blocked for delivery.” This made it clear that the issue was not with my view, template, or routing, but with how the file was being uploaded and stored.

**Fix:**  
I debugged the issue and confirmed the file was uploading with the wrong **Cloudinary** upload preset. The preset was unintentionally set to `Unsigned`, which caused **Cloudinary** to apply restricted access rules to non-image files, including PDFs. Because of this, PDFs uploaded through **Django** were flagged and not served publicly.

To resolve the issue, I:

1. Went to **Cloudinary** → Settings → Upload → Upload Presets.  
2. Opened the active preset (`hoqrv1uc`) and changed `Signing mode` from `Unsigned` back to `Signed`.  
3. Saved the preset.  
4. Back in **Django**, deleted the previously uploaded CV files from the admin panel so they would be removed from **Cloudinary**.  
5. Re-uploaded the PDF and DOC files using `models.FileField(upload_to='cv/')` instead of a `CloudinaryField`.  
6. Confirmed the new files were stored under `/media/cv/` and served directly by **Django**, avoiding **Cloudinary** restrictions entirely.

After applying these steps, the download links began working correctly and the PDF loaded without errors.

**Lesson Learned:**  
This issue happened because I mixed file handling responsibilities between **Django** and **Cloudinary**. Using `CloudinaryField` for non-image documents can trigger unexpected access restrictions, especially when the upload preset is set to `Unsigned`. For downloadable documents like PDFs, storing them through **Django**’s own `FileField` is more reliable. If I ever rely on **Cloudinary** for file storage again, I should always verify the preset’s signing mode and delivery permissions before uploading.

---

## Environment Variable Loading Error

**Bug:**  
Over the course of three days I attempted to diagnose a series of increasingly confusing and misleading errors caused by **Django** failing to load my environment variables from `.env`. The symptoms appeared unrelated at first: `You must set settings.ALLOWED_HOSTS if DEBUG is False`, `The SECRET_KEY setting must not be empty`, missing attributes like `settings.ENVIRONMENT`, and even failures where `settings.BASE_DIR` did not exist.  

The first signal that something was fundamentally wrong came from the fact that *none* of the expected variables defined in my `.env` file were being read. Running commands such as:

    python manage.py shell -c "from django.conf import settings; print(settings.ENVIRONMENT)"

constantly resulted in errors indicating the attribute did not exist. Any attempt to print settings attributes failed because **Django** never successfully imported the full `config/settings.py` file. The root crash always happened during this line:

    SECRET_KEY = env("SECRET_KEY")

When this line failed, the entire settings module aborted before completion. Because **Django** couldn’t load settings, it silently fell back to `LazySettings`. That fallback state created a chain reaction:

- `ENVIRONMENT` didn’t exist  
- `DEBUG` defaulted to `False`  
- `ALLOWED_HOSTS` didn’t load  
- Template context processors didn’t load  
- Even basic values like `BASE_DIR` and `__file__` weren’t available  
- `manage.py` commands produced misleading secondary errors  

This failure mode made the debugging process extremely difficult because **every error message pointed to the wrong thing**. The problem was not ALLOWED_HOSTS, DEBUG, or any missing attribute — the problem was that settings never finished importing at all.

As I tried to track the cause, the following confusing behaviours appeared:

- Rewriting `.env` had no effect.  
- Deleting `.env` entirely had no effect.  
- Creating a new `.env` file still caused the same corrupted string to appear.  
- Restarting VS Code did not help.  
- Restarting PowerShell did not help.  
- Even rebooting the entire machine did not help.  
- Checking `Env:` in PowerShell showed no system-level `SECRET_KEY`.  
- Checking the Registry showed no `SECRET_KEY`.  
- Searching the entire user directory revealed multiple `.env` files but none contained the corrupted value.  
- `settings.__file__` could not be printed because the module never imported.  
- `from config import settings` always triggered the same error, even after full resets.  

The corrupted value that caused the crash looked like:

    !p5s65i&)@t6kw-^=k=(i0_s7+p@hz(ub$g^x%ur52d#e!1n@

This value did not exist in any `.env` file across my system. It also did not exist in environment variables, registry keys, venv activation scripts, or VS Code launch configurations. Yet **Django** consistently reported that value as the environment variable name it was trying to read, indicating that the first line of `.env` was being parsed incorrectly.

This eventually indicated a deeper issue: the `.env` file inside the project directory was being read incorrectly — not ignored, but read in a corrupted form.

**Fix:**  
The breakthrough came only after isolating the exact place the failure occurred. Importing the settings module directly via:

    python
    >>> from importlib import import_module
    >>> import_module("config.settings")

produced the same corrupted SECRET_KEY error long before **Django** loaded anything else. This confirmed the failure was specifically occurring during the environment-loading phase and not during URL routing, template loading, or any of the other errors I initially suspected.

I then recreated the `.env` file multiple times, but the corrupted value continued to appear. After eliminating every external cause (VS Code extension `.env` files, Windows registry variables, stray project copies, wrong interpreter paths, and backups), the only remaining possibility was that the `.env` file itself contained invisible characters that `django-environ` was failing to interpret.

The file was saved in the wrong **text encoding**, most likely UTF-16 with a hidden BOM (byte-order mark) added by Windows or a previous editor. This meant:

- The first character of `.env` wasn’t actually `S` from `SECRET_KEY=`  
- It was a non-printable BOM  
- `django-environ` interpreted that as part of the variable name  
- It treated the variable name as the corrupted string  
- It failed to match it to any variable defined in memory  
- It threw the `ImproperlyConfigured` error  
- The entire import process halted  

This explained why the corrupted string appeared even after deleting and recreating the file: the new `.env` was still written using the same bad encoding unless explicitly saved as UTF-8.

To fix the problem permanently, I:

1. Deleted the `.env` file entirely.  
2. Created a brand new `.env` file manually inside VS Code.  
3. Used VS Code’s encoding controls to ensure the file was saved as **UTF-8 (no BOM)**.  
4. Inserted the environment variables manually, beginning with `SECRET_KEY=` as the first character in the file.  
5. Regenerated a fresh Django secret key using Python:

        python -c "import secrets, string; chars=string.ascii_letters+string.digits+string.punctuation; print(''.join(secrets.choice(chars) for _ in range(50)))"

6. Saved the `.env` file again, confirming UTF-8 encoding.  
7. Fully restarted VS Code (closing all windows).  
8. Reactivated the virtual environment.  
9. Tested settings import using:

        python manage.py shell -c "from django.conf import settings; print(settings.SECRET_KEY[:10] + '...')"

Once this worked, **Django** finally loaded the `.env` correctly, settings imported fully, and `ENVIRONMENT`, `DEBUG`, and `ALLOWED_HOSTS` all behaved as expected.

A secondary issue appeared afterward: a `ModuleNotFoundError` for `portfolio.context_processors.about_data`. This occurred because the file had been accidentally deleted earlier. I restored it as:

    from .models import About

    def about_data(request):
        try:
            about = About.objects.first()
        except About.DoesNotExist:
            about = None
        return {'about': about}

Restarting the server resolved the final error, and the entire project loaded normally.

**Lesson Learned:**  
When **Django** refuses to load environment variables, and especially when `settings.py` fails at the first call to `env("SECRET_KEY")`, the most important step is to verify the encoding of `.env`. A single file saved with a BOM or incorrect encoding can cause cascading failures that appear unrelated. If `settings.py` fails early, **Django** silently enters `LazySettings`, hiding the real failure and generating misleading errors across unrelated subsystems.
  
From now on, I will always ensure that `.env` files are created as UTF-8 (no BOM), contain no blank lines at the top, and are validated using direct imports (`import_module("config.settings")`). This prevents multi-day debugging cascades caused by hidden characters and ensures **Django** loads the intended configuration each time.

