from ..models import User, Task
from . import api

user = Task.query.filter_by(username="sea")
print(user.title)
