# P21 author-host five-seed orchestrator, explicitly opt-in at execution.
# Runs ONLY official TRAIN-derived internal validation; NEVER official TEST.
# Do not rewrite existing P9/P15 or PDF. No full-training wall-time deadline.
param(
  [string]$Python = ".\.venv-p15-local\Scripts\python.exe"
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
  throw "Missing verified P21 Python interpreter: $Python"
}
$base = "results/controlled_extensions"
if (-not (Test-Path -LiteralPath $base -PathType Container)) {
  throw "Run this script from the NCKH repository root"
}

# Cheap and synthetic-only checks first (the grouped-stack test FITs FABRICATED data).
foreach ($suite in @(
  "test_p21_science_acceptance.py",
  "test_p21_science_aggregation.py",
  "test_p21_science_synthetic.py"
)) {
  & $Python -m unittest discover -s tests -p $suite -v
  if ($LASTEXITCODE -ne 0) { throw "NO_GO: failed synthetic suite $suite" }
}
& $Python -X utf8 tools/p21_protocol_validator.py --verify-local-train-sha
if ($LASTEXITCODE -ne 0) { throw "NO_GO: immutable protocol/source check failed" }

$seedList = @(1103,2207,3301,4409,5501)
foreach ($seed in $seedList) {
  $folders = @(Get-ChildItem -Path $base -Directory -Filter "p21_train_only_science_seed_${seed}_*" -ErrorAction Stop)
  $accepted = @()
  foreach ($folder in $folders) {
    $reportPath = Join-Path $folder.FullName "run_report.json"
    if (Test-Path -LiteralPath $reportPath -PathType Leaf) {
      $data = Get-Content -LiteralPath $reportPath -Raw -Encoding UTF8 | ConvertFrom-Json
      if ($data.status -eq "PASS_INTERNAL_TRAIN_VALIDATION_SEED_ONLY" -and [int]$data.seed -eq $seed) {
        $accepted += $folder
      }
    }
  }
  if ($accepted.Count -gt 1) {
    throw "NO_GO: multiple accepted attempts for seed $seed; do not cherry-pick results"
  }
  if ($accepted.Count -eq 1) {
    Write-Host "SKIP already accepted seed $seed : $($accepted[0].Name)"
    continue
  }

  # New attempt number, never remove/overwrite failed/interrupted evidence.
  $attempt = 1
  do {
    $suffix = "{0:D2}" -f $attempt
    $relativeOut = "$base/p21_train_only_science_seed_${seed}_$suffix"
    $taken = Test-Path -LiteralPath $relativeOut
    $attempt += 1
  } while ($taken)
  Write-Host "Starting supervised full P21 seed $seed ($relativeOut)"
  & $Python -X utf8 tools/p21_science_supervisor.py `
    --authorize I_AUTHORIZE_P21_TRAIN_ONLY_POST_HOC_FULL_SCIENCE `
    --seed $seed `
    --out-dir $relativeOut
  if ($LASTEXITCODE -ne 0) {
    throw "STOP: seed $seed failed or resource gate refused. Preserve evidence; rerun this script only after reviewing the blocker"
  }
}

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$summary = "$base/p21_train_only_science_summary_$stamp"
& $Python -X utf8 tools/p21_science_aggregate.py --out-dir $summary
if ($LASTEXITCODE -ne 0) {
  throw "NO_GO: five-seed aggregation failed; do not publish or edit PDF using partial scores"
}
Write-Host "PASS: Five paired seeds measured on P21 INTERNAL VALIDATION only."
Write-Host "Summary: $summary/report.md"
Write-Host "No official TEST, historical frozen result, or prior PDF was changed."
