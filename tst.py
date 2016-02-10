#!/usr/bin/env python
import os
import time
from datetime import datetime,timedelta
import pickle
import commands
import json
import sys
import sslib
import copy


(status, output) = commands.getstatusoutput('kill '+'14483')
print status
print output