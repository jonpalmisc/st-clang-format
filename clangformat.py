import sublime
import sublime_plugin

import subprocess


class ClangFormatCommand(sublime_plugin.TextCommand):
    """Format the current buffer."""

    def run(self, edit: sublime.Edit, style: str):
        command = ["clang-format", "-style", style, "-"]

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )

        global_region = sublime.Region(0, self.view.size())
        buffer = self.view.substr(global_region)

        result, error = process.communicate(buffer.encode("utf-8"))
        if error:
            sublime.error_message("Failed to format buffer.")
            return

        self.view.replace(edit, global_region, result.decode("utf-8"))

    def input(self, args):
        return StyleInputHandler()


class StyleInputHandler(sublime_plugin.ListInputHandler):
    """Input handler to choose format presets."""

    def list_items(self):
        return ["Local", "LLVM", "WebKit"]
