const schema = {
    "title": "Arctic Ocean GUI",
    "description": "Input the parameters to run the Arctic Ocean acoustic models",
    "type": "object",
    "properties": {
        "map": {
            "title": "Create map",
            "type": "object",
            "required": ["minlon", "maxlon", "minlat", "maxlat", "cenlon", "cenlat", "source_file", "receiver_file", "radius", "shape"],
            "properties": {
                "data_selection": {
                    "title": "",
                    "type": "object",
                    "required": ["coast_res", "color_db", "depth"],
                    "properties": {
                        "coast_res": {
                            "title": "Coastline resolution",
                            "default": "high",
                            "enum": [
                                "low",
                                "high"
                            ],
                            "enumNames": [
                                "Low",
                                "High",
                            ]
                        },
                        "color_db": {
                            "title": "Coloring database",
                            "enum": [
                                "IBCAO_2min",
                                "IBCAO_20min",
                                "IBCAO_30arcsec",
                                "HYCOM_salinity",
                                "HYCOM_temperature",
                                "ECCOv4_temperature",
                                "ocean_model_salinity",
                                "ocean_model_temperature",
                            ],
                            "enumNames": [
                                "IBCAO 2 min - bathymetry",
                                "IBCAO 20 min - bathymetry",
                                "IBCAO 30arcsec - bathymetry",
                                "HYCOM - Fram 300m - salinity",
                                "HYCOM - Fram 300m - temperature",
                                "ECCOv4 - temperature",
                                "Ocean Model - salinity",
                                "Ocean Model - temperature"
                            ]
                        },
                    }, "dependencies": {
                        "color_db": {
                            "oneOf": [
                                {
                                    "properties": {
                                        "color_db": {
                                            "enum": [
                                                "ECCOv4_temperature",
                                            ]
                                        },
                                        "depth": {
                                            title: "Depth (m)",
                                            description: "Only changeable for ECCO and Ocean Model",
                                            type: "number",
                                            default: 5,
                                            enum: [5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105, 116, 127, 140, 154, 172, 195, 223, 257,
                                                300, 351, 410, 477, 553, 635, 722, 814, 910, 1007, 1106, 1206, 1306, 1409, 1517, 1634,
                                                1765, 1914, 2084, 2276, 2491, 2729, 2990, 3274, 3581, 3911, 4264, 4640, 5039, 5461, 5906]
                                        },
                                    },
                                },
                                {
                                    "properties": {
                                        "color_db": {
                                            "enum": [
                                                "ocean_model_salinity",
                                                "ocean_model_temperature"
                                            ]
                                        },
                                        "depth": {
                                            title: "Depth (m)",
                                            description: "Only changeable for ECCO and Ocean Model",
                                            type: "number",
                                            default: 6.7,
                                            enum: [6.7, 12.1, 18.5, 26.2, 35.2, 45, 55, 65, 75, 85, 95, 105, 115, 125, 135, 146.5, 161.5, 180, 200, 220, 240, 260, 301, 327, 361, 402.5, 250, 500, 551.5, 614, 700, 800, 900, 1000, 1100, 1225, 1400, 1600, 1800, 2010, 2270, 2610, 3000, 3400, 3800, 4200, 4600, 5000, 5400, 5800]
                                        },
                                    },
                                },
                                {
                                    "properties": {
                                        "color_db": {
                                            "enum": [
                                                "HYCOM_salinity",
                                                "HYCOM_temperature",
                                            ]
                                        },
                                        "depth": {
                                            description: "Only changeable for ECCO and Ocean Model",
                                            title: "Depth (m)",
                                            type: "number",
                                            default: 300,
                                            enum: [300]
                                        },
                                    },

                                },
                                {
                                    "properties": {
                                        "color_db": {
                                            "enum": [
                                                "IBCAO_2min",
                                                "IBCAO_20min",
                                                "IBCAO_30arcsec",
                                            ]
                                        },
                                        "depth": {
                                            title: "Depth (m)",
                                            description: "Only changeable for ECCO and Ocean Model",
                                            type: "number",
                                            default: 0,
                                            enum: [0]
                                        },
                                    },
                                },
                            ]
                        }
                    },
                },
                "minlon": {
                    "title": "Minimum longitude [°E]",
                    "type": "integer",
                    "default": -180,
                },
                "maxlon": {
                    "title": "Maximum longitude [°E]",
                    "type": "integer",
                    "default": 180,
                },
                "cenlon": {
                    "title": "Center longitude [°E]",
                    "type": "integer",
                    "default": -5,
                },
                "minlat": {
                    "title": "Minimum latitude [°N]",
                    "type": "integer",
                    "default": 70,
                },
                "maxlat": {
                    "title": "Maximum latitude [°N]",
                    "type": "integer",
                    "default": 90,
                },
                "cenlat": {
                    "title": "Center latitude [°N]",
                    "type": "integer",
                    "default": 85,
                },
                "radius": {
                    "title": "Map radius",
                    "type": "integer",
                    "default": 15,
                },
                "shape": {
                    "title": "Map shape",
                    "type": "string",
                    "default": "rectangular",
                    "enum": [
                        "circular",
                        "rectangular"
                    ],
                    "enumNames": [
                        "Circular",
                        "Rectangular",
                    ]
                },
                "source_file": {
                    "title": "Select file to load sources from",
                    "description": "Select file to load sources from",
                    "type": "string",
                    "format": "data-url",
                },
                "receiver_file": {
                    "title": "Select file to load receivers from",
                    "description": "Select file to load receivers from",
                    "type": "string",
                    "format": "data-url"
                }
            },
        },
        "model": {
            "title": "Model parameters",
            "description": "Select which models to run and cofigure the model runs.",
            "type": "object",
            "required": ["source", "receiver", "delC", "delR", "ssp_database", "profile_type", "timestep"],
            "properties": {
                "source": {
                    "title": "Select source",
                    "description": "Input source index (1 is the first line in the input file). Use the map for a visual representation of where the sources and receivers are.",
                    "default": 1,
                    "type": "integer",
                },
                "receiver": {
                    "title": "Select receiver",
                    "description": "Input receiver index (1 is the first line in the input file). Use the map for a visual representation of where the sources and receivers are.",
                    "default": 2,
                    "type": "integer",
                },
                "delC": {
                    "title": "DR[km]:C",
                    "description": "Sound speed step size",
                    "default": 5,
                    "type": "integer",
                },
                "delR": {
                    "title": "DR[km]:z",
                    "description": "Bathymetry step size",
                    "default": 10,
                    "type": "integer",
                },
                "ssp_database": {
                    "title": "Sound speed database",
                    "description": "Sound speed database for modeling",
                    "type": "integer",
                    "default": 0,
                    "enum": [
                        0,
                        1,
                    ],
                    "enumNames": [
                        "ECCOv4",
                        "WOA",
                    ]
                },
                "timestep":{
                    "title": "Select timestep",
                    "description": "Select when to run the model for. ECCO only supports Annual.",
                    "type": "integer",
                    "default": 0,
                    "enum": [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                    ],
                    "enumNames": [
                        "Annual",
                        "January",
                        "February",
                        "March",
                        "April",
                        "June",
                        "July",
                        "August",
                        "September",
                        "October",
                        "November",
                        "December",
                        "Winter",
                        "Spring",
                        "Summer",
                        "Fall",
                    ]
                },
                "profile_type": {
                    "title": "Select profile type",
                    "description": "Select profile for modeling",
                    "type": "integer",
                    "default": 0,
                    "enum": [
                        0,
                        1,
                        2,
                        3
                    ],
                    "enumNames": [
                        "Sound speed c(r,z)",
                        "Temperature T(r,z)",
                        "Salinity S(r,z)",
                        "Bouyancy N(r,z) "
                    ]
                },
                "model_choice": {
                    "title": "Select model(s) to run",
                    "description": "Select one or more models to run with the given parameters.",
                    "type": "object",
                    "required": ["run_ram", "run_mpiram", "run_bellhop", "run_eigenray"],
                    "properties": {
                        "run_ram": {
                            "title": "RAM",
                            "type": "boolean",
                            "default": false,
                        },
                        "run_mpiram": {
                            "title": "MPIRAM",
                            "type": "boolean",
                            "default": false,
                        },
                        "run_bellhop": {
                            "title": "Bellhop",
                            "type": "boolean",
                            "default": false,
                        },
                        "run_eigenray": {
                            "title": "Eigenray",
                            "type": "boolean",
                            "default": false
                        }
                    },
                    "dependencies": {
                        "run_ram": {
                            "oneOf": [
                                {
                                    "properties": {
                                        "run_ram": {
                                            "const": false
                                        }
                                    }
                                },
                                {
                                    "properties": {
                                        "run_ram": {
                                            "const": true
                                        },
                                        "RAM": {
                                            "required": ["freq"],
                                            "properties": {
                                                "freq": {
                                                    "title": "frequency",
                                                    "type": "number",
                                                    "default": 100,
                                                }
                                            }
                                        }
                                    }
                                }
                            ]
                        },
                        "run_mpiram": {
                            "oneOf": [
                                {
                                    "properties": {
                                        "run_mpiram": {
                                            "const": false
                                        }
                                    }
                                },
                                {
                                    "properties": {
                                        "run_mpiram": {
                                            "const": true
                                        },
                                        "MPIRAM": {
                                            "required": ["freq", "time_window", "q_value"],
                                            "properties": {
                                                "freq": {
                                                    "title": "Frequency",
                                                    "type": "integer",
                                                    "default": 50
                                                },
                                                "time_window": {
                                                    "title": "Time window",
                                                    "type": "integer",
                                                    "default": 10
                                                },
                                                "q_value": {
                                                    "title": "Q-value",
                                                    "type": "integer",
                                                    "default": 5
                                                }
                                            }
                                        },
                                    }
                                }
                            ]
                        },
                        "run_bellhop": {
                            "oneOf": [
                                {
                                    "properties": {
                                        "run_bellhop": {
                                            "const": false
                                        }
                                    }
                                },
                                {
                                    "properties": {
                                        "run_bellhop": {
                                            "const": true
                                        },
                                        "Bellhop": {
                                            "required": ["freq", "simtype"],
                                            "properties": {
                                                "freq": {
                                                    "title": "Frequency",
                                                    "type": "integer",
                                                    "default": 50
                                                },
                                                "simtype": {
                                                    "title": "Simulation type",
                                                    "type": "array",
                                                    "uniqueItems": true,
                                                    "items": {
                                                        "type": "string",
                                                        "enum": [
                                                            "R",
                                                            "E",
                                                            "I",
                                                            "S",
                                                            "C"
                                                        ],
                                                        "enumNames": [
                                                            "Raytracing",
                                                            "Eigenrays",
                                                            "Incoherent transmission loss",
                                                            "Semi-coherent transmission loss",
                                                            "Coherent transmission loss"
                                                        ]
                                                    },
                                                }
                                            }
                                        },
                                    }
                                }
                            ]
                        },
                        "run_eigenray": {
                            "oneOf": [
                                {
                                    "properties": {
                                        "run_eigenray": {
                                            "const": false
                                        }
                                    }
                                },
                                {
                                    "properties": {
                                        "run_eigenray": {
                                            "const": true
                                        },
                                        "Eigenray": {
                                            "required": ["run_type", "ray_num", "epsilon", "bot_reflect", "save_paths", "use_bottom", "angle_range"],
                                            "properties": {
                                                "run_type": {
                                                    "title": "Run type",
                                                    "type": "integer",
                                                    "default": 0,
                                                    "enumNames": [
                                                        "Eigenray",
                                                        "Timefront",
                                                    ],
                                                    "enum": [
                                                        0,
                                                        1
                                                    ]
                                                },
                                                "ray_num": {
                                                    "title": "Number of rays",
                                                    "type": "integer",
                                                    "default": 2500
                                                },
                                                "epsilon": {
                                                    "title": "Epsilon value",
                                                    "type": "string",
                                                    "default": "1e-5"
                                                },
                                                "bot_reflect": {
                                                    "title": "Max number of bottom reflections allowed",
                                                    "type": "integer",
                                                    "default": 3,
                                                },
                                                "save_paths": {
                                                    "title": "Save eigenray paths?",
                                                    "type": "boolean",
                                                    "default": true,
                                                },
                                                "use_bottom": {
                                                    "title": "Use bottom when modeling?",
                                                    "type": "boolean",
                                                    "default": true,
                                                },
                                                "angle_range": {
                                                    "title": "Angle range",
                                                    "type": "string",
                                                    "default": "-10, 10"
                                                }
                                            }
                                        }
                                    }
                                }
                            ]
                        },
                    },
                },
            },
        }, 
    },
};


const uiSchema = {
    "map": {
        "source_file": {
            "ui:options": {
                "accept": ".dat"
            },
            "ui:widget": "file",
        },
        "receiver_file": {
            "ui:options": {
                "accept": ".dat"
            },
            "ui:widget": "file",
        }
    },
    "model": {
        "model_choice": {
            "Bellhop": {
                "simtype": {
                    "ui:widget": "checkboxes",
                },
            },
        }
    }
}

export {
    schema,
    uiSchema,
}