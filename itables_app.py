"""Run this app with: streamlit run itables_app.py"""

import itables.options as it_opt
import pyarrow
import streamlit as st
from itables.sample_dfs import get_countries, get_dict_of_test_dfs
from itables.streamlit import interactive_table
from st_aggrid import AgGrid
from streamlit.components.v1.components import MarshallComponentException

st.logo(
    "https://raw.githubusercontent.com/mwouts/itables/main/src/itables/logo/logo.svg",
    link="https://mwouts.github.io/itables/streamlit.html",
)
st.markdown(
    "![ITables](https://raw.githubusercontent.com/mwouts/itables/main/src/itables/logo/wide.svg)"
)
st.sidebar.markdown(
    """
                    # ITables in Streamlit
                    ![Stars](https://img.shields.io/github/stars/mwouts/itables)
                    """
)


caption = st.sidebar.text_input("Caption", value="Countries")
classes = st.sidebar.multiselect(
    "Classes",
    options=["display", "nowrap", "compact", "cell-border", "stripe"],
    default=it_opt.classes.split(" "),
)
buttons = st.sidebar.multiselect(
    "Buttons",
    options=["pageLength", "copyHtml5", "csvHtml5", "excelHtml5", "colvis"],
    default=["copyHtml5", "csvHtml5", "excelHtml5", "colvis"],
)

style = st.sidebar.text_input("Style", value=it_opt.style)

render_with = st.sidebar.selectbox(
    "Render with", ["st.dataframe", "streamlit-aggrid", "itables"], index=2
)

it_args = {}
if classes != it_opt.classes.split(" "):
    it_args["classes"] = classes
if style != it_opt.style:
    it_args["style"] = style

if buttons:
    it_args["buttons"] = buttons

include_html = st.sidebar.checkbox("Include HTML")

if caption:
    it_args = {"caption": caption, **it_args}

if render_with == "st.dataframe":

    def interactive_table(df, **not_used):
        return st.dataframe(df)

    snippet = """st.dataframe(df)
"""

elif render_with == "streamlit-aggrid":

    def interactive_table(df, key=None, **not_used):
        return AgGrid(df, key=key)

    snippet = """from st_aggrid import AgGrid

AgGrid(df, key=None)
"""
else:
    formatted_args = ["df"] + [
        f"{key}='{value}'" if isinstance(value, str) else f"{key}={value}"
        for key, value in it_args.items()
    ]
    formatted_args = ",\n                  ".join(formatted_args)
    snippet = f"""from itables.streamlit import interactive_table

interactive_table({formatted_args})
"""

st.markdown(
    f"""```python
{snippet}
```
"""
)

df = get_countries(html=include_html)

interactive_table(df, **it_args)

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
