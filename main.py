import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import simplejson as json
import pprint as pp
import sys
import collections
import time
import datetime
import cPickle as pickle
import os
import atexit
import pandas
import sys
from multiprocessing import Pool

reload(sys)
sys.setdefaultencoding('utf8')

silent = False
search_limit = 50
max_albums = 2000
max_tracks = 1
spotify_id = os.environ.get('SPOTIPY_CLIENT_ID')
spotify_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(
    client_id=spotify_id, client_secret=spotify_secret)
spotify = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager)

artist_names = set()
fresh_album_ids = set()
older_artists = set()
yesterdays_rank = {}
alphabet = range(ord('a'), ord('z') + 1)
letterIndex = 0
query = "tag:new " + chr(alphabet[letterIndex]) + "*"
lengthResetter = 0
queries = ["tag:new a", "tag:new b", "tag:new c", "tag:new d", "tag:new e", "tag:new f", "tag:new g", "tag:new h",
           "tag:new i", "tag:new j", "tag:new k",
           "tag:new l", "tag:new m", "tag:new n", "tag:new o", "tag:new p", "tag:new q", "tag:new r", "tag:new s",
           "tag:new t", "tag:new u", "tag:new v",
           "tag:new w", "tag:new x", "tag:new y", "tag:new z", "tag:new a*", "tag:new b*", "tag:new c*", "tag:new d*",
           "tag:new e*", "tag:new f*", "tag:new g*",
           "tag:new h*", "tag:new i*", "tag:new j*", "tag:new k*", "tag:new l*", "tag:new m*", "tag:new n*",
           "tag:new o*", "tag:new p*", "tag:new q*", "tag:new r*",
           "tag:new s*", "tag:new t*", "tag:new u*", "tag:new v*", "tag:new w*", "tag:new x*", "tag:new y*",
           "tag:new z*", "tag:new aa*", "tag:new ab*", "tag:new ac*",
           "tag:new ad*", "tag:new ae*", "tag:new af*", "tag:new ag*", "tag:new ah*", "tag:new ai*", "tag:new aj*",
           "tag:new ak*", "tag:new al*", "tag:new am*", "tag:new an*",
           "tag:new ao*", "tag:new ap*", "tag:new aq*", "tag:new ar*", "tag:new as*", "tag:new at*", "tag:new au*",
           "tag:new av*", "tag:new aw*", "tag:new ax*", "tag:new ay*",
           "tag:new az*", "tag:new ba*", "tag:new bb*", "tag:new bc*", "tag:new bd*", "tag:new be*", "tag:new bf*",
           "tag:new bg*", "tag:new bh*", "tag:new bi*", "tag:new bj*",
           "tag:new bk*", "tag:new bl*", "tag:new bm*", "tag:new bn*", "tag:new bo*", "tag:new bp*", "tag:new bq*",
           "tag:new br*", "tag:new bs*", "tag:new bt*", "tag:new bu*",
           "tag:new bv*", "tag:new bw*", "tag:new bx*", "tag:new by*", "tag:new bz*", "tag:new ca*", "tag:new cb*",
           "tag:new cc*", "tag:new cd*", "tag:new ce*", "tag:new cf*",
           "tag:new cg*", "tag:new ch*", "tag:new ci*", "tag:new cj*", "tag:new ck*", "tag:new cl*", "tag:new cm*",
           "tag:new cn*", "tag:new co*", "tag:new cp*", "tag:new cq*",
           "tag:new cr*", "tag:new cs*", "tag:new ct*", "tag:new cu*", "tag:new cv*", "tag:new cw*", "tag:new cx*",
           "tag:new cy*", "tag:new cz*", "tag:new da*", "tag:new db*",
           "tag:new dc*", "tag:new dd*", "tag:new de*", "tag:new df*", "tag:new dg*", "tag:new dh*", "tag:new di*",
           "tag:new dj*", "tag:new dk*", "tag:new dl*", "tag:new dm*",
           "tag:new dn*", "tag:new do*", "tag:new dp*", "tag:new dq*", "tag:new dr*", "tag:new ds*", "tag:new dt*",
           "tag:new du*", "tag:new dv*", "tag:new dw*", "tag:new dx*",
           "tag:new dy*", "tag:new dz*", "tag:new ea*", "tag:new eb*", "tag:new ec*", "tag:new ed*", "tag:new ee*",
           "tag:new ef*", "tag:new eg*", "tag:new eh*", "tag:new ei*",
           "tag:new ej*", "tag:new ek*", "tag:new el*", "tag:new em*", "tag:new en*", "tag:new eo*", "tag:new ep*",
           "tag:new eq*", "tag:new er*", "tag:new es*", "tag:new et*",
           "tag:new eu*", "tag:new ev*", "tag:new ew*", "tag:new ex*", "tag:new ey*", "tag:new ez*", "tag:new fa*",
           "tag:new fb*", "tag:new fc*", "tag:new fd*", "tag:new fe*",
           "tag:new ff*", "tag:new fg*", "tag:new fh*", "tag:new fi*", "tag:new fj*", "tag:new fk*", "tag:new fl*",
           "tag:new fm*", "tag:new fn*", "tag:new fo*", "tag:new fp*",
           "tag:new fq*", "tag:new fr*", "tag:new fs*", "tag:new ft*", "tag:new fu*", "tag:new fv*", "tag:new fw*",
           "tag:new fx*", "tag:new fy*", "tag:new fz*", "tag:new ga*",
           "tag:new gb*", "tag:new gc*", "tag:new gd*", "tag:new ge*", "tag:new gf*", "tag:new gg*", "tag:new gh*",
           "tag:new gi*", "tag:new gj*", "tag:new gk*", "tag:new gl*",
           "tag:new gm*", "tag:new gn*", "tag:new go*", "tag:new gp*", "tag:new gq*", "tag:new gr*", "tag:new gs*",
           "tag:new gt*", "tag:new gu*", "tag:new gv*", "tag:new gw*",
           "tag:new gx*", "tag:new gy*", "tag:new gz*", "tag:new ha*", "tag:new hb*", "tag:new hc*", "tag:new hd*",
           "tag:new he*", "tag:new hf*", "tag:new hg*", "tag:new hh*",
           "tag:new hi*", "tag:new hj*", "tag:new hk*", "tag:new hl*", "tag:new hm*", "tag:new hn*", "tag:new ho*",
           "tag:new hp*", "tag:new hq*", "tag:new hr*", "tag:new hs*",
           "tag:new ht*", "tag:new hu*", "tag:new hv*", "tag:new hw*", "tag:new hx*", "tag:new hy*", "tag:new hz*",
           "tag:new ia*", "tag:new ib*", "tag:new ic*", "tag:new id*",
           "tag:new ie*", "tag:new if*", "tag:new ig*", "tag:new ih*", "tag:new ii*", "tag:new ij*", "tag:new ik*",
           "tag:new il*", "tag:new im*", "tag:new in*", "tag:new io*",
           "tag:new ip*", "tag:new iq*", "tag:new ir*", "tag:new is*", "tag:new it*", "tag:new iu*", "tag:new iv*",
           "tag:new iw*", "tag:new ix*", "tag:new iy*", "tag:new iz*",
           "tag:new ja*", "tag:new jb*", "tag:new jc*", "tag:new jd*", "tag:new je*", "tag:new jf*", "tag:new jg*",
           "tag:new jh*", "tag:new ji*", "tag:new jj*", "tag:new jk*",
           "tag:new jl*", "tag:new jm*", "tag:new jn*", "tag:new jo*", "tag:new jp*", "tag:new jq*", "tag:new jr*",
           "tag:new js*", "tag:new jt*", "tag:new ju*", "tag:new jv*",
           "tag:new jw*", "tag:new jx*", "tag:new jy*", "tag:new jz*", "tag:new ka*", "tag:new kb*", "tag:new kc*",
           "tag:new kd*", "tag:new ke*", "tag:new kf*", "tag:new kg*",
           "tag:new kh*", "tag:new ki*", "tag:new kj*", "tag:new kk*", "tag:new kl*", "tag:new km*", "tag:new kn*",
           "tag:new ko*", "tag:new kp*", "tag:new kq*", "tag:new kr*",
           "tag:new ks*", "tag:new kt*", "tag:new ku*", "tag:new kv*", "tag:new kw*", "tag:new kx*", "tag:new ky*",
           "tag:new kz*", "tag:new la*", "tag:new lb*", "tag:new lc*",
           "tag:new ld*", "tag:new le*", "tag:new lf*", "tag:new lg*", "tag:new lh*", "tag:new li*", "tag:new lj*",
           "tag:new lk*", "tag:new ll*", "tag:new lm*", "tag:new ln*",
           "tag:new lo*", "tag:new lp*", "tag:new lq*", "tag:new lr*", "tag:new ls*", "tag:new lt*", "tag:new lu*",
           "tag:new lv*", "tag:new lw*", "tag:new lx*", "tag:new ly*",
           "tag:new lz*", "tag:new ma*", "tag:new mb*", "tag:new mc*", "tag:new md*", "tag:new me*", "tag:new mf*",
           "tag:new mg*", "tag:new mh*", "tag:new mi*", "tag:new mj*",
           "tag:new mk*", "tag:new ml*", "tag:new mm*", "tag:new mn*", "tag:new mo*", "tag:new mp*", "tag:new mq*",
           "tag:new mr*", "tag:new ms*", "tag:new mt*", "tag:new mu*",
           "tag:new mv*", "tag:new mw*", "tag:new mx*", "tag:new my*", "tag:new mz*", "tag:new na*", "tag:new nb*",
           "tag:new nc*", "tag:new nd*", "tag:new ne*", "tag:new nf*",
           "tag:new ng*", "tag:new nh*", "tag:new ni*", "tag:new nj*", "tag:new nk*", "tag:new nl*", "tag:new nm*",
           "tag:new nn*", "tag:new no*", "tag:new np*", "tag:new nq*",
           "tag:new nr*", "tag:new ns*", "tag:new nt*", "tag:new nu*", "tag:new nv*", "tag:new nw*", "tag:new nx*",
           "tag:new ny*", "tag:new nz*", "tag:new oa*", "tag:new ob*",
           "tag:new oc*", "tag:new od*", "tag:new oe*", "tag:new of*", "tag:new og*", "tag:new oh*", "tag:new oi*",
           "tag:new oj*", "tag:new ok*", "tag:new ol*", "tag:new om*",
           "tag:new on*", "tag:new oo*", "tag:new op*", "tag:new oq*", "tag:new or*", "tag:new os*", "tag:new ot*",
           "tag:new ou*", "tag:new ov*", "tag:new ow*", "tag:new ox*",
           "tag:new oy*", "tag:new oz*", "tag:new pa*", "tag:new pb*", "tag:new pc*", "tag:new pd*", "tag:new pe*",
           "tag:new pf*", "tag:new pg*", "tag:new ph*", "tag:new pi*",
           "tag:new pj*", "tag:new pk*", "tag:new pl*", "tag:new pm*", "tag:new pn*", "tag:new po*", "tag:new pp*",
           "tag:new pq*", "tag:new pr*", "tag:new ps*", "tag:new pt*",
           "tag:new pu*", "tag:new pv*", "tag:new pw*", "tag:new px*", "tag:new py*", "tag:new pz*", "tag:new qa*",
           "tag:new qb*", "tag:new qc*", "tag:new qd*", "tag:new qe*",
           "tag:new qf*", "tag:new qg*", "tag:new qh*", "tag:new qi*", "tag:new qj*", "tag:new qk*", "tag:new ql*",
           "tag:new qm*", "tag:new qn*", "tag:new qo*", "tag:new qp*",
           "tag:new qq*", "tag:new qr*", "tag:new qs*", "tag:new qt*", "tag:new qu*", "tag:new qv*", "tag:new qw*",
           "tag:new qx*", "tag:new qy*", "tag:new qz*", "tag:new ra*",
           "tag:new rb*", "tag:new rc*", "tag:new rd*", "tag:new re*", "tag:new rf*", "tag:new rg*", "tag:new rh*",
           "tag:new ri*", "tag:new rj*", "tag:new rk*", "tag:new rl*",
           "tag:new rm*", "tag:new rn*", "tag:new ro*", "tag:new rp*", "tag:new rq*", "tag:new rr*", "tag:new rs*",
           "tag:new rt*", "tag:new ru*", "tag:new rv*", "tag:new rw*",
           "tag:new rx*", "tag:new ry*", "tag:new rz*", "tag:new sa*", "tag:new sb*", "tag:new sc*", "tag:new sd*",
           "tag:new se*", "tag:new sf*", "tag:new sg*", "tag:new sh*",
           "tag:new si*", "tag:new sj*", "tag:new sk*", "tag:new sl*", "tag:new sm*", "tag:new sn*", "tag:new so*",
           "tag:new sp*", "tag:new sq*", "tag:new sr*", "tag:new ss*",
           "tag:new st*", "tag:new su*", "tag:new sv*", "tag:new sw*", "tag:new sx*", "tag:new sy*", "tag:new sz*",
           "tag:new ta*", "tag:new tb*", "tag:new tc*", "tag:new td*",
           "tag:new te*", "tag:new tf*", "tag:new tg*", "tag:new th*", "tag:new ti*", "tag:new tj*", "tag:new tk*",
           "tag:new tl*", "tag:new tm*", "tag:new tn*", "tag:new to*",
           "tag:new tp*", "tag:new tq*", "tag:new tr*", "tag:new ts*", "tag:new tt*", "tag:new tu*", "tag:new tv*",
           "tag:new tw*", "tag:new tx*", "tag:new ty*", "tag:new tz*",
           "tag:new ua*", "tag:new ub*", "tag:new uc*", "tag:new ud*", "tag:new ue*", "tag:new uf*", "tag:new ug*",
           "tag:new uh*", "tag:new ui*", "tag:new uj*", "tag:new uk*",
           "tag:new ul*", "tag:new um*", "tag:new un*", "tag:new uo*", "tag:new up*", "tag:new uq*", "tag:new ur*",
           "tag:new us*", "tag:new ut*", "tag:new uu*", "tag:new uv*",
           "tag:new uw*", "tag:new ux*", "tag:new uy*", "tag:new uz*", "tag:new va*", "tag:new vb*", "tag:new vc*",
           "tag:new vd*", "tag:new ve*", "tag:new vf*", "tag:new vg*",
           "tag:new vh*", "tag:new vi*", "tag:new vj*", "tag:new vk*", "tag:new vl*", "tag:new vm*", "tag:new vn*",
           "tag:new vo*", "tag:new vp*", "tag:new vq*", "tag:new vr*",
           "tag:new vs*", "tag:new vt*", "tag:new vu*", "tag:new vv*", "tag:new vw*", "tag:new vx*", "tag:new vy*",
           "tag:new vz*", "tag:new wa*", "tag:new wb*", "tag:new wc*",
           "tag:new wd*", "tag:new we*", "tag:new wf*", "tag:new wg*", "tag:new wh*", "tag:new wi*", "tag:new wj*",
           "tag:new wk*", "tag:new wl*", "tag:new wm*", "tag:new wn*",
           "tag:new wo*", "tag:new wp*", "tag:new wq*", "tag:new wr*", "tag:new ws*", "tag:new wt*", "tag:new wu*",
           "tag:new wv*", "tag:new ww*", "tag:new wx*", "tag:new wy*",
           "tag:new wz*", "tag:new xa*", "tag:new xb*", "tag:new xc*", "tag:new xd*", "tag:new xe*", "tag:new xf*",
           "tag:new xg*", "tag:new xh*", "tag:new xi*", "tag:new xj*",
           "tag:new xk*", "tag:new xl*", "tag:new xm*", "tag:new xn*", "tag:new xo*", "tag:new xp*", "tag:new xq*",
           "tag:new xr*", "tag:new xs*", "tag:new xt*", "tag:new xu*",
           "tag:new xv*", "tag:new xw*", "tag:new xx*", "tag:new xy*", "tag:new xz*", "tag:new ya*", "tag:new yb*",
           "tag:new yc*", "tag:new yd*", "tag:new ye*", "tag:new yf*",
           "tag:new yg*", "tag:new yh*", "tag:new yi*", "tag:new yj*", "tag:new yk*", "tag:new yl*", "tag:new ym*",
           "tag:new yn*", "tag:new yo*", "tag:new yp*", "tag:new yq*",
           "tag:new yr*", "tag:new ys*", "tag:new yt*", "tag:new yu*", "tag:new yv*", "tag:new yw*", "tag:new yx*",
           "tag:new yy*", "tag:new yz*", "tag:new za*", "tag:new zb*",
           "tag:new zc*", "tag:new zd*", "tag:new ze*", "tag:new zf*", "tag:new zg*", "tag:new zh*", "tag:new zi*",
           "tag:new zj*", "tag:new zk*", "tag:new zl*", "tag:new zm*",
           "tag:new zn*", "tag:new zo*", "tag:new zp*", "tag:new zq*", "tag:new zr*", "tag:new zs*", "tag:new zt*",
           "tag:new zu*", "tag:new zv*", "tag:new zw*", "tag:new zx*",
           "tag:new zy*", "tag:new zz*", "tag:new 0*", "tag:new 1*", "tag:new 2*", "tag:new 3*", "tag:new 4*",
           "tag:new 5*", "tag:new 6*", "tag:new 7*", "tag:new 8*", "tag:new 9*"]
albumholder = []
backup = []


def fetch_albums(albums):
    ret_albums = []
    max_batch = 20
    ids = []
    for album in albums:
        ids.append(album['id'])

    for i in xrange(0, len(ids), max_batch):
        nids = ids[i:i + max_batch]

        retries = 5
        while retries > 0:
            try:
                results = spotify.albums(nids)
                albums = results['albums']
                ret_albums.extend(albums)
                break
            except:
                raise
                if True:
                    retries -= 1
                    if not silent:
                        print 'retrying A ...', retries
                    time.sleep(1)
    return ret_albums


def fetch_artists(ids):
    ret_artists = []
    max_batch = 20

    for i in xrange(0, len(ids), max_batch):
        nids = ids[i:i + max_batch]

        retries = 5
        while retries > 0:
            try:
                results = spotify.artists(nids)
                artists = results['artists']
                ret_artists.extend(artists)
                break
            except:
                raise
                if True:
                    retries -= 1
                    if not silent:
                        print 'retrying B ...', retries
                    time.sleep(1)
    return ret_artists


def get_new_albums(chunks):
    # Gets new albums using tag:new call, saves all album data to albums[], and saves all album ID to fresh_album_id
    albums = []
    letterIndex = 0
    query = str(chunks)
    print query
    lengthResetter = 0
    results = spotify.search(q=query, type='album', limit=search_limit)

    albums.extend(fetch_albums(results['albums']['items']))

    while results['albums']['next']:
        if not silent:
            print len(albums)
        retries = 5
        while retries > 0:
            try:
                results = spotify.next(results['albums'])
                time.sleep(1)
                break
            except:
                if True:
                    retries -= 1
                    if not silent:
                        print 'retrying ...', retries
                    time.sleep(1.5)
        try:
            albums.extend(fetch_albums(results['albums']['items']))
        except Exception as e:
            print("Ran into issue:")
            print(str(e))
            continue
        # if (len(albums) - lengthResetter > max_albums) or (len(albums) >= max_albums):
        # print("# of albums:", len(albums))
        # print("lengthresetter:", lengthResetter)
        if (len(albums) - lengthResetter > max_albums) or (len(albums) >= max_albums):
            break

        lengthResetter = len(albums)

    if not silent:
        print 'total albums', len(albums)

    # for album in albums:
    #     fresh_album_ids.add(album['id'])
    # print("im about to finish gets")
    return albums


def create_fresh_album_ids(albums):
    fresh_album_ids = set()
    for album in albums:
        fresh_album_ids.add(album['id'])
    return fresh_album_ids


def is_compilation(album):
    various_artists = '0LyfQWJT6nXafLPZqxe9Of'

    if album['album_type'] == 'compilation':
        return True

    if album['album_type'] == 'single':
        return True

    for artist in album['artists']:
        if artist['id'] == various_artists:
            if not silent:
                print 'skipped', artist['id']
            return True
    return False


def artist_has_older_album(aid):
    # [Sub Process_2] uses older_artists from cache to check if artist is new
    # calls API using plugged artist ID to check for all releases, cross-checks found album IDs with fresh_album_ids
    if aid in older_artists:
        return True
    else:
        tries = 3
        for i in range(tries):
            try:
                results = spotify.artist_albums(
                    aid, limit=50, album_type='single,album')
            except Exception as e:
                if i < tries - 1:  # i is zero indexed
                    print("Ran into issue, retrying...")
                    time.sleep(5)
                    continue
                else:
                    print 'Cannot resolve artist, skipping album'
                    return True
            break
        tot = results['total']
        for album in results['items']:
            if album['id'] not in fresh_album_ids:  # AHAH
                older_artists.add(aid)
                return True
    return False


def process_albums1(albums):
    # filters out compilations, albums older than 2 weeks, and dedups logged artist names for ultimate output
    # after filtering, creates a filtered album array named out_albums that overwrites main album array
    out_albums = []
    for album in albums:
        if is_compilation(album):
            continue
        aname = album['artists'][0]['name']

        album['days_on_chart'] = get_days_on_chart(album)
        if album['days_on_chart'] > 14:
            # print album['days_on_chart']
            continue
        # dedup by artist names
        if aname in artist_names:
            continue
        artist_names.add(aname)

        out_albums.append(album)
    return out_albums


def process_albums2(albums):
    # reads album array that has been processed from 1, starts a new out_albums array
    # calls artist_has_older_album to check true, plugging in the artist ID from album array
    out_albums = []
    for i, album in enumerate(albums):
        if not silent:
            print i, 'of', len(albums), 'found', len(out_albums)
        if artist_has_older_album(album['artists'][0]['id']):
            # print album
            continue
        out_albums.append(album)
    return out_albums


def get_artist_info(uris):
    # [Sub Process_4] all artist URI's from albums[] get plugged in to artist call, returning artist info
    # unsure how this for loop operates syntaxically
    page_size = 50

    map = {}
    for start in xrange(0, len(uris), page_size):
        turis = uris[start:start + page_size]
        results = spotify.artists(turis)
        for artist in results['artists']:
            map[artist['uri']] = artist
    return map


def process_albums4(albums):
    # get the artist followers for the remaining artists
    if albums:
        uris = []
        for album in albums:
            uris.append(album['artist_uri'])

        fmap = get_artist_info(uris)

        for album in albums:
            ainfo = fmap[album['artist_uri']]
            album['artist_followers'] = ainfo['followers']['total']
            album['artist_popularity'] = ainfo['popularity']
            if 'images' in ainfo and len(ainfo['images']) > 0:
                album['artist_image'] = ainfo['images'][0]['url']

        albums.sort(key=lambda a: a['popularity'], reverse=True)
        albums.sort(key=lambda a: a['artist_popularity'], reverse=True)
        albums.sort(key=lambda a: a['artist_followers'], reverse=True)

        max_followers = albums[0]['artist_followers'] + 1
        for album in albums:
            nfollows = album['artist_followers'] * 100.0 / max_followers
            album['nartist_followers'] = nfollows
            score = (10 * nfollows +
                     album['popularity'] + album['artist_popularity']) / 12.
            album['score'] = score

        albums.sort(key=lambda a: a['score'], reverse=True)

        for rank, album in enumerate(albums):
            print rank, album['score']
            album['rank'] = rank
            if album['id'] in yesterdays_rank:
                yrank = yesterdays_rank[album['id']]
                album['prev_rank'] = yrank
                if rank < yrank:
                    album['delta_rank'] = 'up'
                elif rank > yrank:
                    album['delta_rank'] = 'down'
                else:
                    album['delta_rank'] = 'same'
            else:
                album['prev_rank'] = -1
                album['delta_rank'] = 'up'
    if not albums:
        print('no albums to process')

    return albums


def cache_save():
    f = open('cache.pkl', 'wb')
    pickle.dump(older_artists, f, -1)
    f.close()
    if not silent:
        print 'cached', len(older_artists), 'artists'


def cache_load():
    obj = set()
    if os.path.exists('cache.pkl'):
        f = open('cache.pkl', "rb")
        obj = pickle.load(f)
        f.close()
        if not silent:
            print 'loaded', len(obj), 'artists'
    atexit.register(cache_save)
    return obj


def filter_tracks(album):
    # [Sub of Process_3] takes extraneous data out of track field
    out = []
    for track in album['tracks']['items'][:max_tracks]:
        ttrack = {
            'id': track['id'],
            'preview_url': track['preview_url'],
            'name': track['name']
        }
        out.append(ttrack)
    return out


def get_days_on_chart(album):
    now = datetime.date.today()
    try:
        rel = datetime.datetime.strptime(
            album['release_date'], '%Y-%m-%d').date()
        dt = now - rel
        return dt.days
    except:
        return 1000


def process_albums3(albums):
    # Sorts albums by popularity field, then deletes extraneous data in array (including genre because its always blank)
    # Redesigns image art structure, ensuring fields are populated if missing
    albums.sort(key=lambda a: a['popularity'], reverse=True)
    for album in albums:
        album['tracks'] = filter_tracks(album)

        del album['available_markets']
        del album['copyrights']
        del album['external_ids']
        del album['external_urls']
        del album['genres']
        del album['type']

        album['artist_name'] = album['artists'][0]['name']
        album['artist_uri'] = album['artists'][0]['uri']
        del album['artists']

        image_large = None
        image_med = None
        images = album['images']

        if len(images) > 0:
            for image in images:
                if image_large == None and image['width'] > 400:
                    image_large = image['url']
                if image_med == None and image['width'] <= 400 and \
                        image['width'] >= 300:
                    image_med = image['url']

            if image_large == None:
                image_large = images[0]['url']
            if image_med == None:
                image_med = image_large
            image_small = images[-1]['url']

        del album['images']
        album['image_large'] = image_large
        album['image_med'] = image_med
        album['image_small'] = image_small

        del album['release_date_precision']
        del album['href']
    return albums


def make_date_hist(albums):
    # Finds how many albums came out on each day and saves the count set
    hist = collections.defaultdict(int)
    for album in albums:
        hist[album['release_date']] += 1
        # print hist
    return hist


def save(json_blob, name):
    js = json.dumps(json_blob)
    f = open(name, 'w')
    print >> f, js
    f.close()


def load_yesterdays_rank():
    yranks = {}
    path = 'yesterday.js'
    if os.path.exists(path):
        f = open(path)
        js = f.read()
        f.close()
        obj = json.loads(js)
        for album in obj['albums']:
            yranks[album['id']] = album['rank']

    if not silent:
        print 'loaded', len(yranks), 'albums from yesterday'
    return yranks


def pool_party():
    pool = Pool(processes=8, maxtasksperchild=1000)
    albums = pool.map(get_new_albums, queries[0:727])
    print("about to start sublist combine")
    albums = [ent for sublist in albums for ent in sublist]
    print("about to finish pool party")
    return albums


def save_album_ids(albums):
    print("about to print album ids")
    result = []
    for album in albums:
        my_dict = {'id': album['artists'][0]['id']}
        # print my_dict
        result.append(my_dict)
    with open('data.json', 'w') as file_handler:
        for item in result:
            file_handler.write("{}\n".format(item))
    return


def save_gets(albums):
    backup = []
    backup = albums
    with open("backup.txt", "wb") as fp:
        pickle.dump(backup, fp)
    print("about to finish save_gets")
    return backup


def load_gets():
    print("do i reach here")
    with open("backup.txt", "rb") as fp:
        b = pickle.load(fp)
        print("i successfully loaded backup")
    return backup


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--silent':
        silent = True
    older_artists = cache_load()
    yesterdays_rank = load_yesterdays_rank()
    # yesterday = datetime.date.today() - datetime.timedelta(1)
    # yesterdaysDate = yesterday.strftime('%Y%m%d')
    # yesterdaysFile_myFile = yesterday.strftime('backup.txt')
    # file_names = os.listdir("E:/Projects/Firebase/fresher-faces/crawl")
    albums = pool_party()
    fresh_album_ids = create_fresh_album_ids(albums)
    # save_album_ids(albums)

    if not silent:
        print 'new albums', len(albums)

    albums = process_albums1(albums)
    new_albums = len(albums)
    all_hist = make_date_hist(albums)
    albums = process_albums2(albums)
    albums = process_albums3(albums)
    albums = process_albums4(albums)

    fresh_hist = make_date_hist(albums)

    json_blob = {
        'albums': albums,
        'version': '1.0',
        'new_albums': new_albums,
        'date': str(datetime.datetime.now()),
        'release_date_hist': all_hist,
        'fresh_date_hist': fresh_hist,
    }
    save("success", name='success.txt')
    print 'success.txt saved'
    save(json_blob, name='new_releases.js')
    print('new_releases.js saved')
    json_blob['albums'] = json_blob['albums'][:40]
    save(json_blob, name='quick_releases.js')
    print('quick_releases.js saved')
