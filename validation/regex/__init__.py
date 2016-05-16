from gronexctl.validation import Base, ExceptionBase

class Regex(Base):

    def __init__(self, re_string, *args, **kwargs):
        import re

        self.string = re_string
        self.regex = re.compile(self.string)
        super(self.__class__, self).__init__(*args, **kwargs)


    def check(self, target):
        if not self.regex.match(target):
            raise RegexException(target, self.string)


class RegexException(ExceptionBase):
    def __init__(self, target, regex_str):
        super(self.__class__, self).__init__(
            'Regular expression match failed for: {0}, should match: {1}'
                .format(target, regex_str)
        )

addon_name = Regex('^[a-zA-Z0-9_]+$')
module_set_id = Regex('^[a-z0-9_]+$')
module_set_name = Regex('^[a-zA-Z0-9-_ ./]+$')
module_set_description = Regex('^[a-zA-Z0-9-_ ,./]+$')
