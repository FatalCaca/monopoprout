__author__ = 'simon.ballu@gmail.com'

def resolve_text(text, *args):
        for index, argument in enumerate(args):
            text = text.replace('&' + repr(index + 1), argument)

        return text