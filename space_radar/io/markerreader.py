from space_radar.logutils import LogMixin


class MarkerTextReader(LogMixin):
    """"
    Iterate over text between two markers
    Markes can be the same
    If not specified, it uses ~~~~ as marker
    """

    def __init__(self, filename: str, begin_marker="~~~~", end_marker="~~~~"):
        self._begin_marker = begin_marker
        self._end_marker = end_marker
        self._filename = filename

    def iter(self):
        text_list = []
        self.logger.info("Loading file %s", self._filename)
        with open(self._filename) as f:
            between_markers = False
            for line in f:
                if not between_markers and line.startswith(self._begin_marker):
                    between_markers = True
                elif line.startswith(self._end_marker):
                    between_markers = False
                    yield "".join(text_list)
                    text_list = []
                elif between_markers:
                    text_list.append(line)
