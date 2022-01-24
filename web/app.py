"""
John Doe's Flask API.
"""

from flask import Flask, abort, send_from_directory
import logging
import os
import config

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)
my_app = Flask(__name__)




def get_options():
    """
    Options from command line or configuration file.
    Returns namespace object with option value for port
    """
    # Defaults from configuration files;
    #   on conflict, the last value read has precedence
    options = config.configuration()
    # We want: PORT, DOCROOT, possibly LOGGING

    if options.PORT <= 1000:
        log.warning(("Port {} selected. " +
                         " Ports 0..1000 are reserved \n" +
                         "by the operating system").format(options.port))

    return options


@my_app.route("/")
def hello():
    return "UOCIS docker demo!\n"
@my_app.route('/<path:path>')
def file_check(path):
    #log.info(path)
    full = os.path.join("web"+os.sep+"pages"+os.sep,path)
    #log.info(full)
    if ".." in path or "~" in path:
        abort(403)

    file_exists = full
    if file_exists:
        #log.info("we got here")
        dir = os.path.dirname(full)
        return send_from_directory('pages'+os.sep, path), 200
    return abort(404)

@my_app.errorhandler(403)
def forbidden(e):
    return send_from_directory('pages'+os.sep, '403.html'), 403
@my_app.errorhandler(404)
def not_found(e):
    return send_from_directory('pages'+os.sep, '404.html'), 404


if __name__ == "__main__":
    options = get_options()
    my_app.run(debug=options.DEBUG,host="0.0.0.0",port=options.PORT)
