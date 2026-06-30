"""
RR ELEVATE — AUTHENTICATION MODULE
Handles: Founder login, Agent/Client signup + approval, role-based access
"""

import streamlit as st
import pandas as pd
import csv
import os
import hashlib
from datetime import datetime

USERS_FILE = "users.csv"
USER_HEADERS = ["username", "password_hash", "role", "full_name", "email", "phone", "status", "created_date"]

# ── PASSWORD HASHING ──
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ── INIT USERS FILE ──
def init_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(USER_HEADERS)
            # Default founder account — CHANGE THIS PASSWORD AFTER FIRST LOGIN
            writer.writerow([
                "founder", hash_password("RRElevate2026"), "Founder",
                "Rishi Rajput", "founder@rrelevate.com", "", "approved",
                datetime.now().strftime("%d-%m-%Y")
            ])

def load_users():
    init_users_file()
    try:
        return pd.read_csv(USERS_FILE)
    except Exception:
        return pd.DataFrame(columns=USER_HEADERS)

def save_user(username, password, role, full_name, email, phone, status="pending"):
    init_users_file()
    users = load_users()
    if username in users["username"].values:
        return False, "Username already exists"
    with open(USERS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            username, hash_password(password), role, full_name, email, phone,
            status, datetime.now().strftime("%d-%m-%Y")
        ])
    return True, "Account created"

def update_user_status(username, new_status):
    users = load_users()
    users.loc[users["username"] == username, "status"] = new_status
    users.to_csv(USERS_FILE, index=False)

def verify_login(username, password):
    users = load_users()
    match = users[users["username"] == username]
    if match.empty:
        return None, "Username not found"
    row = match.iloc[0]
    if row["password_hash"] != hash_password(password):
        return None, "Incorrect password"
    if row["status"] == "pending":
        return None, "Your account is pending approval from the Founder"
    if row["status"] == "rejected":
        return None, "Your account access was denied"
    return row, "success"

# ── SESSION STATE HELPERS ──
def is_logged_in():
    return st.session_state.get("auth_user") is not None

def current_user():
    return st.session_state.get("auth_user")

def current_role():
    user = current_user()
    return user["role"] if user is not None else None

def logout():
    st.session_state.auth_user = None
    st.session_state.auth_view = "login"
    st.rerun()

# ── LOGIN / SIGNUP UI ──
def render_auth_screen():
    st.markdown("""
    <style>
    .auth-wrap { max-width: 420px; margin: 60px auto; }
    .auth-logo { text-align:center; margin-bottom: 32px; }
    .auth-card { background:#181820; border:1px solid rgba(201,162,39,0.15); border-radius:14px; padding:36px; }
    </style>
    """, unsafe_allow_html=True)

    if "auth_view" not in st.session_state:
        st.session_state.auth_view = "login"

    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="auth-logo">
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.8rem;font-weight:800;color:#fff">
            RR <span style="color:#C9A227">Elevate</span> Realty
        </div>
        <div style="font-size:0.7rem;color:#888;letter-spacing:0.15em;text-transform:uppercase;margin-top:4px">
            AI Command Center
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="auth-card">', unsafe_allow_html=True)

    if st.session_state.auth_view == "login":
        st.markdown("##### 🔐 Sign In")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Sign In", use_container_width=True, type="primary"):
            if not username or not password:
                st.error("Please enter username and password")
            else:
                user, msg = verify_login(username, password)
                if user is not None:
                    st.session_state.auth_user = user.to_dict()
                    st.success("Welcome back!")
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("---")
        st.caption("New agent or client?")
        if st.button("Create an Account", use_container_width=True):
            st.session_state.auth_view = "signup"
            st.rerun()

    elif st.session_state.auth_view == "signup":
        st.markdown("##### 📝 Create Account")
        role = st.selectbox("I am a", ["Agent", "Client"])
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        username = st.text_input("Choose Username")
        password = st.text_input("Choose Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Submit for Approval", use_container_width=True, type="primary"):
            if not all([full_name, email, username, password]):
                st.error("Please fill all required fields")
            elif password != confirm:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                ok, msg = save_user(username, password, role, full_name, email, phone, status="pending")
                if ok:
                    st.success("✅ Account created! Waiting for Founder approval. You'll be able to log in once approved.")
                else:
                    st.error(msg)

        st.markdown("---")
        if st.button("← Back to Sign In", use_container_width=True):
            st.session_state.auth_view = "login"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── CLIENT PORTAL — what clients see after login ──
def render_client_portal():
    user = current_user()
    full_name = user.get("full_name", "")
    email = (user.get("email") or "").strip().lower()
    phone = str(user.get("phone") or "").strip()

    # Header
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0D0D15,#111118);
                border-bottom:1px solid rgba(201,162,39,0.2);
                padding:18px 24px;display:flex;justify-content:space-between;align-items:center;margin-bottom:24px">
        <div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:1.3rem;font-weight:700;color:#fff">
                Welcome, <span style="color:#C9A227">{full_name}</span>
            </div>
            <div style="font-size:0.7rem;color:#888;margin-top:2px">Your Property Journey with RR Elevate Realty</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Logout", key="client_logout"):
        logout()

    # Load website leads and match by email or phone
    leads_file = "leads_from_website.csv"
    my_leads = []
    if os.path.exists(leads_file):
        leads_df = pd.read_csv(leads_file)
        if not leads_df.empty:
            leads_df["Email"] = leads_df["Email"].astype(str).str.strip().str.lower()
            leads_df["Phone"] = leads_df["Phone"].astype(str).str.strip()
            match = leads_df[(leads_df["Email"] == email) | (leads_df["Phone"] == phone)]
            my_leads = match.to_dict("records")

    if not my_leads:
        st.markdown("""
        <div style="text-align:center;padding:80px 20px">
            <div style="font-size:3.5rem;margin-bottom:20px">🏠</div>
            <div style="font-size:1.1rem;font-weight:700;color:#fff;margin-bottom:10px">No Enquiry Found Yet</div>
            <div style="font-size:0.85rem;color:#888;max-width:420px;margin:0 auto;line-height:1.8">
                We couldn't find a property enquiry linked to your account.
                Make sure you used the same email or phone number when you
                submitted an enquiry on our website.
            </div>
            <div style="margin-top:24px;background:rgba(201,162,39,0.08);border:1px solid rgba(201,162,39,0.2);
                        border-radius:10px;padding:14px 28px;font-size:0.8rem;color:#C9A227;display:inline-block">
                📞 Need help? Call +91 98765 43210
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    status_colors = {"Hot": "#E84855", "Warm": "#C9A227", "Cold": "#555"}
    status_labels = {
        "Hot": "🔥 Our team is actively working on your request",
        "Warm": "📋 Your enquiry is being reviewed",
        "Cold": "📨 Received — awaiting advisor follow-up",
    }

    for lead in my_leads:
        scolor = status_colors.get(lead.get("Status", "Warm"), "#C9A227")
        slabel = status_labels.get(lead.get("Status", "Warm"), "Submitted")
        st.markdown(f"""
        <div style="background:#181820;border:1px solid rgba(201,162,39,0.15);border-radius:14px;
                    padding:28px;margin-bottom:20px">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px">
                <div>
                    <div style="font-size:0.62rem;color:#888;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px">Your Enquiry</div>
                    <div style="font-family:'Space Grotesk',sans-serif;font-size:1.1rem;font-weight:700;color:#fff">{lead.get('Interest','General Inquiry')}</div>
                </div>
                <div style="background:{scolor}22;border:1px solid {scolor}44;border-radius:20px;padding:6px 16px;font-size:0.7rem;font-weight:700;color:{scolor}">
                    {lead.get('Status','Warm')}
                </div>
            </div>
            <div style="font-size:0.85rem;color:#aaa;margin-bottom:18px">{slabel}</div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.06)">
                <div>
                    <div style="font-size:0.6rem;color:#888;letter-spacing:0.08em;text-transform:uppercase">City</div>
                    <div style="font-size:0.85rem;color:#fff;font-weight:600;margin-top:3px">{lead.get('City','—')}</div>
                </div>
                <div>
                    <div style="font-size:0.6rem;color:#888;letter-spacing:0.08em;text-transform:uppercase">Budget</div>
                    <div style="font-size:0.85rem;color:#C9A227;font-weight:700;margin-top:3px">{lead.get('Budget','—')}</div>
                </div>
                <div>
                    <div style="font-size:0.6rem;color:#888;letter-spacing:0.08em;text-transform:uppercase">Submitted</div>
                    <div style="font-size:0.85rem;color:#fff;font-weight:600;margin-top:3px">{lead.get('Date','—')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(201,162,39,0.06);border:1px solid rgba(201,162,39,0.15);border-radius:10px;
                padding:18px 24px;margin-top:8px;text-align:center">
        <div style="font-size:0.82rem;color:#aaa">Have a question about your enquiry?</div>
        <div style="font-size:0.9rem;color:#C9A227;font-weight:700;margin-top:6px">📞 +91 98765 43210 &nbsp;·&nbsp; hello@rrelevate.in</div>
    </div>
    """, unsafe_allow_html=True)

# ── PENDING APPROVALS UI (for Founder) ──
def render_pending_approvals():
    users = load_users()
    pending = users[users["status"] == "pending"]

    st.markdown("""
    <div style="padding:20px 0 16px">
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.4rem;font-weight:700;color:#fff">
            🔐 User <span style="color:#C9A227">Approvals</span>
        </div>
        <div style="font-size:0.7rem;color:#888;margin-top:4px">{} pending requests</div>
    </div>
    """.format(len(pending)), unsafe_allow_html=True)

    if pending.empty:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px">
            <div style="font-size:3rem;margin-bottom:16px">✅</div>
            <div style="font-size:1rem;font-weight:700;color:#fff;margin-bottom:8px">No Pending Approvals</div>
            <div style="font-size:0.82rem;color:#888">New agent and client signups will appear here.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for _, row in pending.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"""
                <div style="background:#1E1E28;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:14px 18px;margin-bottom:8px">
                    <div style="font-weight:700;color:#fff;font-size:0.9rem">{row['full_name']} <span style="color:#C9A227;font-size:0.65rem">({row['role']})</span></div>
                    <div style="font-size:0.72rem;color:#888;margin-top:4px">@{row['username']} · {row['email']} · {row['phone']}</div>
                    <div style="font-size:0.62rem;color:#555;margin-top:4px">Applied: {row['created_date']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("✅ Approve", key=f"appr_{row['username']}", use_container_width=True):
                    update_user_status(row['username'], "approved")
                    st.rerun()
            with col3:
                if st.button("❌ Reject", key=f"rej_{row['username']}", use_container_width=True):
                    update_user_status(row['username'], "rejected")
                    st.rerun()

    st.markdown("---")
    st.markdown("##### All Users")
    approved = users[users["status"] != "pending"]
    if not approved.empty:
        st.dataframe(
            approved[["username", "full_name", "role", "email", "status"]],
            use_container_width=True, hide_index=True
        )
