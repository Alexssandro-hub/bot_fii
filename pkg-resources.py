import pkg_resources

# Carregar as bibliotecas do arquivo requirements.txt
with open("codebase/bot_fii/requirements.txt", "r") as file:
    required_packages = file.read().splitlines()

# Verificar se as bibliotecas estão instaladas
missing_packages = []
for package in required_packages:
    try:
        pkg_resources.require(package)
    except pkg_resources.DistributionNotFound:
        missing_packages.append(package)
    except pkg_resources.VersionConflict as e:
        print(f"Conflito de versão: {e}")

# Exibir pacotes ausentes
if missing_packages:
    print("Bibliotecas ausentes:")
    for pkg in missing_packages:
        print(f" - {pkg}")
else:
    print("Todas as bibliotecas estão instaladas!")
