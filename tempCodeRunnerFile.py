def resizeEvent(self, event):
        super().resizeEvent(event)
        self._check_scroll_needed()