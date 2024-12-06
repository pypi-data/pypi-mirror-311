import streamlit as st
import streamlit_antd_components as sac
from antelope.utils import analysis_utils
from antelope.utils.streamlit_utils import (
    dropdown_query_table,
    enter_args,
    display_analysis,
)
from antelope.utils.external_utils import schedule_analysis, analysis_progress
from antelope.utils.analysis_utils import reload_analysis


def reset_state():
    st.session_state.result = None


def show(username, tables):

    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

    with col2:

        st.title("Analysis")
        st.subheader("Run analysis on the database")

        def reset_state():
            st.session_state.result = None

        st.divider()
        if not hasattr(st.session_state, "result"):
            reset_state()

        # load analysis functions
        analysis_functions = analysis_utils.import_analysis(
            tables["Experimenter"].connection, tables
        )

        # get user to select the function they want
        st.markdown("#### Select function")
        folder = st.selectbox(
            "Select analysis folder",
            list(analysis_functions.keys()),
            on_change=reset_state,
        )
        func_dict = {f.name: f for f in analysis_functions[folder] if f.hidden == False}
        name = st.selectbox(
            "Select analysis function",
            list(func_dict.keys()),
            on_change=reset_state,
        )
        function = func_dict[name]

        # display docstring
        st.text("")
        st.markdown(function.__doc__)
        if st.button("Reload functions"):
            analysis_functions = reload_analysis(
                tables["Experimenter"].connection, tables
            )
            st.rerun()
        st.divider()

        # get user to select the restriction they want to apply
        st.markdown("#### Enter restriction")
        if hasattr(function, "key"):
            key = function.key
        else:
            key = {}
        if isinstance(function.query, str):
            table = tables[function.query].proj()
        elif isinstance(function.query, list):
            table = tables[function.query[0]]
            for q in function.query[1:]:
                table = table * tables[q].proj()
        _, restriction = dropdown_query_table(
            tables, {"table": table & key}, username, headless=True
        )

        if _ == None:
            st.error("No data available to run analysis on.")

        else:
            # get the user to input the arguments
            if hasattr(function, "args") and function.args:
                st.divider()
                st.markdown("#### Enter arguments")
                args = enter_args(function)
            else:
                args = {}

            # run the function
            st.divider()
            st.markdown("#### Select mode")
            sac.buttons(
                [sac.ButtonsItem(label="Local"), sac.ButtonsItem(label="Cluster")],
                key="mode",
                use_container_width=True,
            )

            if st.session_state.mode == "Local":
                st.text("")
                result = None
                if st.button("Run"):

                    @st.cache_data(ttl=600)
                    def cache_fct(name, restriction, **args):
                        fct = func_dict[name]
                        try:
                            return fct(restriction, **args)
                        except Exception as e:
                            st.error(
                                f"""
                            Your function has an error.\n
                            Error message:\n
                            {e}
                            """
                            )

                    result = cache_fct(name, restriction, **args)
                    st.session_state.result = result

                st.divider()
                if hasattr(st.session_state, "result"):
                    display_analysis(
                        st.session_state.result, function.returns, table.primary_key
                    )

            if st.session_state.mode == "Cluster":
                st.text("")

                savepath = st.text_input("Enter the path to save the results to")
                numcpus = st.number_input(
                    "Enter the number of cpus to use",
                    min_value=1,
                    max_value=64,
                    value=1,
                )
                time = st.number_input(
                    "Enter the time to run the job for (minutes)",
                    min_value=10,
                    max_value=24 * 60,
                    value=60,
                )
                password = st.text_input(
                    "Please enter your cluster password", type="password"
                )

                st.text("")
                if st.button("Schedule analysis job"):

                    try:
                        schedule_analysis(
                            function,
                            restriction,
                            savepath,
                            numcpus,
                            time,
                            password,
                            args,
                        )
                    except Exception as e:
                        print(e)
                        st.error(
                            "Job scheduling failed. Please check your inputs and try again."
                        )
                    else:
                        st.text("")
                        st.success("Job sent to cluster.")

                # if there are any downlaods this session
                if "analysis_jobs" in st.session_state:

                    # button which shows spikesort statuses
                    st.text("")
                    if st.button("Check analysis progress"):

                        analysis_progress()
