def get_help():
    text = "Here are the commands that I understand:\n " \
           "`/xlrelease connect url username password`: Connect to XL Release " \
           "i.e. `/xlrelease connect https://xlrelease.com admin admin`\n" \
           "`/xlrelease create`: Create a new release from templates\n" \
           "`/xlrelease track`: Track existing release"
    return {
        "text": text
    }


def get_connect_help():
    text = "Provide all required parameters to configure XL Release : `/xlrelease connect url username password`\n " \
           "Example : `/xlrelease connect https://xlrelease.com admin admin`"
    return {
        "text": text
    }


def get_general_error():
    text = "Are you connected to XL Release? Try `/xlrelease help` for more details."
    return {
        "text": text
    }
