# -*- coding: utf-8 -*-
# pylint: disable=invalid-name, too-many-instance-attributes

"""This module contains a class representing the capabilities of
music services"""

from __future__ import (
    absolute_import, unicode_literals
)


class Capabilities(object):
    """A class representing the capabilities of a music service.

    Each music service indicates to the controller that it can handle,
    or requires, certain functionality by setting a bit in the binary
    representation of an integer known as "Capabilities".  It is available
    in the music services data returned by
    `MusicService.get_data_for_name()`.
    A full description of the purpose of each of these flags is
    at http://musicpartners.sonos.com/docs?q=node/134. SoCo ignores most (
    but not all) of them. An instance of this class converts the integer
    representation of Capabilities into a number of boolean properties on
    the instance, and can provide a set of strings indicating the flags
    which are set.

    Examples:

        >>> from soco.music_services import MusicService, Capabilities
        >>> ms= MusicService.get_data_for_name('Spotify')
        >>> print (ms['Capabilities'])
        68115
        >>> cap = Capabilities(68115)
        >>> cap.favoritesalbums
        True
        >>> cap.usercontentplaylists
        True
        >>> cap.supportactions
        False
        >>> print(cap.as_set())
        {'extendedmetadata',
         'favoritesalbums',
         'favoritestracks',
         'includeSMAPIcontext',
         'search',
         'usercontentplaylists'}
     """

    def __init__(self, capability_number):
        """
        Args:
            capability_number (int): The integer representation of the
                capability flags
        """

        self.capability_number = capability_number

        # The names of some of these properties are a little awkward but are
        # those used by Sonos in its python SMAPI self-test module available at
        # musicpartners.sonos.com.
        # The value of each flag has been obtained by creating a dummy service
        # at [yoursonosip]:1400/customsd.htm, setting and clearing the options
        # available, and seeing what effect that has on the capability number

        #
        #  In the Sonos SMAPI self-test
        #

        #: bool:The service can be searched
        self.search = (capability_number & 1) > 0

        #: bool: The user can favorite tracks from this service
        self.favoritestracks = (capability_number & 2) > 0

        #: bool: The user can favorite albums from this service
        self.favoritesalbums = (capability_number & 16) > 0

        # In the self-test module, but not referred to at
        # http://musicpartners.sonos.com/?q=node/134 or on the customsd page
        # self.favoritesartists = False

        #: bool: The user can edit playlists
        self.usercontentplaylists = (capability_number & 2048) > 0

        #: bool: The controller should report when the track has finished
        #:  playing
        self.playbacklogging = (capability_number & 64) > 0

        #: bool: The controller should report number of seconds played, during
        #: playback
        self.eventanddurationloggingduringplayback = (
            capability_number & 4096) > 0

        #: bool: The controller should report the addition of an account for
        #: this service
        self.accountlogging = (capability_number & 8192) > 0

        #: bool: The controller may make calls for extended metadata. All
        #: services should support this
        self.extendedmetadata = (capability_number & 512) > 0

        #
        # Not in the Sonos SMAPI self-test
        #

        #: bool: Content should not be used for alarms (eg transient streams,
        #: live events etc)
        self.disablealarmsupport = (capability_number & 1024) > 0

        #: bool: No more than one account may be associated with this service.
        # According to the Sonos docs, this flag should not be set for a
        # service in production (but sometimes it does seem to be)
        self.disablemultipleaccountsupport = (capability_number & 16384) > 0

        #: bool:  Receive implicit or explicit actions for getMediaUri requests
        self.supportactions = (capability_number & 32768) > 0

        #: bool: Include SMAPI context headers with all requests
        self.includeSMAPIcontext = (capability_number & 65536) > 0

        #: bool: Include a <deviceCert> sub-element of the <credentials>
        #: element in the SOAP header.
        self.requiresdevicecertificate = (capability_number & 131072) > 0

        #: bool: Include the Sonos player ID for the player sending the
        #: request in  a <zonePlayerId> sub-element of the <credentials>
        #: element in the SOAP header.
        self.includezoneplayerIDs = (capability_number & 262144) > 0

        #: bool: Include a <contextId> element with every setPlayedSeconds,
        #: reportPlayStatus, and reportPlaySeconds request
        self.addplaycontexttoreporting = (capability_number & 524288) > 0

    def as_set(self):
        """

        Returns:
            set: A set of strings, representing the capabilities of the
            relevant service

        """
        return (set([key for (key, value) in self.__dict__.items() if value
                     is True]))

    def __str__(self):
        return self.as_set().__str__()

    def __repr__(self):
        return "<{0}({1}): {2} at {3}>".format(
            self.__class__.__name__,
            self.capability_number, self.as_set(), hex(id(self)))
