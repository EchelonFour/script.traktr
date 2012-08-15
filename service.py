# -*- coding: utf-8 -*-
#

import xbmc
import xbmcaddon

from utilities import Debug
import utilities
import notification_service as ns
import sync_update as su

__author__ = "Ralph-Gordon Paul, Adrian Cowan"
__credits__ = ["Ralph-Gordon Paul", "Adrian Cowan", "Justin Nemeth",  "Sean Rudford"]
__license__ = "GPL"
__maintainer__ = "Ralph-Gordon Paul"
__email__ = "ralph-gordon.paul@uni-duesseldorf.de"
__status__ = "Production"

__settings__ = xbmcaddon.Addon( "script.traktutilities" )
__language__ = __settings__.getLocalizedString

Debug("service: " + __settings__.getAddonInfo("id") + " - version: " + __settings__.getAddonInfo("version"))

# starts update/sync
def autostart():
    if utilities.checkSettings(True):
        notificationThread = ns.NotificationService()
        notificationThread.start()

        autosync_moviecollection = __settings__.getSetting("autosync_moviecollection")
        autosync_tvshowcollection = __settings__.getSetting("autosync_tvshowcollection")
        autosync_cleanmoviecollection = __settings__.getSetting("autosync_cleanmoviecollection")
        autosync_cleantvshowcollection = __settings__.getSetting("autosync_cleantvshowcollection")
        autosync_seenmovies = __settings__.getSetting("autosync_seenmovies")
        autosync_seentvshows = __settings__.getSetting("autosync_seentvshows")
        try:
            if autosync_moviecollection == "true":
                utilities.notification("Trakt Utilities", __language__(1180).encode( "utf-8", "ignore" )) # start movie collection update
                su.updateMovieCollection(True)
                if autosync_cleanmoviecollection:
                    su.cleanMovieCollection(True)
            if xbmc.abortRequested:
                raise SystemExit()

            if autosync_tvshowcollection == "true":
                su.notification("Trakt Utilities", __language__(1181).encode( "utf-8", "ignore" )) # start tvshow collection update
                su.updateTVShowCollection(True)
                if autosync_cleantvshowcollection:
                    su.cleanTVShowCollection(True)
            if xbmc.abortRequested:
                raise SystemExit()

            if autosync_seenmovies == "true":
                Debug("autostart sync seen movies")
                su.notification("Trakt Utilities", __language__(1182).encode( "utf-8", "ignore" )) # start sync seen movies
                su.syncSeenMovies(True)
            if xbmc.abortRequested:
                raise SystemExit()

            if autosync_seentvshows == "true":
                Debug("autostart sync seen tvshows")
                su.notification("Trakt Utilities", __language__(1183).encode( "utf-8", "ignore" )) # start sync seen tv shows
                su.syncSeenTVShows(True)
            if xbmc.abortRequested:
                raise SystemExit()

            if autosync_moviecollection == "true" or autosync_tvshowcollection == "true" or autosync_seenmovies == "true" or autosync_seentvshows == "true":
                su.notification("Trakt Utilities", __language__(1184).encode( "utf-8", "ignore" )) # update / sync done
        except SystemExit:
            notificationThread.abortRequested = True
            Debug("[Service] Auto sync processes aborted due to shutdown request")

        notificationThread.join()

autostart()
