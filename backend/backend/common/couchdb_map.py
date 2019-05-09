# -*- coding: utf-8 -*-


def STATISTICS_TIME_MANGO(start_time=None, end_time=None, porn=None, food=None):
    mango = {
        'selector': {
            'date': {
                '$gt': start_time,
                '$lt': end_time
            },
            '$or': [
                {
                    'tags': {

                    }
                }
            ]
        }
    }


    mango = {
        'selector': {
            '$or': [{
                '$and': [
                    {
                        'tags': {
                            '$ne': {}
                        }
                    },
                    {
                        'tags': {
                            'netural'
                        }
                    }
                ],
                'tags': {
                    '$ne': {}
                }}, {
                'geo': {
                    '$ne': []
            }}]
        },
        'fields': ['_id', 'text', 'tags'],
        'limit': 100,
        'use_index': 'json:date-index'
    }
    if start_time or end_time:
        mango['selector'].update({'date': {}})
    if start_time:
        mango['selector']['date'].update({'$gt': start_time})
    if end_time:
        mango['selector']['date'].update({'$lt': end_time})
    if porn or food:
        mango['selector'].update('tags')


def statistics_track_random(start_time=None, end_time=None, user_id=None, limit=10000, skip=0):
    mango = {
        'selector': {
            'geo': {
                '$ne': []
            }
        },
        'use_index': 'json:geo-index',
        'limit': limit,
        'skip': skip
    }

    if start_time or end_time:
        mango['selector'].update(dict(date={}))
        mango['selector']['date'].update({'$gte': start_time}) if start_time else None
        mango['selector']['date'].update({'$lte': end_time}) if end_time else None
        mango.update(dict(use_index='json:date-index'))
    if user_id:
        mango['selector'].update(dict(user=user_id))
        mango.update(dict(use_index='json:user-date-index'))

    return mango


STATISTICS = {
    "_id": "_design/statistics",
    "views": {
        "time_geo_all_tags": {
            "map": "function (doc) {\n  if ((doc.time) && (doc.geo.length != 0) && (doc.tags.length != 0)) {\n    emit(doc.date, {\"_id\": doc._id, \"text\": doc.text, \"user\": doc.user, \"geo\": doc.geo, \"date\": doc.date, \"img_id\": doc.img_id, \"tags\": doc.tags});\n  }\n}"
        },
        "user_geo": {
            "map": "function (doc) {\n  if (doc.geo.length != 0) {\n    emit(doc.user, {\"_id\": doc.id, \"text\": doc.text, \"user\": doc.user, \"tags\": doc.tags, \"date\": doc.date});\n  }\n}"
        },
        "zone_tags": {
            "reduce": "_sum",
            "map": "function (doc) {\n  var ignore = [\"neutral\", \"sexy\", \"drawings\", \"nonfood\"];\n  if (doc.zone && doc.tags.length != 0) {\n    for (var tag in doc.tags) {\n      if (tag == \"text\") {\n        for (var _tag in doc.tags[tag]) {\n          if ((_tag == \"sentiment\") && !(doc.tags[tag][_tag] in ignore)) {\n            emit([doc.zone, tag, doc.tags[tag][_tag], doc.date], 1);\n          }\n          if (!(_tag in ignore) && (doc.tags[tag][_tag] > 0)) {\n            emit([doc.zone, tag, _tag, doc.date], 1);\n          }\n        }\n      } else {\n        for (var _tag in doc.tags[tag]) {\n          if (!(_tag in ignore) && (doc.tags[tag][_tag] > 0.9)) {\n            emit([doc.zone, tag, _tag, doc.date], 1);\n          }\n        }\n      }\n    }\n  }\n}"
        },
        "machine_result": {
            "reduce": "_sum",
            "map": "function (doc) {\n  var ignore = [\"neutral\", \"sexy\", \"drawings\", \"nonfood\"]\n  if (doc.tags[\"nsfw\"]) {\n    for (var tags in doc.tags[\"nsfw\"]) {\n      if ((!tags in ignore) && (doc.tags[\"nsfw\"][tags] > 0.9)) {\n        emit(tags, 1);\n      }\n    }\n    for (var tags in doc.tags[\"food179\"]) {\n      if ((!tags in ignore) && (doc.tags[\"food179\"][tags] > 0.9)) {\n        emit(tags, 1);\n      }\n    }\n  }\n}"
        }
    },
    "language": "javascript"
}


UNLEARNING = {
  "_id": "_design/unlearning",
  "views": {
    "machine": {
      "map": "function (doc) {\n  if ((doc.img_id.length != 0) && (doc.process == 0)) {\n    emit(doc._id, {\"_id\": doc._id, \"_rev\": doc._rev, \"img_id\": doc.img_id});\n  }\n}"
    },
    "text": {
      "map": "function (doc) {\n  if (doc.process_text == 0) {\n    emit(doc._id, {\"_id\": doc._id, \"_rev\": doc._rev, \"text\": doc.text});\n  }\n}"
    },
    "zone": {
      "map": "function (doc) {\n  if (!doc.zone) {\n    emit(doc._id, {\"_id\": doc._id, \"_rev\": doc._rev, \"geo\": doc.geo});\n  }\n}"
    }
  },
  "language": "javascript"
}
