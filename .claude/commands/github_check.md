# GitHub Check

Verificar conexión y configuración de GitHub para el proyecto.

## Instructions

Ejecutar verificaciones de GitHub en secuencia y reportar resultados.

### 1. Verificar GitHub CLI instalado
```bash
gh --version
```
- Si falla: Informar que `gh` CLI no está instalado
- Sugerir: `brew install gh` (macOS) o ver https://cli.github.com/

### 2. Verificar autenticación GitHub
```bash
gh auth status
```
- Debe mostrar cuenta autenticada
- Si falla: Sugerir `gh auth login`

### 3. Verificar Git remoto configurado
```bash
git remote -v
```
- Debe mostrar `origin` apuntando a GitHub
- Si no hay remote: Informar que no está configurado

### 4. Verificar acceso al repositorio
```bash
gh repo view --json name,owner,url
```
- Si funciona: Mostrar info del repo
- Si falla: Verificar permisos o que el repo exista

### 5. Verificar branch actual
```bash
git branch --show-current
```
- Mostrar branch actual

### 6. Verificar estado de sync con remote
```bash
git fetch origin --dry-run 2>&1
```
- Verificar que se puede conectar al remote

### 7. Verificar issues y PRs (opcional)
```bash
gh issue list --limit 5
gh pr list --limit 5
```
- Mostrar issues y PRs recientes si existen

## Report

Reportar resultados como JSON:

```json
{
  "status": "ready|warning|error",
  "checks": [
    {
      "name": "gh_cli_installed",
      "passed": boolean,
      "message": "string"
    },
    {
      "name": "gh_authenticated",
      "passed": boolean,
      "message": "string",
      "account": "string (if passed)"
    },
    {
      "name": "git_remote_configured",
      "passed": boolean,
      "message": "string",
      "remote_url": "string (if passed)"
    },
    {
      "name": "repo_access",
      "passed": boolean,
      "message": "string",
      "repo_name": "string (if passed)"
    },
    {
      "name": "remote_sync",
      "passed": boolean,
      "message": "string"
    }
  ],
  "summary": {
    "current_branch": "string",
    "open_issues": number,
    "open_prs": number
  },
  "next_steps": ["string"]
}
```

### Ejemplo de Output

```json
{
  "status": "ready",
  "checks": [
    {"name": "gh_cli_installed", "passed": true, "message": "gh version 2.40.0"},
    {"name": "gh_authenticated", "passed": true, "message": "Logged in", "account": "usuario"},
    {"name": "git_remote_configured", "passed": true, "message": "Remote configurado", "remote_url": "git@github.com:org/repo.git"},
    {"name": "repo_access", "passed": true, "message": "Acceso verificado", "repo_name": "tac-bootstrap"},
    {"name": "remote_sync", "passed": true, "message": "Conexión exitosa"}
  ],
  "summary": {
    "current_branch": "main",
    "open_issues": 3,
    "open_prs": 1
  },
  "next_steps": []
}
```
