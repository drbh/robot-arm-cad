# robot arm cad


<img width="1115" alt="robot-arm-cad-screen" src="https://github.com/user-attachments/assets/09727a89-fa91-4e87-a693-30d5b5091c90" />

Small scripts that generate CAD files for a simple robot arm.

```bash
uv run elbow-forearm.py
uv run upper-arm.py
uv run wrist-bracket.py
```

see the output files in `output`. 


```bash
.
├── README.md
├── elbow-forearm.py
├── output
│   ├── elbow-forearm.3mf
│   ├── upper-arm.3mf
│   └── wrist-backet.3mf
├── pyproject.toml
├── upper-arm.py
├── uv.lock
└── wrist-bracket.py
```

*NOTE when printing you'll need two copies of various parts (upper-arm, elbow-forarm) and some of the servo back peices. A more complete set of instructions will be added with a full part list (eventually) 
