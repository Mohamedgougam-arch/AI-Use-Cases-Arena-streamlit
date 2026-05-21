from __future__ import annotations

import html
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st

from arena.admin_leaderboard import build_admin_contributor_rows, get_admin_totals
from arena.analytics import (
    generate_executive_summary,
    get_category_distribution,
    get_department_stats,
    get_impact_effort_matrix,
    get_quick_wins,
    get_strategic_bets,
    get_theme_counts,
    get_total_votes,
    get_top_use_case,
    get_trending_use_cases,
    get_voting_trend_data,
)
from arena.auth import ADMIN_DISPLAY_NAME, normalize_email
from arena.constants import (
    CATEGORIES,
    DEPARTMENTS,
    EFFORT_LEVELS,
    IMPACT_LEVELS,
    SORT_OPTIONS,
    departments_match,
    get_display_department,
)
from arena.filters import collect_tags, filter_and_sort_use_cases
from arena.participants import (
    SCORE_POINTS,
    SCORE_RULES,
    build_participant_scores,
    get_participant_score,
    is_participant_score_leader,
)
from arena.scoring import is_quick_win
from arena.store import ArenaStore
from arena.ui.components import (
    dashboard_hero,
    empty_state,
    format_date,
    format_relative_date,
    heatmap_html,
    innovation_momentum_card,
    page_header,
    required_select,
    render_use_case_card,
    render_vote_controls,
    section_heading,
    stat_card,
)
from arena.ui.effects import celebrate_submission


def render_dashboard(store: ArenaStore, email: str, is_admin: bool) -> None:
    use_cases = store.use_cases
    dashboard_hero(
        "AI Use Cases Arena" if is_admin else "Your AI Use Cases Arena",
        "Administrator overview" if is_admin else "Welcome back",
        email,
        is_admin=is_admin,
    )

    total_votes = get_total_votes(use_cases)
    top = get_top_use_case(use_cases)
    dept_stats = get_department_stats(use_cases)
    trending = get_trending_use_cases(use_cases, 3)
    quick_wins = get_quick_wins(use_cases)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        stat_card("Total Use Cases", len(use_cases), icon_key="file")
    with c2:
        stat_card("Total Votes", total_votes, icon_key="votes")
    with c3:
        stat_card(
            "Top-Ranked Use Case",
            top["votes"] if top else 0,
            (top["title"][:30] + "...") if top else None,
            icon_key="trophy",
        )
    with c4:
        stat_card(
            "Most Active Department",
            dept_stats[0]["useCaseCount"] if dept_stats else 0,
            dept_stats[0]["department"] if dept_stats else None,
            icon_key="building",
        )

    left, right = st.columns([2, 1])
    with left:
        st.markdown('<div class="panel-glass-start"></div>', unsafe_allow_html=True)
        col_h, col_link = st.columns([4, 1])
        with col_h:
            section_heading("Trending Use Cases", icon="📈")
        with col_link:
            if st.button("View all", key="dash_view_gallery"):
                st.session_state["page"] = "Gallery"
                st.rerun()
        if not trending:
            empty_state(
                "No use cases yet",
                "Submissions from teams will appear here once the arena has activity."
                if is_admin
                else "Be the first to submit an AI use case for your team.",
            )
            if not is_admin and st.button("Submit Use Case", key="dash_empty_submit", type="primary"):
                st.session_state["page"] = "Submit Use Case"
                st.rerun()
        else:
            for uc in trending:
                render_use_case_card(
                    store, email, uc, show_detail_button=False
                )

    with right:
        st.markdown('<div class="panel-glass-start"></div>', unsafe_allow_html=True)
        section_heading("Quick Wins", icon="⚡")
        st.markdown(
            '<p class="muted-copy panel-sub">High impact, low effort opportunities</p>',
            unsafe_allow_html=True,
        )
        if not quick_wins:
            st.markdown('<p class="muted-copy">No quick wins identified yet.</p>', unsafe_allow_html=True)
        else:
            for uc in quick_wins[:4]:
                st.markdown(
                    f'<p class="qw-title">{html.escape(uc["title"])}</p>'
                    f'<p class="qw-score">Score {uc["innovationScore"]}</p>',
                    unsafe_allow_html=True,
                )
                if st.button("Open", key=f"qw_{uc['id']}", use_container_width=True):
                    st.session_state["detail_id"] = uc["id"]
                    st.session_state["page"] = "Use Case Detail"
                    st.rerun()

        st.markdown('<div class="panel-glass-start panel-spaced"></div>', unsafe_allow_html=True)
        section_heading("Hottest Departments", icon="🔥", icon_tone="orange")
        if dept_stats:
            rows = "".join(
                f'<div class="dept-row"><span>{i + 1}. {html.escape(d["department"])}</span>'
                f'<strong>{d["innovationScore"]}</strong></div>'
                for i, d in enumerate(dept_stats[:5])
            )
            st.markdown(f'<div class="dept-list">{rows}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="muted-copy">No department activity yet.</p>', unsafe_allow_html=True)

        innovation_momentum_card(total_votes, len(use_cases) > 0)

    st.markdown('<div class="panel-glass-start heatmap-panel"></div>', unsafe_allow_html=True)
    section_heading("AI Opportunity Heatmap")
    st.markdown(heatmap_html(dept_stats), unsafe_allow_html=True)


def render_submit(store: ArenaStore, email: str) -> None:
    st.markdown('<div class="page-submit-marker"></div>', unsafe_allow_html=True)
    page_header(
        "Submit a Use Case",
        "Your idea is saved under your login email. You earn points when others vote.",
        icon="➕",
    )

    with st.form("submit_form", clear_on_submit=True):
        title = st.text_input("Title *", placeholder="e.g. AI-Powered Contract Review")
        description = st.text_area(
            "Description *", placeholder="Brief overview of the use case"
        )
        business_problem = st.text_area(
            "Business Problem", placeholder="What challenge does this solve?"
        )
        proposed_solution = st.text_area(
            "Proposed AI Solution", placeholder="How would AI address this?"
        )
        c1, c2 = st.columns(2)
        with c1:
            department = required_select("Department *", list(DEPARTMENTS), "Select department")
            impact = required_select("Expected Impact *", list(IMPACT_LEVELS), "Impact level")
        with c2:
            category = required_select("Category *", list(CATEGORIES), "Select category")
            effort = required_select("Effort *", list(EFFORT_LEVELS), "Effort level")
        tags = st.text_input(
            "Tags (comma-separated)", placeholder="NLP, Automation, Quick Win"
        )
        submitted = st.form_submit_button(
            "Submit to Arena",
            type="primary",
            use_container_width=True,
        )
        if submitted:
            missing = not (
                title
                and description
                and department
                and impact
                and effort
                and category
            )
            if missing:
                st.markdown(
                    '<p class="form-error">Please fill in all required fields.</p>',
                    unsafe_allow_html=True,
                )
            else:
                store.submit_use_case(
                    email,
                    {
                        "title": title.strip(),
                        "description": description.strip(),
                        "businessProblem": business_problem.strip(),
                        "proposedSolution": proposed_solution.strip(),
                        "department": department,
                        "impact": impact,
                        "effort": effort,
                        "category": category,
                        "tags": [t.strip() for t in tags.split(",") if t.strip()],
                    },
                )
                celebrate_submission(SCORE_POINTS["submit"])


def render_gallery(store: ArenaStore, email: str) -> None:
    use_cases = store.use_cases
    page_header(
        "Use Case Gallery",
        "Discover, vote, and discuss AI ideas from across Invest-NL.",
        icon="▦",
    )

    st.markdown('<p class="field-label">Search use cases</p>', unsafe_allow_html=True)
    search = st.text_input(
        "Search use cases",
        placeholder="Search...",
        label_visibility="collapsed",
    )
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    tags = collect_tags(use_cases)
    with c1:
        dept = st.selectbox("Department", ["All"] + list(DEPARTMENTS))
    with c2:
        cat = st.selectbox("Category", ["All"] + list(CATEGORIES))
    with c3:
        imp = st.selectbox("Impact", ["All"] + list(IMPACT_LEVELS))
    with c4:
        eff = st.selectbox("Effort", ["All"] + list(EFFORT_LEVELS))
    with c5:
        tag = st.selectbox("Tag", ["All"] + tags)
    with c6:
        sort_labels = {k: v for k, v in SORT_OPTIONS}
        sort = st.selectbox(
            "Sort by",
            list(sort_labels.keys()),
            format_func=lambda k: sort_labels[k],
        )

    filtered = filter_and_sort_use_cases(
        use_cases,
        search=search,
        department=None if dept == "All" else dept,
        category=None if cat == "All" else cat,
        impact=None if imp == "All" else imp,
        effort=None if eff == "All" else eff,
        tag=None if tag == "All" else tag,
        sort=sort,
    )

    if not use_cases:
        empty_state(
            "No use cases yet",
            "Be the first to submit an AI use case for your team.",
        )
    elif not filtered:
        empty_state(
            "No use cases found",
            "Try adjusting your filters or search query.",
        )
    else:
        st.markdown(
            f'<p class="result-count">{len(filtered)} use case(s)</p>',
            unsafe_allow_html=True,
        )
        for uc in filtered:
            render_use_case_card(store, email, uc)


def render_detail(store: ArenaStore, email: str, is_admin: bool) -> None:
    uc_id = st.session_state.get("detail_id")
    if not uc_id:
        st.warning("Select a use case from the gallery.")
        if st.button("Go to Gallery"):
            st.session_state["page"] = "Gallery"
            st.rerun()
        return

    use_case = store.get_use_case(uc_id)
    if not use_case:
        st.error("Use case not found.")
        if st.button("Back to gallery"):
            st.session_state["page"] = "Gallery"
            st.rerun()
        return

    if st.button("← Back to gallery"):
        st.session_state["page"] = "Gallery"
        st.rerun()

    st.title(use_case["title"])
    if use_case.get("submitterEmail"):
        st.caption(use_case["submitterEmail"])
    st.write(use_case["description"])
    st.write(
        f"Submitted {format_date(use_case['createdAt'])} · "
        f"{get_display_department(use_case['department'])} · {use_case['category']} · "
        f"{use_case['status']}"
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Votes", use_case["votes"])
    with c2:
        ranked = sorted(store.use_cases, key=lambda u: u["innovationScore"], reverse=True)
        rank = next((i + 1 for i, u in enumerate(ranked) if u["id"] == uc_id), 0)
        st.metric("Arena Rank", f"#{rank}")
    with c3:
        st.metric("Impact / Effort", f"{use_case['impact']} / {use_case['effort']}")

    render_vote_controls(store, email, use_case)

    st.subheader("Business Problem")
    st.write(use_case.get("businessProblem") or "—")
    st.subheader("Proposed AI Solution")
    st.write(use_case.get("proposedSolution") or "—")

    if use_case.get("tags"):
        st.markdown(" ".join(f"`#{t}`" for t in use_case["tags"]))

    st.subheader("AI-Generated Summary (placeholder)")
    summary = (
        f'This use case proposes leveraging AI to address "{use_case.get("businessProblem", "")[:80]}..." '
        f"through {use_case.get('proposedSolution', '')[:100]}... "
        f"With {use_case['impact']} impact and {use_case['effort']} effort, "
        f"it scores {use_case['innovationScore']} on the innovation index."
    )
    st.info(summary)

    _render_creator_messages(store, email, is_admin, use_case)

    st.subheader(f"Discussion ({len(use_case.get('comments', []))})")
    for c in use_case.get("comments", []):
        with st.container():
            st.markdown(f"**{c['userName']}** · {format_relative_date(c['createdAt'])}")
            st.write(c["text"])

    if not is_admin:
        comment = st.text_area("Add your thoughts...")
        if st.button("Post Comment") and comment.strip():
            store.add_comment(email, uc_id, comment.strip())
            st.toast(f"+{SCORE_POINTS['comment']} point")
            st.rerun()
    else:
        st.caption("Administrators can vote and review but do not post public comments.")

    similar = [
        uc
        for uc in store.use_cases
        if uc["id"] != uc_id
        and (
            uc["category"] == use_case["category"]
            or departments_match(uc["department"], use_case["department"])
        )
    ]
    similar.sort(key=lambda u: u["innovationScore"], reverse=True)
    if similar[:3]:
        st.subheader("Similar Use Cases")
        for uc in similar[:3]:
            render_use_case_card(store, email, uc, show_vote=False)


def _render_creator_messages(
    store: ArenaStore, email: str, is_admin: bool, use_case: dict[str, Any]
) -> None:
    creator = normalize_email(use_case.get("submitterEmail") or "")
    viewer = normalize_email(email)
    is_creator = bool(creator and viewer == creator)
    can_send = bool(email and creator and not is_creator)

    if not creator and not is_admin:
        return

    st.subheader("Messages for the creator" if is_creator else "Message for the creator")
    if is_creator or is_admin:
        messages = use_case.get("creatorMessages", [])
        if not messages:
            st.caption("No messages yet.")
        for m in messages:
            st.markdown(f"**{m['fromName']}** ({m['fromEmail']}) · {format_relative_date(m['createdAt'])}")
            st.write(m["text"])

    if can_send:
        msg = st.text_area("Private note to creator")
        if st.button("Send to creator") and msg.strip():
            if store.add_creator_message(email, use_case["id"], msg):
                st.success("Message sent — only the creator can read this.")
                st.rerun()
            else:
                st.error("You cannot message yourself on your own use case.")


def render_insights(store: ArenaStore) -> None:
    use_cases = store.use_cases
    page_header(
        "Insights & Analytics",
        "Data-driven view of AI innovation across Invest-NL.",
        icon="📈",
    )

    if st.button("Generate AI Executive Summary"):
        with st.spinner("Generating..."):
            st.session_state["exec_summary"] = generate_executive_summary(use_cases)

    if st.session_state.get("exec_summary"):
        st.markdown("### AI Executive Summary")
        st.write(st.session_state["exec_summary"])

    quick_wins = get_quick_wins(use_cases)
    strategic = get_strategic_bets(use_cases)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Use Cases", len(use_cases))
    c2.metric("Total Votes", get_total_votes(use_cases))
    c3.metric("Quick Wins", len(quick_wins))
    c4.metric("Strategic Bets", len(strategic))

    top_voted = sorted(use_cases, key=lambda u: u["votes"], reverse=True)[:6]
    dept_stats = get_department_stats(use_cases)
    category_data = get_category_distribution(use_cases)
    themes = get_theme_counts(use_cases)
    matrix = get_impact_effort_matrix(use_cases)
    trend = get_voting_trend_data(use_cases)
    contributors = build_participant_scores(use_cases)[:6]

    col_a, col_b = st.columns(2)
    with col_a:
        if top_voted:
            df = pd.DataFrame(
                [{"title": u["title"][:25], "votes": u["votes"]} for u in top_voted]
            )
            fig = px.bar(df, x="title", y="votes", title="Top Voted Use Cases")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#c8d4cc")
            st.plotly_chart(fig, use_container_width=True)
    with col_b:
        if category_data:
            df = pd.DataFrame(category_data)
            fig = px.pie(df, names="name", values="value", title="Category Distribution")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#c8d4cc")
            st.plotly_chart(fig, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        if dept_stats:
            df = pd.DataFrame(dept_stats[:8])
            fig = px.bar(df, x="department", y="innovationScore", title="Department Leaderboard")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#c8d4cc")
            st.plotly_chart(fig, use_container_width=True)
    with col_d:
        if trend:
            df = pd.DataFrame(trend)
            fig = px.line(df, x="month", y="votes", title="Voting Trends")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#c8d4cc")
            st.plotly_chart(fig, use_container_width=True)

    if matrix:
        df = pd.DataFrame(matrix)
        fig = px.scatter(
            df,
            x="effort",
            y="impact",
            size="votes",
            hover_name="title",
            title="Impact vs Effort Matrix",
            labels={"effort": "Effort", "impact": "Impact"},
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#c8d4cc")
        st.plotly_chart(fig, use_container_width=True)

    if themes:
        df = pd.DataFrame(themes)
        fig = px.bar(df, x="name", y="count", title="Most Common Themes")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#c8d4cc")
        st.plotly_chart(fig, use_container_width=True)

    q1, q2 = st.columns(2)
    with q1:
        st.subheader("Quick Wins")
        for uc in quick_wins:
            st.write(f"**{uc['title']}** — score {uc['innovationScore']}")
    with q2:
        st.subheader("Strategic Bets")
        for uc in strategic:
            st.write(f"**{uc['title']}** — score {uc['innovationScore']}")

    st.subheader("Most Active Contributors")
    if contributors:
        for u in contributors:
            st.write(f"**{u['name']}** ({u['email']}) — **{u['score']}** pts")
    else:
        st.caption("No contributors yet.")


def render_leaderboard(store: ArenaStore) -> None:
    use_cases = store.use_cases
    page_header(
        "Admin Leaderboard",
        "Overview of signed-in users and arena activity. Ranked by score.",
        icon="🏆",
    )
    st.info("Admin only. Lists users who signed in, merged with submissions, votes, and scores.")

    totals = get_admin_totals(use_cases)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total use cases", totals["totalUseCases"])
    c2.metric("Total votes", totals["totalVotes"])
    contributors = build_admin_contributor_rows(use_cases, store.known_users)
    c3.metric("Users (signed in / active)", len(contributors))

    col_table, col_guide = st.columns([2, 1])
    with col_table:
        st.subheader("All users by score")
        if contributors:
            df = pd.DataFrame(contributors)
            st.dataframe(
                df[
                    [
                        "rank",
                        "name",
                        "email",
                        "score",
                        "submissions",
                        "votesReceived",
                        "votesCast",
                        "comments",
                        "lastSignedInAt",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.caption("No users yet.")

    with col_guide:
        st.subheader("How scoring works")
        for label, points in SCORE_RULES:
            st.write(f"**{label}** — +{points} pts")


def render_battle(store: ArenaStore) -> None:
    stats = get_department_stats(store.use_cases)
    max_score = stats[0]["innovationScore"] if stats else 1

    page_header(
        "Department Battle Mode",
        "Which team will lead the AI transformation?",
        icon="⚔",
    )

    st.markdown(
        '<p class="hero-title" style="font-size:1.75rem;text-align:center;">'
        "Which team will lead the AI transformation?</p>",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Current Leader", stats[0]["department"] if stats else "—")
    c2.metric("Total Submissions", sum(d["useCaseCount"] for d in stats))
    c3.metric("Total Votes", sum(d["totalVotes"] for d in stats))

    st.subheader("Live Department Rankings")
    if not stats:
        st.caption("No department rankings yet.")
        return

    for i, d in enumerate(stats, 1):
        pct = min(100, int((d["innovationScore"] / max_score) * 100)) if max_score else 0
        st.write(f"**#{i} {d['department']}**")
        st.progress(pct / 100, text=f"Score {d['innovationScore']} · {d['useCaseCount']} cases · {d['totalVotes']} votes")
