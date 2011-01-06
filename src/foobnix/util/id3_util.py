#-*- coding: utf-8 -*-
'''
Created on 24 нояб. 2010

@author: ivan
'''
from foobnix.cue.cue_reader import update_id3_for_cue
from foobnix.util.image_util import get_image_by_path
from foobnix.util.time_utils import normalize_time
from foobnix.util.bean_utils import update_bean_from_normalized_text
from foobnix.util.file_utils import file_extension
from foobnix.util.fc import FC
from foobnix.util import LOG
from foobnix.util.audio import get_mutagen_audio
import os
def decode_cp866(text):
    try:
        decode_text = text.decode("cp866")
        if decode_text.find(u"├") >= 0 :
            #LOG.warn("File tags encoding is very old cp866")
            text = decode_text.replace(
                u"\u252c", u'ё').replace(
                u"├", "").replace(
                u"░", u"р").replace(
                u"▒", u"с").replace(
                u"▓", u"т").replace(
                u"│", u"у").replace(
                u"┤", u"ф").replace(
                u"╡", u"х").replace(
                u"╢", u"ц").replace(
                u"╖", u"ч").replace(
                u"╕", u"ш").replace(
                u"╣", u"щ").replace(
                u"║", u"ъ").replace(
                u"╗", u"ы").replace(
                u"╝", u"ь").replace(
                u"╜", u"э").replace(
                u"╛", u"ю").replace(
                u"┐", u"я")
            #fix ёш to ё
            text = text.replace(u'\u0451\u0448', u'\u0451')
    except:
        pass
    return text

def update_id3_for_beans(beans):
    try:
        map(update_id3, beans)
    except Exception, e:
        LOG.error("update id3 error", e)
    return beans


def update_id3(bean):
    if bean and bean.path and os.path.isfile(bean.path):
        try:
            audio = get_mutagen_audio(bean.path)            
        except Exception, e:
            LOG.warn("ID3 NOT MP3", e, bean.path)
            return bean

        if audio and audio.has_key('artist'): bean.artist = decode_cp866(audio["artist"][0])
        if audio and audio.has_key('title'): bean.title = decode_cp866(audio["title"][0])
        #if audio and audio.has_key('tracknumber'): bean.tracknumber = audio["tracknumber"][0]
        #else: 
            #if audio and not audio.has_key('tracknumber'): 
        duration_sec = bean.duration_sec
        if not bean.duration_sec:
            if audio and audio.info and audio.info.length: duration_sec = int(audio.info.length)

        if audio and audio.info:
            bean.info = audio.info.pprint()

        if bean.artist and bean.title:
            bean.text = bean.artist + " - " + bean.title

        if bean.tracknumber:
            try:
                bean.tracknumber = int(bean.tracknumber)
            except:
                bean.tracknumber = ""
        
        bean = update_bean_from_normalized_text(bean)        
        
        bean.time = normalize_time(duration_sec)

    return bean

def add_update_image_paths(beans):
    for bean in beans:
        if bean.path:
            bean.image = get_image_by_path(bean.path)
    return beans

def update_id3_wind_filtering(beans):
    beans = update_id3_for_beans(beans)
    beans = update_id3_for_cue(beans)
    beans = add_update_image_paths(beans)
    result = []
    for bean in beans:
        result.append(bean)
    return result
