#!/usr/bin/env python

#checking ability to ser env var from script

import os

os.environ["myvar1"]="holaa"
print "Var value="+os.getenv("VAR1")