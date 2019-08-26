from string import (ascii_letters, digits)


class Sanitation:

    @staticmethod
    def string(text):
        allowed_characters = ascii_letters + digits + '-_.'

        text = str(text)
        new_text = []

        for character in text:
            if character in allowed_characters:
                new_text.append(character)
            else:
                new_text.append('_')

        return ''.join(new_text)

    @staticmethod
    def dedup(object):
        """
        deduplicate object
        """
        new_list = []
        for item in object:
            if item not in new_list:
                new_list.append(item)

        return new_list
