# Smart Student Success

This project includes a desktop application (`app.py`) and a browser-based
version (`web_app.py`).

## Run the browser version locally

From the project folder in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run web_app.py
```

Streamlit opens the app in your browser. The browser version keeps records in
the current visitor session only; it does not write them to the shared student
database. Use aliases instead of real names, and do not enter sensitive student
information in a public deployment.

## Publish a public link

To get a public URL, publish this project through a hosting account that
supports Streamlit (for example, Streamlit Community Cloud):

1. Create a GitHub repository and upload the project files, including
   `web_app.py`, `student_model.pkl`, and `requirements.txt`.
2. Do **not** upload `student_success.db`, which is excluded by `.gitignore`.
3. In the hosting service, create a new Streamlit app from that repository and
   set the app file to `web_app.py`.
4. Deploy the app. The hosting service will provide the public URL to share.

This workspace cannot publish the project or create that URL without access to
your hosting account. The public web app is a demo; its records are temporary
and isolated to each active visitor session.
