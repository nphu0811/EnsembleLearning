#!/usr/bin/env python3
"""Independent, read-only portable audit of the committed Creative Rebuild V2.

Does NOT require PowerPoint, training data, Windows, or installing presentation
skills. Validates actual binary outputs in GitHub rather than trusting saved QA.
Pass means *technical structural acceptance*, not human approval of narration.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

DEFAULT = Path(__file__).resolve().parents[1] / "presentation/nckh_defense/creative_rebuild_v2"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}

def assert_true(ok, message):
    if not ok:
        raise ValueError(message)

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def media_probe(path):
    cmd = ["ffprobe", "-v", "error", "-show_format", "-show_streams",
           "-of", "json", str(path)]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)

def pdf_pages(path):
    result = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, check=True)
    match = re.search(r"^Pages:\s*(\d+)$", result.stdout, re.MULTILINE)
    assert_true(match is not None, "pdfinfo missing Pages line")
    return int(match.group(1))

def audit(base):
    files = {
        "pptx": "NCKH_Ensemble_IDS_Creative_Final.pptx",
        "mp4": "NCKH_Ensemble_IDS_Creative_Preview.mp4",
        "report_v7": "Bao_cao_NCKH_EnsembleLearning_REVISION_V7.pdf",
        "slides_pdf": "NCKH_Ensemble_IDS_Static.pdf",
        "delivery_zip": "NCKH_Ensemble_IDS_Creative_Delivery.zip",
        "source_zip": "LaTeX_Revision_V7_Source.zip",
        "checksums": "checksums.sha256",
        "script": "Kich_ban_6_phut_Humanized.md",
        "qna": "QnA_Humanized.md",
        "qa": "QA_Report.md",
    }
    for key, name in files.items():
        assert_true((base / name).is_file() and (base / name).stat().st_size > 0,
                    f"Missing/empty {key}: {name}")
    stats_path = base / "NCKH_Ensemble_IDS_Creative_Final.native_stats.json"
    original = json.loads(stats_path.read_text(encoding="utf-8"))
    assert_true(len(original) == 29, "expected 29 authored slides in native stats")
    slide_rows = []
    with zipfile.ZipFile(base / files["pptx"]) as z:
        assert_true(z.testzip() is None, "PPTX corrupt ZIP member")
        names = z.namelist()
        slides = sorted(
            [s for s in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", s)],
            key=lambda v: int(re.search(r"slide(\d+)\.xml", v).group(1))
        )
        assert_true(len(slides) == 29, f"expected 29 physical slides, got {len(slides)}")
        for i, name in enumerate(slides, 1):
            root = ET.fromstring(z.read(name))
            timings = len(root.findall(".//p:timing", NS))
            motions = len(root.findall(".//p:animMotion", NS))
            scales = len(root.findall(".//p:animScale", NS))
            effects = len([e for e in root.findall(".//p:cTn", NS)
                           if e.get("presetID") is not None])
            hidden = root.get("show") == "0"
            ids = {el.attrib["id"] for el in root.findall(".//p:cNvPr", NS)}
            targets = [el.attrib.get("spid") for el in root.findall(".//p:spTgt", NS)]
            assert_true(all(t in ids for t in targets), f"Slide {i} has invalid animation targets")
            assert_true(timings == (1 if i <= 17 else 0),
                        f"Slide {i} timing/hidden-main mismatch")
            assert_true(hidden == (i > 17), f"Slide {i} hidden-Q&A mismatch")
            if i <= 17:
                assert_true(effects > 0, f"Slide {i} missing internal animation")
            slide_rows.append(dict(slide=i, hidden=hidden, motion_paths=motions,
                                   scale=scales, effects=effects, timing=timings))
    motion = sum(x["motion_paths"] for x in slide_rows)
    scales = sum(x["scale"] for x in slide_rows)
    effects = sum(x["effects"] for x in slide_rows)
    assert_true(motion >= 50 and scales >= 10 and effects >= 400,
                f"Insufficient real in-slide effects: {motion=},{scales=},{effects=}")
    for i, (new, old) in enumerate(zip(slide_rows, original), 1):
        for field in ("slide", "hidden", "effects", "motion_paths", "scale"):
            assert_true(new[field] == old[field], f"Slide {i} disagrees with historical stats: {field}")

    timeline = json.loads((base / "timeline.json").read_text(encoding="utf-8"))
    assert_true(len(timeline) == 17, "timeline must have 17 main slides")
    prev = 0.0
    for i, entry in enumerate(timeline, 1):
        assert_true(entry["slide"] == i, f"Timeline slide identity {i}")
        assert_true(math.isclose(entry["start"], prev, abs_tol=.001),
                    f"Timeline discontinuity on slide {i}")
        assert_true(entry["end"] > entry["start"], f"Timeline non-positive length slide {i}")
        assert_true(entry["speech_start"] >= entry["start"] and
                    entry["speech_end"] <= entry["end"]+.02,
                    f"Voice runs beyond slide {i}")
        prev = entry["end"]
    assert_true(math.isclose(prev, 360, abs_tol=.1), "Total authored timeline != 360 sec")

    probe = media_probe(base / files["mp4"])
    duration = float(probe["format"]["duration"])
    assert_true(abs(duration - 360.0) < .25, f"MP4 not 6:00: {duration}")
    video = next((s for s in probe["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in probe["streams"] if s["codec_type"] == "audio"), None)
    assert_true(video is not None and video["width"] == 1920 and video["height"] == 1080,
                "MP4 not Full-HD video")
    assert_true(audio is not None, "MP4 missing narration/audio stream")

    reports = {"report_v7": pdf_pages(base / files["report_v7"]),
               "slides_pdf": pdf_pages(base / files["slides_pdf"])}
    assert_true(reports == {"report_v7": 49, "slides_pdf": 29},
                f"Unexpected report/slide PDF pages: {reports}")
    assert_true(digest(base / files["report_v7"]) ==
                "3579e41be58d24aee3807e000ffe6d762ebb857f1c588c1f0c503ef6f29cee0e",
                "V7 report changed relative to frozen humanized result")
    with zipfile.ZipFile(base / files["source_zip"]) as z:
        assert_true(z.testzip() is None, "LaTeX source ZIP corrupt")
    with zipfile.ZipFile(base / files["delivery_zip"]) as z:
        assert_true(z.testzip() is None, "Delivery ZIP corrupt")
        members = set(z.namelist())
        assert_true(all(files[k] in members for k in
                        ("pptx", "mp4", "report_v7", "slides_pdf", "source_zip", "script")),
                    "Delivery ZIP missing critical deliverable")

    expected = {}
    for line in (base / "checksums.sha256").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        m = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        assert_true(m is not None, f"Invalid SHA manifest row: {line[:100]}")
        expected[m.group(2)] = m.group(1)
    assert_true(len(expected) >= 200, "SHA manifest unexpectedly short")
    mismatches = [name for name, sha in expected.items()
                  if not (base / name).is_file() or digest(base / name) != sha]
    assert_true(not mismatches, f"Release manifest mismatch: {mismatches[:7]}")
    return {
        "status": "PASS_BINARY_TECHNICAL_AUDIT",
        "commit_artifact_source": str(base),
        "pptx_slides": len(slide_rows),
        "main_slides": 17,
        "hidden_qna": 12,
        "native_effects": effects,
        "native_motion_paths": motion,
        "native_scales": scales,
        "mp4_seconds": duration,
        "mp4_resolution": [video["width"], video["height"]],
        "mp4_audio_present": True,
        "pdf_pages": reports,
        "sha_manifest_entries": len(expected),
        "delivery_zip_crc_pass": True,
        "latex_source_zip_crc_pass": True,
        "human_audio_pronunciation_verified": False,
        "human_projector_rehearsal_verified": False,
        "disclaimer": "No new training or independent real-world scientific evaluation.",
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, default=DEFAULT)
    args = parser.parse_args()
    try:
        print(json.dumps(audit(args.dir), indent=2, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, ensure_ascii=False))
        return 1

if __name__ == "__main__":
    sys.exit(main())
