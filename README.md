<div align="center">
    <img src="assets/logo.png" style="width:25%">
    <p style="font-size:2em">ligth_autobaka</p>
</div>

**light_autobaka** is python util to automatically calculate average of each subject from ***Bakaláři***

***"light"*** cause it's powered by **request** and **bs4** instead dynamically going through the page as a [previous version](https://github.com/bag1s3k/AutoBaka.git)

## Recommendation

- use `uv` package manager

```bash
https://github.com/bag1s3k/light_autobaka.git
cd light_autobaka
uv sync
```

## Configuration

- rename `.env.example` and write your own login credentials
- rename `config.toml.example` and customize
    - `base_url` = login url without **/login**
    - `marks_endpoint` = url endpoint to marks in **chronological** view (Grade > Interim Grading > Chronological button)

<p><img src="assets/screenshot_chronological.png" alt="Chronological button" style="width:100%;"/></p>

## Run

```bash
uv run ./main.py
```

## Output (default)

- `marks` = raw marks data
- `result.txt` = text output with calcuated averages
- `logs.log`
