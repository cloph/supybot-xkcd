###
# coding: utf-8
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
###
from datetime import date
from supybot.commands import *
import supybot.callbacks as callbacks
import supybot.utils as utils
import simplejson as json


def GetXkcdInfo(index, printurl=0):
    try:
        text = utils.web.getUrl('http://xkcd.com/{}/info.0.json'.format(index))
        xkcdInfo = json.loads(text)
        # assemble the response string
        response = u'xkcd: »{}« posted on {} ({})'.format(
            xkcdInfo['title'],
            date(int(xkcdInfo['year']),
                 int(xkcdInfo['month']),
                 int(xkcdInfo['day'])).isoformat(),
            xkcdInfo['alt'])

        if printurl == 1:
            response = u'{} http://xkcd.com/{}/'.format(
                response, xkcdInfo['num'])

        return response.encode('utf-8')
    except utils.web.Error, e:
        if printurl == 1:
            e = '{} - please visit the URL yourself: ' \
                'http://xkcd.com/{}/'.format(str(e), index)
        return e
    except Exception, e:
        print 'unknown error {}'.format(str(e))
        return 'unknown error - please visit the URL yourself: ' \
               'http://xkcd.com/{}/'.format(index)


class XKCD(callbacks.PluginRegexp):
    """the xkcd plugin snarfs the messages for either an URL to a xkcd comic
    or for special short form like e.g. xkcd#1234"""
    # what subs implement a snarfer
    regexps = ['parseURL', 'parseID']

    # noinspection PyIncorrectDocstring,PyUnusedLocal
    @urlSnarfer
    def parseID(self, irc, msg, match):
        r"""(?:^|\s)xkcd(?: |#|:)(\d+)(:?\s|$)"""
        index = match.group(1)
        xkcdInfo = GetXkcdInfo(index, printurl=1)
        irc.reply('{}'.format(xkcdInfo))

    # noinspection PyIncorrectDocstring,PyUnusedLocal
    @urlSnarfer
    def parseURL(self, irc, msg, match):
        r"""(?:https?://)?xkcd.com/(\d+)/?"""
        index = match.group(1)
        xkcdInfo = GetXkcdInfo(index, printurl=0)
        irc.reply('{}'.format(xkcdInfo))

    # noinspection PyIncorrectDocstring,PyUnusedLocal,PyMethodMayBeStatic
    def xkcd(self, irc, msg, args, index):
        """<index>
        
        Ask the bot to get xkcd info based on the comic index
        If no index is given, return info on the current comic"""
        xkcdInfo = GetXkcdInfo(index, printurl=1)
        irc.reply('{}'.format(xkcdInfo))
    xkcd = wrap(xkcd, [additional('positiveInt')])

Class = XKCD
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
