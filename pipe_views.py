import sublime


class PipeViews(object):
    dest_view_name = "Dest"

    def __init__(self):
        self.source_last_pos = 0
        self.is_running = False

        self.dest_view = None
        self.source_view_id = None

    def create_destination(self):
        dest_view = sublime.active_window().new_file()
        dest_view.set_name(self.dest_view_name)

        self.dest_view = dest_view

        self.on_view_created(dest_view)

        return dest_view

    def prepare_copy(self, source_view):
        """
        'Lock' the source view, and clear the destination view, if it exists.
        """
        self.source_view_id = source_view.id()
        self.source_last_pos = 0

        dest_view = self.dest_view
        if dest_view:
            edit = dest_view.begin_edit()
            region = sublime.Region(0, dest_view.size())
            dest_view.erase(edit, region)
            dest_view.end_edit(edit)
        else:
            # Creating the dest view breaks modify listening; do it outside of
            # the current call stack
            sublime.set_timeout(self.create_destination, 100)

    def pipe_text(self, view):
        """
        Incrementally update the destination view.
        """
        if self.is_running or view.id() != self.source_view_id:
            return

        self.is_running = True
        try:
            prev_source_last_pos = self.source_last_pos

            dest_view = self.dest_view
            # We're paranoid. Check dest view availability on every run, not just
            # on first run, in case the user closed it.
            if dest_view is None:
                dest_view = self.create_destination()

                # Copy text before readhead
                edit = dest_view.begin_edit()
                dest_view.insert(edit, 0, view.substr(sublime.Region(0, prev_source_last_pos)))
                dest_view.end_edit(edit)

            edit = dest_view.begin_edit()
            new_source_last_pos = view.size()
            region = sublime.Region(prev_source_last_pos, new_source_last_pos)
            dest_view.replace(edit, region, view.substr(region))
            dest_view.end_edit(edit)

            self.source_last_pos = new_source_last_pos
        finally:
            self.is_running = False

    def on_view_created(self, view):
        "Hook called when the destination view is created."
