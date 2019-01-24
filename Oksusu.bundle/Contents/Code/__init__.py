from oksusu import *
NAME = 'oksusu'
PREFIX = '/video/oksusu'
ICON = 'icon-default.jpg'
ART = 'art-default.jpg'

####################################################################################################
def Start():
    ObjectContainer.title1 = NAME
    DirectoryObject.thumb = R(ICON)
    HTTP.CacheTime = 0

####################################################################################################
@handler(PREFIX, NAME, thumb = ICON, art = ART)
def MainMenu():
    oc = ObjectContainer()
    try:
        message = DoStartLoginCheck()
        message = 'Ver : ' + VERSION + ' - ' + message
        if GetLoginStatus() is not 'SUCCESS':
            message = DoStartLoginCheck()
            message = 'Ver:' + VERSION + ' - ' + message
        else:
            for menu in TOP_MENU_LIST:
                tmp = menu.split(':')
                if tmp[2] == 'M':
                    oc.add(DirectoryObject(key = Callback(Menu, title=unicode(tmp[0]), type=tmp[1]), title = unicode(tmp[0])))
                else:
                    oc.add(DirectoryObject(key = Callback(ContentList, title=unicode(tmp[0]), type=tmp[1], param=tmp[2]), title = unicode(tmp[0])))
        oc.add(DirectoryObject(key = Callback(Label, message=message), title = unicode(message)))
    except Exception as e:
        LOG('<<<Exception>>> MainMenu: %s' % e)
    return oc

####################################################################################################
@route(PREFIX + '/Menu')
def Menu(title, type):
    oc = ObjectContainer(title2 = unicode(title))
    try:
        for item in MENU_LIST:
            tmp = item.split(':')
            if type == tmp[0]:
                oc.add(DirectoryObject(key = Callback(ContentList, title=unicode(tmp[1]), type=None, param=tmp[2], param2=tmp[3]), title = unicode(tmp[1])))
    except Exception as e:
        LOG('<<<Exception>>> Menu: %s' % e)
    return oc

####################################################################################################
@route(PREFIX + '/ContentList')
def ContentList(title, type, param, param2=None, pageNo='1'):
    if param2 is not None: 
        type = param
        param = param2
    oc = ObjectContainer(title2 = unicode(title))
    try:
        has_more, items = GetList(type, param, pageNo)
        for item in items:
            if type == 'LIVE':
                save_param = '|'.join( [type, item['id'], item['channel_title'], item['img'] ])
                oc.add(DirectoryObject(key = Callback(Quality, 
                                title = unicode(item['channel_title']), type = type, 
                                code = item['id'], summary = item['episode_title'], 
                                thumb = item['img'], save_param = save_param, 
                                music_yn=item['music_yn']),
                        title = item['channel_title'],
                        summary = item['episode_title'],
                        thumb = item['img']))
            elif type == 'CH' and param == 'C':
                oc.add(DirectoryObject(key = Callback(ContentList, 
                                title = unicode(item['channel_title']),
                                type = type,
                                param = item['id']),
                        title = item['channel_title'],
                        summary = item['episode_title'],
                        thumb = item['img']))
            elif type == 'CH' and param is not None:
                save_param = '|'.join( [type, item['ch_id'], item['ch_title'], item['img'] ])
                oc.add(DirectoryObject(key = Callback(Quality, 
                                title = unicode(item['episode_title']), type = type,
                                code = item['url'], summary = item['episode_title'],
                                thumb = item['img'], save_param = save_param),
                        title = item['episode_title'],
                        summary = item['episode_title'],
                        thumb = item['img']))
            elif type == 'CLIP':
                oc.add(DirectoryObject(key = Callback(ContentList, 
                                title = unicode(item['title']),
                                type = item['id'],
                                param = 'P'),
                        title = item['title'],
                        summary = item['summary'],
                        thumb = item['img']))
            elif param == 'P':
                oc.add(DirectoryObject(key = Callback(Quality, 
                                title = unicode(item['title']), type = type,
                                code = item['id'], summary = item['summary'],
                                thumb = item['img'], save_param = None),
                        title = item['title'],
                        summary = item['summary'],
                        thumb = item['img']))
            elif param == 'C':
                oc.add(DirectoryObject(key = Callback(ContentList, 
                                title = unicode(item['title']),
                                type = item['series_id'],
                                param = 'E'),
                        title = item['title'],
                        summary = item['summary'],
                        thumb = item['img']))
            elif param == 'E':
                title2 = item['no'] + '회 ' + '(' + item['title'] + ')'
                save_param = '|'.join( ['C', item['series_id'], item['program_title'], item['img'] ])
                oc.add(DirectoryObject(key = Callback(Quality, 
                                title = unicode(title2), type = type,
                                code = item['id'], summary = item['summary'],
                                thumb = item['img'], save_param = save_param),
                        title = title2,
                        summary = item['summary'],
                        thumb = item['img']))
            elif type == 'Watched':
                if item['type'] == 'LIVE' or item['type'] == 'P':
                    save_param = '|'.join( [item['type'], item['id'], item['title'], item['img'] ])
                    oc.add(DirectoryObject(key = Callback(Quality, 
                                title = unicode(item['title']), type = item['type'], 
                                code = item['id'], summary = item['title'], 
                                thumb = item['img'], save_param = save_param),
                        title = item['title'],
                        summary = item['title'],
                        thumb = item['img']))
                elif item['type'] == 'CH':
                    oc.add(DirectoryObject(key = Callback(ContentList, 
                                title = unicode(item['title']),
                                type = item['type'],
                                param = item['id']),
                        title = item['title'],
                        summary = item['title'],
                        thumb = item['img']))
                elif item['type'] == 'C':
                    oc.add(DirectoryObject(key = Callback(ContentList, 
                                title = unicode(item['title']),
                                type = item['id'],
                                param = 'E'),
                        title = item['title'],
                        summary = item['title'],
                        thumb = item['img']))
        if pageNo != '1':
            oc.add(DirectoryObject(
                key = Callback(ContentList, title=title, type=type, param=param, pageNo=str(int(pageNo)-1)),
                title = unicode('<< 이전 페이지')
            ))
        if has_more == 'Y':
            oc.add(DirectoryObject(
                key = Callback(ContentList, title=title, type=type, param=param, pageNo=str(int(pageNo)+1)),
                title = unicode('다음 페이지 >>')
            ))
    except Exception as e:
        LOG('<<<Exception>>> ContentList: %s' % e)
    return oc

####################################################################################################
@route(PREFIX + '/Quality')
def Quality(title, type, code, summary, thumb, save_param, music_yn='N'):
    oc = ObjectContainer(title2 = unicode(title))
    message = '시청불가'
    try:
        if type == 'CH': 
            url = code
            oc.add(
                CreateVideoClipObject(
                    url = url, title = unicode(title), thumb = thumb, art = None,
                    summary = unicode(summary), type=type, save_param=save_param, 
                    include_container = False
                ))
        else:
            url = GetURL(code)
            str = ['FHD', 'HD', 'SD', 'AUTO']
            for s in str:
                if s == 'AUTO' and len(oc)>0: break
                if url[s] is not None:
                    if music_yn == 'Y' and Client.Product != 'Plex for iOS':
                        oc.add(CreateTrackObject(url=url[s], title=unicode(title), summary=summary,  thumb=thumb))
                    else:
                        title2 = title + ' [' + s + ']'
                        #summary = summary + '\n' + url[s]
                        oc.add(
                            CreateVideoClipObject(
                                url = url[s], title = unicode(title2), thumb = thumb, art = None,
                                summary = unicode(summary), type=type, save_param=save_param, 
                                include_container = False
                            ))
    except Exception as e:
        LOG('<<<Exception>>> Quality: %s' % e)
    if len(oc) == 0:
        oc.add(DirectoryObject(key = Callback(Label, message=message), title = unicode(message)))
    return oc

####################################################################################################
@route(PREFIX + '/CreateVideoClipObject', include_container = bool)
def CreateVideoClipObject(url, title, thumb, art, summary, type, save_param, 
                          optimized_for_streaming = True,
                          include_container = False, *args, **kwargs):

    vco = VideoClipObject(
        key = Callback(CreateVideoClipObject,
        url = url, title = title, thumb = thumb, art = art, summary = summary,
        type=type, save_param=save_param,
        optimized_for_streaming = optimized_for_streaming,
        include_container = True),
        rating_key = url,
        title = title,
        thumb = thumb,
        art = art,
        summary = summary,
        items = [
            MediaObject(
                parts = [
                    PartObject(
                        key = HTTPLiveStreamURL(Callback(PlayVideo, url = url, type=type, save_param=save_param))
                    )
                ],
                optimized_for_streaming = optimized_for_streaming,
            )
        ]
    )

    if include_container:
        return ObjectContainer(objects = [vco])
    else:
        return vco

####################################################################################################
@route(PREFIX + '/createtrackobject', include_container = bool)
def CreateTrackObject(url, title, summary, thumb, include_container=False, *args, **kwargs):
    container = Container.MP4
    audio_codec = AudioCodec.AAC
    track_object = TrackObject(
        key = Callback(CreateTrackObject, url=url, title=title, summary=summary, thumb=thumb, include_container=True),
        rating_key = url,
        title = title,
        summary = summary,
        items = [
            MediaObject(
                parts = [
                    PartObject(key=url)
                ],
                container = container,
                audio_codec = audio_codec,
                audio_channels = 2
            )
        ], 
        thumb = Resource.ContentsOfURLWithFallback(thumb)
    )

    if include_container:
        return ObjectContainer(objects=[track_object])
    else:
        return track_object

####################################################################################################
@indirect
@route(PREFIX + '/PlayVideo.m3u8')
def PlayVideo(url, type, save_param):
    try:
        if save_param is not None:
            SaveWatchedList(save_param)
    except Exception as e:
        LOG('<<<Exception>>> PlayVideo: %s' % e)
    return IndirectResponse(VideoClipObject, key = url)

####################################################################################################
@route(PREFIX + '/label')
def Label(message):
    oc = ObjectContainer(title2 = unicode(message))
    oc.add(DirectoryObject(key = Callback(Label, message=message),title = unicode(message)))
    return oc
