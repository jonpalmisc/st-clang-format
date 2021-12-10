import sublime
import sublime_plugin

import subprocess


class ClangFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit):
        command = ["clang-format", "-style", "LLVM", "-"]

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )

        buffer = self.view.substr(sublime.Region(0, self.view.size()))

        result, error = process.communicate(buffer.encode("utf-8"))
        if error:
            return

        self.view.replace(
            edit, sublime.Region(0, self.view.size()), result.decode("utf-8")
        )

        pass
