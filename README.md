# The Cacao Project by HotCacao

**Roster**

Devin Lin: Frontend

Alice Ni: Backend

Joseph Yusufov: Backend

Hilary Zen: Project Manager and Frontend

# How to Run this Project

1. Git clone this repo by running:

```
git clone https://github.com/hilaryzen/HotCacao.git
```

2. Install Flask in the repo folder with:

```
cd HotCacao
pip3 install flask
```

If the pip3 command did not work for you, create a virtual environment, activate it, and install Flask with the following lines:

```
python3 -m venv myvenv
. myvenv/bin/activate
pip3 install flask
```

3. If you already have a wiki.db file, run the following command to delete it:

```
rm db_builder.py
```

Now all users should run:

```
python3 db_builder.py
```

4. Run The Cacao Project with:

```
python3 app.py
```

5. Go to http://localhost:5000/ to read some stories!

6. After you are done looking at the site, if you are running a virtual environment you can close it with:

```
deactivate
```
