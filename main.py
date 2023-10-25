from flask import Flask, jsonify, request
import requests
import regex as re
import browser_cookie3
from bardapi.constants import SESSION_HEADERS
from bardapi import Bard

app = Flask(__name__)


def extract_bard_cookie(cookies: bool = False) -> dict:
    """Extracts the Bard cookie from the browser."""

    supported_browsers = [
        browser_cookie3.safari,
    ]

    cookie_dict = {}

    for browser_fn in supported_browsers:
        try:
            cookiejar = browser_fn(domain_name=".google.com")

            for cookie in cookiejar:
                if cookie.name == "__Secure-1PSID" and cookie.value.endswith("."):
                    cookie_dict["__Secure-1PSID"] = cookie.value
                if cookies:
                    if cookie.name == "__Secure-1PSIDTS":
                        cookie_dict["__Secure-1PSIDTS"] = cookie.value
                    elif cookie.name == "__Secure-1PSIDCC":
                        cookie_dict["__Secure-1PSIDCC"] = cookie.value
                if len(cookie_dict) == 3:
                    return cookie_dict
        except Exception as error:
            print(error)
            continue

    if not cookie_dict:
        raise Exception("No supported browser found or issue with cookie extraction")

    return cookie_dict


@app.route("/get_ripeness", methods=["POST"])
def get_ripeness():
    """Gets the ripeness range of a fruit image."""
    try:
        fruit_name = request.form.get("fruit_name", "")
        image_data = request.files.get("image")

        if not fruit_name:
            return jsonify({"error": "No fruit_name received"}), 400
        if image_data is None:
            return jsonify({"error": "No image received"}), 400

        image_data = image_data.read()

        bardcookies = extract_bard_cookie(cookies=True)
        print(bardcookies)
        token = bardcookies["__Secure-1PSID"]

        session = requests.Session()
        session.headers = SESSION_HEADERS
        session.cookies.set("__Secure-1PSID", token)

        if "__Secure-1PSIDTS" in bardcookies:
            session.cookies.set("__Secure-1PSIDTS", bardcookies["__Secure-1PSIDTS"])
        if "__Secure-1PSIDCC" in bardcookies:
            session.cookies.set("__Secure-1PSIDCC", bardcookies["__Secure-1PSIDCC"])

        bard = Bard(token=token, session=session)

        bard_answer = bard.ask_about_image(
            f"(I need a short and simple answer with bold text no example needed as I am an expert about ripeness just need the guess) Please analyze this {fruit_name} image and guess the {fruit_name} ripeness range: 0-25% (unripe/green), 25-50% (almost ripe), 50-75% (ripe), 75-90% (almost overripe), 90-100% (overripe, rotten or moldy).)",
            image_data,
        )

        pattern = r"(\d+-\d+%)"
        patterngeneral = r"(\d+%)"
        match = re.search(pattern, bard_answer["content"])
        matchgeneral = re.search(patterngeneral, bard_answer["content"])
        if match:
            ripeness_range = match.group(1)
            return jsonify({"ripeness_range": ripeness_range})
        elif matchgeneral:
            ripeness_range = matchgeneral.group(1)
            return jsonify({"ripeness_range": ripeness_range})
        else:
            return (
                jsonify(
                    {
                        "error": "Ripeness range not found in the text.",
                        "answer": bard_answer["content"],
                    }
                ),
                400,
            )
    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=17992, debug=True)
