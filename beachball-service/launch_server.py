#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import io

import flask
from flask_cache import Cache
import matplotlib.pyplot as plt
from matplotlib.colors import hex2color
from obspy.imaging.beachball import beach

plt.switch_backend("agg")


app = flask.Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


def make_cache_key(*args, **kwargs):
    path = flask.request.path
    args = str(hash(frozenset(flask.request.args.items())))
    return (path + args).encode('utf-8')


@app.route("/mt")
@cache.cached(key_prefix=make_cache_key)
def mt_plot():
    """
    Return a moment tensor image.
    """
    formats = {
        "png": "image/png",
        "svg": "image/svg+xml"
    }

    args = flask.request.args
    m_rr = float(args["m_rr"])
    m_tt = float(args["m_tt"])
    m_pp = float(args["m_pp"])
    m_rt = float(args["m_rt"])
    m_rp = float(args["m_rp"])
    m_tp = float(args["m_tp"])
    focmec = (m_rr, m_tt, m_pp, m_rt, m_rp, m_tp)

    # Allow hexcolors.
    color = args.get("color", "red")
    try:
        hexcolor = "#" + color
        hex2color(hexcolor)
        color = hexcolor
    except ValueError:
        pass

    size = int(args.get("size", 32))
    lw = float(args.get("lw", 1))
    format = args.get("format", "png")

    if format not in formats.keys():
        flask.abort(500)

    dpi = 100
    fig = plt.figure(figsize=(float(size) / float(dpi),
                              float(size) / float(dpi)),
                     dpi=dpi)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    bb = beach(focmec, xy=(0, 0), width=200, linewidth=lw, facecolor=color)
    ax.add_collection(bb)
    ax.set_xlim(-105, 105)
    ax.set_ylim(-105, 105)

    temp = io.BytesIO()
    plt.savefig(temp, format=format, dpi=dpi, transparent=True)
    plt.close(fig)
    plt.close("all")
    temp.seek(0, 0)

    return flask.send_file(temp, mimetype=formats[format],
                           add_etags=False,
                           attachment_filename="mt.%s" % format)


def serve(port=12111, debug=False):
    """
    Start the server.

    :param port: The port to launch on.
    :param debug: Debug on/off.
    """
    host = "0.0.0.0"

    if debug:
        app.run(port=port, debug=debug, host=host)
    else:
        # Use the gevent WSGI server to get a much more stable "production"
        # environment.
        from gevent.wsgi import WSGIServer

        http_server = WSGIServer((host, port), app)
        http_server.serve_forever()


def main():
    parser = argparse.ArgumentParser(
        description="Launch the beachball server.")
    parser.add_argument("--port", default=12345,
                        help="web server port", type=int)
    parser.add_argument("--debug", action="store_true", help="debug mode")

    args = parser.parse_args()

    serve(port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
