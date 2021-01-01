import traceback
import json
import sys


def add(*args):
    return sum(args)


def factorial(val):
    import math
    return str(math.factorial(val))


def youtube_lookup(url):
    from youtube_dl import YoutubeDL
    with YoutubeDL({"quiet": True}) as ydl:
        return ydl.extract_info(url, download=False)


def ytmusic_search(query):
    from ytmusicapi import YTMusic
    ytmusic = YTMusic()
    return ytmusic.search(query)


handlers = {
    "add": add,
    "factorial": factorial,
    "youtube:lookup": youtube_lookup,
    "ytmusic:search": ytmusic_search
}


def init_app(exit_secret):
    while True:
        data = json.loads(sys.stdin.readline())
        if data.get("C4NCL0S3") == exit_secret:
            break
        inputPayload = data["payload"]
        response = {"qID": data["qID"]}
        try:
            if inputPayload["path"] not in handlers:
                raise KeyError(
                    f"Invalid query endpoint [{inputPayload['path']}]")
            handler = handlers[inputPayload["path"]]
            response["payload"] = json.dumps(handler(*inputPayload["data"]))
        except:
            exc = sys.exc_info()
            response["error"] = {"type": exc[0].__name__, "message": str(
                exc[1]), "traceback": traceback.format_exc()}
        finally:
            print(json.dumps(response), flush=True)


if __name__ == "__main__":
    init_app(sys.argv[1])
