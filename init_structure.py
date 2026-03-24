import os

folders = [
    "app/ui",
    "src/connectors",
    "src/config",
    "src/domain",
    "src/services",
    "src/storage",
    "src/transform",
    "src/utils",
    "tests",
    "data/raw",
    "data/processed",
    "data/cache",
    "notebooks"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    # Crear .gitkeep para que Git rastree las carpetas aunque estén vacías
    with open(os.path.join(folder, ".gitkeep"), "w") as f:
        pass

print("✅ Estructura de carpetas creada exitosamente.")
