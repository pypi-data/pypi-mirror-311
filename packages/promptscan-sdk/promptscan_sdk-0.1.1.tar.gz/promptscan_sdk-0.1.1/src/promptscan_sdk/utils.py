from dateutil import parser


def serialize_datetime(v):
    return v.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_datetime(v):
    return parser.parse(v) if v else v
