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

