<div align="center">
    <img src="assets/logo.png" style="width:25%">
    <h1>ligth_autobaka</h1>
</div>

**light_autobaka** is python util to automatically calculate average of each subject from ***Bakaláři***

***"light"*** cause it's powered by **request** and **bs4** instead dynamically going through the page as a [previous version](https://github.com/bag1s3k/AutoBaka.git)

## Recommendation

- use `uv` package manager

```bash
git clone https://github.com/bag1s3k/light_autobaka.git
cd light_autobaka
uv sync
```

## Usage

## Configuration

- `base_url` - login url without **/login**
- `login_endpoint` - login page
- `after_login_endpoint` - url after you login
- `marks_endpoint` - url endpoint to marks in **chronological** view (Grade > Interim Grading > Chronological button)

<p align="center"><img src="assets/screenshot_chronological.png" alt="Chronological button" style="width:90%"/></p>

## Local Run

```bash
uv run -m main
```

## Github Actions + Pages
1. Fork my repo
2. Go to **GitHub Pages** settings and change source to **GitHub Actions**
3. Go to **GitHub Actions** and anable them and activate **deploy.yml** workflow
4. Go to the `secrets` of repo
5. Create following variables:
    - `USERNAME` - your bakalari username
    - `PASSWORD` - your bakalari password
    - `DATA` - configuration of app (instead `config.toml`), it's **json object**

        ```json
        {"base_url": "https://website.com", "login_endpoint": "login", "after_login_endpoint": "dashboard", "marks_endpoint": "next/prubzna.aspx?s=chrono"}
        ```

## Output (default)

- `marks` - raw marks data
- `result.txt` - text output with calcuated averages
- `logs.log`
- `index.html` - only via **CI environment**

## Future features maybe
- absence prediction
- marks prediction
