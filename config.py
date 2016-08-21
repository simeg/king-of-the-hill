# -*- coding: utf-8 -*-
import os
from flask import Flask

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'app.db'),
    DEBUG=False,
    SECRET_KEY='4Sfdye27s&"{72qq',  # Randomized
    USERNAME='jo8/yhiu23@d!]',      # Randomized
    PASSWORD='9d]5aZtDS@k]/";/'     # Randomized
))
app.config.from_envvar('APP_SETTINGS', silent=True)
