from flask import Flask, Response, abort, request
from werkzeug.exceptions import HTTPException, InternalServerError

from ..problem import problem

app = Flask(__name__)


@app.errorhandler(Exception)
def handle_error_last_resort(_):
    return handle_server_error(InternalServerError())


@app.errorhandler(500)
def handle_server_error(err: HTTPException):
    return problem(err.code, err.name)


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
def handle_client_error(err: HTTPException):
    return problem(err.code, err.name, instance=request.path)


@app.errorhandler(404)
def handle_not_found(err: HTTPException):
    auth_err = auth_error()
    if auth_err is not None:
        return auth_err
    return handle_client_error(err)


@app.errorhandler(405)
def handle_method_not_allowed(err: HTTPException):
    response = problem(err.code, err.name, instance=request.path)
    response.headers.add("allow", "GET")
    return response


def auth_error() -> Response | None:
    auth_header = request.headers.get("Authorization")

    if auth_header is None:
        return problem(401, "Unauthorized", instance=request.path)

    if auth_header == "Bearer super-secret":
        return None

    return problem(403, "Forbidden", instance=request.path)


def require_auth():
    response = auth_error()
    if response is not None:
        abort(response)


@app.get("/info")
def info():
    require_auth()

    return {
        "month": "7",
        "num": 2966,
        "link": "",
        "year": "2024",
        "news": "",
        "safe_title": "Exam Numbers",
        "transcript": "",
        "alt": "Calligraphy exam: Write down the number 37, spelled out, nicely.",
        "img": "https://imgs.xkcd.com/comics/exam_numbers.png",
        "title": "Exam Numbers",
        "day": "31",
    }


@app.get("/<int:comicId>/info")
def comic(comicId):
    require_auth()

    if comicId < 1:
        return problem(400, "Comic ID too low", instance=request.path)
    if comicId > 2**31:
        raise Exception("Overflow for 32-bit signed int")
        # return problem(400, "Comic ID too high", instance=request.path)
    if comicId > 3000:
        abort(404)

    return {
        "month": "7",
        "num": 614,
        "link": "",
        "year": "2009",
        "news": "",
        "safe_title": "Woodpecker",
        "transcript": "[[A man with a beret and a woman are standing on a boardwalk, leaning on a handrail.]]\nMan: A woodpecker!\n<<Pop pop pop>>\nWoman: Yup.\n\n[[The woodpecker is banging its head against a tree.]]\nWoman: He hatched about this time last year.\n<<Pop pop pop pop>>\n\n[[The woman walks away.  The man is still standing at the handrail.]]\n\nMan: ... woodpecker?\nMan: It's your birthday!\n\nMan: Did you know?\n\nMan: Did... did nobody tell you?\n\n[[The man stands, looking.]]\n\n[[The man walks away.]]\n\n[[There is a tree.]]\n\n[[The man approaches the tree with a present in a box, tied up with ribbon.]]\n\n[[The man sets the present down at the base of the tree and looks up.]]\n\n[[The man walks away.]]\n\n[[The present is sitting at the bottom of the tree.]]\n\n[[The woodpecker looks down at the present.]]\n\n[[The woodpecker sits on the present.]]\n\n[[The woodpecker pulls on the ribbon tying the present closed.]]\n\n((full width panel))\n[[The woodpecker is flying, with an electric drill dangling from its feet, held by the cord.]]\n\n{{Title text: If you don't have an extension cord I can get that too.  Because we're friends!  Right?}}",
        "alt": "If you don't have an extension cord I can get that too.  Because we're friends!  Right?",
        "img": "https://imgs.xkcd.com/comics/woodpecker.png",
        "title": "Woodpecker",
        "day": "24",
    }
