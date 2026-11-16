$ErrorActionPreference = 'Stop'
$project = $PSScriptRoot
$backend = $null
$base = 'http://127.0.0.1:8001'
try {
    try { $null = Invoke-RestMethod "$base/health" -TimeoutSec 2 }
    catch {
        $backend = Start-Process -FilePath (Join-Path $project '.venv\Scripts\python.exe') `
            -ArgumentList '-m','uvicorn','backend.main:app','--host','127.0.0.1','--port','8001' `
            -WorkingDirectory $project -WindowStyle Hidden -PassThru `
            -RedirectStandardError (Join-Path $project 'backend-stderr.log') `
            -RedirectStandardOutput (Join-Path $project 'backend-stdout.log')
        $ready = $false
        for ($i = 0; $i -lt 20; $i++) {
            Start-Sleep -Milliseconds 300
            try { $null = Invoke-RestMethod "$base/health" -TimeoutSec 1; $ready = $true; break } catch {}
        }
        if (-not $ready) { throw 'Backend did not start. Check backend-stderr.log.' }
    }
    $choices = Invoke-RestMethod "$base/curriculums" -TimeoutSec 5
    Write-Host "Backend ready; $(@($choices).Count) active curriculums."
    Push-Location (Join-Path $project 'frontend')
    try { & 'C:\Program Files\nodejs\npm.cmd' run dev }
    finally { Pop-Location }
}
finally { if ($backend -and -not $backend.HasExited) { Stop-Process -Id $backend.Id -Force } }
