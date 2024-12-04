"""Module for all CurrentTrackFeatures

Classes:
"""

from logging import getLogger
from typing import Any

from homeassistant.const import STATE_UNKNOWN

from custom_components.spotcast.sensor.abstract_sensor import (
    SpotcastSensor,
    SensorStateClass,
    SensorDeviceClass,
)

LOGGER = getLogger(__name__)


class AbstractAudioFeatureSensor(SpotcastSensor):
    """A Home Assistant sensor reporting information about the profile
    of a Spotify Account

    Methods:
        - async_update
    """

    STATE_CLASS: str = SensorStateClass.MEASUREMENT
    FEATURE_NAME = "abstract"

    @property
    def _generic_id(self) -> str:
        return f"current_track_{self.FEATURE_NAME}"

    @property
    def name(self) -> str:
        feature = self.FEATURE_NAME.replace("_", " ")
        feature = [x.capitalize() for x in feature.split(" ")]
        feature = " ".join(feature)
        return f"Spotcast - {self.account.name} Current Track {feature}"

    def _cleanup(self, feature: Any) -> Any:
        return feature

    async def async_update(self):
        audio_features = self.account.current_item["audio_features"]
        audio_feature = audio_features.get(self.FEATURE_NAME)

        if audio_feature is None:
            self._attr_state = STATE_UNKNOWN
        else:
            self._attr_state = self._cleanup(audio_feature)


class AbstractPercentSensor(AbstractAudioFeatureSensor):
    UNITS_OF_MEASURE = "%"
    _attr_suggested_display_precision = 1

    def _cleanup(self, feature: float) -> float:
        return feature * 100


class CurrentTrackDanceabilitySensor(AbstractPercentSensor):
    FEATURE_NAME = "danceability"
    ICON = "mdi:dance-ballroom"


class CurrentTrackEnergySensor(AbstractPercentSensor):
    FEATURE_NAME = "energy"
    ICON = "mdi:lightning-bolt"


class CurrentTrackKeySensor(AbstractAudioFeatureSensor):

    FEATURE_NAME = "key"
    STATE_CLASS = None
    ICON = "mdi:language-csharp"
    KEYS = (
        "C",
        "C#/D♭",
        "D",
        "D#/E♭",
        "E",
        "F",
        "F#/G♭",
        "G",
        "G#/A♭",
        "A",
        "A#/B♭",
        "B",
    )

    def _cleanup(self, feature: int) -> str:

        if feature >= 0 and feature < len(self.KEYS):
            return self.KEYS[feature]

        return "-"


class CurrentTrackLoudnessSensor(AbstractAudioFeatureSensor):
    FEATURE_NAME = "loudness"
    UNITS_OF_MEASURE = "dB"
    ICON = "mdi:bullhorn"
    _attr_suggested_display_precision = 1

    @property
    def device_class(self) -> SensorDeviceClass:
        return SensorDeviceClass.SOUND_PRESSURE

    @property
    def icon(self) -> str:
        if not isinstance(self._attr_state, (float, int)):
            return "mdi:volume-off"

        if self._attr_state < -40:
            return "mdi:volume-low"

        if self._attr_state < -20:
            return "mdi:volume-medium"

        return "mdi:volume-high"


class CurrentTrackModeSensor(AbstractAudioFeatureSensor):
    FEATURE_NAME = "mode"
    STATE_CLASS = None
    ICON = "mdi:music"

    def _cleanup(self, feature: int) -> str:
        return "major" if feature == 1 else "minor"


class CurrentTrackSpeechinessSensor(AbstractPercentSensor):
    FEATURE_NAME = "speechiness"
    ICON = "mdi:speaker-message"


class CurrentTrackAcousticnessSensor(AbstractPercentSensor):
    FEATURE_NAME = "acousticness"
    ICON = "mdi:guitar-acoustic"

    @property
    def icon(self) -> str:
        if not isinstance(self._attr_state, float) or self._attr_state > 50:
            return "mdi:guitar-acoustic"

        return "mdi:guitar-electric"


class CurrentTrackInstrumentalnessSensor(AbstractPercentSensor):
    FEATURE_NAME = "instrumentalness"
    ICON = "mdi:piano"


class CurrentTrackLivenessSensor(AbstractPercentSensor):
    FEATURE_NAME = "liveness"
    ICON = "mdi:account-group"


class CurrentTrackValenceSensor(AbstractPercentSensor):
    FEATURE_NAME = "valence"
    ICON = "mdi:emoticon"

    @property
    def icon(self) -> str:
        if not isinstance(self._attr_state, float):
            return "mdi:emoticon-outline"

        if self._attr_state < 20:
            return "mdi:emoticon-cry"
        if self._attr_state < 40:
            return "mdi:emoticon-sad"
        if self._attr_state < 60:
            return "mdi:emoticon-neutral"
        if self._attr_state < 80:
            return "mdi:emoticon-happy"

        return "mdi:emoticon-excited"


class CurrentTrackTempoSensor(AbstractAudioFeatureSensor):
    FEATURE_NAME = "tempo"
    UNITS_OF_MEASURE = "bpm"
    ICON = "mdi:metronome"
    _attr_suggested_display_precision = 0


class CurrentTrackTimeSignatureSensor(AbstractAudioFeatureSensor):
    FEATURE_NAME = "time_signature"
    STATE_CLASS = None
    ICON = "mdi:music-clef-treble"

    def _cleanup(self, feature: int) -> str:
        return f"{feature}/4"


SENSORS = (
    CurrentTrackDanceabilitySensor,
    CurrentTrackEnergySensor,
    CurrentTrackKeySensor,
    CurrentTrackLoudnessSensor,
    CurrentTrackModeSensor,
    CurrentTrackSpeechinessSensor,
    CurrentTrackAcousticnessSensor,
    CurrentTrackInstrumentalnessSensor,
    CurrentTrackLivenessSensor,
    CurrentTrackValenceSensor,
    CurrentTrackTempoSensor,
    CurrentTrackTimeSignatureSensor
)
