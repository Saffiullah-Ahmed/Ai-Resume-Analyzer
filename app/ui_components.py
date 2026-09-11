import streamlit as st

def render_hero(title: str, subtitle: str):
    """Renders main application hero banner."""
    st.markdown(
        f"""
        <div class="hero-container">
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_feature_card(icon: str, title: str, description: str):
    """Renders small informative dashboard feature cards."""
    st.markdown(
        f"""
        <div class="feature-card">
            <div style="font-size: 20px; margin-bottom: 6px;">{icon}</div>
            <div style="font-size: 14px; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">{title}</div>
            <div style="font-size: 12px; color: #94A3B8; line-height: 1.4;">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_metric_card(title: str, value: str, icon: str):
    """Renders metric summary box."""
    st.markdown(
        f"""
        <div class="metric-card-container">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 13px; font-weight: 600; color: #94A3B8;">{title}</span>
                <span style="font-size: 18px;">{icon}</span>
            </div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 26px; font-weight: 800; color: #FFFFFF; margin-top: 6px;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_score_card(score: float, config: dict):
    """Renders visual overall match score component."""
    st.markdown(
        f"""
        <div style="background: {config['bg_gradient']}; border: 1.5px solid {config['border_color']}; border-radius: 12px; padding: 22px; text-align: center;">
            <div style="display: inline-block; background-color: {config['badge_bg']}; color: {config['badge_text']}; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 10px;">
                {config['icon']} {config['label']}
            </div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 42px; font-weight: 800; color: {config['text_color']};">
                {score:.1f}%
            </div>
            <div style="font-size: 12px; font-weight: 600; color: {config['text_color']}; opacity: 0.8; margin-top: 6px;">
                Overall Match Alignment
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_recommendation_card(missing_skills: list):
    """Renders recommended missing skills block."""
    st.markdown(
        """
        <div style="background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 18px;">
            <div style="font-size: 15px; font-weight: 700; color: #FFFFFF; margin-bottom: 10px;">
                💡 Missing Skill Gap Recommendations
            </div>
        """,
        unsafe_allow_html=True
    )
    if missing_skills:
        badges = "".join([f'<span style="display: inline-block; background-color: rgba(239, 68, 68, 0.2); color: #FCA5A5; padding: 5px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; margin: 0 6px 6px 0; border: 1px solid #EF4444;">+ {s}</span>' for s in missing_skills])
        st.markdown(f"<div>{badges}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size: 13px; color: #4ADE80; font-weight: 600;">✅ Excellent alignment! No critical skill gaps identified.</div></div>', unsafe_allow_html=True)

def render_empty_state():
    """Renders empty placeholder prior to analysis run."""
    st.markdown(
        """
        <div style="background: #0F172A; border: 2px dashed #334155; border-radius: 12px; padding: 40px; text-align: center; margin-top: 10px;">
            <div style="font-size: 32px; margin-bottom: 8px;">📊</div>
            <div style="font-size: 16px; font-weight: 700; color: #F8FAFC;">Ready for Matching Analysis</div>
            <div style="font-size: 13px; color: #94A3B8; max-width: 400px; margin: 4px auto 0 auto;">Upload candidate resume and target job requirements above, then click 'Run Algorithmic Matching' to view metrics.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_footer(title: str, tagline: str):
    """Renders application footer."""
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background-color: #0F172A; border-radius: 12px; padding: 20px; text-align: center; color: #FFFFFF; border: 1px solid #1E293B;">
            <div style="font-family: 'Outfit', sans-serif; font-size: 15px; font-weight: 700;">{title}</div>
            <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">{tagline}</div>
        </div>
        """,
        unsafe_allow_html=True
    )