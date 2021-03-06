import re, uuid, random
import os
# Time checkers
from datetime import datetime
import time

# Requests, Generate Password and Check Password
from flask import Blueprint, jsonify, request

# Models and database
from ..extensions import db
from ..models import User, Membership, Profile, ProfileMembership
    
exchange_routes = Blueprint('exchange_routes', __name__)