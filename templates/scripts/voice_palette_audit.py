#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = {
    "provider",
    "voice",
    "language",
    "gender",
    "age_band",
    "delivery",
    "emotion",
    "rate",
    "pitch",
    "allowed_for",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit voice palette diversity and topic assignments.")
    parser.add_argument("--config", default="voice_profiles.json")
    parser.add_argument("--min-profiles", type=int, default=12)
    parser.add_argument("--min-assigned-profiles", type=int, default=2)
    parser.add_argument("--min-genders", type=int, default=2)
    parser.add_argument("--min-age-bands", type=int, default=2)
    args = parser.parse_args()

    path = Path(args.config)
    data = json.loads(path.read_text(encoding="utf-8"))
    profiles = data.get("profiles", {})
    assignments = data.get("assignments", {})
    errors: list[str] = []

    if len(profiles) < args.min_profiles:
        errors.append(f"expected at least {args.min_profiles} profiles, got {len(profiles)}")
    if not assignments:
        errors.append("missing assignments")

    for profile_id, profile in profiles.items():
        missing = sorted(REQUIRED_FIELDS - set(profile))
        if missing:
            errors.append(f"{profile_id} missing fields: {', '.join(missing)}")

    assigned_profile_ids = set(assignments.values())
    unknown = sorted(pid for pid in assigned_profile_ids if pid not in profiles)
    if unknown:
        errors.append(f"assignments reference unknown profiles: {', '.join(unknown)}")
    if len(assigned_profile_ids) < args.min_assigned_profiles:
        errors.append(f"expected at least {args.min_assigned_profiles} assigned profiles, got {len(assigned_profile_ids)}")

    assigned_profiles = [profiles[pid] for pid in assigned_profile_ids if pid in profiles]
    all_profiles = list(profiles.values())
    all_genders = {p.get("gender") for p in all_profiles}
    all_age_bands = {p.get("age_band") for p in all_profiles}
    all_deliveries = {p.get("delivery") for p in all_profiles}
    all_languages = {p.get("language") for p in all_profiles}
    genders = {p.get("gender") for p in assigned_profiles}
    age_bands = {p.get("age_band") for p in assigned_profiles}
    deliveries = {p.get("delivery") for p in assigned_profiles}

    if len(all_genders) < args.min_genders:
        errors.append(f"palette expected at least {args.min_genders} genders, got {sorted(all_genders)}")
    if len(all_age_bands) < args.min_age_bands:
        errors.append(f"palette expected at least {args.min_age_bands} age bands, got {sorted(all_age_bands)}")
    if len(genders) < args.min_genders:
        errors.append(f"expected at least {args.min_genders} assigned genders, got {sorted(genders)}")
    if len(age_bands) < args.min_age_bands:
        errors.append(f"expected at least {args.min_age_bands} assigned age bands, got {sorted(age_bands)}")

    print(f"profiles={len(profiles)} assignments={len(assignments)} assigned_profiles={len(assigned_profile_ids)}")
    print(f"palette_genders={sorted(all_genders)}")
    print(f"palette_age_bands={sorted(all_age_bands)}")
    print(f"palette_languages={sorted(all_languages)}")
    print(f"palette_deliveries={sorted(all_deliveries)}")
    print(f"assigned_genders={sorted(genders)}")
    print(f"assigned_age_bands={sorted(age_bands)}")
    print(f"assigned_deliveries={sorted(deliveries)}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        raise SystemExit(1)

    print("voice palette audit passed")


if __name__ == "__main__":
    main()
