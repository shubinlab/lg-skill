param(
  [ValidateSet('project', 'user')]
  [string]$Scope = 'user',
  [ValidateSet('agents', 'claude', 'cursor', 'gemini', 'copilot', 'opencode', 'roo', 'cline', 'windsurf')]
  [string]$Agent = 'agents'
)

$homeRoot = $HOME
$roots = @{
  agents = @{ user = "$homeRoot\.agents\skills"; project = ".agents\skills" }
  claude = @{ user = "$homeRoot\.claude\skills"; project = ".claude\skills" }
  cursor = @{ user = "$homeRoot\.cursor\skills"; project = ".cursor\skills" }
  gemini = @{ user = "$homeRoot\.gemini\skills"; project = ".gemini\skills" }
  copilot = @{ user = "$homeRoot\.copilot\skills"; project = ".github\skills" }
  opencode = @{ user = "$homeRoot\.config\opencode\skills"; project = ".opencode\skills" }
  roo = @{ user = "$homeRoot\.roo\skills"; project = ".roo\skills" }
  cline = @{ user = "$homeRoot\.cline\skills"; project = ".cline\skills" }
  windsurf = @{ user = "$homeRoot\.codeium\windsurf\skills"; project = ".devin\skills" }
}

$destination = Join-Path $roots[$Agent][$Scope] 'lg-monitor-control'
New-Item -ItemType Directory -Force -Path $destination | Out-Null
Copy-Item -Force .\SKILL.md (Join-Path $destination 'SKILL.md')
Write-Output "installed lg-monitor-control -> $destination"
