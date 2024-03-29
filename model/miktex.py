from os import environ, path
from sys import platform
import os, subprocess, pathlib

class MikTexNotFound(Exception):
    pass

class DirectoryNotFound(Exception):
    pass

class OSNotSupported(Exception):
    pass

class MikTex():
    """Statically processes all variables required to spawn a child process for miktex"""

    _engine = "pdflatex"
    _template = "template.tex"
    _silentmode = "--interaction=batchmode"
    _path = environ['PATH'].split(';')
    _exec = "{0}{1}".format(_engine,".exe") if ("win" in platform) else (_engine if ("linux" in platform) else "")
    mikTexPath = r""
    if(len(_exec) == 0):
        raise OSNotSupported("Interpreter only supports Windows and Linux platforms")

    mikTexPaths = [path.normpath(p) for p in _path if "miktex" in p.lower()]
    root = pathlib.Path(__file__).parent.absolute().parent.absolute()
    wdir = os.path.join(root, "Userfiles")

    #TODO: Potentially allow user to pick miktex installation?
    if (len(mikTexPaths) >= 1):
        mikTexPath = os.path.join(mikTexPaths[0], _exec)
        if not os.path.exists(mikTexPath):
            raise MikTexNotFound(f"No tex to pdf processor found in MikTex folder: {mikTexPath}")
    else:
        raise MikTexNotFound("No MikTex installation found in PATH")

    if not os.path.exists(wdir):
        raise DirectoryNotFound(f"Directory {wdir} could not be located")

    @staticmethod
    def write_to_pdf(program="", prooffound="False", stepstaken="0", proctime="", rulesused="", prooftree="", progname="helloworld", sequence=""):
        source = ""
        target = f"{''.join(progname.split()).lower()}.tex"
        with open(os.path.join(MikTex.wdir, MikTex._template), 'r') as temp:
            source = temp.read().replace('[program]', program).replace('[progname]', progname).replace('[prooffound]', str(prooffound)).replace("[stepstaken]", str(stepstaken)).replace('[proctime]', str(proctime)).replace('[rulesused]', rulesused).replace('[tree]', prooftree).replace('[sequence]', sequence)
        with open(os.path.join(MikTex.wdir, target), 'w') as temp:
            temp.write(source)
        mikTexThread = subprocess.Popen([MikTex._engine, MikTex._silentmode, target], cwd=MikTex.wdir)
        mikTexThread.wait()

