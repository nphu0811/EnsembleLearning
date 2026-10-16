# P15: run the two REMAINING frozen full-TRAIN models in series, with NO wall-time deadline.
# The Python supervisor still checks RAM, disk, process-tree RSS and source/provenance.
# This script never invokes the original Phase-9 evaluation main() or official TEST.
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$python = Join-Path $repoRoot '.venv-p15-local\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    throw "No local Python environment: $python"
}
$jobs = @(
    @{
        Name = 'random_forest_42'
        Pilot = 'results/reproducibility/p15_local_rf42_pilot_01/run_report.json'
        Output = 'results/reproducibility/p15_local_rf42_full_02'
    },
    @{
        Name = 'stacking_42'
        Pilot = 'results/reproducibility/p15_local_stack_pilot_01/run_report.json'
        Output = 'results/reproducibility/p15_local_stack_full_01'
    }
)

Push-Location $repoRoot
try {
    foreach ($job in $jobs) {
        $candidate = $job.Name
        $output = $job.Output
        $pilot = $job.Pilot
        if (-not (Test-Path -LiteralPath $pilot -PathType Leaf)) {
            throw "Missing matching prior pilot evidence: $pilot"
        }
        if (Test-Path -LiteralPath $output) {
            throw "Output already exists; do not overwrite previous attempts: $output"
        }
        Write-Host "P15 full TRAIN: $candidate; NO wall-time deadline, 2-GiB RSS watchdog retained."
        Write-Host "Resource logs and artifact go to: $output"
        & $python 'tools/p15_local_supervisor.py' --mode full --candidate $candidate --pilot-report $pilot --out-dir $output --timeout-min 0
        $exit = $LASTEXITCODE
        if ($exit -ne 0) {
            throw "STOP: $candidate exited $exit. Preserve run_report.json and resource log. The NEXT model was NOT started."
        }
        $reportPath = Join-Path $output 'run_report.json'
        if (-not (Test-Path -LiteralPath $reportPath -PathType Leaf)) {
            throw "STOP: missing report after $candidate; next model NOT started."
        }
        $report = Get-Content -LiteralPath $reportPath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($report.result -ne 'PASS' -or
            $report.mode -ne 'full' -or
            $report.candidate -ne $candidate -or
            $report.worker_checks.passed -ne $true -or
            $report.worker_checks.train_rows -ne 175341 -or
            $null -ne $report.stop_reason -or
            $report.wall_time_policy.enabled -ne $false) {
            throw "STOP: $candidate report is NOT a verified full PASS. Next model NOT started."
        }
        Write-Host "PASS: $candidate (175341 TRAIN rows, watched). Next candidate may start."
    }
    Write-Host "P15: both remaining FULL runs reported PASS. Keep .joblib on laptop; submit JSON/CSV logs for independent review."
}
finally {
    Pop-Location
}
