import streamlit as st
from frontend.api_client import call_api, APIError
from frontend.ui_components import render_header, remove_footer, render_toggle, render_progress, display_error

def main():
    st.set_page_config(
        page_title="ArchiGenie - AI Architecture Assistant",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    remove_footer()
    render_header()

    if 'architecture' not in st.session_state:
        st.session_state.architecture = None

    provider_selection = st.selectbox(
        "Select AI Provider",
        ["HuggingFace (Free)", "OpenAI (Paid)"],
        help="Choose the AI provider for architecture generation",
        index=0
    )
    st.session_state.provider = provider_selection.split()[0].lower()

    switch_mode = render_toggle()

    if switch_mode:
        functional_mode()
    else:
        guided_mode()

def functional_mode():
    st.header("📝 Functional Requirement Mode")
    with st.form("functional_form"):
        requirement = st.text_area(
            "Describe your application functionality (e.g., 'An AI-powered e-commerce store'):",
            height=150
        )
        submitted = st.form_submit_button("🔍 Generate Architecture")
        if submitted:
            handle_functional_submission(requirement)
    display_results()

def guided_mode():
    st.header("🔧 Guided Mode (Technical Selection)")
    with st.form("guided_form"):
        col1, col2 = st.columns(2)
        with col1:
            architecture = st.radio(
                "Core Architecture Pattern",
                ["Monolithic", "Microservices", "SOA", "Serverless", "Event-Driven",
                 "Hexagonal", "Layered", "Cloud-Native", "Hybrid/Custom"]
            )
            custom_arch = st.text_input("Describe your Custom Architecture") if architecture == "Hybrid/Custom" else ""
            services = st.multiselect("Business Services:", [
                "User/Identity Management", "Authentication & Authorization", "Data Processing",
                "Business Logic / Core Services", "API Management", "Notification & Messaging",
                "Analytics & Reporting", "Logging & Auditing", "External Integrations"
            ])
            integration = st.multiselect("Integration Methods:", [
                "REST APIs", "GraphQL", "Message Queues (Kafka, RabbitMQ)", "gRPC", "WebSockets",
                "File/Batch Data Exchange", "Middleware Integration"
            ])
        with col2:
            data_storage = st.multiselect("Primary Data Store:", [
                "SQL Databases (PostgreSQL, MySQL)", "NoSQL (MongoDB, DynamoDB, Cassandra)",
                "Time-Series / Specialized Databases", "Data Warehousing (BigQuery, Redshift)",
                "Blockchain-based Storage"
            ])
            caching = st.multiselect("Secondary Storage & Caching:", [
                "In-Memory Caching (Redis, Memcached)", "Object Storage (S3, Azure Blob)",
                "File Systems / Cold Storage"
            ])
            data_processing = st.multiselect("Data Processing Patterns:", [
                "Batch Processing", "Stream Processing", "Event Sourcing"
            ])
            security = st.multiselect("Security Measures:", [
                "OAuth2", "JWT", "SAML", "API Keys", "RBAC", "ABAC",
                "Data Encryption (In Transit & At Rest)", "Firewalls & VPNs", "DDoS Protection"
            ])
            compliance = st.multiselect("Compliance Standards:", [
                "GDPR", "HIPAA", "SOC 2", "PCI-DSS"
            ])
            deployment = st.radio("Deployment Environment", [
                "Cloud (AWS, Azure, GCP)", "On-Premise", "Hybrid/Multi-Cloud"
            ])
        expected_concurrency = st.slider("Expected Concurrency", 1, 10000, 100)
        latency = st.slider("Latency Requirements (ms)", 1, 1000, 200)
        throughput = st.slider("Throughput Targets (req/sec)", 1, 10000, 500)
        resilience = st.multiselect("Resilience Features:", [
            "Fault Tolerance (Circuit Breakers, Redundancy)", "Multi-Region Deployment", "Auto-Healing Mechanisms"
        ])
        advanced_features = st.multiselect("Advanced Features:", [
            "AI/ML Integration (LLM, Predictive Analytics)", "IoT/Edge Integration",
            "Blockchain Integration", "Micro Frontends", "Real-Time Collaboration"
        ])
        submitted = st.form_submit_button("🚀 Generate Architecture")
        if submitted:
            handle_guided_submission(
                architecture=architecture,
                custom_arch=custom_arch,
                services=services,
                integration=integration,
                data_storage=data_storage,
                caching=caching,
                data_processing=data_processing,
                security=security,
                compliance=compliance,
                deployment=deployment,
                expected_concurrency=expected_concurrency,
                latency=latency,
                throughput=throughput,
                resilience=resilience,
                advanced_features=advanced_features
            )
    display_results()

def handle_functional_submission(requirement):
    if not requirement.strip():
        st.warning("⚠️ Please enter a functional requirement")
        return
    try:
        with st.spinner("🧠 Analyzing requirements..."):
            result = call_api("/generate-prompt", {
                "functional_requirement": requirement,
                "provider": st.session_state.provider
            })
            st.session_state.architecture = result.get("architecture")
    except APIError as e:
        display_error(e)

def handle_guided_submission(**kwargs):
    try:
        payload = kwargs
        payload["provider"] = st.session_state.provider
        with st.spinner("🔨 Building architecture blueprint..."):
            result = call_api("/generate-prompt", payload)
            st.session_state.architecture = result.get("architecture")
    except APIError as e:
        display_error(e)

def display_results():
    if st.session_state.architecture:
        st.subheader("Final Architecture Design")
        st.markdown(st.session_state.architecture)

if __name__ == "__main__":
    main()
