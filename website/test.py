import datetime
import smtplib
import ssl
import time

import pandas as pd
from sqlalchemy import and_

from __init__ import db

from .models import Note, Post, Search, User

result = db.query.join(Search).filter(Search.frequency=='daily')