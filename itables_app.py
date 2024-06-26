"""Run this app with: streamlit run itables_app.py"""

import pyarrow
import streamlit as st
from itables.sample_dfs import get_countries, get_dict_of_test_dfs
from itables.streamlit import interactive_table
from st_aggrid import AgGrid
from streamlit.components.v1 import html
from streamlit.components.v1.components import MarshallComponentException

st.set_page_config(layout="wide")
logo_col, title_col = st.columns([0.1, 0.9])
with logo_col:
    st.markdown(
        "![ITables](https://raw.githubusercontent.com/mwouts/itables/main/src/itables/logo/logo.svg)"
    )
with title_col:
    html(
        """
         <h1>
         <a href="https://mwouts.github.io/itables">ITables</a>
         <a class="github-button" href="https://github.com/mwouts/itables" data-icon="octicon-star" data-show-count="true"></a>
         in Streamlit</h1>
         <h2>Python DataFrames as Interactive <a href="https://datatables.net">DataTables</a>
         </h2>
        <script src="https://buttons.github.io/buttons.js"></script>"""
    )

st.header("Code snippet")

st.markdown(
    """
```python
from itables.streamlit import interactive_table

interactive_table(df, ...)  # add caption, buttons, style, etc ... like you do with 'show' in a notebook
```
"""
)

st.header("Countries")

caption_col, classes_col, buttons_col, style_col, render_with_col = st.columns(
    [0.10, 0.25, 0.25, 0.20, 0.10]
)
caption = caption_col.text_input("Caption", value="Countries")
classes = classes_col.multiselect(
    "Classes",
    options=["display", "nowrap", "compact", "cell-border", "stripe"],
    default=["display", "nowrap"],
)
buttons = buttons_col.multiselect(
    "Buttons",
    options=["pageLength", "copyHtml5", "csvHtml5", "excelHtml5", "colvis"],
    default=["copyHtml5", "csvHtml5", "excelHtml5", "colvis"],
)

style = style_col.text_input(
    "Style", value="table-layout:auto;width:auto;margin:auto;caption-side:bottom"
)

render_with = render_with_col.selectbox(
    "Render with", ["st.dataframe", "streamlit-aggrid", "itables"], index=2
)

if render_with == "st.dataframe":

    def interactive_table(df, **not_used):
        return st.dataframe(df)

elif render_with == "streamlit-aggrid":

    def interactive_table(df, key=None, **not_used):
        return AgGrid(df, key=key)


it_args = dict(
    classes=classes,
    style=style,
)
if buttons:
    it_args["buttons"] = buttons

include_html = st.checkbox("Include HTML")
df = get_countries(html=include_html)

interactive_table(df, caption=caption, **it_args)

st.header("More sample dataframes")
test_dfs = get_dict_of_test_dfs()
tabs = st.tabs(test_dfs.keys())

for (name, df), tab in zip(test_dfs.items(), tabs):
    with tab:
        try:
            interactive_table(df, key=name, classes=classes, style=style)
        except (
            # ITables
            NotImplementedError,
            # st.dataframe
            ValueError,
            # streamlit-aggrid
            pyarrow.lib.ArrowInvalid,
            MarshallComponentException,
        ) as e:
            st.warning(e)
