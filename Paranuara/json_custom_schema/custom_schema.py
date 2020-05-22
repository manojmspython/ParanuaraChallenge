SCHEMA = {'companies': {
    "type": "array",
    "items": [
        {
            "type": "object",
            "properties": {
                "index": {
                    "type": "integer"
                },
                "company": {
                    "type": "string"
                }
            },
            "required": [
                "index",
                "company"
            ]
        }
    ]
},
    'people': {
        "type": "array",
        "items": [
            {
                "type": "object",
                "properties": {
                    "_id": {
                        "type": "string"
                    },
                    "index": {
                        "type": "integer"
                    },
                    "guid": {
                        "type": "string"
                    },
                    "has_died": {
                        "type": "boolean"
                    },
                    "balance": {
                        "type": "string"
                    },
                    "picture": {
                        "type": "string"
                    },
                    "age": {
                        "type": "integer"
                    },
                    "eyeColor": {
                        "type": "string"
                    },
                    "name": {
                        "type": "string"
                    },
                    "gender": {
                        "type": "string"
                    },
                    "company_id": {
                        "type": "integer"
                    },
                    "email": {
                        "type": "string"
                    },
                    "phone": {
                        "type": "string"
                    },
                    "address": {
                        "type": "string"
                    },
                    "about": {
                        "type": "string"
                    },
                    "registered": {
                        "type": "string"
                    },
                    "tags": {
                        "type": "array",
                        "items": [
                            {
                                "type": "string"
                            },
                            {
                                "type": "string"
                            },
                            {
                                "type": "string"
                            },
                            {
                                "type": "string"
                            },
                            {
                                "type": "string"
                            },
                            {
                                "type": "string"
                            },
                            {
                                "type": "string"
                            }
                        ]
                    },
                    "friends": {
                        "type": "array",
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "index": {
                                        "type": "integer"
                                    }
                                },
                                "required": [
                                    "index"
                                ]
                            },
                            {
                                "type": "object",
                                "properties": {
                                    "index": {
                                        "type": "integer"
                                    }
                                },
                                "required": [
                                    "index"
                                ]
                            },
                            {
                                "type": "object",
                                "properties": {
                                    "index": {
                                        "type": "integer"
                                    }
                                },
                                "required": [
                                    "index"
                                ]
                            }
                        ]
                    },
                    "greeting": {
                        "type": "string"
                    },
                    "favouriteFood": {
                        "type": "array",
                        "items": [
                            {
                                "type": "string"
                            },
                            {
                                "type": "string"
                            },
                            {
                                "type": "string"
                            },
                            {
                                "type": "string"
                            }
                        ]
                    }
                },
                "required": [
                    "_id",
                    "index",
                    "guid",
                    "has_died",
                    "balance",
                    "picture",
                    "age",
                    "eyeColor",
                    "name",
                    "gender",
                    "company_id",
                    "email",
                    "phone",
                    "address",
                    "about",
                    "registered",
                    "tags",
                    "friends",
                    "greeting",
                    "favouriteFood"
                ]
            }
        ]
    }}
