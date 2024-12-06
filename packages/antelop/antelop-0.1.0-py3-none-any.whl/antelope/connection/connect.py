import datajoint as dj
import os
from antelope.utils.os_utils import get_config


def dbconnect(username, password):
    """
    Function loads configuration from home and
    returns a connection to the database.
    """

    # load config file
    config = get_config()

    dj.config["database.host"] = config["mysql"]["host"]
    dj.config["database.user"] = username
    dj.config["database.password"] = password
    dj.config["stores"] = {
        "raw_ephys": {
            "protocol": "s3",
            "endpoint": config["s3"]["host"],
            "bucket": "antelope-external-data",
            "location": "/raw_ephys",
            "access_key": username,
            "secret_key": password,
        },
        "feature_behaviour": {
            "protocol": "s3",
            "endpoint": config["s3"]["host"],
            "bucket": "antelope-external-data",
            "location": "/features_behaviour",
            "access_key": username,
            "secret_key": password,
        },
        "dlcmodel": {
            "protocol": "s3",
            "endpoint": config["s3"]["host"],
            "bucket": "antelope-external-data",
            "location": "/dlcmodel",
            "access_key": username,
            "secret_key": password,
        },
        "behaviour_video": {
            "protocol": "s3",
            "endpoint": config["s3"]["host"],
            "bucket": "antelope-external-data",
            "location": "/behaviour_video",
            "access_key": username,
            "secret_key": password,
        },
        "labelled_frames": {
            "protocol": "s3",
            "endpoint": config["s3"]["host"],
            "bucket": "antelope-external-data",
            "location": "/labelled_frames",
            "access_key": username,
            "secret_key": password,
        },
        "evaluated_frames": {
            "protocol": "s3",
            "endpoint": config["s3"]["host"],
            "bucket": "antelope-external-data",
            "location": "/evaluated_frames",
            "access_key": username,
            "secret_key": password,
        },
    }

    conn = dj.conn(reset=True)

    return conn


def connect():
    """
    Function used by streamlit to connect to database and effectively
    cache the connection.
    Streamlit internal caching mechanism is not used because we had
    a number of crashes, particularly when mutlithreading.
    """

    import streamlit as st

    pid = os.getpid()

    if f"conn-{pid}" in st.session_state:
        if st.session_state[f"conn-{pid}"].is_connected:
            return st.session_state[f"conn-{pid}"]

    st.session_state[f"conn-{pid}"] = dbconnect(
        st.session_state.username, st.session_state.password
    )
    return st.session_state[f"conn-{pid}"]


# check credentials and return connection
def check_credentials():
    try:
        import streamlit as st

        conn = dbconnect(st.session_state.username, st.session_state.password)
        return True

    except Exception:
        return False
