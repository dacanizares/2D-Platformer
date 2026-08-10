[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$gcc = "C:\msys64\ucrt64\bin\gcc.exe"
$pkgConfig = "C:\msys64\ucrt64\bin\pkg-config.exe"
$outputDirectory = Join-Path $projectRoot "bin\rel-windows"
$output = Join-Path $outputDirectory "platformer.exe"

if (-not (Test-Path -LiteralPath $gcc)) {
    throw "MSYS2 UCRT64 GCC was not found at $gcc."
}
if (-not (Test-Path -LiteralPath $pkgConfig)) {
    throw "MSYS2 UCRT64 pkg-config was not found at $pkgConfig."
}
& $pkgConfig --exists raylib
if ($LASTEXITCODE -ne 0) {
    throw "Raylib for MSYS2 UCRT64 is missing. Install mingw-w64-ucrt-x86_64-raylib."
}

New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
$sources = Get-ChildItem (Join-Path $projectRoot "src") -Filter *.c | Sort-Object Name | ForEach-Object FullName
$raylibFlags = @(& $pkgConfig --cflags --libs raylib) -split "\s+" | Where-Object { $_ }

& $gcc -std=c17 -pedantic -Wall -Wextra -Wshadow -Wconversion -O2 -DNDEBUG "-I$(Join-Path $projectRoot 'src')" @sources -o $output @raylibFlags
if ($LASTEXITCODE -ne 0) { throw "The build failed ($LASTEXITCODE)." }

Write-Host "Built $output"
