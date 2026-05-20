from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from arena.auth import (
    ADMIN_DISPLAY_NAME,
    ADMIN_EMAIL,
    get_display_name_from_email,
    is_admin_email,
    normalize_email,
)
from arena.constants import normalize_department
from arena.scoring import (
    calculate_innovation_score,
    derive_use_case_badges,
    get_days_since_created,
)
from arena.storage import load_state, save_state


class ArenaStore:
    def __init__(self) -> None:
        self._state = load_state()

    @property
    def use_cases(self) -> list[dict[str, Any]]:
        return self._state["useCases"]

    @property
    def known_users(self) -> list[dict[str, Any]]:
        return self._state["knownUsers"]

    def reload(self) -> None:
        self._state = load_state()

    def persist(self) -> None:
        save_state(self._state)

    def get_voted_ids(self, email: str) -> list[str]:
        return list(self._state["userVotes"].get(normalize_email(email), []))

    def has_voted(self, email: str, use_case_id: str) -> bool:
        return use_case_id in self.get_voted_ids(email)

    def register_login(self, email: str) -> None:
        normalized = normalize_email(email)
        if not normalized or "@" not in normalized or normalized == ADMIN_EMAIL:
            return
        now = datetime.now(timezone.utc).isoformat()
        users = self._state["knownUsers"]
        existing = next((u for u in users if u["email"] == normalized), None)
        if existing:
            existing["lastSeenAt"] = now
        else:
            users.append(
                {"email": normalized, "firstSeenAt": now, "lastSeenAt": now}
            )
        self.persist()

    def submit_use_case(self, email: str, data: dict[str, Any]) -> dict[str, Any]:
        normalized = normalize_email(email)
        now = datetime.now(timezone.utc).isoformat()
        uc_id = f"uc-{int(datetime.now().timestamp() * 1000)}"
        uc: dict[str, Any] = {
            "id": uc_id,
            "title": data["title"],
            "description": data["description"],
            "businessProblem": data.get("businessProblem", ""),
            "proposedSolution": data.get("proposedSolution", ""),
            "department": normalize_department(data["department"]),
            "category": data["category"],
            "impact": data["impact"],
            "effort": data["effort"],
            "tags": data.get("tags", []),
            "votes": 0,
            "voterIds": [],
            "voterEmails": [],
            "comments": [],
            "creatorMessages": [],
            "submitter": get_display_name_from_email(normalized),
            "submitterId": normalized,
            "submitterEmail": normalized,
            "createdAt": now,
            "innovationScore": 0,
            "status": "Submitted",
            "badges": [],
        }
        uc["innovationScore"] = calculate_innovation_score(
            0, uc["impact"], uc["effort"], 0, 0
        )
        uc["badges"] = derive_use_case_badges(uc)
        self._state["useCases"].insert(0, uc)
        self.persist()
        return uc

    def _update_use_case(self, uc_id: str, updater) -> None:
        for i, uc in enumerate(self._state["useCases"]):
            if uc["id"] == uc_id:
                updated = updater(uc)
                if updated is not None:
                    self._state["useCases"][i] = updated
                break
        self.persist()

    def vote(self, email: str, use_case_id: str) -> bool:
        normalized = normalize_email(email)
        votes_map = self._state["userVotes"]
        user_votes = votes_map.setdefault(normalized, [])
        if use_case_id in user_votes:
            return False

        def updater(uc: dict[str, Any]) -> dict[str, Any]:
            if normalized in uc.get("voterEmails", []):
                return uc
            votes = uc["votes"] + 1
            uc = {
                **uc,
                "votes": votes,
                "voterEmails": [*uc.get("voterEmails", []), normalized],
                "voterIds": [*uc.get("voterIds", []), normalized],
            }
            days = get_days_since_created(uc["createdAt"])
            uc["innovationScore"] = calculate_innovation_score(
                votes, uc["impact"], uc["effort"], len(uc["comments"]), days
            )
            uc["badges"] = derive_use_case_badges(uc)
            return uc

        found = any(uc["id"] == use_case_id for uc in self.use_cases)
        if not found:
            return False

        user_votes.append(use_case_id)
        self._update_use_case(use_case_id, updater)
        return True

    def unvote(self, email: str, use_case_id: str) -> bool:
        normalized = normalize_email(email)
        votes_map = self._state["userVotes"]
        user_votes = votes_map.get(normalized, [])
        if use_case_id not in user_votes:
            return False

        def updater(uc: dict[str, Any]) -> dict[str, Any]:
            if normalized not in uc.get("voterEmails", []):
                return uc
            votes = max(0, uc["votes"] - 1)
            uc = {
                **uc,
                "votes": votes,
                "voterEmails": [e for e in uc.get("voterEmails", []) if e != normalized],
                "voterIds": [i for i in uc.get("voterIds", []) if i != normalized],
            }
            days = get_days_since_created(uc["createdAt"])
            uc["innovationScore"] = calculate_innovation_score(
                votes, uc["impact"], uc["effort"], len(uc["comments"]), days
            )
            uc["badges"] = derive_use_case_badges(uc)
            return uc

        votes_map[normalized] = [v for v in user_votes if v != use_case_id]
        self._update_use_case(use_case_id, updater)
        return True

    def add_comment(self, email: str, use_case_id: str, text: str) -> bool:
        if is_admin_email(email):
            return False
        normalized = normalize_email(email)
        comment = {
            "id": f"comment-{int(datetime.now().timestamp() * 1000)}",
            "useCaseId": use_case_id,
            "userId": normalized,
            "userEmail": normalized,
            "userName": get_display_name_from_email(normalized),
            "text": text.strip(),
            "createdAt": datetime.now(timezone.utc).isoformat(),
        }

        def updater(uc: dict[str, Any]) -> dict[str, Any]:
            comments = [*uc.get("comments", []), comment]
            uc = {**uc, "comments": comments}
            days = get_days_since_created(uc["createdAt"])
            uc["innovationScore"] = calculate_innovation_score(
                uc["votes"], uc["impact"], uc["effort"], len(comments), days
            )
            uc["badges"] = derive_use_case_badges(uc)
            return uc

        self._update_use_case(use_case_id, updater)
        return True

    def add_creator_message(self, email: str, use_case_id: str, text: str) -> bool:
        normalized = normalize_email(email)
        uc = next((u for u in self.use_cases if u["id"] == use_case_id), None)
        if not uc or not text.strip():
            return False
        creator = normalize_email(uc.get("submitterEmail") or "")
        if not creator or normalized == creator:
            return False

        message = {
            "id": f"creator-msg-{int(datetime.now().timestamp() * 1000)}",
            "useCaseId": use_case_id,
            "fromEmail": normalized,
            "fromName": (
                ADMIN_DISPLAY_NAME
                if is_admin_email(normalized)
                else get_display_name_from_email(normalized)
            ),
            "text": text.strip(),
            "createdAt": datetime.now(timezone.utc).isoformat(),
        }

        def updater(u: dict[str, Any]) -> dict[str, Any]:
            return {
                **u,
                "creatorMessages": [*u.get("creatorMessages", []), message],
            }

        self._update_use_case(use_case_id, updater)
        return True

    def get_use_case(self, use_case_id: str) -> dict[str, Any] | None:
        return next((uc for uc in self.use_cases if uc["id"] == use_case_id), None)
