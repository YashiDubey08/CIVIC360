
import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
from supabase import create_client
from streamlit_geolocation import streamlit_geolocation


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CIVIC360 | Municipal Operations",
    page_icon="🏙️",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"


# =========================================================
# SUPABASE CONNECTION
# =========================================================

@st.cache_resource
def connect_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


try:
    supabase = connect_supabase()
    db_connected = True
except Exception as e:
    supabase = None
    db_connected = False
    st.error(f"Database connection failed: {e}")


# =========================================================
# COMMON FUNCTIONS
# =========================================================

def fetch_reports():

    if supabase is None:
        return []

    try:
        response = (
            supabase.table("reports")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        return response.data or []

    except Exception as e:
        st.error(f"Could not fetch reports: {e}")
        return []


def upload_photo(image):

    if image is None:
        return None

    try:
        file_name = f"{uuid.uuid4()}_{image.name}"

        image_bytes = image.getvalue()

        supabase.storage.from_("evidence").upload(
            file_name,
            image_bytes,
            file_options={
                "content-type": image.type,
                "upsert": "true"
            }
        )

        public_url = (
            supabase.storage
            .from_("evidence")
            .get_public_url(file_name)
        )

        return public_url

    except Exception as e:
        st.error(f"Photo upload failed: {e}")
        return None


def show_status(status):

    colors = {
        "Submitted": "🟡",
        "Under Review": "🔵",
        "Assigned": "🟣",
        "In Progress": "🟠",
        "Resolved": "🟢",
        "Rejected": "🔴"
    }

    return f"{colors.get(status, '⚪')} {status}"


# =========================================================
# GLOBAL STYLING
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #0b1628;
    color: #ffffff;
}

[data-testid="stSidebar"] {
    background-color: #101f35;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

h1, h2, h3 {
    color: #ffffff;
}

p, label {
    color: #d1deed;
}

.stButton > button {
    background: linear-gradient(90deg, #087eae, #36c6e9);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    min-height: 43px;
}

.stButton > button:hover {
    background: #53d8f3;
    color: #071629;
    border: none;
}

div[data-testid="stMetric"] {
    background: #142943;
    border: 1px solid #284c6c;
    padding: 18px;
    border-radius: 12px;
}

div[data-testid="stMetricValue"] {
    color: #55d9f5;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# COVER PAGE
# =========================================================

if st.session_state.page == "home":

    # Hide dashboard sidebar on cover page
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 3rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.write("")

    st.markdown(
        "<p style='text-align:center;color:#58d9f5;"
        "letter-spacing:3px;font-weight:bold;'>"
        "✦ SMARTER CITIES • BETTER TOMORROWS ✦"
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h1 style='text-align:center;color:white;"
        "font-size:76px;font-weight:850;'>"
        "🏙️ CIVIC360"
        "</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='text-align:center;color:#55d9f5;'>"
        "Smart Civic Issue Reporting & Tracking Platform"
        "</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:#d1deed;"
        "font-size:17px;'>"
        "Transforming the way cities identify, report and manage "
        "civic challenges through one unified platform."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    st.markdown(
        "<h2 style='text-align:center;color:white;'>"
        "Everything Your City Needs, In One Place"
        "</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:#b7cce0;'>"
        "Discover a smarter approach to civic management."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    # Feature cards
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("## 📍")
            st.subheader("Report Issues")
            st.write(
                "Report potholes, damaged roads, open drains "
                "and other civic problems with location details."
            )

    with col2:
        with st.container(border=True):
            st.markdown("## 📊")
            st.subheader("Track Complaints")
            st.write(
                "Monitor submitted reports and follow "
                "their progress through different stages."
            )

    with col3:
        with st.container(border=True):
            st.markdown("## 🗺️")
            st.subheader("Smart Analytics")
            st.write(
                "Explore civic issue patterns through maps, "
                "visualizations and data insights."
            )

    st.write("")
    st.write("")

    st.markdown(
        "<h3 style='text-align:center;color:#55d9f5;'>"
        "YOUR CITY • YOUR VOICE • YOUR IMPACT"
        "</h3>",
        unsafe_allow_html=True
    )

    st.write("")

    left, middle, right = st.columns([1, 1.5, 1])

    with middle:

        if st.button(
            "🚀 GET STARTED",
            use_container_width=True
        ):

            st.session_state.page = "dashboard"
            st.rerun()

    st.stop()


# =========================================================
# DASHBOARD SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🏙️ CIVIC360")

    st.caption("Live Municipal Operations Portal")

    st.divider()

    role = st.selectbox(
        "Select your role",
        [
            "Citizen",
            "Municipal Admin",
            "Field Technician"
        ]
    )

    st.divider()

    st.subheader("Navigation")

    page = st.radio(
        "Go to",
        [
            "📷 Report Hazard",
            "🛠️ Issue Tracker & Operations",
            "📊 Analytics & Spatial Heatmap"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    if db_connected:
        st.success("Database Connected")
    else:
        st.error("Database Disconnected")

    if st.button("🏠 Back to Cover Page"):

        st.session_state.page = "home"
        st.rerun()


# =========================================================
# MAIN DASHBOARD HEADER
# =========================================================

st.title("🏙️ CIVIC360")

st.caption(
    "Smart Civic Issue Reporting and Tracking Platform"
)

st.divider()


# =========================================================
# MODULE 1: REPORT HAZARD
# =========================================================

if page == "📷 Report Hazard":

    st.header("Report Infrastructure Issue")

    st.write(
        "Submit a civic complaint with its location and photograph."
    )

    st.subheader("1. Live GPS Location")

    location = streamlit_geolocation()

    latitude = None
    longitude = None

    if location:

        coords = location.get("coords", location)

        latitude = coords.get(
            "latitude",
            coords.get("lat")
        )

        longitude = coords.get(
            "longitude",
            coords.get("lon")
        )

        if latitude is not None and longitude is not None:

            st.success(
                f"GPS Captured: {latitude:.5f}, {longitude:.5f}"
            )

        else:
            st.warning(
                "Location not captured. Allow browser location permission."
            )

    else:

        st.warning(
            "Location not captured. Allow browser location permission and try again."
        )

    st.divider()

    st.subheader("2. Hazard Details")

    with st.form("report_form", clear_on_submit=True):

        hazard_type = st.selectbox(
            "Hazard Classification",
            [
                "Pothole",
                "Surface Crack",
                "Open Drain",
                "Debris/Road Blockage",
                "Traffic Light/Sign Failure",
                "Streetlight Outage",
                "Other"
            ]
        )

        severity = st.selectbox(
            "Severity Level",
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ]
        )

        address = st.text_input(
            "Address / Location",
            placeholder="Enter the issue location"
        )

        description = st.text_area(
            "Issue Description",
            placeholder="Describe the civic issue..."
        )

        image = st.file_uploader(
            "Upload Evidence Photograph",
            type=["jpg", "jpeg", "png"]
        )

        if image:
            st.image(
                image,
                caption="Uploaded evidence",
                width=300
            )

        submitted = st.form_submit_button(
            "🚀 Submit Report",
            use_container_width=True
        )

        if submitted:

            if not address or not description:

                st.error(
                    "Please enter the address and description."
                )

            elif latitude is None or longitude is None:

                st.error(
                    "Please capture your GPS location before submitting."
                )

            elif not db_connected:

                st.error(
                    "Database is not connected. Please check Supabase settings."
                )

            else:

                with st.spinner("Submitting your report..."):

                    report_id = (
                        "REP-" + uuid.uuid4().hex[:10].upper()
                    )

                    image_url = upload_photo(image)

                    report_data = {
                        "report_id": report_id,
                        "type": hazard_type,
                        "severity": severity,
                        "address": address,
                        "description": description,
                        "lat": float(latitude),
                        "lon": float(longitude),
                        "status": "Submitted",
                        "image_url": image_url,
                        "created_at": datetime.now().astimezone().isoformat()
                    }

                    try:

                        supabase.table("reports").insert(
                            report_data
                        ).execute()

                        st.success(
                            f"Your report {report_id} was saved successfully!"
                        )

                        st.balloons()

                    except Exception as e:

                        st.error(
                            f"Report submission failed: {e}"
                        )


# =========================================================
# MODULE 2: ISSUE TRACKER & OPERATIONS
# =========================================================

elif page == "🛠️ Issue Tracker & Operations":

    st.header("Issue Tracker & Municipal Operations")

    reports = fetch_reports()

    df = pd.DataFrame(reports)

    if df.empty:

        st.info(
            "No reports available yet. Submit a civic issue first."
        )

    else:

        total_reports = len(df)

        pending = len(
            df[df["status"] == "Submitted"]
        )

        progress = len(
            df[df["status"] == "In Progress"]
        )

        resolved = len(
            df[df["status"] == "Resolved"]
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Reports", total_reports)
        c2.metric("Pending", pending)
        c3.metric("In Progress", progress)
        c4.metric("Resolved", resolved)

        st.divider()

        st.subheader("All Registered Complaints")

        display_columns = [
            "report_id",
            "type",
            "severity",
            "address",
            "status",
            "created_at"
        ]

        available_columns = [
            col for col in display_columns
            if col in df.columns
        ]

        st.dataframe(
            df[available_columns],
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("Update Complaint Status")

        selected_report = st.selectbox(
            "Select Report ID",
            df["report_id"].tolist()
        )

        new_status = st.selectbox(
            "New Status",
            [
                "Submitted",
                "Under Review",
                "Assigned",
                "In Progress",
                "Resolved",
                "Rejected"
            ]
        )

        if role in ["Municipal Admin", "Field Technician"]:

            if st.button("Update Status"):

                try:

                    supabase.table("reports").update(
                        {"status": new_status}
                    ).eq(
                        "report_id",
                        selected_report
                    ).execute()

                    st.success(
                        f"{selected_report} updated to {new_status}."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Status update failed: {e}"
                    )

        else:

            st.info(
                "Status updates are available to Municipal Admin "
                "and Field Technician demo roles."
            )

        st.divider()

        st.subheader("Complaint Details")

        selected_data = df[
            df["report_id"] == selected_report
        ].iloc[0]

        st.write(
            f"**Report ID:** {selected_data['report_id']}"
        )

        st.write(
            f"**Issue:** {selected_data['type']}"
        )

        st.write(
            f"**Severity:** {selected_data['severity']}"
        )

        st.write(
            f"**Address:** {selected_data['address']}"
        )

        st.write(
            f"**Status:** {show_status(selected_data['status'])}"
        )

        st.write(
            f"**Description:** {selected_data['description']}"
        )

        if selected_data.get("image_url"):

            st.image(
                selected_data["image_url"],
                caption="Submitted Evidence",
                width=350
            )


# =========================================================
# MODULE 3: ANALYTICS & SPATIAL HEATMAP
# =========================================================

elif page == "📊 Analytics & Spatial Heatmap":

    st.header("Analytics & Spatial Heatmap")

    reports = fetch_reports()

    df = pd.DataFrame(reports)

    if df.empty:

        st.info(
            "No data available for analytics yet."
        )

    else:

        st.subheader("Overall Statistics")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Total Issues",
            len(df)
        )

        c2.metric(
            "High/Critical Issues",
            len(
                df[df["severity"].isin(["High", "Critical"])]
            )
        )

        c3.metric(
            "Resolved Issues",
            len(
                df[df["status"] == "Resolved"]
            )
        )

        st.divider()

        # Issue classification chart

        st.subheader("Issues by Classification")

        issue_counts = (
            df["type"]
            .value_counts()
            .reset_index()
        )

        issue_counts.columns = [
            "Issue Type",
            "Count"
        ]

        st.bar_chart(
            issue_counts.set_index("Issue Type")
        )

        st.divider()

        # Severity chart

        st.subheader("Severity Distribution")

        severity_counts = (
            df["severity"]
            .value_counts()
            .reset_index()
        )

        severity_counts.columns = [
            "Severity",
            "Count"
        ]

        st.bar_chart(
            severity_counts.set_index("Severity")
        )

        st.divider()

        # Status chart

        st.subheader("Complaint Status Distribution")

        status_counts = (
            df["status"]
            .value_counts()
            .reset_index()
        )

        status_counts.columns = [
            "Status",
            "Count"
        ]

        st.bar_chart(
            status_counts.set_index("Status")
        )

        st.divider()

        # Spatial heatmap

        st.subheader("Civic Issue Location Map")

        map_df = df[
            ["lat", "lon"]
        ].copy()

        map_df["lat"] = pd.to_numeric(
            map_df["lat"],
            errors="coerce"
        )

        map_df["lon"] = pd.to_numeric(
            map_df["lon"],
            errors="coerce"
        )

        map_df = map_df.dropna()

        if not map_df.empty:

            map_df = map_df.rename(
                columns={
                    "lat": "latitude",
                    "lon": "longitude"
                }
            )

            st.map(
                map_df,
                latitude="latitude",
                longitude="longitude",
                size=100
            )

        else:

            st.warning(
                "No valid GPS coordinates available for mapping."
            )

        st.divider()

        st.subheader("Complete Reports Dataset")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    "<p style='text-align:center;color:#7f9dbb;'>"
    "CIVIC360 | Smart Civic Issue Reporting & Tracking Platform"
    "</p>",
    unsafe_allow_html=True
)
