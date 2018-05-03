# -*- coding: utf-8 -*-
from . import BaseZolSpider


class ScreenSpider(BaseZolSpider):
    name = 'screen'
    start_urls = ['http://detail.zol.com.cn/lcd/']


class MouseSpider(BaseZolSpider):
    name = 'mouse'
    start_urls = ['http://detail.zol.com.cn/mice/']


class HeadsetSpider(BaseZolSpider):
    name = 'headset'
    start_urls = ['http://detail.zol.com.cn/microphone/shanghai/']


class KeyboardSpider(BaseZolSpider):
    name = 'keyboard'
    start_urls = ['http://detail.zol.com.cn/keyboard/shanghai/']
