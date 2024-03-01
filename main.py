import glob
import os.path
import pathlib
import generation.converts as converts
import generation.copyright as gencopy
import generation.dump_py as dumpy

release_year = 2023
repo = "https://github.com/yoimerdr/gallerynpy"


def generate_dumpy_renpy():
    """
    Generate some empty renpy classes and functions to correct lint errors in the IDE.

    All the src/gallerynpy/store package is generated with this.
    """
    args = [dumpy.PyParameter("*args"), dumpy.PyParameter("**kwargs")]
    display_pck = dumpy.PyPackage(
        name="display",
        variables=[
            dumpy.PyVariable("core", value="displayable", has_value=True)
        ],
        files=[
            dumpy.PyFile(
                name="im",
                imports=[
                    dumpy.PyImport(
                        dumpy.Nameable("displayable"),
                        imports=[dumpy.Nameable("Displayable")],
                        relative=True
                    )
                ],
                classes=[
                    dumpy.PyClass(name="Surfer", methods=[
                        dumpy.PyFunction("get_size", simple_return="1920, 1080"),
                    ]),
                    dumpy.PyClass(
                        name="Image",
                        parent=dumpy.Nameable("Displayable"),
                        methods=[
                            dumpy.PyFunction(name="__init__", params=[
                                dumpy.PyParameter("path"),

                            ]),
                            dumpy.PyFunction(name="load", simple_return="Surfer()")
                        ]
                    ),
                    dumpy.PyClass(
                        name="Scale",
                        parent=dumpy.Nameable("Displayable"),
                        methods=[
                            dumpy.PyFunction(name="__init__", params=[
                                dumpy.PyParameter("path"),
                                dumpy.PyParameter("width"),
                                dumpy.PyParameter("height"),
                                *args
                            ])
                        ]
                    )
                ]
            ),
            dumpy.PyFile(
                name="transform",
                classes=[dumpy.PyClass("ATLTransform")]
            ),
            dumpy.PyFile(
                name="displayable",
                classes=[dumpy.PyClass("Displayable")]
            )
        ],
        import_all=True
    )

    renpy_pck = dumpy.PyPackage(
        name="renpy",
        files=[
            dumpy.PyFile(
                name="config",
                variables=[
                    dumpy.PyVariable(name="basedir", value="'/'")
                ]
            )
        ],
        functions=[
            dumpy.PyFunction(
                name="loadable",
                params=[dumpy.PyParameter("path")],
                simple_return="True"
            ),
            dumpy.PyFunction(
                name="get_registered_image",
                params=[dumpy.PyParameter("name")],
                simple_return="Image(name)"
            ),
            dumpy.PyFunction(name="restart_interaction")
        ],
        packages=[
            display_pck
        ],
        import_all=True
    )

    store_pck = dumpy.PyPackage(
        "store",
        imports=[
            dumpy.PyImport(
                dumpy.Nameable("renpy.display"),
                relative=True,
                import_all=True
            )
        ],
        variables=[
            dumpy.PyVariable(name="dissolve")
        ],
        classes=[
            dumpy.PyClass(
                name="Action",
                methods=[
                    dumpy.PyFunction(name="get_sensitive", simple_return="True"),
                    dumpy.PyFunction(name="get_selected", simple_return="False"),
                    dumpy.PyFunction(name="__call__", params=[
                        dumpy.PyParameter(name="*args"),
                        dumpy.PyParameter(name="**kwargs")
                    ])
                ]
            ),
            dumpy.PyClass(
                name="Solid",
                parent=dumpy.Nameable("Displayable"),
                methods=[
                    dumpy.PyFunction(name="__init__", params=[
                        dumpy.PyParameter("color")
                    ])
                ]),
            dumpy.PyClass(
                name="Composite",
                methods=[
                    dumpy.PyFunction(name="__init__", params=[
                        dumpy.PyParameter("size", ),
                        dumpy.PyParameter("positions"),
                        dumpy.PyParameter("displayable")
                    ])
                ]
            ),
            dumpy.PyClass(name="Button", methods=[
                dumpy.PyFunction(name="__init__", params=[
                    dumpy.PyParameter(name="action")
                ])
            ]),
            dumpy.PyClass(name="Function", methods=[
                dumpy.PyFunction(name="__init__", params=[
                    dumpy.PyParameter("callable", ),
                    *args
                ])
            ]),
            dumpy.PyClass(name="Call", methods=[
                dumpy.PyFunction(name="__init__", params=[
                    dumpy.PyParameter("label", ),
                    *args
                ])
            ]),
            dumpy.PyClass(name="Play", methods=[
                dumpy.PyFunction(name="__init__", params=[
                    dumpy.PyParameter("canal", ),
                    dumpy.PyParameter("resource", )
                ])
            ]),
            dumpy.PyClass(name="Stop", methods=[
                dumpy.PyFunction(name="__init__", params=[
                    dumpy.PyParameter("canal", ),
                ])
            ]),
            dumpy.PyClass(name="Null"),
            dumpy.PyClass(name="NullAction", parent=dumpy.Nameable(name="Action")),
            dumpy.PyClass(name="Return"),
            dumpy.PyClass(name="Gallery", methods=[
                dumpy.PyFunction(name="image", params=[
                    dumpy.PyParameter(name="displayable"),
                    *args
                ]),
                dumpy.PyFunction(name="condition", params=[
                    dumpy.PyParameter(name="condition"),
                    *args
                ]),
                dumpy.PyFunction(name="button", params=[
                    dumpy.PyParameter(name="name"),
                    *args
                ]),
                dumpy.PyFunction(name="make_button", params=[
                    dumpy.PyParameter("name"),
                    dumpy.PyParameter("disp"),
                    *args
                ], return_type="Button")
            ])
        ],
        packages=[
            renpy_pck
        ],
        files=[
            dumpy.PyFile(name="ui", functions=[
                dumpy.PyFunction(name="adjustment")
            ]),
            dumpy.PyFile(name="persistent", variables=[
                dumpy.PyVariable(name="gallerynpy_with_speed"),
                dumpy.PyVariable(name="gallerynpy_animation_speed")
            ]),
            dumpy.PyFile(name="config", variables=[
                dumpy.PyVariable(name="screen_width", value=1920),
                dumpy.PyVariable(name="screen_height", value=1080)
            ])
        ],
        import_all=False
    )

    store_pck.create()


def add_copyright():
    files = glob.glob("gallerynpy/**/*.py", recursive=True)
    gencopy.remove_from(files, release_year, "Yoimer Davila", repo)
    gencopy.add_to(files, release_year, "Yoimer Davila", repo)


def generate_rpy():
    """
    Copy the contents of the _ren.py files and pass them to an .rpy file according to the renpy instruction present in it.
    """
    files = glob.glob("gallerynpy/**/*.py", recursive=True)
    out = pathlib.Path(os.path.abspath("dist"))
    converts.to_rpyf(files, out_folder=str(out))
    gencopy.add_to(out.glob("**/*.rpy"), release_year, "Yoimer Davila", repo)


# generate_dumpy_renpy()
add_copyright()

generate_rpy()

