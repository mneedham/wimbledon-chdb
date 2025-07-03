# Analyzing Wimbledon data

I wanted to know how far away from defeat players are in their Wimbledon matches and that's what this app does.

You can try it out at https://wimbledon.streamlit.app

Or if you want to try it locally:

```
git clone git@github.com:mneedham/wimbledon-chdb.git
cd wimbledon-cdb
```

And then run:

```
uv run --with chdb --with plotly --with streamlit \
streamlit run app.py  --server.headless True
```