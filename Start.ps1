param([int]$Port=8501)
$ErrorActionPreference="Stop"
Set-Location $PSScriptRoot
if (!(Test-Path ".venv\Scripts\python.exe")) {
 if (Get-Command py -ErrorAction SilentlyContinue) { & py -3 -m venv .venv }
 else { & python -m venv .venv }
 if ($LASTEXITCODE -ne 0) { throw "Install Python 3.11 or newer first." }
}
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Installation failed. Check your internet connection." }
& .\.venv\Scripts\python.exe site_content.py
if ($LASTEXITCODE -ne 0) { throw "Please fix content.json before starting." }
& .\.venv\Scripts\python.exe -m streamlit run streamlit_app.py --server.port $Port
