# Reglas del proyecto
- Python 3.11+, solo biblioteca estándar (+ pytest para tests).
- Capas (cada una depende solo de la inferior): domain -> repository -> service.
- Dinero siempre en centavos (int). Nunca float.
- Comando de tests: `PYTHONPATH=src pytest -q`
- No cambies los contratos (docs/spec.md, Protocol en repository.py) sin proponerlo y detenerte.
- Un cambio = una capa. Cada tarea termina con los tests en verde.
