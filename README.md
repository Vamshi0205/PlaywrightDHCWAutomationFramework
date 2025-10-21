# Playwright + Behave Test Framework

End-to-end UI tests using **Playwright (Python)** and **Behave** with a simple HTML report.

---

## Prerequisites

- **Python 3.12+** (recommended)
- **Git**
- Windows PowerShell or any terminal

> Check Python: `py -0p` (Windows) or `python3 --version` (macOS/Linux)

---

**Clone**

```bash
git clone <YOUR_REPO_URL> PlaywrightDHCWAutomationFramework
cd PlaywrightDHCWAutomationFramework/playwright_bdd_dhcw

Activate Virtual Environment by 

py -3.12 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

** Project Dependencies can be installed by **

python -m pip install -U pip
python -m pip install -e .
python -m pip install behave playwright pyyaml pydantic python-dotenv
python -m playwright install chromium

**To Run Tests **

Open Terminal and run command 
-- python -m behave tests/features -D env=qa


**For HTMIL reports **

Install behave html formatter
Open Terminal and run command 
python -m pip install behave-html-formatter


**To Run Tests with HTML reports **

Open Terminal and run command
-- python -m behave tests/features -D env=qa -f behave_html_formatter:HTMLFormatter -o artifacts/behave-report.html
 



**Project Layout: **
repo-root/
├─ pyproject.toml
├─ src/
│  └─ framework/
│     ├─ core/ (config/paths etc.)
│     └─ base/ (BasePage)
└─ tests/
   ├─ config/
   │  └─ qa.yaml
   ├─ pages/
   │  └─ home_page.py
   └─ features/
      ├─ environment.py
      ├─ homepage_nav.feature
      └─ steps/
         └─ home_steps.py
