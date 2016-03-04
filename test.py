###
# coding: utf-8
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
###

from supybot.test import *


class XKCDTestCase(ChannelPluginTestCase):
    plugins = ('xkcd',)

    sampleComicIndex = 40
    sampleComicTitle = 'Light'
    sampleComicDate = '2006-01-01'
    sampleComicAlt = 'Like a beacon'

    expectedResponse = 'xkcd: »{}« posted on {} ({})'.format(
        sampleComicTitle, sampleComicDate, sampleComicAlt)
    expectedResponseWithURL = '{} http://xkcd.com/{}/'.format(
        expectedResponse, sampleComicIndex)

    if network:
        def testFullURL(self):
            self.assertSnarfResponse(
                'bla https://xkcd.com/{} bla'.format(self.sampleComicIndex),
                self.expectedResponse)

        def testShort(self):
            self.assertSnarfResponse(
                'bla bla xkcd#{} bla bla'.format(
                    self.sampleComicIndex), self.expectedResponseWithURL)

        def testCommand(self):
            self.assertResponse('xkcd {}'.format(self.sampleComicIndex,),
                                self.expectedResponseWithURL)
            # cannot possibly know the response for current one…
            self.assertNotError('xkcd')

    def testInvalidCommands(self):
        self.assertSnarfNoResponse('bla on xkcd xkcd#')
        self.assertSnarfNoResponse('bla on xkcd 123a something')
        self.assertHelp('xkcd 1 1')
        self.assertError('xkcd bla')
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
