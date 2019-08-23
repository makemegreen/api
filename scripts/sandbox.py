from flask import current_app as app

from sandbox_helpers.create_sandbox import run_sandbox


@app.manager.command
def sandbox():
    run_sandbox()
