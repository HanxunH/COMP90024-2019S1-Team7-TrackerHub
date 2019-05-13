# -*- coding: utf-8 -*-
"""
@Author: Lihuan Zhang

This file including the two design document for couchdb used for learning and statistics
"""


STATISTICS = {
    "_id": "_design/statistics",
    "views": {
        "time_geo_all_tags": {
            "map": "function (doc) {\n  var ignore = [\"\", \"neutral\", \"sexy\", \"drawings\", \"non_food\"];\n  \n  if ((doc.date) && (doc.geo.length != 0) && (doc.tags.length != 0)) {\n    var result = new Array();\n    for (var tag in doc.tags) {\n      if (tag == \"text\") {\n        for (var _tag in doc.tags[tag]) {\n          if ((_tag == \"sentiment\") && !(doc.tags[tag][_tag] in ignore)) {\n            result.push(doc.tags[tag][_tag]);\n          }\n          if (!(ignore.indexOf(_tag) > 0) && (doc.tags[tag][_tag] > 0)) {\n            result.push(\"text.\" + _tag);\n          }\n        }\n      } else {\n        for (var _tag in doc.tags[tag]) {\n          if (!(ignore.indexOf(_tag) > 0) && (doc.tags[tag][_tag] > 0.9)) {\n            result.push(_tag);\n          }\n        }\n      }\n    }\n    emit(doc.date, {\"_id\": doc._id, \"text\": doc.text, \"user\": doc.user, \"geo\": doc.geo, \"date\": doc.date, \"img_id\": doc.img_id, \"tags\": result});\n  }\n}"
        },
        "user_geo": {
            "map": "function (doc) {\n  var ignore = [\"\", \"neutral\", \"sexy\", \"drawings\", \"non_food\"];\n  \n  if (doc.geo.length != 0) {\n    var result = new Array();\n    for (var tag in doc.tags) {\n      if (tag == \"text\") {\n        for (var _tag in doc.tags[tag]) {\n          if ((_tag == \"sentiment\") && !(doc.tags[tag][_tag] in ignore)) {\n            result.push(doc.tags[tag][_tag]);\n          }\n          if (!(ignore.indexOf(_tag) > 0) && (doc.tags[tag][_tag] > 0)) {\n            result.push(\"text.\" + _tag);\n          }\n        }\n      } else {\n        for (var _tag in doc.tags[tag]) {\n          if (!(ignore.indexOf(_tag) > 0) && (doc.tags[tag][_tag] > 0.9)) {\n            result.push(_tag);\n          }\n        }\n      }\n    }\n    emit(doc.user, {\"_id\": doc.id, \"text\": doc.text, \"user\": doc.user, \"tags\": result, \"date\": doc.date, \"geo\": doc.geo, \"img_id\": doc.img_id});\n  }\n}"
        },
        "zone_tags": {
            "reduce": "_sum",
            "map": "function (doc) {\n  if (doc.zone && doc.tags.length != 0) {\n    for (var tag in doc.tags) {\n      if (tag == \"text\") {\n        for (var _tag in doc.tags[tag]) {\n          if (_tag == \"sentiment\") {\n            emit([doc.zone, tag, \"sentiment.\" + doc.tags[tag][_tag], doc.date], 1);\n          }\n          if (doc.tags[tag][_tag] > 0) {\n            emit([doc.zone, tag, \"text.\" + _tag, doc.date], 1);\n          }\n        }\n      } else {\n        for (var _tag in doc.tags[tag]) {\n          if (doc.tags[tag][_tag] > 0.9) {\n            emit([doc.zone, tag, _tag, doc.date], 1);\n          }\n        }\n      }\n    }\n  }\n}"
        },
        "machine_result": {
            "reduce": "_sum",
            "map": "function (doc) {\n  if (doc.tags[\"nsfw\"]) {\n    for (var tags in doc.tags[\"nsfw\"]) {\n      if (doc.tags[\"nsfw\"][tags] > 0.9) {\n        emit(tags, 1);\n      }\n    }\n    for (var tags in doc.tags[\"food179\"]) {\n      if (doc.tags[\"food179\"][tags] > 0.9) {\n        emit(tags, 1);\n      }\n    }\n  }\n}"
        },
        "vic_zone_tags": {
            "reduce": "_sum",
            "map": "function (doc) {\n  if (doc.vic_zone && doc.tags.length != 0) {\n    for (var tag in doc.tags) {\n      if (tag == \"text\") {\n        for (var _tag in doc.tags[tag]) {\n          if (_tag == \"sentiment\") {\n            emit([doc.vic_zone, tag, \"sentiment.\" + doc.tags[tag][_tag], doc.date], 1);\n          }\n          if (doc.tags[tag][_tag] > 0) {\n            emit([doc.vic_zone, tag, \"text.\" + _tag, doc.date], 1);\n          }\n        }\n      } else {\n        for (var _tag in doc.tags[tag]) {\n          if (doc.tags[tag][_tag] > 0.9) {\n            emit([doc.vic_zone, tag, _tag, doc.date], 1);\n          }\n        }\n      }\n    }\n  }\n}"
        },
        "text_result": {
            "reduce": "_sum",
            "map": "function (doc) {\n  if (doc.tags[\"text\"]) {\n    for (var tags in doc.tags[\"text\"]) {\n      if (tags == \"sentiment\") {\n        emit(doc.tags[\"text\"][tags], 1)\n      } else if (doc.tags[\"text\"][tags] > 0.9) {\n        emit(tags, 1);\n      }\n    }\n  }\n}"
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
        },
        "vic_zone": {
            "map": "function (doc) {\n  if (!doc.vic_zone) {\n    emit(doc._id, {\"_id\": doc._id, \"_rev\": doc._rev, \"geo\": doc.geo});\n  }\n}"
        }
    },
    "language": "javascript"
}
