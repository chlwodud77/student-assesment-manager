from cx_Freeze import setup, Executable
import sys

buildOptions = dict(packages = ["sys",
                                "PyQt5",
                                "sqlite3",
                                "random",
                                "openpyxl"],  # 1
	excludes = ["tkinter",
                "pytz",
                "notebook",
                "numpy",
                "numpydoc",
                "numexpr",
                "matplotlib",
                "lxml",
                "jupyter_client",
                "jupyter_core",
                "pandas",
                "PIL",
                "scipy"],
    include_files = ["classManage.py",
                    "backend.py",
                    "excelManage.py",
                    "scoreManage.py",
                    "subjectManage.py",
                    "studentManager.db",
                    "manager.ui",
                    "icon.ico"])

# 2
base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = [Executable("manager.py", base=base, icon="icon.ico")]

# 3
setup(
    name='Student Manage Application',
    version = "1.0",
    author = "jay",
    description = "",
    options = dict(build_exe = buildOptions),
    executables = exe
)