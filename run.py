#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import create_app

if __name__ == '__main__':
    create_app().run(debug = True,threaded = True)
