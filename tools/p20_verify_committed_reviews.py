"""Read-only structural/hash/evidence audit of committed P20-PRE AI reviews.

Safe for CI: no data CSVs from raw/, no model/joblib import, no training, no TEST.
The 80-file copied packet lives only on the author laptop; absent packet-only
anchors are SKIPPED and reported, never counted as verified.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
P20 = ROOT / "defense/p20_pre_2026_10_17_01"
SOURCE_COMMIT = "b3acf2e2f8ad15bdf4b11bb9450927a57309d968"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def code_of_recommendation(data) -> str | None:
    if isinstance(data, str):
        return data
    if isinstance(data, dict):
        return data.get("code", data.get("decision"))
    return None


def safe_repo_evidence(raw: str) -> Path | None:
    if not isinstance(raw, str) or not raw or "\\" in raw or ":" in raw:
        return None
    p = Path(raw)
    if p.is_absolute() or ".." in p.parts:
        return None
    # Avoid touching symlinked external data.
    source = ROOT / p
    try:
        target = source.resolve()
        if not target.is_relative_to(ROOT.resolve()):
            return None
        if source.is_symlink():
            return None
        return target
    except (OSError, ValueError):
        return None


def run_audit() -> dict:
    checks = []
    skipped = []
    reviewed = {"A": None, "B": None, "C": None}
    evidence_cache = {}

    def check(what: str, truth) -> None:
        checks.append({"check": what, "passed": bool(truth)})

    with (P20 / "packet_02/receipt.json").open(encoding="utf-8") as f:
        receipt = json.load(f)
    with (P20 / "packet_02/manifest.csv").open(encoding="utf-8-sig", newline="") as f:
        manifest = list(csv.DictReader(f))
    check("80 manifest rows", len(manifest) == receipt["entries"] == 80)
    check("manifest sha256", digest(P20 / "packet_02/manifest.csv") == receipt["manifest_sha256"])
    with (P20 / "review_reports_frozen.json").open(encoding="utf-8") as f:
        frozen = json.load(f)
    check("frozen commit", frozen.get("source_commit") == SOURCE_COMMIT)
    check("matching packet receipt", frozen.get("packet_manifest_sha256") == receipt["manifest_sha256"])
    check("3 frozen reports", [e.get("reviewer") for e in frozen["reports"]] == ["A", "B", "C"])

    for record in frozen["reports"]:
        rid = record["reviewer"]
        check(rid + " original source commit", record.get("source_commit") == SOURCE_COMMIT)
        for item in record["files"]:
            path = P20 / item["path"]
            check("safe report file " + item["path"], path.resolve().is_relative_to(P20.resolve()))
            check("SHA/bytes " + item["path"],
                  path.is_file() and digest(path) == item["sha256"]
                  and path.stat().st_size == item["bytes"])
        with (P20 / ("reviewer_" + rid + "/report.json")).open(encoding="utf-8") as f:
            report = json.load(f)
        reviewed[rid] = report
        check(rid + " reviewer identity", report.get("reviewer") == rid)
        check(rid + " same packet", report.get("packet_manifest_sha256") == receipt["manifest_sha256"])
        check(rid + " MAJOR_REVISION_REQUIRED", code_of_recommendation(report.get("recommendation")) == "MAJOR_REVISION_REQUIRED")
        check(rid + " 5 criteria", len(report.get("criteria_assessment", {})) == 5)
        check(rid + " 12 taxonomies", len(report.get("taxonomy_coverage", [])) == 12)
        check(rid + " >=10 questions", len(report.get("questions", [])) >= 10)
        identifiers = [item["id"] for item in report["concerns"]]
        check(rid + " unique concerns", len(identifiers) == len(set(identifiers)))
        for obj in report["concerns"]:
            check(obj["id"] + " still OPEN", obj.get("status") == "OPEN")
            check(obj["id"] + " calibrated severity", obj.get("severity") in {"MAJOR", "MINOR"})
            check(obj["id"] + " documented", all(bool(obj.get(k)) for k in
                  ("claim_pointer", "issue_key", "concern", "why_it_matters", "acceptance_test", "severity_rationale")))
        for obj in [*report["concerns"], *report["questions"], *report["strengths"]]:
            pointers = obj.get("evidence")
            check(obj["id"] + " has pointers", bool(pointers) and isinstance(pointers, list))
            for i, ev in enumerate(pointers or []):
                key = f"{obj['id']}-e{i}"
                raw = ev.get("path")
                check(key + " locator+anchor", bool(ev.get("locator")) and bool(ev.get("anchor")))
                candidate = safe_repo_evidence(raw)
                check(key + " path-safe", candidate is not None)
                if candidate is None:
                    continue
                if candidate.exists() and candidate.is_file() and candidate.suffix.lower() not in {".pdf", ".joblib"}:
                    if raw not in evidence_cache:
                        evidence_cache[raw] = normalize(candidate.read_text(encoding="utf-8-sig"))
                    check(key + " repo source anchor", normalize(ev["anchor"]) in evidence_cache[raw])
                else:
                    # Only the two locally generated packet extracts are expected
                    # to be absent from the tracked repository.
                    check(key + " local-only allowed",
                          raw in {"literature_reported_facts.csv", "literature_scope.json"})
                    skipped.append({"pointer": key, "path": raw, "reason": "PACKET_ONLY_NOT_IN_GIT"})

    with (P20 / "synthesis/concern_register.json").open(encoding="utf-8") as f:
        register = json.load(f)
    originals = [c for r in reviewed.values() for c in r["concerns"]]
    known_ids = [c["id"] for c in originals]
    linked = [id for g in register["concerns"] for id in g["reviewer_concern_ids"]]
    check("17 source concerns", len(originals) == 17)
    check("all source concerns exactly once", sorted(linked) == sorted(known_ids) and len(linked) == len(set(linked)))
    check("9 open groups", len(register["concerns"]) == 9 and all(g.get("status") == "OPEN" for g in register["concerns"]))
    check("P20 PRE disposition", register.get("disposition") == "P20_PRE_REVIEW_COMPLETED_WITH_OPEN_CONCERNS")
    check("5 real consensus groups", sum(g.get("consensus") for g in register["concerns"]) == 5)
    for g in register["concerns"]:
        check(g["id"] + " consensus definition", g["consensus"] == (len({x[0] for x in g["reviewer_concern_ids"]}) >= 2))
        check(g["id"] + " resolution actionable", bool(g.get("acceptance_test")))
    result = {
        "scope": "P20-PRE read-only review hashes, original concern integrity and tracked evidence anchors; not full 80-file packet QA or human review",
        "source_commit": SOURCE_COMMIT,
        "passed": sum(x["passed"] for x in checks),
        "failed": sum(not x["passed"] for x in checks),
        "checks": checks,
        "local_only_skipped_count": len(skipped),
        "local_only_skipped": skipped,
        "reviewer_qa": {id: {"concerns": len(r["concerns"]), "questions": len(r["questions"])}
                        for id, r in reviewed.items()},
    }
    return result


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, help="write a NEW JSON report; never overwrite existing evidence")
    args = p.parse_args()
    result = run_audit()
    print(json.dumps({k: result[k] for k in
                      ("scope", "passed", "failed", "local_only_skipped_count", "reviewer_qa")}, ensure_ascii=False))
    if args.out is not None:
        if args.out.exists():
            p.error("Refuse to overwrite existing QA output")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("x", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    return 0 if result["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
