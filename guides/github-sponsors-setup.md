# Setting Up GitHub Sponsors

How to add the "Sponsor this project" button to any GitHub repo and structure a sponsors profile that converts.

---

## Overview

GitHub Sponsors lets you add a funding button to any public repository. Clicking it takes visitors to your GitHub Sponsors profile — or to external funding links you configure. This guide covers:

1. The technical hook (`.github/FUNDING.yml`)
2. What belongs on your Sponsors profile
3. Org-level vs repo-level behavior
4. A replication template you can drop into any project

---

## The Technical Hook: `.github/FUNDING.yml`

This file is all that's required to activate the "Sponsor this project" sidebar button on a GitHub repo.

```yaml
# .github/FUNDING.yml

# GitHub Sponsors (your username)
github: [your-username]

# Optional: additional funding platforms
# patreon: your-patreon-username
# open_collective: your-collective-name
# ko_fi: your-ko-fi-username
# custom: ['https://your-custom-url.com']
```

**Rules:**
- Must live at `.github/FUNDING.yml` in the repository root
- `github:` takes a YAML list (even for one name)
- Multiple platforms are supported simultaneously
- No build step, no CI required — GitHub reads it directly

**After pushing:** The "Sponsor this project" section appears in the right sidebar of the repo's main page within a few minutes.

---

## GitHub Sponsors Profile Structure

Your profile at `github.com/sponsors/your-username` is separate from the FUNDING.yml. It's where sponsors land after clicking. Structure it to answer three questions fast:

### 1. Bio / What You're Building

One crisp paragraph. Explain:
- What you work on (tools, libraries, infra, frameworks)
- Who benefits (developers, companies, open source ecosystems)
- Why it matters

Keep it under 100 words. Visitors skim.

### 2. Current Focus (Pinned)

Use the "Featured work" section to highlight your active project. Include:
- What problem it solves
- Who uses it
- A link to the repo

Update this whenever you shift focus — stale pinned content signals abandonment.

### 3. Tiers

Tier design determines conversion. Recommended structure:

| Tier | Price | Purpose |
|------|-------|---------|
| Coffee | $5/mo | Entry point — "show support" tier |
| Supporter | $15/mo | Core tier — most sponsors land here |
| Advocate | $50/mo | For power users who get clear value |
| Company | $200+/mo | Enterprise use, custom perks if needed |

**Tier copy guidelines:**
- Name the tier after what the sponsor _is_, not what they _get_
- Be specific about perks ("name in README sponsors section" beats "recognition")
- Don't over-promise on higher tiers unless you can deliver

### 4. Goals (Optional but Effective)

Public funding goals ("working toward 10 sponsors to cover hosting costs") create social proof and progress momentum. Use them when:
- You have a concrete milestone to fund
- You're comfortable with the goal being visible at $0

---

## Org-level vs Repo-level Behavior

| Scenario | Behavior |
|----------|----------|
| FUNDING.yml only in repo | Button appears on that repo |
| FUNDING.yml in org's `.github` repo | Applies to all org repos as default |
| FUNDING.yml in both | Repo-level file overrides org default |

This means you can set a default at the org level and selectively override per-repo. Useful for monorepos or orgs with mixed funding needs.

---

## Replication Template

Steps to wire up GitHub Sponsors on any public repo:

**Step 1: Create `.github/FUNDING.yml`**

```yaml
github: [your-github-username]
```

**Step 2: Allow `.github/` in your `.gitignore`** (if using a whitelist)

```gitignore
!.github/
!.github/FUNDING.yml
```

**Step 3: Commit and push**

```bash
git add .github/FUNDING.yml
git commit -m "Add GitHub Sponsors funding button"
git push
```

**Step 4: Set up your Sponsors profile** (one-time, reusable across repos)

Go to `github.com/sponsors/your-username` → "Set up GitHub Sponsors" if not done, or edit your existing profile.

**Step 5: Verify**

- Visit your repo on GitHub
- Check the right sidebar for "Sponsor this project"
- Click it — confirm it routes to your sponsors profile

---

## What This Does Not Cover

- GitHub Sponsors eligibility (requires approval in your region)
- Tax forms and payout setup (handled in GitHub billing settings)
- Sponsor-only content (GitHub has private repo sponsorship perks)

For those, see the [official GitHub Sponsors documentation](https://docs.github.com/en/sponsors).
