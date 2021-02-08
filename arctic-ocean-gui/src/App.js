import './App.css';
import Form from "@rjsf/material-ui";

function App() {
  const schema = {
    title: "Arctic Ocean GUI",
    description: "Input the parameters to run the Arctic Ocean acoustic models",
    type: "object",
    properties: {
      "map": {
        title: "Create map",
        type: "object",
        required: ["coast_res", "color_db", "minlon", "maxlon", "minlat", "maxlat", "cenlon", "cenlat", "source_file", "receiver_file", "depth", "radius", "shape"],
        properties: {
          "coast_res": {
            title: "Coastline resolution",
            default: "high",
            enum: [
              "low",
              "high"
            ],
            enumNames: [
              "Low",
              "High",
            ]
          },
          "color_db": {
            title: "Coloring database",
            default: "IBCAO_2min",
            enum: [
              "IBCAO_2min",
              "IBCAO_20min",
              "IBCAO_30arcsec",
              "HYCOM_salinity",
              "HYCOM_temperature",
              "ECCOv4_temperature",
              "ocean_model_salinity",
              "ocean_model_temperature",
            ],
            enumNames: [
              "IBCAO - bathymetry",
              "HYCOM - Fram - salinity",
              "HYCOM - Fram - temperature",
              "ECCOv4 - temperature",
              "Ocean Model - salinity",
              "Ocean Model - temperature"
            ]
          },
          "depth": {
            title: "Depth",
            description: "Only meaningful for ECCO and Ocean Model",
            type: "integer",
            default: 5
          },
          "minlon": {
            title: "Minimum longitude",
            type: "integer",
            default: -180,
          },
          "maxlon": {
            title: "Maximum longitude",
            type: "integer",
            default: 180,
          },
          "minlat": {
            title: "Minimum latitude",
            type: "integer",
            default: 75,
          },
          "maxlat": {
            title: "Maximum latitude",
            type: "integer",
            default: 90,
          },
          "cenlon": {
            title: "Center longitude",
            type: "integer",
            default: -5,
          },
          "cenlat": {
            title: "Center latitude",
            type: "integer",
            default: 75,
          },
          "radius": {
            title: "Map radius",
            type: "integer",
            default: 15,
          },
          "shape": {
            title: "Map shape",
            type: "string",
            default: "rectangular",
            enum: [
              "circular",
              "rectangular"
            ],
            enumNames: [
              "Circular",
              "Rectangular",
            ]
          },
          "source_file": {
            title: "Select file to load sources from",
            description: "Select file to load sources from",
            type: "string",
            format: "data-url",
          },
          "receiver_file": {
            title: "Select file to load receivers from",
            description: "Select file to load receivers from",
            type: "string",
            format: "data-url"
          }
        },
      },
      "model": {
        title: "Model parameters",
        description: "Select which models to run and cofigure the model runs.",
        type: "object",
        required: ["source", "receiver", "delC", "delR", "ssp_database", "profile_type", "timestep"],
        properties: {
          "source": {
            title: "Select source",
            description: "Input source index (1 is the first line in the input file). Use the map for a visual representation of where the sources and receivers are.",
            default: 1,
            type: "integer",
          },
          "receiver": {
            title: "Select receiver",
            description: "Input receiver index (1 is the first line in the input file). Use the map for a visual representation of where the sources and receivers are.",
            default: 3,
            type: "integer",
          },
          "delC": {
            title: "delC",
            description: "Sound speed step size",
            default: 5,
            type: "integer",
          },
          "delR": {
            title: "delR",
            description: "Bathymetry step size",
            default: 10,
            type: "integer",
          },
          "ssp_database": {
            title: "Sound speed database",
            description: "Sound speed database for modeling",
            type: "integer",
            default: 0,
            enum: [
              0,
              1,
              2,
              3
            ],
            enumNames: [
              "ECCOv4",
              "WOA",
              "GECCO2007",
              "OceanModel"
            ]
          },
          "profile_type": {
            title: "Select profile",
            description: "Select profile for modeling",
            type: "integer",
            default: 0,
            enum: [
              0,
              1,
              2,
              3
            ],
            enumNames: [
              "Sound speed c(r,z)",
              "Temperature T(r,z)",
              "Salinity S(r,z)",
              "Bouyancy N(r,z) "
            ]
          },
          "timestep": {
            title: "Select timestep",
            description: "Select when to run the model for. Annual uses the annual average.",
            type: "integer",
            default: 0,
            enum: [
              0,
            ],
            enumNames: [
              "Annual",
            ]
          },
          "model_choice": {
            title: "Select model(s) to run",
            description: "Select one or more models to run with the given parameters.",
            type: "object",
            properties: {
              "run_ram": {
                title: "RAM",
                "type": "boolean"
              },
              "run_mpiram": {
                title: "MPIRAM",
                "type": "boolean"
              },
              "run_bellhop": {
                title: "Bellhop",
                type: "boolean"
              },
              "run_eigenray": {
                title: "Eigenray",
                type: "boolean"
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
                        properties: {
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
                        properties: {
                          "freq": {
                            title: "Frequency",
                            type: "integer",
                            default: 50
                          },
                          "time_window": {
                            title: "Time window",
                            type: "integer",
                            default: 5
                          },
                          "q_value": {
                            title: "Q-value",
                            type: "integer",
                            default: 2
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
                        properties: {
                          "freq": {
                            title: "Frequency",
                            type: "integer",
                            default: 50
                          },
                          "simtype": {
                            "title": "Simulation type",
                            "type": "array",
                            "uniqueItems": true,
                            items: {
                              type: "string",
                              enum: [
                                "R",
                                "E",
                                "I",
                                "S",
                                "C"
                              ],
                              enumNames: [
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
                        properties: {
                          "run_type": {
                            title: "Run type",
                            type: "string",
                            default: "Eigenray",
                            enum: [
                              "Eigenray",
                              "Timefront",
                            ]
                          },
                          "ray_num": {
                            title: "Number of rays",
                            type: "integer",
                            default: 2500
                          },
                          "epsilon": {
                            title: "Epsilon value",
                            type: "string",
                            default: "1e-5"
                          },
                          "bot_reflect": {
                            title: "Max number of bottom reflections allowed",
                            type: "integer",
                            default: 3,
                          },
                          "save_paths": {
                            title: "Save eigenray paths?",
                            type: "boolean",
                            default: true,
                          },
                          "use_bottom": {
                            title: "Use bottom when modeling?",
                            type: "boolean",
                            default: true,
                          },
                          "angle_range": {
                            title: "Angle range",
                            type: "string",
                            default: "-15, 15"
                          }
                        }
                      }
                    }
                  }
                ]
              },// gher
            },
          },
        },
      }
    },
  };

  const uiSchema = {
    "map": {
      "source_file": {
        "ui:options": {
          accept: ".dat"
        },
        "ui:widget": "file",
      },
      "receiver_file": {
        "ui:options": {
          accept: ".dat"
        },
        "ui:widget": "file",
      }
    },
    "model": {
      "timestep": {
        "ui:disabled": true,
      },
      "model_choice": {
        "RAM": {
          //"ui:title": " ",
        },
        "MPIRAM": {
          //"ui:title": " ",
        },
        "Bellhop": {
          //"ui:title": " ",
          simtype: {
            "ui:widget": "checkboxes",
          },
        },
        "Eigenray": {
          //"ui:title": " ",
        }
      }
    }
  }

  const saveParameters = (event) => {
    console.log(event);
    const fileData = JSON.stringify(event.formData);
    const blob = new Blob([fileData], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.download = 'ap_params.json';
    link.href = url;
    link.click();
  }


  const log = (e) => console.log(e.formData);

  return (
    <div className="App">
      <div>
        <Form schema={schema}
          uiSchema={uiSchema}
          onChange={log}
          onSubmit={saveParameters}
          onError={log} />
      </div>
    </div>
  );
}

export default App;
