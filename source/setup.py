import cx_Freeze

exes = [cx_Freeze.Executable("game.py")]

cx_Freeze.setup(
    name = "I_Have_Time",
    options = { "build.exe" : { "packages" : ["os", "random", "math", "pygame"],
                                "includes" : ["gameActors"],
                                "include_files" : ["images", "sounds"] }},
    executables = exes
)