param(
  [string]$Version = "0.1.6",
    [switch]$OneFile
)

$ErrorActionPreference = 'Stop'
$Root = Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $Root

python -m pip install -r requirements.txt

$pyArgs = @(
    '-m', 'PyInstaller',
    '--noconsole',
    '--name', 'NTERayTracingPanel',
    '--add-data', 'web;web',
    'app.py'
)

if ($OneFile) {
    $pyArgs = @('-m', 'PyInstaller', '--noconsole', '--onefile', '--name', 'NTERayTracingPanel', '--add-data', 'web;web', 'app.py')
}

python @pyArgs

$ReleaseRoot = Join-Path $Root "release"
$PackageDir = Join-Path $ReleaseRoot "NTERayTracingPanel-v$Version"
if (Test-Path $PackageDir) {
    Remove-Item -LiteralPath $PackageDir -Recurse -Force
}
New-Item -ItemType Directory -Path $PackageDir -Force | Out-Null

if ($OneFile) {
    Copy-Item -LiteralPath (Join-Path $Root 'dist\NTERayTracingPanel.exe') -Destination $PackageDir -Force
} else {
    Copy-Item -LiteralPath (Join-Path $Root 'dist\NTERayTracingPanel') -Destination $PackageDir -Recurse -Force
}

Copy-Item README.md,README.en.md,CHANGELOG.md,NOTICE.md,LICENSE,run_exe_as_admin.bat -Destination $PackageDir -Force
Copy-Item docs -Destination $PackageDir -Recurse -Force

Compress-Archive -Path (Join-Path $PackageDir '*') -DestinationPath (Join-Path $ReleaseRoot "NTERayTracingPanel-v$Version.zip") -Force
Write-Output "Release package: $PackageDir"
