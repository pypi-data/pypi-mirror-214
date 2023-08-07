class DataWiseError(Exception):
  def __init__(self, msg):
    self.msg = msg
    super().__init__(f"Error: {self.msg}")

class DataWiseInternalError(DataWiseError):
  """
  Raised when an internal error occurs
  """

class BadRequestError(DataWiseError):
  """
  Raised when a bad request happens
  """
  def __init__(self, error_msg=""):
    super().__init__(error_msg)

class AuthorizationError(DataWiseError):
  def __init__(self):
    super().__init__(f"Invalid authorization token.")

class TranslationError(DataWiseError):
  def __init__(self, error_msg=""):
    super().__init__(f"We couldn't translate your query. {error_msg}")