reference = "NEN-EN1991-2-H5"

load_factors = [
  {
    "value": 1.2,
    "symbol": "γ_G"
  },
  {
    "value": 1.2,
    "symbol": "γ_Q1"
  },
  {
    "value": 1.35,
    "symbol": "γ_Q2"
  },
  {
    "value": 1,
    "symbol": "γ_A"
  }
]

resistance_factors = [
  {
    "value": 1.15,
    "symbol": "γ_M1",
    "reference": "CUR96:2019, 2.4.4.3",
  },
  {
    "value": 1.2,
    "symbol": "γ_M2",
    "reference": "CUR96:2019, 2.4.4.3",
  },
  {
    "value": 1.15,
    "symbol": "γ_M1,stab",
    "reference": "CUR96:2019, 2.4.4.3",
  },
  {
    "value": 1.15,
    "symbol": "γ_M2,stab",
    "reference": "CUR96:2019, 2.4.4.3",
  },
  {
    "value": 0.9,
    "symbol": "η_ct",
    "reference": "",
  },
  {
    "value": 0.9,
    "symbol": "η_cm",
    "reference": "",
  },
  {
    "value": 0.75,
    "symbol": "η_cv",
    "reference": "",
  },
  {
    "value": 1,
    "symbol": "η_cf",
    "reference": "",
  },
  {
    "value": 0.3,
    "symbol": "η_cc",
    "reference": "",
  }
]

loadcases = [
  {
    "load_combination": {"g": 1},
    "load_factors": {},
    "design_limits": ["d_crp"],
    "symbol": "crp",
    "limitstate": "sls",
    "strength_factors": [],
    "stiffness_factors": ["η_cv"]
  },
  {
    "load_combination": {"q_fk": 1},
    "load_factors": {},
    "design_limits": ["d_max"],
    "symbol": "gr1",
    "limitstate": "sls",
    "strength_factors": [],
    "stiffness_factors": ["η_cm", "η_ct"]
  },
  {
    "load_combination": {"Q_serv": 1},
    "load_factors": {},
    "design_limits": ["d_max"],
    "symbol": "gr2",
    "limitstate": "sls",
    "strength_factors": [],
    "stiffness_factors": ["η_cm", "η_ct"]
  },
  {
    "load_combination": {"g": 1},
    "load_factors": {},
    "design_limits": ["f_min"],
    "symbol": "f_init",
    "limitstate": "sls",
    "strength_factors": [],
    "stiffness_factors": []
  },
  {
    "load_combination": {"g": 1},
    "load_factors": {},
    "design_limits": ["f_min"],
    "symbol": "f_eol",
    "limitstate": "sls",
    "strength_factors": [],
    "stiffness_factors": ["η_cm", "η_ct"]
  },
  {
    "load_combination": {"g": 1, "TC1": 1},
    "load_factors": {},
    "design_limits": ["a_max"],
    "symbol": "TC1",
    "limitstate": "sls",
    "strength_factors": [],
    "stiffness_factors": ["η_cm", "η_ct"]
  },
  {
    "load_combination": {"T": 1},
    "load_factors": {},
    "design_limits": ["dL_max"],
    "symbol": "T",
    "limitstate": "sls",
    "strength_factors": [],
    "stiffness_factors": ["η_cm", "η_ct"]
  },
  {
    "load_combination": {"g": 1},
    "load_factors": {"g": "γ_G"},
    "symbol": "crp",
    "limitstate": "uls",
    "strength_factors": ["γ_M1", "γ_M2"],
    "stiffness_factors": ["η_cc", "η_cm", "η_ct"]
  },
  {
    "load_combination": {"g": 1, "q_fk": 1, "q_flk": 1, "W": 0.3, "T": 0.3},
    "load_factors": {"g": "γ_G", "q_fk": "γ_Q1", "q_flk": "γ_Q1", "W": "γ_Q2", "T": "γ_G"},
    "symbol": "gr1",
    "limitstate": "uls",
    "strength_factors": ["γ_M1", "γ_M2"],
    "stiffness_factors": ["η_cm", "η_ct"]
  },
  {
    "load_combination": {"g": 1, "Q_serv": 1, "W": 0.3, "T": 0.3},
    "load_factors": {"g": "γ_G", "Q_serv": "γ_Q1", "W": "γ_Q2", "T": "γ_Q2"},
    "symbol": "gr2",
    "limitstate": "uls",
    "strength_factors": ["γ_M1", "γ_M2"],
    "stiffness_factors": ["η_cm", "η_ct"]
  },
  {
    "load_combination": {"g": 1, "Q_fwk": 1},
    "load_factors": {"g": "γ_G", "Q_fwk": "γ_Q1"},
    "symbol": "Q_fwk",
    "limitstate": "uls",
    "strength_factors": ["γ_M1", "γ_M2"],
    "stiffness_factors": ["η_cm", "η_ct"]
  },
  {
    "load_combination": {"g": 1, "Q_sv": 1},
    "load_factors": {"g": "γ_G","Q_sv": "γ_A"},
    "symbol": "Q_sv",
    "limitstate": "uls",
    "strength_factors": [],
    "stiffness_factors": []
  },
  {
    "load_combination": {"g": 1, "q_fk": 0.4, "q_flk": 0.4, "W": 1, "T": 0.3},
    "load_factors": {"g": "γ_G", "q_fk": "γ_Q2", "q_flk": "γ_Q2", "W": "γ_Q1", "T": "γ_Q2"},
    "symbol": "W",
    "limitstate": "uls",
    "strength_factors": ["γ_M1", "γ_M2"],
    "stiffness_factors": ["η_cm", "η_ct"]
  },
  {
    "load_combination": {"g": 1, "q_fk": 0.4, "q_flk": 0.4, "W": 0.3, "T": 1},
    "load_factors": {"g": "γ_G", "q_fk": "γ_Q2", "q_flk": "γ_Q2", "W": "γ_Q2", "T": "γ_Q1"},
    "symbol": "T",
    "limitstate": "uls",
    "strength_factors": ["γ_M1", "γ_M2"],
    "stiffness_factors": ["η_cm", "η_ct"]
  },


  {
    "load_combination":{"g": 1, "Q_serv": 0.8, "W": 0.3, "T": 0.3, "S": 1},
    "load_factors": {"g": "γ_G", "Q_serv": "γ_Q2", "W": "γ_Q2", "T": "γ_Q2", "S": "γ_Q1"},
    "symbol": "S",
    "limitstate": "uls",
    "strength_factors": ["γ_M1", "γ_M2"],
    "stiffness_factors": ["η_cm", "η_ct"]
  }
]

loads = [
  {
    "description": "Aslasten: [25.0, 25.0] kN, wielprent: 250 mm x 250 mm, spoorbreedte: 1750 mm, wielbasis: 3000 mm",
    "wheel_contact": [
      250,
      250
    ],
    "track_width": 1750,
    "symbol": "Q_serv",
    "wheel_base": 3000,
    "class": "vehicle",
    "brake_force": 15000,
    "axle_loads": [
      25000,
      25000
    ]
  },
  {
    "description": "Aslasten: [80.0, 40.0] kN, wielprent: 200 mm x 200 mm, spoorbreedte: 1200 mm, wielbasis: 3000 mm",
    "wheel_contact": [
      200,
      200
    ],
    "track_width": 1200,
    "symbol": "Q_sv",
    "wheel_base": 3000,
    "class": "vehicle",
    "brake_force": 72000,
    "axle_loads": [
      80000,
      40000
    ]
  },
  {
    "unit": "N",
    "class": "force",
    "value": 7000,
    "symbol": "Q_fwk",
    "contact": [
      100,
      100
    ],
  },
  {
    "unit": "N/mm^2",
    "class": "udl",
    "value": 0.005,
    "symbol": "q_fk",
    "description": "Waarde: 5.0 kN/m<sup>2</sup>"
  },
  {
    "unit": "N/mm^2",
    "class": "traction",
    "value": 0.0005,
    "symbol": "q_flk",
    "description": "Waarde: 5.0 kN/m<sup>2</sup>"
  },
  {
    "unit": "N/mm",
    "class": "linear_mass",
    "value": 0,
    "symbol": "g",
    "description": None
  },
  {
    "class": "pedestrian_flow",
    "symbol": "TC1",
    "person_mass": 0.07,
    "people_count": 10,
    "people_density": None,
    "step_frequency": 2.3
  },
  {
    "class": "pedestrian_flow",
    "symbol": "TC2",
    "person_mass": 0.07,
    "people_count": None,
    "people_density": 0.2,
    "step_frequency": 2.3
  },
  {
    "class": "pedestrian_flow",
    "symbol": "TC3",
    "person_mass": 0.07,
    "people_count": None,
    "people_density": 0.5,
    "step_frequency": 2.3
  },
  {
    "class": "pedestrian_flow",
    "symbol": "TC4",
    "person_mass": 0.07,
    "people_count": None,
    "people_density": 1,
    "step_frequency": 2.3
  },
  {
    "class": "pedestrian_flow",
    "symbol": "TC5",
    "person_mass": 0.07,
    "people_count": None,
    "people_density": 1.5,
    "step_frequency": 2.3
  },
  {
    "class": "temperature",
    "symbol": "T",
    "description": None
  },
  {
    "class": "wind",
    "symbol": "W",
    "description": None
  },
  {
    "class": "udl",
    "value": 0,
    "symbol": "S",
    "description": None
  }
]

design_limits = [
  {
    "class": "deflection",
    "value": 100,
    "symbol": "d_max",
    "description": "Max. live load deflection"
  },
  {
    "class": "eigenfrequency",
    "value": 3.0,
    "symbol": "f_min",
    "description": "Min. eigenfrequency"
  },
  {
    "class": "acceleration",
    "value": 1.0,
    "symbol": "a_max,p",
    "description": "Max. acceleration due to pedestrians"
  },
  {
    "class": "acceleration",
    "value": 2.5,
    "symbol": "a_max,v",
    "description": "Max. acceleration due to vandals"
  },
  {
    "class": "deflection",
    "value": None,
    "symbol": "d_crp",
    "description": "Max. creep deflection"
  },
  {
    "class": "thermal_expansion",
    "value": None,
    "symbol": "dL_max",
    "description": "Max. expansion/contraction"
  }

]



