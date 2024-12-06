from loguru import logger
from mpd_inspector.parser.mpd_tags import MPD

from media_muncher.codecstrings import CodecStringParser
from media_muncher.handlers.dash import DASHHandler


class DashAnalyser:
    def __init__(self, handler: DASHHandler) -> None:
        self.handler = handler
        self.messages = []

    def extract_renditions(self):
        dash_obj: MPD = self.handler.document

        if len(dash_obj.periods) > 1:
            logger.warning(
                "More than 1 period found. Only the first period will be taken into account"
            )

        period = dash_obj.periods[0]

        audio_renditions = {}
        video_renditions = {}

        for adaptation_set in period.adaptation_sets:
            # Audio
            if (
                adaptation_set.content_type == "audio"
                or adaptation_set.mime_type.startswith("audio")
            ):
                for representation in adaptation_set.representations:
                    codec = CodecStringParser.parse_codec_string(
                        representation.codecs or adaptation_set.codecs
                    )

                    codec["bitrate"] = representation.bandwidth
                    codec['language'] = adaptation_set.lang
                    audio_renditions[representation.id] = codec

            # Video
            if (
                adaptation_set.content_type == "video"
                or adaptation_set.mime_type.startswith("video")
            ):
                for representation in adaptation_set.representations:
                    codec = CodecStringParser.parse_codec_string(
                        representation.codecs or adaptation_set.codecs
                    )
                    codec["resolution"] = (representation.width, representation.height)
                    codec["bitrate"] = representation.bandwidth
                    codec["framerate"] = representation.frame_rate
                    video_renditions[representation.id] = codec

        return [*video_renditions.values(), *audio_renditions.values()]

    def extract_packaging_info(self):
        return {"container": "ISOBMFF"}
