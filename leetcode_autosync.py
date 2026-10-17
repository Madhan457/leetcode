
import os
import json
import re
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
SOLUTIONS_DIR = BASE_DIR / "solutions"
SOLUTIONS_DIR.mkdir(exist_ok=True)

load_dotenv(BASE_DIR / ".env")

LEETCODE_SESSION = os.getenv("LEETCODE_SESSION", "").strip()
CSRF_TOKEN = os.getenv("LEETCODE_CSRF_TOKEN", "").strip()

GRAPHQL_URL = "https://leetcode.com/graphql/"

RECENT_SUBMISSIONS_QUERY = """
query recentAcSubmissions($username: String!, $limit: Int!) {
    recentAcSubmissionList(username: $username, limit: $limit) {
        id
        title
        titleSlug
        timestamp
        lang
    }
}
"""

SUBMISSION_DETAILS_QUERY = """
query submissionDetails($submissionId: Int!) {
    submissionDetails(submissionId: $submissionId) {
        code
        lang {
            name
            verboseName
        }
        question {
            titleSlug
        }
    }
}
"""


def create_session():
    session = requests.Session()

    session.headers.update({
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com/",
        "Origin": "https://leetcode.com",
        "User-Agent": "Mozilla/5.0",
    })

    session.cookies.set(
        "LEETCODE_SESSION",
        LEETCODE_SESSION,
        domain="leetcode.com",
    )
    session.cookies.set(
        "csrftoken",
        CSRF_TOKEN,
        domain="leetcode.com",
    )
    session.headers["x-csrftoken"] = CSRF_TOKEN

    return session


def graphql(session, query, variables):
    response = session.post(
        GRAPHQL_URL,
        json={
            "query": query,
            "variables": variables,
        },
        timeout=30,
    )

    print("HTTP status:", response.status_code)
    response.raise_for_status()

    result = response.json()

    if result.get("errors"):
        messages = [
            error.get("message", "Unknown GraphQL error")
            for error in result["errors"]
        ]
        raise RuntimeError("; ".join(messages))

    return result.get("data") or {}


def safe_filename(name):
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    return name.strip(" .") or "solution"


def main():
    if not LEETCODE_SESSION or not CSRF_TOKEN:
        print("Missing LeetCode credentials in .env.")
        print("Check LEETCODE_SESSION and LEETCODE_CSRF_TOKEN.")
        return

    username = input("LeetCode username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    session = create_session()

    try:
        data = graphql(
            session,
            RECENT_SUBMISSIONS_QUERY,
            {
                "username": username,
                "limit": 20,
            },
        )

        submissions = data.get("recentAcSubmissionList") or []

        print("Found submissions:", len(submissions))

        metadata_file = SOLUTIONS_DIR / "submissions.json"
        metadata_file.write_text(
            json.dumps(submissions, indent=2),
            encoding="utf-8",
        )

        java_submissions = [
            item for item in submissions
            if "java" in str(item.get("lang", "")).lower()
        ]

        print("Java submissions:", len(java_submissions))

        downloaded = 0

        for submission in java_submissions:
            submission_id = submission.get("id")
            title = submission.get("title", "solution")
            slug = submission.get("titleSlug", title)

            try:
                detail_data = graphql(
                    session,
                    SUBMISSION_DETAILS_QUERY,
                    {"submissionId": int(submission_id)},
                )

                details = detail_data.get("submissionDetails")

                if not details:
                    print(
                        "Source unavailable:",
                        title,
                        "(submission ID:",
                        submission_id,
                        ")",
                    )
                    continue

                code = details.get("code")

                if not code:
                    print("No source code returned:", title)
                    continue

                language = details.get("lang") or {}
                language_name = language.get("name", "")

                if "java" not in language_name.lower():
                    print("Skipping non-Java source:", title)
                    continue

                filename = (
                    f"{safe_filename(slug)}_{submission_id}.java"
                )
                output_file = SOLUTIONS_DIR / filename

                output_file.write_text(code, encoding="utf-8")
                print("Saved:", output_file.name)
                downloaded += 1

                time.sleep(0.5)

            except (ValueError, requests.RequestException, RuntimeError) as error:
                print("Download failed:", title, "-", error)

        print()
        print("Download complete.")
        print("Java files downloaded:", downloaded)
        print("Output folder:", SOLUTIONS_DIR)

    except requests.RequestException as error:
        print("Request failed:", error)
        print("Check your internet connection and LeetCode login cookies.")
    except (ValueError, RuntimeError) as error:
        print("LeetCode API error:", error)


if __name__ == "__main__":
    main()
