class Message:
    """
    Message is a unit of work in liten
    """
    code = 'code'
    markdown = 'markdown'
    def __init__(self):
        """
        Create and initialize works
        """
        self._type= None
        self._user = []
        self._assistant = []

    @property
    def type(self):
        """ type of message - code, markdown """
        return self._type
    
    @type.setter
    def type(self, value):
        self._type = value

    @property
    def user(self):
        """ user message text """
        return self._user
    
    @user.setter
    def user(self, value):
        self._user = value

    def add_user(self, msg):
        """ Add msg to user message array """
        self._user.append(msg)

    @property
    def assistant(self):
        """ assistant message text """
        return self._assistant
    
    @assistant.setter
    def assistant(self, value):
        self._assistant = value

    def add_assistant(self, msg):
        """ Add msg to assistant message array """
        self._assistant.append(msg)

    def to_str(self):
        str_val=f"type:{self._type},user:{self._user},assistant:{self._assistant}"
        return str_val
        
    
    
