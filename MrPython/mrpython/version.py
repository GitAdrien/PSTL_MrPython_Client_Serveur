
MRPYTHON_VERSION_MAJOR = 0
MRPYTHON_VERSION_MINOR = 1
MRPYTHON_VERSION_PATCH = 4
MRPYTHON_VERSION_TAG = ""


def version_string():
    return "{}.{}.{}{}".format(MRPYTHON_VERSION_MAJOR,
                               MRPYTHON_VERSION_MINOR,
                               MRPYTHON_VERSION_PATCH,
                               "" if MRPYTHON_VERSION_TAG == "" else ("-" + MRPYTHON_VERSION_TAG))

