from .extensions import db

class User(db.Model):
    # User login table, unseen by users
    id = db.Column(db.Integer, primary_key=True)
    publicId = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(35), unique=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    otp_token = db.Column(db.String(64))

class Platform(db.Model):
    # Partnered platforms available on SCC
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False, unique=True)

class Account(db.Model):
    # Linked accounts from partnered platforms
    userId = db.Column(db.String(64), ForeignKey('user.publicId'))
    username = db.Column(db.String(35), primary_key=True)
    platform = db.Column(db.String(35), ForeignKey('platform.name'), primary_key=True)

class Membership(db.Model):
    # Table with all available memberships
    name = db.Column(db.String(25), primary_key=True)
    price = db.Column(db.Float(precision=10)) # BTC Price
    can_exchange = db.Column(db.Bool)
    can_borrow = db.Column(db.Bool)
    can_lend = db.Column(db.Bool)
    exchange_small_fee = db.Column(db.Float)
    exchange_large_fee = db.Column(db.Float)
    exchange_limit = db.Column(db.Float)
    borrow_base_fee = db.Column(db.Float)
    borrow_daily_fee = db.Column(db.Float)
    borrow_grace_fee = db.Column(db.Float)
    minimum_interest = db.Column(db.Float)
    max_borrow_days = db.Column(db.Integer)
    max_grace_days = db.Column(db.Integer)
    grace_penalty = db.Column(db.Float)
    max_borrow_amount = db.Column(db.Float)
    lend_first_fee = db.Column(db.Float)
    lend_daily_fee = db.Column(db.Float)

class Profile(db.Model):
    # Table for user profile available publicly
    userId = db.Column(db.String(64), ForeignKey('user.publicId'), primary_key=True)
    banned = db.Column(db.Bool, default=False)
    exchange_ban_due = db.Column(db.DateTime)
    borrow_ban_due = db.Column(db.DateTime)
    lend_ban_due = db.Column(db.DateTime)
    xp = db.Column(db.Float, default=0.0)
    public_stats = db.Column(db.Bool, default=True)
    public_level = db.Column(db.Bool, default=True)
    public_xp = db.Column(db.Bool, default=True)
    public_name = db.Column(db.Bool, default=True)
    has_tfa = db.Column(db.Bool, default=False)

class Ignored(db.Model):
    # Table of users that have been ignored
    ignoredById = db.Column(db.String(64), ForeignKey('profile.userId'))
    ignoredId = db.Column(db.String(64), ForeignKey('profile.userId'))

class ProfileMembership(db.Model):
    # Table with memberships of all users
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(64), ForeignKey('profile.userId'), unique=True)
    membership = db.Column(db.String(25), ForeignKey('membership.name'))
    valid_until = db.Column(db.DateTime)
    paid_per_day = db.Column(db.Float)

class Currency(db.Model):
    # Table that displays all the currencies available on 
    # our website paired with the platform they can be used on
    name = db.Column(db.String(20), primary_key=True)
    platform = db.Column(db.String(35), ForeignKey('platform.name'), primary_key=True)

class BorrowStatus(db.Model):
    # Table with borrow statuses
    status = db.Column(db.String(64), primary_key=True)

class Borrow(db.Model):
    # Table with all borrow requests
    id = db.Column(db.Integer, primary_key=True)
    ref_id = db.Column(db.String(64))
    currency = db.Column(db.String(20), ForeignKey('currency.name'))
    amount = db.Column(db.Float(precision=10))
    paid = db.Column(db.Float(precision=10), default=0)
    by_id = db.Column(db.String(64), ForeignKey('profile.userId'))
    through_id = db.Column(db.String(64), ForeignKey('profile.userId'))
    interest = db.Column(db.Float)
    status = db.Column(db.String(64), ForeignKey('borrowstatus.status'))
    return_date = db.Column(db.DateTime)
    grace_date = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime)

class ExchangeStatus(db.Model):
    # Table with exchange statuses
    status = db.Column(db.String(64), primary_key=True)

class Exchange(db.Model):
    # Table with all exchange requests
    id = db.Column(db.Integer, primary_key=True)
    ref_id = db.Column(db.String(64))
    from_currency = db.Column(db.String(20), ForeignKey('currency.name'))
    from_amount = db.Column(db.Float(precision=10))
    to_currency = db.Column(db.String(20), ForeignKey('currency.name'))
    to_amount = db.Column(db.Float(precision=10))
    by_id = db.Column(db.String(64), ForeignKey('profile.userId'))
    through_id = db.Column(db.String(64), ForeignKey('profile.userId'))
    status = db.Column(db.String(64), ForeignKey('exchangestatus.status'))
    created_date = db.Column(db.DateTime)