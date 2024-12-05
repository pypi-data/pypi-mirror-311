"""
scenario (1):
    ╭─ computer A ─────────────╮
    │  ╭─ python program ────╮ │
    │  │  server_runtime     │ │
    │  │        ││           │ │
    │  │  server_connector ○─┼─┼─╮
    │  ╰─────────────────────╯ │ │
    ╰──────────────────────────╯ │
    ╭─ computer B ─────────────╮ │
    │  ╭─ python program ────╮ │ │
    │  │  client_runtime     │ │ │
    │  │        ││           │ │ │
    │  │  client_connector ●─┼─┼─╯
    │  ╰─────────────────────╯ │
    ╰──────────────────────────╯
        server_connector: http://<server_ip>:2140
        client_connector: http://localhost:2142
        
scenario (2):
    ╭─ computer A ──────────────╮
    │  ╭─ python program ─────╮ │
    │  │  webapp_backend      │ │
    │  │        ││            │ │
    │  │  webapp_connector ○──┼─┼────────────╮
    │  ╰──────────────────────╯ │            │
    ╰───────────────────────────╯            │
    ╭─ computer B ───────────────────────────┼──────╮
    │  ╭─ python program ────╮ ╭─ browser ───┼────╮ │
    │  │  client_runtime     │ │             │    │ │
    │  │        ││           │ │             │    │ │
    │  │  client_connector ●─┼─┼─ webapp_frontend │ │
    │  ╰─────────────────────╯ ╰──────────────────╯ │
    ╰───────────────────────────────────────────────╯
        webapp_connector: http://example.com:2141
        webapp_frontend : https://example.com/some/path
        client_connector: http://localhost:2142
"""

import os

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 2014

# DELETE BELOW
SERVER_DEFAULT_PORT = int(os.getenv('AIRCONTROL_SERVER_PORT', '2140'))
WEBAPP_DEFAULT_PORT = int(os.getenv('AIRCONTROL_WEBAPP_PORT', '2141'))
CLIENT_DEFAULT_PORT = int(os.getenv('AIRCONTROL_CLIENT_PORT', '2142'))
