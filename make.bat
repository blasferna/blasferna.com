@echo off
SETLOCAL

:: Call the correct command block
GOTO :%1

:run
    echo Running...
    python src/generator.py serve
    goto :EOF

:build
    echo Running...
    python src/generator.py build
    goto :EOF

:end
