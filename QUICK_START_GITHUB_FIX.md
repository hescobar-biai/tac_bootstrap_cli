# ⚡ Quick Start - GitHub Fix

## Lo que se arregló
- ❌ PR no se creaba en `adw_sdlc_iso.py`
- ❌ Merge fallaba en `adw_sdlc_zte_iso.py` ("PR not found")

## ✅ Solución aplicada
1. **PR creation directo**: `gh pr create` en bash (no execute_template)
2. **PR validation**: Verifica PR existe antes de mergear
3. **State tracking**: Guarda PR URL para reutilizar

## 🚀 Usa los flujos normalmente

### Flujo 5 fases (sin auto-merge)
```bash
uv run adws/adw_sdlc_iso.py 123
```
→ ✅ Crea PR + completa plan, build, test, review, document

### Flujo 6 fases (con auto-merge a main)
```bash
uv run adws/adw_sdlc_zte_iso.py 123
```
→ ✅ Crea PR + merge automático a producción

## 📊 Resultados esperados
- ✅ PR aparece en GitHub (título: `[ADW] #123 - ...`)
- ✅ Comentarios en issue con actualizaciones
- ✅ Merge exitoso si todo pasó (ZTE flow)
- ✅ Errores claros si algo falla (con instrucciones)

## 📁 Archivos de referencia
- `FIX_GITHUB_ES.md` - Guía completa en español
- `GITHUB_FIX_SUMMARY.md` - Documentación técnica

## ⚙️ Detalles técnicos (si necesitas)
- `adws/adw_modules/git_ops.py`: Nueva función `create_pr_direct()`
- `adws/adw_ship_iso.py`: Nueva función `validate_pr_exists()`

---
**Estado**: ✅ Listo para usar | Commits: d6e6959, c88335e
