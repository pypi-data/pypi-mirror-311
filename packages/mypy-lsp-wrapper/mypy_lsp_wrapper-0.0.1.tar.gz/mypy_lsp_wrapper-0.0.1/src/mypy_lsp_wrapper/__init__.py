import os
import json
import logging
from mypy import api

from lsprotocol import types

from pygls.cli import start_server
from pygls.lsp.server import LanguageServer
from pygls.workspace import TextDocument


class PublishDiagnosticServer(LanguageServer):
    """Language server demonstrating "push-model" diagnostics."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.diagnostics = {}

    def parse(self, document: TextDocument):
        diagnostics = []

        relpath = os.path.relpath(document.path)
        errors, _, exit_code = api.run([relpath, "-O", "json"])

        if exit_code == 0:
            self.diagnostics[document.uri] = (document.version, [])
            return

        for line in errors.strip().splitlines():
            error = json.loads(line)
            if error["file"] != relpath:
                continue

            if error["severity"] == "error":
                severity = types.DiagnosticSeverity.Error
            else:
                severity = types.DiagnosticSeverity.Warning

            logging.info(f"{error}")

            diagnostics.append(
                types.Diagnostic(
                    message=f"[{error['code']}] {error["message"]}",
                    severity=severity,
                    range=types.Range(
                        start=types.Position(
                            line=error["line"] - 1, character=error["column"] - 1
                        ),
                        end=types.Position(
                            line=error["line"] - 1, character=error["column"] - 1
                        ),
                    ),
                )
            )

        self.diagnostics[document.uri] = (document.version, diagnostics)


server = PublishDiagnosticServer("diagnostic-server", "v1")


@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
@server.feature(types.TEXT_DOCUMENT_DID_SAVE)
def did_open(ls: PublishDiagnosticServer, params: types.DidOpenTextDocumentParams):
    """Parse each document when it is opened"""
    doc = ls.workspace.get_text_document(params.text_document.uri)
    ls.parse(doc)

    for uri, (version, diagnostics) in ls.diagnostics.items():
        ls.text_document_publish_diagnostics(
            types.PublishDiagnosticsParams(
                uri=uri,
                version=version,
                diagnostics=diagnostics,
            )
        )


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    start_server(server)
