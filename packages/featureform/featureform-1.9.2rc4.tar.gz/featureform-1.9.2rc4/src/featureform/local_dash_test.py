import pytest
import os
from .cli import app
import json
import shutil
import stat

features = [
    {
        "all-variants": ["quickstart"],
        "type": "Feature",
        "default-variant": "quickstart",
        "name": "avg_transactions",
        "variants": {
            "quickstart": {
                "description": "",
                "entity": "user",
                "name": "avg_transactions",
                "owner": "default_user",
                "provider": "local-mode",
                "data-type": "float32",
                "variant": "quickstart",
                "status": "ready",
                "location": {
                    "entity": "CustomerID",
                    "value": "TransactionAmount",
                    "timestamp": "",
                },
                "source": {"Name": "average_user_transaction", "Variant": "quickstart"},
                "tags": [],
                "properties": {},
            }
        },
    }
]
labels = [
    {
        "all-variants": ["quickstart"],
        "type": "Label",
        "default-variant": "quickstart",
        "name": "fraudulent",
        "variants": {
            "quickstart": {
                "description": "",
                "entity": "user",
                "data-type": "bool",
                "name": "fraudulent",
                "owner": "default_user",
                "provider": "",
                "variant": "quickstart",
                "status": "ready",
                "location": {
                    "entity": "CustomerID",
                    "value": "IsFraud",
                    "timestamp": "",
                },
                "source": {"Name": "transactions", "Variant": "quickstart"},
                "trainingSets": {
                    "fraud_training": [
                        {
                            "description": "",
                            "name": "fraud_training",
                            "owner": "default_user",
                            "variant": "quickstart",
                            "status": "ready",
                            "label": {"Name": "fraudulent", "Variant": "quickstart"},
                            "features": {
                                "avg_transactions": [
                                    {
                                        "description": "",
                                        "entity": "user",
                                        "name": "avg_transactions",
                                        "owner": "default_user",
                                        "provider": "local-mode",
                                        "data-type": "float32",
                                        "variant": "quickstart",
                                        "status": "ready",
                                        "location": {
                                            "entity": "CustomerID",
                                            "value": "TransactionAmount",
                                            "timestamp": "",
                                        },
                                        "source": {
                                            "Name": "average_user_transaction",
                                            "Variant": "quickstart",
                                        },
                                        "tags": [],
                                        "properties": {},
                                    }
                                ]
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "tags": [],
                "properties": {},
            }
        },
    }
]
sources = [
    {
        "all-variants": ["transactions"],
        "type": "Source",
        "default-variant": "quickstart",
        "name": "transactions",
        "variants": {
            "quickstart": {
                "description": "A dataset of fraudulent transactions",
                "name": "transactions",
                "source-type": "Source",
                "owner": "default_user",
                "provider": "local-mode",
                "variant": "quickstart",
                "status": "ready",
                "labels": {
                    "fraudulent": [
                        {
                            "description": "",
                            "entity": "user",
                            "data-type": "bool",
                            "name": "fraudulent",
                            "owner": "default_user",
                            "provider": "",
                            "variant": "quickstart",
                            "status": "ready",
                            "location": {
                                "entity": "CustomerID",
                                "value": "IsFraud",
                                "timestamp": "",
                            },
                            "source": {"Name": "transactions", "Variant": "quickstart"},
                            "trainingSets": {
                                "fraud_training": [
                                    {
                                        "description": "",
                                        "name": "fraud_training",
                                        "owner": "default_user",
                                        "variant": "quickstart",
                                        "status": "ready",
                                        "label": {
                                            "Name": "fraudulent",
                                            "Variant": "quickstart",
                                        },
                                        "features": {
                                            "avg_transactions": [
                                                {
                                                    "description": "",
                                                    "entity": "user",
                                                    "name": "avg_transactions",
                                                    "owner": "default_user",
                                                    "provider": "local-mode",
                                                    "data-type": "float32",
                                                    "variant": "quickstart",
                                                    "status": "ready",
                                                    "location": {
                                                        "entity": "CustomerID",
                                                        "value": "TransactionAmount",
                                                        "timestamp": "",
                                                    },
                                                    "source": {
                                                        "Name": "average_user_transaction",
                                                        "Variant": "quickstart",
                                                    },
                                                    "tags": [],
                                                    "properties": {},
                                                }
                                            ]
                                        },
                                        "tags": [],
                                        "properties": {},
                                    }
                                ]
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "features": {},
                "training-sets": {
                    "fraud_training": [
                        {
                            "description": "",
                            "name": "fraud_training",
                            "owner": "default_user",
                            "variant": "quickstart",
                            "status": "ready",
                            "label": {"Name": "fraudulent", "Variant": "quickstart"},
                            "features": {
                                "avg_transactions": [
                                    {
                                        "description": "",
                                        "entity": "user",
                                        "name": "avg_transactions",
                                        "owner": "default_user",
                                        "provider": "local-mode",
                                        "data-type": "float32",
                                        "variant": "quickstart",
                                        "status": "ready",
                                        "location": {
                                            "entity": "CustomerID",
                                            "value": "TransactionAmount",
                                            "timestamp": "",
                                        },
                                        "source": {
                                            "Name": "average_user_transaction",
                                            "Variant": "quickstart",
                                        },
                                        "tags": [],
                                        "properties": {},
                                    }
                                ]
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "tags": [],
                "properties": {},
            }
        },
    },
    {
        "all-variants": ["average_user_transaction"],
        "type": "Source",
        "default-variant": "quickstart",
        "name": "average_user_transaction",
        "variants": {
            "quickstart": {
                "description": "the average transaction amount for a user",
                "name": "average_user_transaction",
                "source-type": "Source",
                "owner": "default_user",
                "provider": "local-mode",
                "variant": "quickstart",
                "status": "ready",
                "labels": {},
                "features": {
                    "avg_transactions": [
                        {
                            "description": "",
                            "entity": "user",
                            "name": "avg_transactions",
                            "owner": "default_user",
                            "provider": "local-mode",
                            "data-type": "float32",
                            "variant": "quickstart",
                            "status": "ready",
                            "location": {
                                "entity": "CustomerID",
                                "value": "TransactionAmount",
                                "timestamp": "",
                            },
                            "source": {
                                "Name": "average_user_transaction",
                                "Variant": "quickstart",
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "training-sets": {
                    "fraud_training": [
                        {
                            "description": "",
                            "name": "fraud_training",
                            "owner": "default_user",
                            "variant": "quickstart",
                            "status": "ready",
                            "label": {"Name": "fraudulent", "Variant": "quickstart"},
                            "features": {
                                "avg_transactions": [
                                    {
                                        "description": "",
                                        "entity": "user",
                                        "name": "avg_transactions",
                                        "owner": "default_user",
                                        "provider": "local-mode",
                                        "data-type": "float32",
                                        "variant": "quickstart",
                                        "status": "ready",
                                        "location": {
                                            "entity": "CustomerID",
                                            "value": "TransactionAmount",
                                            "timestamp": "",
                                        },
                                        "source": {
                                            "Name": "average_user_transaction",
                                            "Variant": "quickstart",
                                        },
                                        "tags": [],
                                        "properties": {},
                                    }
                                ]
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "tags": [],
                "properties": {},
            }
        },
    },
]
training_sets = [
    {
        "all-variants": ["quickstart"],
        "type": "TrainingSet",
        "default-variant": "quickstart",
        "name": "fraud_training",
        "variants": {
            "quickstart": {
                "description": "",
                "name": "fraud_training",
                "owner": "default_user",
                "variant": "quickstart",
                "status": "ready",
                "label": {"Name": "fraudulent", "Variant": "quickstart"},
                "features": {
                    "avg_transactions": [
                        {
                            "description": "",
                            "entity": "user",
                            "name": "avg_transactions",
                            "owner": "default_user",
                            "provider": "local-mode",
                            "data-type": "float32",
                            "variant": "quickstart",
                            "status": "ready",
                            "location": {
                                "entity": "CustomerID",
                                "value": "TransactionAmount",
                                "timestamp": "",
                            },
                            "source": {
                                "Name": "average_user_transaction",
                                "Variant": "quickstart",
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "tags": [],
                "properties": {},
            }
        },
    }
]
entities = [
    {
        "description": "",
        "type": "Entity",
        "name": "user",
        "features": {
            "avg_transactions": [
                {
                    "description": "",
                    "entity": "user",
                    "name": "avg_transactions",
                    "owner": "default_user",
                    "provider": "local-mode",
                    "data-type": "float32",
                    "variant": "quickstart",
                    "status": "ready",
                    "location": {
                        "entity": "CustomerID",
                        "value": "TransactionAmount",
                        "timestamp": "",
                    },
                    "source": {
                        "Name": "average_user_transaction",
                        "Variant": "quickstart",
                    },
                    "tags": [],
                    "properties": {},
                }
            ]
        },
        "labels": {
            "fraudulent": [
                {
                    "description": "",
                    "entity": "user",
                    "data-type": "bool",
                    "name": "fraudulent",
                    "owner": "default_user",
                    "provider": "",
                    "variant": "quickstart",
                    "status": "ready",
                    "location": {
                        "entity": "CustomerID",
                        "value": "IsFraud",
                        "timestamp": "",
                    },
                    "source": {"Name": "transactions", "Variant": "quickstart"},
                    "trainingSets": {
                        "fraud_training": [
                            {
                                "description": "",
                                "name": "fraud_training",
                                "owner": "default_user",
                                "variant": "quickstart",
                                "status": "ready",
                                "label": {
                                    "Name": "fraudulent",
                                    "Variant": "quickstart",
                                },
                                "features": {
                                    "avg_transactions": [
                                        {
                                            "description": "",
                                            "entity": "user",
                                            "name": "avg_transactions",
                                            "owner": "default_user",
                                            "provider": "local-mode",
                                            "data-type": "float32",
                                            "variant": "quickstart",
                                            "status": "ready",
                                            "location": {
                                                "entity": "CustomerID",
                                                "value": "TransactionAmount",
                                                "timestamp": "",
                                            },
                                            "source": {
                                                "Name": "average_user_transaction",
                                                "Variant": "quickstart",
                                            },
                                            "tags": [],
                                            "properties": {},
                                        }
                                    ]
                                },
                                "tags": [],
                                "properties": {},
                            }
                        ]
                    },
                    "tags": [],
                    "properties": {},
                }
            ]
        },
        "training-sets": {
            "fraud_training": [
                {
                    "description": "",
                    "name": "fraud_training",
                    "owner": "default_user",
                    "variant": "quickstart",
                    "status": "ready",
                    "label": {"Name": "fraudulent", "Variant": "quickstart"},
                    "features": {
                        "avg_transactions": [
                            {
                                "description": "",
                                "entity": "user",
                                "name": "avg_transactions",
                                "owner": "default_user",
                                "provider": "local-mode",
                                "data-type": "float32",
                                "variant": "quickstart",
                                "status": "ready",
                                "location": {
                                    "entity": "CustomerID",
                                    "value": "TransactionAmount",
                                    "timestamp": "",
                                },
                                "source": {
                                    "Name": "average_user_transaction",
                                    "Variant": "quickstart",
                                },
                                "tags": [],
                                "properties": {},
                            }
                        ]
                    },
                    "tags": [],
                    "properties": {},
                }
            ]
        },
        "status": "ready",
        "tags": [],
        "properties": {},
    }
]
models = []
users = [
    {
        "name": "default_user",
        "type": "User",
        "features": {
            "avg_transactions": [
                {
                    "description": "",
                    "entity": "user",
                    "name": "avg_transactions",
                    "owner": "default_user",
                    "provider": "local-mode",
                    "data-type": "float32",
                    "variant": "quickstart",
                    "status": "ready",
                    "location": {
                        "entity": "CustomerID",
                        "value": "TransactionAmount",
                        "timestamp": "",
                    },
                    "source": {
                        "Name": "average_user_transaction",
                        "Variant": "quickstart",
                    },
                    "tags": [],
                    "properties": {},
                }
            ]
        },
        "labels": {
            "fraudulent": [
                {
                    "description": "",
                    "entity": "user",
                    "data-type": "bool",
                    "name": "fraudulent",
                    "owner": "default_user",
                    "provider": "",
                    "variant": "quickstart",
                    "status": "ready",
                    "location": {
                        "entity": "CustomerID",
                        "value": "IsFraud",
                        "timestamp": "",
                    },
                    "source": {"Name": "transactions", "Variant": "quickstart"},
                    "trainingSets": {
                        "fraud_training": [
                            {
                                "description": "",
                                "name": "fraud_training",
                                "owner": "default_user",
                                "variant": "quickstart",
                                "status": "ready",
                                "label": {
                                    "Name": "fraudulent",
                                    "Variant": "quickstart",
                                },
                                "features": {
                                    "avg_transactions": [
                                        {
                                            "description": "",
                                            "entity": "user",
                                            "name": "avg_transactions",
                                            "owner": "default_user",
                                            "provider": "local-mode",
                                            "data-type": "float32",
                                            "variant": "quickstart",
                                            "status": "ready",
                                            "location": {
                                                "entity": "CustomerID",
                                                "value": "TransactionAmount",
                                                "timestamp": "",
                                            },
                                            "source": {
                                                "Name": "average_user_transaction",
                                                "Variant": "quickstart",
                                            },
                                            "tags": [],
                                            "properties": {},
                                        }
                                    ]
                                },
                                "tags": [],
                                "properties": {},
                            }
                        ]
                    },
                    "tags": [],
                    "properties": {},
                }
            ]
        },
        "training-sets": {
            "fraud_training": [
                {
                    "description": "",
                    "name": "fraud_training",
                    "owner": "default_user",
                    "variant": "quickstart",
                    "status": "ready",
                    "label": {"Name": "fraudulent", "Variant": "quickstart"},
                    "features": {
                        "avg_transactions": [
                            {
                                "description": "",
                                "entity": "user",
                                "name": "avg_transactions",
                                "owner": "default_user",
                                "provider": "local-mode",
                                "data-type": "float32",
                                "variant": "quickstart",
                                "status": "ready",
                                "location": {
                                    "entity": "CustomerID",
                                    "value": "TransactionAmount",
                                    "timestamp": "",
                                },
                                "source": {
                                    "Name": "average_user_transaction",
                                    "Variant": "quickstart",
                                },
                                "tags": [],
                                "properties": {},
                            }
                        ]
                    },
                    "tags": [],
                    "properties": {},
                }
            ]
        },
        "sources": {
            "transactions": [
                {
                    "description": "A dataset of fraudulent transactions",
                    "name": "transactions",
                    "source-type": "Source",
                    "owner": "default_user",
                    "provider": "local-mode",
                    "variant": "quickstart",
                    "status": "ready",
                    "labels": {
                        "fraudulent": [
                            {
                                "description": "",
                                "entity": "user",
                                "data-type": "bool",
                                "name": "fraudulent",
                                "owner": "default_user",
                                "provider": "",
                                "variant": "quickstart",
                                "status": "ready",
                                "location": {
                                    "entity": "CustomerID",
                                    "value": "IsFraud",
                                    "timestamp": "",
                                },
                                "source": {
                                    "Name": "transactions",
                                    "Variant": "quickstart",
                                },
                                "trainingSets": {
                                    "fraud_training": [
                                        {
                                            "description": "",
                                            "name": "fraud_training",
                                            "owner": "default_user",
                                            "variant": "quickstart",
                                            "status": "ready",
                                            "label": {
                                                "Name": "fraudulent",
                                                "Variant": "quickstart",
                                            },
                                            "features": {
                                                "avg_transactions": [
                                                    {
                                                        "description": "",
                                                        "entity": "user",
                                                        "name": "avg_transactions",
                                                        "owner": "default_user",
                                                        "provider": "local-mode",
                                                        "data-type": "float32",
                                                        "variant": "quickstart",
                                                        "status": "ready",
                                                        "location": {
                                                            "entity": "CustomerID",
                                                            "value": "TransactionAmount",
                                                            "timestamp": "",
                                                        },
                                                        "source": {
                                                            "Name": "average_user_transaction",
                                                            "Variant": "quickstart",
                                                        },
                                                    }
                                                ]
                                            },
                                        }
                                    ]
                                },
                            }
                        ]
                    },
                    "features": {},
                    "training-sets": {
                        "fraud_training": [
                            {
                                "description": "",
                                "name": "fraud_training",
                                "owner": "default_user",
                                "variant": "quickstart",
                                "status": "ready",
                                "label": {
                                    "Name": "fraudulent",
                                    "Variant": "quickstart",
                                },
                                "features": {
                                    "avg_transactions": [
                                        {
                                            "description": "",
                                            "entity": "user",
                                            "name": "avg_transactions",
                                            "owner": "default_user",
                                            "provider": "local-mode",
                                            "data-type": "float32",
                                            "variant": "quickstart",
                                            "status": "ready",
                                            "location": {
                                                "entity": "CustomerID",
                                                "value": "TransactionAmount",
                                                "timestamp": "",
                                            },
                                            "source": {
                                                "Name": "average_user_transaction",
                                                "Variant": "quickstart",
                                            },
                                        }
                                    ]
                                },
                            }
                        ]
                    },
                }
            ],
            "average_user_transaction": [
                {
                    "description": "the average transaction amount for a user",
                    "name": "average_user_transaction",
                    "source-type": "Source",
                    "owner": "default_user",
                    "provider": "local-mode",
                    "variant": "quickstart",
                    "status": "ready",
                    "labels": {},
                    "features": {
                        "avg_transactions": [
                            {
                                "description": "",
                                "entity": "user",
                                "name": "avg_transactions",
                                "owner": "default_user",
                                "provider": "local-mode",
                                "data-type": "float32",
                                "variant": "quickstart",
                                "status": "ready",
                                "location": {
                                    "entity": "CustomerID",
                                    "value": "TransactionAmount",
                                    "timestamp": "",
                                },
                                "source": {
                                    "Name": "average_user_transaction",
                                    "Variant": "quickstart",
                                },
                            }
                        ]
                    },
                    "training-sets": {
                        "fraud_training": [
                            {
                                "description": "",
                                "name": "fraud_training",
                                "owner": "default_user",
                                "variant": "quickstart",
                                "status": "ready",
                                "label": {
                                    "Name": "fraudulent",
                                    "Variant": "quickstart",
                                },
                                "features": {
                                    "avg_transactions": [
                                        {
                                            "description": "",
                                            "entity": "user",
                                            "name": "avg_transactions",
                                            "owner": "default_user",
                                            "provider": "local-mode",
                                            "data-type": "float32",
                                            "variant": "quickstart",
                                            "status": "ready",
                                            "location": {
                                                "entity": "CustomerID",
                                                "value": "TransactionAmount",
                                                "timestamp": "",
                                            },
                                            "source": {
                                                "Name": "average_user_transaction",
                                                "Variant": "quickstart",
                                            },
                                        }
                                    ]
                                },
                            }
                        ]
                    },
                }
            ],
        },
        "status": "ready",
        "tags": [],
        "properties": {},
    }
]
providers = [
    {
        "name": "local-mode",
        "type": "Provider",
        "description": "This is local mode",
        "provider-type": "LOCAL_ONLINE",
        "software": "localmode",
        "team": "team",
        "sources": {
            "transactions": [
                {
                    "description": "A dataset of fraudulent transactions",
                    "name": "transactions",
                    "source-type": "Source",
                    "owner": "default_user",
                    "provider": "local-mode",
                    "variant": "quickstart",
                    "status": "ready",
                    "labels": {
                        "fraudulent": [
                            {
                                "description": "",
                                "entity": "user",
                                "data-type": "bool",
                                "name": "fraudulent",
                                "owner": "default_user",
                                "provider": "",
                                "variant": "quickstart",
                                "status": "ready",
                                "location": {
                                    "entity": "CustomerID",
                                    "value": "IsFraud",
                                    "timestamp": "",
                                },
                                "source": {
                                    "Name": "transactions",
                                    "Variant": "quickstart",
                                },
                                "trainingSets": {
                                    "fraud_training": [
                                        {
                                            "description": "",
                                            "name": "fraud_training",
                                            "owner": "default_user",
                                            "variant": "quickstart",
                                            "status": "ready",
                                            "label": {
                                                "Name": "fraudulent",
                                                "Variant": "quickstart",
                                            },
                                            "features": {
                                                "avg_transactions": [
                                                    {
                                                        "description": "",
                                                        "entity": "user",
                                                        "name": "avg_transactions",
                                                        "owner": "default_user",
                                                        "provider": "local-mode",
                                                        "data-type": "float32",
                                                        "variant": "quickstart",
                                                        "status": "ready",
                                                        "location": {
                                                            "entity": "CustomerID",
                                                            "value": "TransactionAmount",
                                                            "timestamp": "",
                                                        },
                                                        "source": {
                                                            "Name": "average_user_transaction",
                                                            "Variant": "quickstart",
                                                        },
                                                        "tags": [],
                                                        "properties": {},
                                                    }
                                                ]
                                            },
                                            "tags": [],
                                            "properties": {},
                                        }
                                    ]
                                },
                                "tags": [],
                                "properties": {},
                            }
                        ]
                    },
                    "features": {},
                    "training-sets": {
                        "fraud_training": [
                            {
                                "description": "",
                                "name": "fraud_training",
                                "owner": "default_user",
                                "variant": "quickstart",
                                "status": "ready",
                                "label": {
                                    "Name": "fraudulent",
                                    "Variant": "quickstart",
                                },
                                "features": {
                                    "avg_transactions": [
                                        {
                                            "description": "",
                                            "entity": "user",
                                            "name": "avg_transactions",
                                            "owner": "default_user",
                                            "provider": "local-mode",
                                            "data-type": "float32",
                                            "variant": "quickstart",
                                            "status": "ready",
                                            "location": {
                                                "entity": "CustomerID",
                                                "value": "TransactionAmount",
                                                "timestamp": "",
                                            },
                                            "source": {
                                                "Name": "average_user_transaction",
                                                "Variant": "quickstart",
                                            },
                                            "tags": [],
                                            "properties": {},
                                        }
                                    ]
                                },
                                "tags": [],
                                "properties": {},
                            }
                        ]
                    },
                    "tags": [],
                    "properties": {},
                }
            ],
            "average_user_transaction": [
                {
                    "description": "the average transaction amount for a user",
                    "name": "average_user_transaction",
                    "source-type": "Source",
                    "owner": "default_user",
                    "provider": "local-mode",
                    "variant": "quickstart",
                    "status": "ready",
                    "labels": {},
                    "features": {
                        "avg_transactions": [
                            {
                                "description": "",
                                "entity": "user",
                                "name": "avg_transactions",
                                "owner": "default_user",
                                "provider": "local-mode",
                                "data-type": "float32",
                                "variant": "quickstart",
                                "status": "ready",
                                "location": {
                                    "entity": "CustomerID",
                                    "value": "TransactionAmount",
                                    "timestamp": "",
                                },
                                "source": {
                                    "Name": "average_user_transaction",
                                    "Variant": "quickstart",
                                },
                                "tags": [],
                                "properties": {},
                            }
                        ]
                    },
                    "training-sets": {
                        "fraud_training": [
                            {
                                "description": "",
                                "name": "fraud_training",
                                "owner": "default_user",
                                "variant": "quickstart",
                                "status": "ready",
                                "label": {
                                    "Name": "fraudulent",
                                    "Variant": "quickstart",
                                },
                                "features": {
                                    "avg_transactions": [
                                        {
                                            "description": "",
                                            "entity": "user",
                                            "name": "avg_transactions",
                                            "owner": "default_user",
                                            "provider": "local-mode",
                                            "data-type": "float32",
                                            "variant": "quickstart",
                                            "status": "ready",
                                            "location": {
                                                "entity": "CustomerID",
                                                "value": "TransactionAmount",
                                                "timestamp": "",
                                            },
                                            "source": {
                                                "Name": "average_user_transaction",
                                                "Variant": "quickstart",
                                            },
                                            "tags": [],
                                            "properties": {},
                                        }
                                    ]
                                },
                                "tags": [],
                                "properties": {},
                            }
                        ]
                    },
                    "tags": [],
                    "properties": {},
                }
            ],
        },
        "features": {
            "avg_transactions": [
                {
                    "description": "",
                    "entity": "user",
                    "name": "avg_transactions",
                    "owner": "default_user",
                    "provider": "local-mode",
                    "data-type": "float32",
                    "variant": "quickstart",
                    "status": "ready",
                    "location": {
                        "entity": "CustomerID",
                        "value": "TransactionAmount",
                        "timestamp": "",
                    },
                    "source": {
                        "Name": "average_user_transaction",
                        "Variant": "quickstart",
                    },
                    "tags": [],
                    "properties": {},
                }
            ]
        },
        "labels": {},
        "status": "status",
        "serializedConfig": "{}",
        "tags": ["local-mode"],
        "properties": {"resource_type": "Provider"},
    }
]

default_user = {
    "name": "default_user",
    "type": "User",
    "features": {
        "avg_transactions": [
            {
                "description": "",
                "entity": "user",
                "name": "avg_transactions",
                "owner": "default_user",
                "provider": "local-mode",
                "data-type": "float32",
                "variant": "quickstart",
                "status": "ready",
                "location": {
                    "entity": "CustomerID",
                    "value": "TransactionAmount",
                    "timestamp": "",
                },
                "source": {"Name": "average_user_transaction", "Variant": "quickstart"},
                "tags": [],
                "properties": {},
            }
        ]
    },
    "labels": {
        "fraudulent": [
            {
                "description": "",
                "entity": "user",
                "data-type": "bool",
                "name": "fraudulent",
                "owner": "default_user",
                "provider": "",
                "variant": "quickstart",
                "status": "ready",
                "location": {
                    "entity": "CustomerID",
                    "value": "IsFraud",
                    "timestamp": "",
                },
                "source": {"Name": "transactions", "Variant": "quickstart"},
                "trainingSets": {
                    "fraud_training": [
                        {
                            "description": "",
                            "name": "fraud_training",
                            "owner": "default_user",
                            "variant": "quickstart",
                            "status": "ready",
                            "label": {"Name": "fraudulent", "Variant": "quickstart"},
                            "features": {
                                "avg_transactions": [
                                    {
                                        "description": "",
                                        "entity": "user",
                                        "name": "avg_transactions",
                                        "owner": "default_user",
                                        "provider": "local-mode",
                                        "data-type": "float32",
                                        "variant": "quickstart",
                                        "status": "ready",
                                        "location": {
                                            "entity": "CustomerID",
                                            "value": "TransactionAmount",
                                            "timestamp": "",
                                        },
                                        "source": {
                                            "Name": "average_user_transaction",
                                            "Variant": "quickstart",
                                        },
                                        "tags": [],
                                        "properties": {},
                                    }
                                ]
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "tags": [],
                "properties": {},
            }
        ]
    },
    "training-sets": {
        "fraud_training": [
            {
                "description": "",
                "name": "fraud_training",
                "owner": "default_user",
                "variant": "quickstart",
                "status": "ready",
                "label": {"Name": "fraudulent", "Variant": "quickstart"},
                "features": {
                    "avg_transactions": [
                        {
                            "description": "",
                            "entity": "user",
                            "name": "avg_transactions",
                            "owner": "default_user",
                            "provider": "local-mode",
                            "data-type": "float32",
                            "variant": "quickstart",
                            "status": "ready",
                            "location": {
                                "entity": "CustomerID",
                                "value": "TransactionAmount",
                                "timestamp": "",
                            },
                            "source": {
                                "Name": "average_user_transaction",
                                "Variant": "quickstart",
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "tags": [],
                "properties": {},
            }
        ]
    },
    "sources": {
        "transactions": [
            {
                "description": "A dataset of fraudulent transactions",
                "name": "transactions",
                "source-type": "Source",
                "owner": "default_user",
                "provider": "local-mode",
                "variant": "quickstart",
                "status": "ready",
                "labels": {
                    "fraudulent": [
                        {
                            "description": "",
                            "entity": "user",
                            "data-type": "bool",
                            "name": "fraudulent",
                            "owner": "default_user",
                            "provider": "",
                            "variant": "quickstart",
                            "status": "ready",
                            "location": {
                                "entity": "CustomerID",
                                "value": "IsFraud",
                                "timestamp": "",
                            },
                            "source": {"Name": "transactions", "Variant": "quickstart"},
                            "trainingSets": {
                                "fraud_training": [
                                    {
                                        "description": "",
                                        "name": "fraud_training",
                                        "owner": "default_user",
                                        "variant": "quickstart",
                                        "status": "ready",
                                        "label": {
                                            "Name": "fraudulent",
                                            "Variant": "quickstart",
                                        },
                                        "features": {
                                            "avg_transactions": [
                                                {
                                                    "description": "",
                                                    "entity": "user",
                                                    "name": "avg_transactions",
                                                    "owner": "default_user",
                                                    "provider": "local-mode",
                                                    "data-type": "float32",
                                                    "variant": "quickstart",
                                                    "status": "ready",
                                                    "location": {
                                                        "entity": "CustomerID",
                                                        "value": "TransactionAmount",
                                                        "timestamp": "",
                                                    },
                                                    "source": {
                                                        "Name": "average_user_transaction",
                                                        "Variant": "quickstart",
                                                    },
                                                    "tags": [],
                                                    "properties": {},
                                                }
                                            ]
                                        },
                                        "tags": [],
                                        "properties": {},
                                    }
                                ]
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "features": {},
                "training-sets": {
                    "fraud_training": [
                        {
                            "description": "",
                            "name": "fraud_training",
                            "owner": "default_user",
                            "variant": "quickstart",
                            "status": "ready",
                            "label": {"Name": "fraudulent", "Variant": "quickstart"},
                            "features": {
                                "avg_transactions": [
                                    {
                                        "description": "",
                                        "entity": "user",
                                        "name": "avg_transactions",
                                        "owner": "default_user",
                                        "provider": "local-mode",
                                        "data-type": "float32",
                                        "variant": "quickstart",
                                        "status": "ready",
                                        "location": {
                                            "entity": "CustomerID",
                                            "value": "TransactionAmount",
                                            "timestamp": "",
                                        },
                                        "source": {
                                            "Name": "average_user_transaction",
                                            "Variant": "quickstart",
                                        },
                                        "tags": [],
                                        "properties": {},
                                    }
                                ]
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "tags": [],
                "properties": {},
            }
        ],
        "average_user_transaction": [
            {
                "description": "the average transaction amount for a user",
                "name": "average_user_transaction",
                "source-type": "Source",
                "owner": "default_user",
                "provider": "local-mode",
                "variant": "quickstart",
                "status": "ready",
                "labels": {},
                "features": {
                    "avg_transactions": [
                        {
                            "description": "",
                            "entity": "user",
                            "name": "avg_transactions",
                            "owner": "default_user",
                            "provider": "local-mode",
                            "data-type": "float32",
                            "variant": "quickstart",
                            "status": "ready",
                            "location": {
                                "entity": "CustomerID",
                                "value": "TransactionAmount",
                                "timestamp": "",
                            },
                            "source": {
                                "Name": "average_user_transaction",
                                "Variant": "quickstart",
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "training-sets": {
                    "fraud_training": [
                        {
                            "description": "",
                            "name": "fraud_training",
                            "owner": "default_user",
                            "variant": "quickstart",
                            "status": "ready",
                            "label": {"Name": "fraudulent", "Variant": "quickstart"},
                            "features": {
                                "avg_transactions": [
                                    {
                                        "description": "",
                                        "entity": "user",
                                        "name": "avg_transactions",
                                        "owner": "default_user",
                                        "provider": "local-mode",
                                        "data-type": "float32",
                                        "variant": "quickstart",
                                        "status": "ready",
                                        "location": {
                                            "entity": "CustomerID",
                                            "value": "TransactionAmount",
                                            "timestamp": "",
                                        },
                                        "source": {
                                            "Name": "average_user_transaction",
                                            "Variant": "quickstart",
                                        },
                                        "tags": [],
                                        "properties": {},
                                    }
                                ]
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "tags": [],
                "properties": {},
            }
        ],
    },
    "status": "ready",
    "tags": [],
    "properties": {},
}
localmode = {
    "name": "local-mode",
    "type": "Provider",
    "description": "This is local mode",
    "provider-type": "LOCAL_ONLINE",
    "software": "localmode",
    "team": "team",
    "sources": {
        "transactions": [
            {
                "description": "A dataset of fraudulent transactions",
                "name": "transactions",
                "source-type": "Source",
                "owner": "default_user",
                "provider": "local-mode",
                "variant": "quickstart",
                "status": "ready",
                "labels": {
                    "fraudulent": [
                        {
                            "description": "",
                            "entity": "user",
                            "data-type": "bool",
                            "name": "fraudulent",
                            "owner": "default_user",
                            "provider": "",
                            "variant": "quickstart",
                            "status": "ready",
                            "location": {
                                "entity": "CustomerID",
                                "value": "IsFraud",
                                "timestamp": "",
                            },
                            "source": {"Name": "transactions", "Variant": "quickstart"},
                            "trainingSets": {
                                "fraud_training": [
                                    {
                                        "description": "",
                                        "name": "fraud_training",
                                        "owner": "default_user",
                                        "variant": "quickstart",
                                        "status": "ready",
                                        "label": {
                                            "Name": "fraudulent",
                                            "Variant": "quickstart",
                                        },
                                        "features": {
                                            "avg_transactions": [
                                                {
                                                    "description": "",
                                                    "entity": "user",
                                                    "name": "avg_transactions",
                                                    "owner": "default_user",
                                                    "provider": "local-mode",
                                                    "data-type": "float32",
                                                    "variant": "quickstart",
                                                    "status": "ready",
                                                    "location": {
                                                        "entity": "CustomerID",
                                                        "value": "TransactionAmount",
                                                        "timestamp": "",
                                                    },
                                                    "source": {
                                                        "Name": "average_user_transaction",
                                                        "Variant": "quickstart",
                                                    },
                                                    "tags": [],
                                                    "properties": {},
                                                }
                                            ]
                                        },
                                        "tags": [],
                                        "properties": {},
                                    }
                                ]
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "features": {},
                "training-sets": {
                    "fraud_training": [
                        {
                            "description": "",
                            "name": "fraud_training",
                            "owner": "default_user",
                            "variant": "quickstart",
                            "status": "ready",
                            "label": {"Name": "fraudulent", "Variant": "quickstart"},
                            "features": {
                                "avg_transactions": [
                                    {
                                        "description": "",
                                        "entity": "user",
                                        "name": "avg_transactions",
                                        "owner": "default_user",
                                        "provider": "local-mode",
                                        "data-type": "float32",
                                        "variant": "quickstart",
                                        "status": "ready",
                                        "location": {
                                            "entity": "CustomerID",
                                            "value": "TransactionAmount",
                                            "timestamp": "",
                                        },
                                        "source": {
                                            "Name": "average_user_transaction",
                                            "Variant": "quickstart",
                                        },
                                        "tags": [],
                                        "properties": {},
                                    }
                                ]
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "tags": [],
                "properties": {},
            }
        ],
        "average_user_transaction": [
            {
                "description": "the average transaction amount for a user",
                "name": "average_user_transaction",
                "source-type": "Source",
                "owner": "default_user",
                "provider": "local-mode",
                "variant": "quickstart",
                "status": "ready",
                "labels": {},
                "features": {
                    "avg_transactions": [
                        {
                            "description": "",
                            "entity": "user",
                            "name": "avg_transactions",
                            "owner": "default_user",
                            "provider": "local-mode",
                            "data-type": "float32",
                            "variant": "quickstart",
                            "status": "ready",
                            "location": {
                                "entity": "CustomerID",
                                "value": "TransactionAmount",
                                "timestamp": "",
                            },
                            "source": {
                                "Name": "average_user_transaction",
                                "Variant": "quickstart",
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "training-sets": {
                    "fraud_training": [
                        {
                            "description": "",
                            "name": "fraud_training",
                            "owner": "default_user",
                            "variant": "quickstart",
                            "status": "ready",
                            "label": {"Name": "fraudulent", "Variant": "quickstart"},
                            "features": {
                                "avg_transactions": [
                                    {
                                        "description": "",
                                        "entity": "user",
                                        "name": "avg_transactions",
                                        "owner": "default_user",
                                        "provider": "local-mode",
                                        "data-type": "float32",
                                        "variant": "quickstart",
                                        "status": "ready",
                                        "location": {
                                            "entity": "CustomerID",
                                            "value": "TransactionAmount",
                                            "timestamp": "",
                                        },
                                        "source": {
                                            "Name": "average_user_transaction",
                                            "Variant": "quickstart",
                                        },
                                        "tags": [],
                                        "properties": {},
                                    }
                                ]
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "tags": [],
                "properties": {},
            }
        ],
    },
    "features": {
        "avg_transactions": [
            {
                "description": "",
                "entity": "user",
                "name": "avg_transactions",
                "owner": "default_user",
                "provider": "local-mode",
                "data-type": "float32",
                "variant": "quickstart",
                "status": "ready",
                "location": {
                    "entity": "CustomerID",
                    "value": "TransactionAmount",
                    "timestamp": "",
                },
                "source": {"Name": "average_user_transaction", "Variant": "quickstart"},
                "tags": [],
                "properties": {},
            }
        ]
    },
    "labels": {},
    "status": "status",
    "serializedConfig": "{}",
    "tags": ["local-mode"],
    "properties": {"resource_type": "Provider"},
}
average_user_transaction = {
    "all-variants": ["average_user_transaction"],
    "type": "Source",
    "default-variant": "quickstart",
    "name": "average_user_transaction",
    "variants": {
        "quickstart": {
            "description": "the average transaction amount for a user",
            "name": "average_user_transaction",
            "source-type": "Source",
            "owner": "default_user",
            "provider": "local-mode",
            "variant": "quickstart",
            "status": "ready",
            "labels": {},
            "features": {
                "avg_transactions": [
                    {
                        "description": "",
                        "entity": "user",
                        "name": "avg_transactions",
                        "owner": "default_user",
                        "provider": "local-mode",
                        "data-type": "float32",
                        "variant": "quickstart",
                        "status": "ready",
                        "location": {
                            "entity": "CustomerID",
                            "value": "TransactionAmount",
                            "timestamp": "",
                        },
                        "source": {
                            "Name": "average_user_transaction",
                            "Variant": "quickstart",
                        },
                        "tags": [],
                        "properties": {},
                    }
                ]
            },
            "training-sets": {
                "fraud_training": [
                    {
                        "description": "",
                        "name": "fraud_training",
                        "owner": "default_user",
                        "variant": "quickstart",
                        "status": "ready",
                        "label": {"Name": "fraudulent", "Variant": "quickstart"},
                        "features": {
                            "avg_transactions": [
                                {
                                    "description": "",
                                    "entity": "user",
                                    "name": "avg_transactions",
                                    "owner": "default_user",
                                    "provider": "local-mode",
                                    "data-type": "float32",
                                    "variant": "quickstart",
                                    "status": "ready",
                                    "location": {
                                        "entity": "CustomerID",
                                        "value": "TransactionAmount",
                                        "timestamp": "",
                                    },
                                    "source": {
                                        "Name": "average_user_transaction",
                                        "Variant": "quickstart",
                                    },
                                    "tags": [],
                                    "properties": {},
                                }
                            ]
                        },
                        "tags": [],
                        "properties": {},
                    }
                ]
            },
            "tags": [],
            "properties": {},
        }
    },
}
user = {
    "description": "",
    "type": "Entity",
    "name": "user",
    "features": {
        "avg_transactions": [
            {
                "description": "",
                "entity": "user",
                "name": "avg_transactions",
                "owner": "default_user",
                "provider": "local-mode",
                "data-type": "float32",
                "variant": "quickstart",
                "status": "ready",
                "location": {
                    "entity": "CustomerID",
                    "value": "TransactionAmount",
                    "timestamp": "",
                },
                "source": {"Name": "average_user_transaction", "Variant": "quickstart"},
                "tags": [],
                "properties": {},
            }
        ]
    },
    "labels": {
        "fraudulent": [
            {
                "description": "",
                "entity": "user",
                "data-type": "bool",
                "name": "fraudulent",
                "owner": "default_user",
                "provider": "",
                "variant": "quickstart",
                "status": "ready",
                "location": {
                    "entity": "CustomerID",
                    "value": "IsFraud",
                    "timestamp": "",
                },
                "source": {"Name": "transactions", "Variant": "quickstart"},
                "trainingSets": {
                    "fraud_training": [
                        {
                            "description": "",
                            "name": "fraud_training",
                            "owner": "default_user",
                            "variant": "quickstart",
                            "status": "ready",
                            "label": {"Name": "fraudulent", "Variant": "quickstart"},
                            "features": {
                                "avg_transactions": [
                                    {
                                        "description": "",
                                        "entity": "user",
                                        "name": "avg_transactions",
                                        "owner": "default_user",
                                        "provider": "local-mode",
                                        "data-type": "float32",
                                        "variant": "quickstart",
                                        "status": "ready",
                                        "location": {
                                            "entity": "CustomerID",
                                            "value": "TransactionAmount",
                                            "timestamp": "",
                                        },
                                        "source": {
                                            "Name": "average_user_transaction",
                                            "Variant": "quickstart",
                                        },
                                        "tags": [],
                                        "properties": {},
                                    }
                                ]
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "tags": [],
                "properties": {},
            }
        ]
    },
    "training-sets": {
        "fraud_training": [
            {
                "description": "",
                "name": "fraud_training",
                "owner": "default_user",
                "variant": "quickstart",
                "status": "ready",
                "label": {"Name": "fraudulent", "Variant": "quickstart"},
                "features": {
                    "avg_transactions": [
                        {
                            "description": "",
                            "entity": "user",
                            "name": "avg_transactions",
                            "owner": "default_user",
                            "provider": "local-mode",
                            "data-type": "float32",
                            "variant": "quickstart",
                            "status": "ready",
                            "location": {
                                "entity": "CustomerID",
                                "value": "TransactionAmount",
                                "timestamp": "",
                            },
                            "source": {
                                "Name": "average_user_transaction",
                                "Variant": "quickstart",
                            },
                            "tags": [],
                            "properties": {},
                        }
                    ]
                },
                "tags": [],
                "properties": {},
            }
        ]
    },
    "status": "ready",
    "tags": [],
    "properties": {},
}
fraudulent = {
    "all-variants": ["quickstart"],
    "type": "Label",
    "default-variant": "quickstart",
    "name": "fraudulent",
    "variants": {
        "quickstart": {
            "description": "",
            "entity": "user",
            "data-type": "bool",
            "name": "fraudulent",
            "owner": "default_user",
            "provider": "",
            "variant": "quickstart",
            "status": "ready",
            "location": {"entity": "CustomerID", "value": "IsFraud", "timestamp": ""},
            "source": {"Name": "transactions", "Variant": "quickstart"},
            "trainingSets": {
                "fraud_training": [
                    {
                        "description": "",
                        "name": "fraud_training",
                        "owner": "default_user",
                        "variant": "quickstart",
                        "status": "ready",
                        "label": {"Name": "fraudulent", "Variant": "quickstart"},
                        "features": {
                            "avg_transactions": [
                                {
                                    "description": "",
                                    "entity": "user",
                                    "name": "avg_transactions",
                                    "owner": "default_user",
                                    "provider": "local-mode",
                                    "data-type": "float32",
                                    "variant": "quickstart",
                                    "status": "ready",
                                    "location": {
                                        "entity": "CustomerID",
                                        "value": "TransactionAmount",
                                        "timestamp": "",
                                    },
                                    "source": {
                                        "Name": "average_user_transaction",
                                        "Variant": "quickstart",
                                    },
                                    "tags": [],
                                    "properties": {},
                                }
                            ]
                        },
                        "tags": [],
                        "properties": {},
                    }
                ]
            },
            "tags": [],
            "properties": {},
        }
    },
}
fraud_training = {
    "all-variants": ["quickstart"],
    "type": "TrainingSet",
    "default-variant": "quickstart",
    "name": "fraud_training",
    "variants": {
        "quickstart": {
            "description": "",
            "name": "fraud_training",
            "owner": "default_user",
            "variant": "quickstart",
            "status": "ready",
            "label": {"Name": "fraudulent", "Variant": "quickstart"},
            "features": {
                "avg_transactions": [
                    {
                        "description": "",
                        "entity": "user",
                        "name": "avg_transactions",
                        "owner": "default_user",
                        "provider": "local-mode",
                        "data-type": "float32",
                        "variant": "quickstart",
                        "status": "ready",
                        "location": {
                            "entity": "CustomerID",
                            "value": "TransactionAmount",
                            "timestamp": "",
                        },
                        "source": {
                            "Name": "average_user_transaction",
                            "Variant": "quickstart",
                        },
                        "tags": [],
                        "properties": {},
                    }
                ]
            },
            "tags": [],
            "properties": {},
        }
    },
}


def remove_keys(obj, rubbish):
    if isinstance(obj, dict):
        obj = {
            key: remove_keys(value, rubbish)
            for key, value in obj.items()
            if key not in rubbish
        }
    elif isinstance(obj, list):
        obj = [remove_keys(item, rubbish) for item in obj if item not in rubbish]
    return obj


def test_setup():
    import subprocess

    apply = subprocess.run(
        ["featureform", "apply", "client/examples/local_quickstart.py", "--local"]
    )
    print("The exit code was: %d" % apply.returncode)
    assert apply.returncode == 0, f"OUT: {apply.stdout}, ERR: {apply.stderr}"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


def check_objs(path, test_obj, client):
    response = client.get(path)
    assert response.status == "200 OK"
    json_resource = json.loads(response.data.decode())
    removed_created_json = remove_keys(json_resource, ["created", "definition"])
    if isinstance(removed_created_json, dict):
        assert test_obj == removed_created_json
    elif isinstance(removed_created_json, list):
        actual = {obj["name"]: obj for obj in removed_created_json}
        expected = {obj["name"]: obj for obj in test_obj}
        assert actual == expected


def test_version(client):
    response = client.get("data/version")
    assert response.status == "200 OK"
    assert response.data is not None
    json_obj = json.loads(response.data)
    assert json_obj["version"] is not None


def test_features(client):
    check_objs("/data/features", features, client)


def test_labels(client):
    check_objs("/data/labels", labels, client)


def test_sources(client):
    check_objs("/data/sources", sources, client)


def test_training_sets(client):
    check_objs("/data/training_sets", training_sets, client)


def test_entities(client):
    check_objs("/data/entities", entities, client)


def test_models(client):
    check_objs("/data/models", models, client)


def test_providers(client):
    check_objs("/data/providers", providers, client)


def test_default_user(client):
    check_objs("/data/users/default_user", default_user, client)


def test_localmode(client):
    check_objs("/data/providers/local-mode", localmode, client)


def test_average_user_transaction(client):
    check_objs(
        "/data/sources/average_user_transaction", average_user_transaction, client
    )


def test_fraudulent(client):
    check_objs("/data/labels/fraudulent", fraudulent, client)


def test_fraud_training(client):
    check_objs("/data/training_sets/fraud_training", fraud_training, client)


def test_user(client):
    check_objs("/data/entities/user", user, client)


def test_cleanup():
    def del_rw(action, name, exc):
        os.chmod(name, stat.S_IWRITE)
        os.remove(name)

    try:
        shutil.rmtree(".featureform", onerror=del_rw)
    except:
        print("File Already Removed")
