### build machine tar
```bash
cd docker
docker build -t singtown-ai-machine .
docker create --name singtown-ai-machine singtown-ai-machine
docker export -o ../build/singtown-ai-machine.tar singtown-ai-machine
docker rm singtown-ai-machine
docker rmi singtown-ai-machine
```
output file: build/singtown-ai-machine.tar

### bulid launcher exe
```bash
uv run -m nuitka singtown-ai-launcher/launcher.py --output-dir=build --mode=standalone --enable-plugin=tk-inter --windows-console-mode=attach --windows-icon-from-ico="assets/fav.ico" --include-data-dir="assets=assets" --include-data-files="pyproject.toml=pyproject.toml"
```

output file: build/launcher.dist

### build installer exe
- download https://github.com/microsoft/WSL/releases, save to build/wsl.msi

```powershell
& 'c:\Program Files (x86)\Inno Setup 6\ISCC.exe' '.\windows\singtown-ai.iss' /dMyAppVersion=0.0.0
```

output file: bulid/singtown-ai-installer-v0.0.0.exe
