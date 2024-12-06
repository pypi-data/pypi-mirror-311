# Build Instructions

Configure the environment

```bash
conda create -n et-engine-docs-cli python=3.11.9
conda activate et-engine-docs-cli
pip install -r requirements.txt
```

# Build

```bash
make clean
make html
```
