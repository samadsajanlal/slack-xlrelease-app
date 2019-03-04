def get_help():
    text = "Here are the commands that I understand:\n " \
           "`/xlrelease connect`: Connect to XL Release\n" \
           "`/xlrelease create`: Create a new release from templates\n" \
           "`/xlrelease track`: Track existing release"
    return {
        "text": text
    }
