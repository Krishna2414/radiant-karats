"""
Template for env.py, the file that holds your local secrets.

1. Copy this file and name the copy env.py (it's already in .gitignore,
   so it will never be pushed to GitHub).
2. Replace the placeholder values with your own.
3. To use SQLite on your own computer, delete the DATABASE_URL line.
4. CLOUDINARY_URL is only needed to upload design photos. Delete that
   line until you have a Cloudinary account.
"""
import os

os.environ.setdefault("SECRET_KEY", "replace-with-a-long-random-string")
os.environ.setdefault(
    "DATABASE_URL", "postgres://user:password@host:5432/database_name"
)
os.environ.setdefault(
    "CLOUDINARY_URL", "cloudinary://api_key:api_secret@cloud_name"
)
os.environ.setdefault("DEBUG", "True")
