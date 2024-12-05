import os
import sys
import threading
from typing import Literal, Optional, Tuple

from loguru import logger
from prompt_toolkit import prompt
from prompt_toolkit.completion import (
    Completer,
    FuzzyCompleter,
    PathCompleter,
    WordCompleter,
)

from dspawpy.cli.menu_prompts import Dcheck, Dio, Dparameter, Dresponse, Dselect

pc = FuzzyCompleter(PathCompleter(expanduser=True))  # path completion
pc_h5 = FuzzyCompleter(
    PathCompleter(expanduser=True, file_filter=lambda p: p.endswith(".h5"))
)  # path completion


class HidePrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def save_figure_dpi300(outfile: str, plt=None):
    """Save matplotlib figure with dpi=300"""
    logger.info(" Saving figure with dpi=300...")
    if plt is None:
        import matplotlib.pyplot as plt

    absfile = os.path.abspath(outfile)
    os.makedirs(os.path.dirname(absfile), exist_ok=True)
    plt.tight_layout()
    plt.savefig(absfile, dpi=300)
    logger.info(f"--> {absfile}")


def get_input(
    user_prompt: str,
    valid_inputs: list,
    completer: Optional[Completer] = None,
    allow_empty: bool = False,
    default_user_input: str = "",
) -> str:
    """Until user give valid input, or return default input if allow_empty is True and user input is empty."""
    if completer is None:
        completer = FuzzyCompleter(WordCompleter(valid_inputs))  # list completion
    from prompt_toolkit import prompt

    while True:
        user_input: str = prompt(user_prompt, completer=completer).strip()
        if allow_empty and len(user_input) == 0:
            return default_user_input
        elif user_input not in valid_inputs:
            continue
        else:
            return user_input


def get_inputs(
    user_prompt: str,
    valid_inputs: list,
    completer: Optional[Completer] = None,
    allow_empty: bool = False,
) -> list:
    """Return valid_inputs list if given empty"""
    if completer is None:
        completer = FuzzyCompleter(WordCompleter(valid_inputs))  # list completion
    from prompt_toolkit import prompt

    while True:
        user_inputs: list = prompt(user_prompt, completer=completer).strip().split()

        if allow_empty and len(user_inputs) == 0:
            return valid_inputs
        else:
            valid = True
            for n in user_inputs:
                if n not in valid_inputs:
                    valid = False
                    break
            if valid:
                return user_inputs
            else:
                continue


def get_lims(
    user_prompt: str,
    language: Literal["EN", "CN"],
) -> Optional[Tuple[float, float]]:
    """Get lower and higher limits from user input"""
    while True:
        userInput = input(user_prompt).strip()
        if userInput == "":
            return None
        elif " " not in userInput:
            logger.warning(f"!!! {userInput}{Dresponse[language][0]}")
            continue
        elif len(userInput.split(" ")) != 2:
            logger.warning(f"!!! {userInput}{Dresponse[language][1]}")
            continue
        else:
            try:
                lims = userInput.split(" ")
                lower = float(lims[0])
                higher = float(lims[1])
                return lower, higher

            except Exception:
                logger.warning(f"!!! {userInput}{Dresponse[language][2]}")
                continue


def pre_ele_band(language: Literal["EN", "CN"]):
    def imp():
        global get_band_data, BSPlotter
        from pymatgen.electronic_structure.plotter import BSPlotter

        from dspawpy.io.read import get_band_data

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["inf"] = prompt(Dio[language]["band"], completer=pc)
    D["ylims"] = get_lims(Dparameter[language][10], language)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc) or "band.png"

    import_thread.join()
    logger.info(Dio[language]["import"])

    band_data = get_band_data(D["inf"])
    logger.debug("got data, initializing plotter...")
    bsp = BSPlotter(band_data)
    logger.debug("plotter initialized")

    return bsp, band_data, D


def pre_ele_pband(language: Literal["EN", "CN"]):
    def imp():
        global get_band_data, BSPlotterProjected
        from pymatgen.electronic_structure.plotter import BSPlotterProjected

        from dspawpy.io.read import get_band_data

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["inf"] = prompt(Dio[language]["pband"], completer=pc)
    D["ylims"] = get_lims(Dparameter[language][10], language)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc) or "band_projected.png"

    import_thread.join()
    logger.info(Dio[language]["import"])

    band_data = get_band_data(D["inf"])
    logger.debug("got data, initializing plotter...")
    bsp = BSPlotterProjected(band_data)
    logger.debug("plotter initialized")

    return bsp, band_data, D


def pre_ph_band(language: Literal["EN", "CN"]):
    def imp():
        global get_phonon_band_data, PhononBSPlotter
        from dspawpy.io.read import get_phonon_band_data

        with HidePrints():
            from pymatgen.phonon.plotter import PhononBSPlotter

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["inf"] = prompt(Dio[language]["phband"], completer=pc)
    D["ylims"] = get_lims(Dparameter[language][10], language)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc) or "ph_band.png"

    import_thread.join()
    logger.info(Dio[language]["import"])

    band_data = get_phonon_band_data(D["inf"])
    logger.debug("got data, initializing plotter...")
    bsp = PhononBSPlotter(band_data)
    logger.debug("plotter initialized")

    return bsp, band_data, D


def pre_ele_dos(language: Literal["EN", "CN"]):
    def imp():
        global DosPlotter, get_dos_data
        from pymatgen.electronic_structure.plotter import DosPlotter

        from dspawpy.io.read import get_dos_data

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["inf"] = prompt(Dio[language]["dos"], completer=pc)
    D["xlims"] = get_lims(Dparameter[language][9], language)
    D["ylims"] = get_lims(Dparameter[language][10], language)
    D["shift"] = get_input(Dselect[language][3], ["y", "n"])
    D["figure"] = prompt(Dio[language]["figure"], completer=pc) or "dos.png"

    import_thread.join()
    logger.info(Dio[language]["import"])

    dos_data = get_dos_data(D["inf"])
    logger.debug("got data, initializing plotter...")
    if D["shift"] == "y":
        dos_plotter = DosPlotter(stack=False, zero_at_efermi=True)
    else:
        dos_plotter = DosPlotter(stack=False, zero_at_efermi=True)
    logger.debug("plotter initialized")

    return dos_plotter, dos_data, D


def pre_ele_pdos(language: Literal["EN", "CN"]):
    def imp():
        global DosPlotter, get_dos_data, CompleteDos
        from pymatgen.electronic_structure.dos import CompleteDos
        from pymatgen.electronic_structure.plotter import DosPlotter

        from dspawpy.io.read import get_dos_data

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["inf"] = prompt(Dio[language]["pdos"], completer=pc)
    D["xlims"] = get_lims(Dparameter[language][9], language)
    D["ylims"] = get_lims(Dparameter[language][10], language)
    D["shift"] = get_input(Dselect[language][3], ["y", "n"])
    D["figure"] = prompt(Dio[language]["figure"], completer=pc) or "pdos.png"

    import_thread.join()
    logger.info(Dio[language]["import"])
    dos_data = get_dos_data(D["inf"])
    logger.debug("got data, initializing plotter...")
    if D["shift"] == "y":
        dos_plotter = DosPlotter(stack=False, zero_at_efermi=True)
    else:
        dos_plotter = DosPlotter(stack=False, zero_at_efermi=True)
    logger.debug("plotter initialized")

    return dos_plotter, dos_data, D


def pre_ph_dos(language: Literal["EN", "CN"]):
    def imp():
        global PhononDosPlotter, get_phonon_dos_data
        from dspawpy.io.read import get_phonon_dos_data

        with HidePrints():
            from pymatgen.phonon.plotter import PhononDosPlotter

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["inf"] = prompt(Dio[language]["phdos"], completer=pc)
    D["xlims"] = get_lims(Dparameter[language][9], language)
    D["ylims"] = get_lims(Dparameter[language][10], language)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc) or "ph_dos.png"
    import_thread.join()
    logger.info(Dio[language]["import"])

    dos_data = get_phonon_dos_data(D["inf"])
    logger.debug("got data, initializing plotter...")
    dos_plotter = PhononDosPlotter(stack=False, sigma=None)
    logger.debug("plotter initialized")

    return dos_plotter, dos_data, D


def online_check(local_dspawpy_version: str, language: Literal["EN", "CN"]):
    """Fetch latses version of dspawpy from pypi"""
    latest_version = None
    # requests is dependency of pymatgen
    from os.path import expanduser

    from requests import exceptions, get

    try:
        logger.info(Dcheck[language][0])
        response = get("https://pypi.org/pypi/dspawpy/json", timeout=3)
        latest_version = response.json()["info"]["version"]
        error_message = None
    except ModuleNotFoundError:
        error_message = Dcheck[language][1]
    except exceptions.Timeout:
        error_message = Dcheck[language][2]
    except exceptions.RequestException as e:
        error_message = f"{Dcheck[language][3]} {e}"
    except Exception as e:
        error_message = f"{Dcheck[language][4]} {e}"
    finally:
        if latest_version:
            if latest_version != local_dspawpy_version:
                logger.info(
                    f"{latest_version} > {local_dspawpy_version}; {Dcheck[language][1]}",
                )
            else:
                logger.info(
                    f"{latest_version} = {local_dspawpy_version}; {Dcheck[language][6]}",
                )

            with open(expanduser("~/.dspawpy_latest_version"), "w") as fin:
                fin.write(latest_version)
        else:
            logger.info(Dcheck[language][7])

    return error_message


def verify_dspawpy_version(check: bool, language: Literal["EN", "CN"]):
    """May skip online check"""
    from os.path import dirname, expanduser, isfile

    import dspawpy

    home = expanduser("~")

    dv = dspawpy.__version__
    df = dirname(dspawpy.__file__).replace(home, "~", 1)

    logger.info(f"{dv}: {df}")

    error_message = None
    if check:
        if isfile(expanduser("~/.dspawpy_latest_version")):
            with open(expanduser("~/.dspawpy_latest_version")) as fin:
                latest_version = fin.read().strip()
            if dv != latest_version:
                error_message = online_check(dv, language)
        else:
            error_message = online_check(dv, language)

        if error_message is not None:
            logger.info(error_message)


def s2(language: Literal["EN", "CN"]):
    """structure结构转化"""

    def imp():
        global convert
        from dspawpy.io.structure import convert

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["menu"] = 2
    D["in"] = prompt(Dio[language]["ins"], completer=pc)
    D["out"] = prompt(Dio[language]["outs"], completer=pc)
    import_thread.join()
    logger.info(Dio[language]["import"])

    convert(infile=D["in"], outfile=D["out"])


def s3_1(language: Literal["EN", "CN"]):
    """volumetricData可视化"""

    def imp():
        global write_VESTA
        from dspawpy.io.write import write_VESTA

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["menu"] = 31
    D["inf"] = prompt(Dio[language]["inf"], completer=pc)
    supported_tasks = ["rho", "potential", "elf", "pcharge", "rhoBound"]
    D["task"] = None
    for task in supported_tasks:
        if task in D["inf"]:
            D["task"] = task
            break
    if not D["task"]:
        D["task"] = get_input(
            f"{supported_tasks}: ",
            supported_tasks,
            completer=WordCompleter(supported_tasks),
        )

    subtype = None
    if D["task"] == "potential":
        if D["inf"].endswith(".h5"):
            from dspawpy.io.read import load_h5

            data = load_h5(D["inf"])
            keys = [k.split("/")[-1] for k in data.keys() if k.startswith("/Potential")]

            if len(keys) == 0:
                raise ValueError(f"{Dresponse[language][3]}{D['infile']}")
            elif len(keys) == 1:
                subtype = keys[0]
            else:
                subtype = get_input(
                    f"{Dselect[language][0]} {keys}: ",
                    keys,
                    completer=WordCompleter(keys),
                )

        elif D["inf"].endswith(".json"):
            from json import load

            with open(D["inf"]) as fin:
                data = load(fin)
                if "Potential" not in data.keys():
                    raise ValueError(f"{Dresponse[language][3]} {D['infile']}")
                keys = [k for k in data["Potential"].keys()]

            if len(keys) == 1:
                subtype = keys[0]
            else:
                subtype = get_input(
                    f"{Dselect[language][0]} {keys}",
                    keys,
                    completer=WordCompleter(keys),
                )
        else:
            raise ValueError(Dresponse[language][2])

    D["outfile"] = prompt(Dio[language]["outf"], completer=pc)

    import_thread.join()
    logger.info(Dio[language]["import"])
    write_VESTA(
        in_filename=D["inf"],
        data_type=D["task"],
        out_filename=D["outfile"],
        subtype=subtype,
    )
    logger.info(Dresponse[language][5])


def s3_2(language: Literal["EN", "CN"]):
    """差分volumetricData可视化"""

    def imp():
        global write_delta_rho_vesta
        from dspawpy.io.write import write_delta_rho_vesta

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["menu"] = 32
    D["total"] = prompt(Dio[language]["tcharge"], completer=pc)
    D["individuals"] = []
    while True:
        individual = prompt(
            Dio[language]["pcharge"],
            completer=pc,
        )
        if individual == "":
            break
        D["individuals"].append(individual)

    supported_tasks = ["rho", "potential", "elf", "pcharge", "rhoBound"]
    D["task"] = None
    for task in supported_tasks:
        if task in D["total"]:
            D["task"] = task
            break
    if not D["task"]:
        D["task"] = get_input(
            f"{supported_tasks}: ",
            supported_tasks,
            completer=WordCompleter(supported_tasks),
        )
    D["outfile"] = prompt(Dio[language]["outf"], completer=pc)

    import_thread.join()
    logger.info(Dio[language]["import"])
    write_delta_rho_vesta(
        total=D["total"],
        individuals=D["individuals"],
        output=D["outfile"],
        data_type=D["task"],
    )
    logger.info(Dresponse[language][5])


def s3_3(language: Literal["EN", "CN"]):
    """volumetricData面平均"""

    def imp():
        global plt, average_along_axis

        import matplotlib.pyplot as plt

        from dspawpy.plot import average_along_axis

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["menu"] = 33
    D["inf"] = prompt(Dio[language]["inf"], completer=pc)
    D["axes"] = get_inputs(Dselect[language][1], ["0", "1", "2"])
    _list = ["rho", "potential", "elf", "pcharge", "rhoBound"]
    D["task"] = get_input(
        f"{_list}: ",
        _list,
        completer=WordCompleter(_list),
    )

    D["subtype"] = None
    if D["task"] == "rho":
        k = "TotalCharge"
    elif D["task"] == "potential":
        if D["inf"].endswith(".h5"):
            from dspawpy.io.read import load_h5

            data = load_h5(D["inf"])
            keys = [k.split("/")[-1] for k in data.keys() if k.startswith("/Potential")]

            if len(keys) == 0:
                raise ValueError(f"{Dresponse[language][3]}{D['infile']}")
            elif len(keys) == 1:
                D["subtype"] = keys[0]
            else:
                D["subtype"] = get_input(
                    Dselect[language][0],
                    keys,
                    completer=WordCompleter(keys),
                )

        elif D["inf"].endswith(".json"):
            from json import load

            with open(D["inf"]) as fin:
                data = load(fin)
                if "Potential" not in data.keys():
                    raise ValueError(f"{Dresponse[language][3]}{D['infile']}")
                keys = [k for k in data["Potential"].keys()]

            if len(keys) == 1:
                D["subtype"] = keys[0]
            else:
                D["subtype"] = get_input(
                    Dselect[language][0],
                    keys,
                    completer=WordCompleter(keys),
                )
        else:
            raise ValueError(Dresponse[language][4])
        k = D["subtype"]
    elif D["task"] == "elf":
        k = "TotalELF"
    elif D["task"] == "pcharge":
        k = "TotalCharge"
    elif D["task"] == "rhoBound":
        k = "Rho"
    else:
        raise ValueError(D["task"])

    ax_indices = [int(a) for a in D["axes"]]
    import_thread.join()
    logger.info(Dio[language]["import"])
    for ai in ax_indices:
        average_along_axis(
            datafile=D["inf"],
            task=D["task"],
            axis=ai,
            subtype=D["subtype"],
            label=f"axis{ai}",
        )
    if len(ax_indices) > 1:
        plt.legend()

    plt.xlabel("Grid Index")
    plt.ylabel(k)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc)

    save_figure_dpi300(D["figure"], plt)


def s4_1(language: Literal["EN", "CN"]):
    """普通能带"""
    bsp, band_data, D = pre_ele_band(language)
    D["menu"] = 41

    is_metal = band_data.is_metal()
    if is_metal:
        bsp.get_plot(ylim=D["ylims"])
    else:
        D["shift"] = get_input(Dselect[language][3], ["y", "n"])
        if D["shift"] == "y":
            from pymatgen.electronic_structure.plotter import BSPlotter

            from dspawpy.io.read import get_band_data

            band_data = get_band_data(D["inf"], zero_to_efermi=True)
            bsp = BSPlotter(band_data)
            bsp.get_plot(False, ylim=D["ylims"])
        else:
            bsp.get_plot(ylim=D["ylims"])

    save_figure_dpi300(D["figure"])


def s4_2(language: Literal["EN", "CN"]):
    """将能带投影到每一种元素分别作图，数据点大小表示该元素对该轨道的贡献"""
    bsp, band_data, D = pre_ele_pband(language)
    D["menu"] = 42

    is_metal = band_data.is_metal()
    if is_metal:
        bsp.get_elt_projected_plots(ylim=D["ylims"])
    else:
        D["shift"] = get_input(Dselect[language][3], ["y", "n"])
        if D["shift"] == "y":
            from pymatgen.electronic_structure.plotter import BSPlotterProjected

            from dspawpy.io.read import get_band_data

            band_data = get_band_data(D["inf"], zero_to_efermi=True)
            bsp = BSPlotterProjected(band_data)
            bsp.get_elt_projected_plots(ylim=D["ylims"])
        else:
            bsp.get_elt_projected_plots(ylim=D["ylims"])

    save_figure_dpi300(D["figure"])


def s4_3(language: Literal["EN", "CN"]):
    """能带投影到不同元素的不同轨道"""
    bsp, band_data, D = pre_ele_pband(language)
    D["menu"] = 43

    banddatatructure = band_data.structure
    assert banddatatructure is not None
    logger.info(banddatatructure)
    es = banddatatructure.composition.elements
    D["dictio"] = {}

    from pymatgen.core import Element

    while True:
        _e = get_input(Dselect[language][4], [str(e) for e in es], allow_empty=True)
        if _e == "":
            break
        e = Element(_e)

        available_orbitals = ["s"]
        orbitals = e.atomic_orbitals
        assert isinstance(orbitals, dict)
        for o in orbitals:
            if "p" in o:
                available_orbitals.append("p")
            elif "d" in o:
                available_orbitals.append("d")
            elif "f" in o:
                available_orbitals.append("f")
        unique_orbitals = list(set(available_orbitals))
        _o = get_input(Dselect[language][5], unique_orbitals)
        _os = _o.split(" ")
        dict_eo = {_e: _os}
        # update dictio
        D["dictio"].update(dict_eo)

    is_metal = band_data.is_metal()
    if is_metal:
        bsp.get_projected_plots_dots(D["dictio"])
    else:
        D["shift"] = get_input(Dselect[language][3], ["y", "n"])
        if D["shift"] == "y":
            from pymatgen.electronic_structure.plotter import BSPlotterProjected

            from dspawpy.io.read import get_band_data

            band_data = get_band_data(D["inf"], zero_to_efermi=True)
            bsp = BSPlotterProjected(band_data)
            bsp.get_projected_plots_dots(D["dictio"], False, ylim=D["ylims"])
        else:
            bsp.get_projected_plots_dots(D["dictio"], ylim=D["ylims"])

    save_figure_dpi300(D["figure"])


def s4_4(language: Literal["EN", "CN"]):
    """将能带投影到不同原子的不同轨道"""
    bsp, band_data, D = pre_ele_pband(language)
    D["menu"] = 44

    banddatatructure = band_data.structure
    assert banddatatructure is not None
    logger.info(banddatatructure)
    sites = banddatatructure.sites
    ns = [str(i) for i in range(len(sites))]
    D["dictio"] = {}
    D["dictpa"] = {}
    while True:
        _n = get_input(Dselect[language][6], ns, allow_empty=True)
        if _n == "":
            break
        _e = sites[int(_n)].specie
        available_orbitals = ["s"]
        orbitals = _e.atomic_orbitals
        assert orbitals is not None
        for o in orbitals:
            if "p" in o:
                available_orbitals.append("p")
                available_orbitals.append("px")
                available_orbitals.append("py")
                available_orbitals.append("pz")
            elif "d" in o:
                available_orbitals.append("d")
                available_orbitals.append("dxy")
                available_orbitals.append("dyz")
                available_orbitals.append("dxz")
                available_orbitals.append("dx2")
                available_orbitals.append("dz2")
            elif "f" in o:
                available_orbitals.append("f")
                available_orbitals.append("f_3")
                available_orbitals.append("f_2")
                available_orbitals.append("f_1")
                available_orbitals.append("f0")
                available_orbitals.append("f1")
                available_orbitals.append("f2")
                available_orbitals.append("f3")

        unique_orbitals = list(set(available_orbitals))
        D["dictpa"].update({str(_e): [int(_n) + 2]})
        _os = get_inputs(Dselect[language][7], unique_orbitals)
        dict_eo = {str(_e): _os}
        # update dictio
        D["dictio"].update(dict_eo)

    logger.info(f"dictpa: {D['dictpa']}")
    logger.info(f"dictio: {D['dictio']}")

    is_metal = band_data.is_metal()
    if is_metal:
        bsp.get_projected_plots_dots_patom_pmorb(
            D["dictio"],
            D["dictpa"],
            ylim=D["ylims"],
        )
    else:
        D["shift"] = get_input(Dselect[language][3], ["y", "n"])
        if D["shift"] == "y":
            from pymatgen.electronic_structure.plotter import BSPlotterProjected

            from dspawpy.io.read import get_band_data

            band_data = get_band_data(D["inf"], zero_to_efermi=True)

            bsp = BSPlotterProjected(band_data)
            bsp.get_projected_plots_dots_patom_pmorb(
                D["dictio"],
                D["dictpa"],
                zero_to_efermi=False,
                ylim=D["ylims"],
            )
        else:
            bsp.get_projected_plots_dots_patom_pmorb(
                D["dictio"],
                D["dictpa"],
                ylim=D["ylims"],
            )

    save_figure_dpi300(D["figure"])


def s4_5(language: Literal["EN", "CN"]):
    """能带反折叠处理"""

    def imp():
        global plot_bandunfolding, plt
        import matplotlib.pyplot as plt

        from dspawpy.plot import plot_bandunfolding

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    bsp, band_data, D = pre_ele_pband(language)
    D["menu"] = 45
    import_thread.join()
    logger.info(Dio[language]["import"])

    plt = plot_bandunfolding(D["inf"])
    plt.ylim(D["ylims"])
    save_figure_dpi300(D["figure"], plt)


def s4_6(language: Literal["EN", "CN"]):
    """band-compare能带对比图处理"""

    def imp():
        global get_band_data, BSPlotter
        from pymatgen.electronic_structure.plotter import BSPlotter

        from dspawpy.io.read import get_band_data

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    bsp, band_data, D = pre_ele_band(language)
    D["menu"] = 46
    D["infile2"] = prompt(Dio[language]["wband"], completer=pc)
    if D["infile2"].endswith(".json"):
        D["infile3"] = prompt(
            Dio[language]["sysjson"],
            completer=pc,
        )
        D["infile2"] = [D["infile2"], D["infile3"]]
    import_thread.join()
    logger.info(Dio[language]["import"])

    if isinstance(D["infile2"], list):
        bd1 = get_band_data(D["infile2"][0], D["infile2"][1])
    else:  # str
        bd1 = get_band_data(D["infile2"])
    assert bd1 is not None, Dresponse[language][6]
    bsp = BSPlotter(bs=bd1)
    bsp2 = BSPlotter(bs=band_data)
    bsp.add_bs(bsp2._bs)
    bsp.get_plot(bs_labels=["wannier interpolated", "DFT"], ylim=D["ylims"])
    save_figure_dpi300(D["figure"])


def s5_1(language: Literal["EN", "CN"]):
    """总的态密度"""
    dos_plotter, dos_data, D = pre_ele_dos(language)
    D["menu"] = 51
    dos_plotter.add_dos("total dos", dos=dos_data)
    dos_plotter.get_plot(xlim=D["xlims"], ylim=D["ylims"])
    save_figure_dpi300(D["figure"])


def s5_2(language: Literal["EN", "CN"]):
    """将态密度投影到不同的轨道上"""
    dos_plotter, dos_data, D = pre_ele_pdos(language)
    D["menu"] = 52
    dos_plotter.add_dos_dict(dos_data.get_spd_dos())
    dos_plotter.get_plot(xlim=D["xlims"], ylim=D["ylims"])
    save_figure_dpi300(D["figure"])


def s5_3(language: Literal["EN", "CN"]):
    """将态密度投影到不同的元素上"""
    dos_plotter, dos_data, D = pre_ele_pdos(language)
    D["menu"] = 53
    dos_plotter.add_dos_dict(dos_data.get_element_dos())
    dos_plotter.get_plot(xlim=D["xlims"], ylim=D["ylims"])
    save_figure_dpi300(D["figure"])


def s5_4(language: Literal["EN", "CN"]):
    """将态密度投影到不同原子的不同轨道上"""

    def imp():
        global Orbital
        from pymatgen.electronic_structure.core import Orbital

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    dos_plotter, dos_data, D = pre_ele_pdos(language)
    D["menu"] = 54
    logger.info(dos_data.structure)
    sites = dos_data.structure.sites
    numbers = [str(i) for i in range(len(sites))]

    D["ns"] = []
    D["oss"] = []
    _e = None
    while True:
        _n = get_input(Dselect[language][6], numbers, allow_empty=True)
        if _n == "":
            break
        available_orbitals = ["s"]
        _e = sites[int(_n)].specie
        orbitals = _e.atomic_orbitals
        assert isinstance(orbitals, dict)
        for o in orbitals:
            if "p" in o:
                available_orbitals.append("p")
                available_orbitals.append("px")
                available_orbitals.append("py")
                available_orbitals.append("pz")
            elif "d" in o:
                available_orbitals.append("d")
                available_orbitals.append("dxy")
                available_orbitals.append("dyz")
                available_orbitals.append("dxz")
                available_orbitals.append("dx2")
                available_orbitals.append("dz2")
            elif "f" in o:
                available_orbitals.append("f")
                available_orbitals.append("f_3")
                available_orbitals.append("f_2")
                available_orbitals.append("f_1")
                available_orbitals.append("f0")
                available_orbitals.append("f1")
                available_orbitals.append("f2")
                available_orbitals.append("f3")
        unique_orbitals = list(set(available_orbitals))
        _os = get_inputs(Dselect[language][7], unique_orbitals)
        D["ns"].append(_n)
        D["oss"].append(_os)

    assert _e is not None
    import_thread.join()
    logger.info(Dio[language]["import"])
    for _n, _os in zip(D["ns"], D["oss"]):
        for _orb in _os:
            logger.info(f"atom-{_n} {_orb}")
            dos_plotter.add_dos(
                f"{_e}(atom-{_n}) {_orb}",  # label
                dos_data.get_site_orbital_dos(
                    dos_data.structure[int(_n)],
                    getattr(Orbital, _orb),
                ),
            )
    dos_plotter.get_plot(xlim=D["xlims"], ylim=D["ylims"])
    save_figure_dpi300(D["figure"])


def s5_5(language: Literal["EN", "CN"]):
    """将态密度投影到不同原子的分裂d轨道(t2g, eg)上"""
    dos_plotter, dos_data, D = pre_ele_pdos(language)
    D["menu"] = 55
    logger.info(dos_data.structure)
    sites = dos_data.structure.sites
    numbers = [str(e) for e in range(len(sites))]
    D["ais"] = get_input(Dselect[language][6], numbers)

    atom_indices = [int(ai) for ai in D["ais"].split()]
    for atom_index in atom_indices:
        dos_plotter.add_dos_dict(
            dos_data.get_site_t2g_eg_resolved_dos(dos_data.structure[atom_index]),
        )

    dos_plotter.get_plot(xlim=D["xlims"], ylim=D["ylims"])
    save_figure_dpi300(D["figure"])


def s5_6(language: Literal["EN", "CN"]):
    """d-带中心分析"""

    def imp():
        global get_dos_data, d_band

        from dspawpy.io.read import get_dos_data
        from dspawpy.io.utils import d_band

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 56
    D["inf"] = prompt(Dio[language]["pdos"], completer=pc)
    D["outfile"] = prompt(Dio[language]["txt"], completer=pc)
    import_thread.join()
    logger.info(Dio[language]["import"])

    dos_data = get_dos_data(D["inf"])
    os.makedirs(os.path.dirname(os.path.abspath(D["outfile"])), exist_ok=True)
    with open(D["outfile"], "w") as f:
        for spin in dos_data.densities:
            # up, down = (1, -1)
            if spin.value == 1:
                s = "up"
            elif spin.value == -1:
                s = "down"
            else:
                raise ValueError(f"Unknown spin: {spin}")
            logger.info("spin=", s)
            f.write(f"spin={s}\n")
            c = d_band(spin, dos_data)
            f.write(str(c) + "\n")
            logger.info(c)


def s6_1(language: Literal["EN", "CN"]):
    """将能带和态密度显示在一张图上"""

    def imp():
        global BSDOSPlotter, pltbd, get_band_data, get_dos_data
        from pymatgen.electronic_structure.plotter import BSDOSPlotter

        from dspawpy.io.read import get_band_data, get_dos_data
        from dspawpy.plot import pltbd

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["menu"] = 61
    D["bandf"] = prompt(Dio[language]["band"], completer=pc)
    D["dosf"] = prompt(Dio[language]["dos"], completer=pc)
    D["ylims"] = get_lims(Dparameter[language][10], language)
    D["outfile"] = prompt(Dio[language]["figure"], completer=pc)
    import_thread.join()
    logger.info(Dio[language]["import"])

    band_data = get_band_data(D["bandf"])
    dos_data = get_dos_data(D["dosf"])

    bdp = BSDOSPlotter(bs_projection=None, dos_projection=None)  # pyright: ignore [reportArgumentType]

    pltbd(bdp, band_data, dos_data, ylim=D["ylims"], filename=D["outfile"])  # type: ignore


def s6_2(language: Literal["EN", "CN"]):
    """将能带和投影态密度显示在一张图上"""

    def imp():
        global BSDOSPlotter, pltbd, get_band_data, get_dos_data
        from pymatgen.electronic_structure.plotter import BSDOSPlotter

        from dspawpy.io.read import get_band_data, get_dos_data
        from dspawpy.plot import pltbd

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 61
    D["bandf"] = prompt(Dio[language]["band"], completer=pc)
    D["dosf"] = prompt(Dio[language]["dos"], completer=pc)
    D["ylims"] = get_lims(Dparameter[language][10], language)
    D["outfile"] = prompt(Dio[language]["figure"], completer=pc)
    projs = ["elements"]
    D["pband"] = get_input(
        Dselect[language][17],
        projs,
        completer=WordCompleter(projs),
        allow_empty=True,
    )
    projs2 = ["elements", "orbitals"]
    D["pdos"] = get_input(
        Dselect[language][17],
        projs2,
        completer=WordCompleter(projs2),
        allow_empty=True,
    )
    import_thread.join()
    logger.info(Dio[language]["import"])

    band_data = get_band_data(D["bandf"])
    dos_data = get_dos_data(D["dosf"])

    bdp = BSDOSPlotter(bs_projection=D["pband"], dos_projection=D["pdos"])

    pltbd(bdp, band_data, dos_data, ylim=D["ylims"], filename=D["outfile"])  # type: ignore


def s7(language: Literal["EN", "CN"]):
    """optical光学性质数据处理"""

    def imp():
        global plot_optical, makedirs
        from os import makedirs

        from dspawpy.plot import plot_optical

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 7
    D["inf"] = prompt(Dio[language]["optical"], completer=pc)
    _list = [
        "AbsorptionCoefficient",
        "ExtinctionCoefficient",
        "RefractiveIndex",
        "Reflectance",
    ]
    D["keys"] = get_inputs(
        Dselect[language][15],
        _list,
        completer=WordCompleter(_list),
        allow_empty=True,
    )
    _list2 = ["X", "Y", "Z", "XY", "YZ", "ZX"]
    D["label"] = get_inputs(
        Dselect[language][16],
        _list2,
        completer=WordCompleter(_list2),
        allow_empty=True,
    )

    D["outd"] = prompt(Dio[language]["outd"], completer=pc)
    import_thread.join()
    logger.info(Dio[language]["import"])

    if D["outd"].strip() != "":
        makedirs(D["outd"], exist_ok=True)
    plot_optical(datafile=D["inf"], keys=D["keys"], axes=D["label"], prefix=D["outd"])


def s8_1(language: Literal["EN", "CN"]):
    """输入文件之生成中间构型"""

    def imp():
        global NEB, write_neb_structures, read

        from dspawpy.diffusion.neb import NEB, write_neb_structures
        from dspawpy.io.structure import read

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["menu"] = 81
    D["inits"] = prompt(Dio[language]["inits"], completer=pc)
    D["fins"] = prompt(Dio[language]["fins"], completer=pc)
    D["nmiddle"] = int(input(Dparameter[language][8]))
    D["method"] = get_input(Dselect[language][9], ["IDPP", "Linear"])
    D["outd"] = prompt(Dio[language]["outd"], completer=pc)

    if D["outd"] == "":
        D["outd"] = "."

    import_thread.join()
    logger.info(Dio[language]["import"])
    init_struct = read(D["inits"])[0]
    final_struct = read(D["fins"])[0]

    neb = NEB(init_struct, final_struct, D["nmiddle"] + 2)
    if D["method"] == "Linear":
        structures = neb.linear_interpolate()
    else:
        try:
            structures = neb.idpp_interpolate()
        except Exception:
            logger.error(Dresponse[language][7])
            structures = neb.linear_interpolate()
            logger.warning(Dresponse[language][8])

    absdir = os.path.abspath(D["outd"])
    os.makedirs(os.path.dirname(absdir), exist_ok=True)
    write_neb_structures(structures, fmt="as", path=absdir)
    logger.info(f"{Dresponse[language][9]} {D['outd']}")

    yn = get_input(Dselect[language][10], ["y", "n"])
    if yn.lower().startswith("y"):
        from dspawpy.diffusion.nebtools import write_json_chain, write_xyz_chain

        write_xyz_chain(preview=True, directory=absdir)
        write_json_chain(preview=True, directory=absdir)


def s8_2(language: Literal["EN", "CN"]):
    """绘制能垒图"""

    def imp():
        global plot_barrier

        from dspawpy.diffusion.nebtools import plot_barrier

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 82
    D["ind"] = prompt(Dio[language]["neb"], completer=pc)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc)
    logger.info(Dresponse[language][10])
    import_thread.join()
    logger.info(Dio[language]["import"])

    if os.path.isdir(D["ind"]):
        plot_barrier(directory=D["ind"], figname=D["figure"], show=False)
    elif os.path.isfile(D["ind"]):
        plot_barrier(datafile=D["ind"], figname=D["figure"], show=False)
    else:
        raise TypeError(D["inf"])


def s8_3(language: Literal["EN", "CN"]):
    """过渡态计算概览"""

    def imp():
        global summary

        from dspawpy.diffusion.nebtools import summary

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 82
    D["ind"] = prompt(Dio[language]["nebdir"], completer=pc)
    D["outd"] = prompt(Dio[language]["outd"], completer=pc)
    import_thread.join()
    logger.info(Dio[language]["import"])

    assert os.path.isdir(D["ind"])
    absdir = os.path.abspath(D["outd"])
    os.makedirs(os.path.dirname(absdir), exist_ok=True)
    summary(
        directory=D["ind"],
        outdir=absdir,
        figname=f"{absdir}/neb_summary.png",
        show=False,
    )


def s8_4(language: Literal["EN", "CN"]):
    """NEB链可视化"""

    def imp():
        global write_json_chain, write_xyz_chain
        from dspawpy.diffusion.nebtools import write_json_chain, write_xyz_chain

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 84
    D["yn"] = get_input(Dselect[language][10], ["y", "n"])
    D["ind"] = prompt(Dio[language]["nebdir"], completer=pc)
    if D["yn"] == "y":
        step = 0
    else:
        step = int(input(Dselect[language][11]))
    dst = prompt(Dio[language]["outd"], completer=pc)
    import_thread.join()
    logger.info(Dio[language]["import"])

    write_xyz_chain(False, D["ind"], step, dst)
    write_json_chain(False, D["ind"], step, dst)


def s8_5(language: Literal["EN", "CN"]):
    """计算构型间距"""

    def imp():
        global read, get_distance
        from dspawpy.diffusion.nebtools import get_distance
        from dspawpy.io.structure import read

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 85
    D["infile1"] = prompt(Dparameter[language][12], completer=pc)
    D["infile2"] = prompt(Dparameter[language][13], completer=pc)
    import_thread.join()
    logger.info(Dio[language]["import"])
    s1 = read(D["infile1"])[0]
    s2 = read(D["infile2"])[0]
    result = get_distance(
        s1.frac_coords,
        s2.frac_coords,
        s1.lattice.matrix,
        s2.lattice.matrix,
    )
    logger.info(str(result))


def s8_6(language: Literal["EN", "CN"]):
    """neb续算"""

    def imp():
        global restart
        from dspawpy.diffusion.nebtools import restart

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 86
    D["ind"] = prompt(Dio[language]["neb"], completer=pc)
    D["outd"] = prompt(Dio[language]["outd"], completer=pc)
    import_thread.join()
    logger.info(Dio[language]["import"])
    restart(D["ind"], D["outd"])


def s8_7(language: Literal["EN", "CN"]):
    """neb计算过程中受力和能量的收敛趋势图"""

    def imp():
        global monitor_force_energy
        from dspawpy.diffusion.nebtools import monitor_force_energy

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 87
    D["ind"] = prompt(Dio[language]["neb_can_be_unfinished"], completer=pc)
    D["fig_dir"] = prompt(Dio[language]["fig_dir"], completer=pc)
    import_thread.join()
    logger.info(Dio[language]["import"])
    monitor_force_energy(D["ind"], D["fig_dir"])


def s9_1(language: Literal["EN", "CN"]):
    """声子能带数据处理"""
    bsp, band_data, D = pre_ph_band(language)
    D["menu"] = 91
    bsp.get_plot(ylim=D["ylims"])  # pyright: ignore [reportArgumentType]
    save_figure_dpi300(D["figure"])


def s9_2(language: Literal["EN", "CN"]):
    """声子态密度数据处理"""
    dos_plotter, dos_data, D = pre_ph_dos(language)
    D["menu"] = 92
    dos_plotter.add_dos(label="Phonon", dos=dos_data)
    dos_plotter.get_plot(
        xlim=D["xlims"],  # pyright: ignore [reportArgumentType]
        ylim=D["ylims"],  # pyright: ignore [reportArgumentType]
        units="thz",
    )

    save_figure_dpi300(D["figure"])


def s9_3(language: Literal["EN", "CN"]):
    """声子热力学数据处理"""

    def imp():
        global plot_phonon_thermal
        from dspawpy.plot import plot_phonon_thermal

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 93
    D["inf"] = prompt(Dio[language]["inf"], completer=pc)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc)
    import_thread.join()
    logger.info(Dio[language]["import"])

    plot_phonon_thermal(D["inf"], D["figure"], False)


def s10_1(language: Literal["EN", "CN"]):
    """轨迹文件转换格式为.xyz或.dump"""

    def imp():
        global convert
        from dspawpy.io.structure import convert

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 101
    D["inf"] = prompt(Dio[language]["inf"], completer=pc)
    D["outf"] = prompt(Dio[language]["outf"], completer=pc)
    import_thread.join()
    logger.info(Dio[language]["import"])
    convert(D["inf"], outfile=D["outf"])


def s10_2(language: Literal["EN", "CN"]):
    """动力学过程中能量、温度等变化曲线"""

    def imp():
        global plot_aimd
        from dspawpy.plot import plot_aimd

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 102
    D["inf"] = prompt(Dio[language]["inf"], completer=pc)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc)
    import_thread.join()
    logger.info(Dio[language]["import"])
    plot_aimd(D["inf"], show=False, figname=D["figure"])


def s10_3(language: Literal["EN", "CN"]):
    """均方位移（MSD）"""

    def imp():
        global MSD, _get_time_step, plot_msd, read, np
        import numpy as np

        from dspawpy.analysis.aimdtools import MSD, _get_time_step, plot_msd
        from dspawpy.io.structure import read

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 103
    D["inf"] = prompt(Dio[language]["inf"], completer=pc)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc)
    D["msdtype"] = (
        get_input(Dselect[language][12], ["xyz", "xy", "xz", "yz", "x", "y", "z", ""])
        or "xyz"
    )
    if D["msdtype"] == "":
        D["msdtype"] = "xyz"

    D["timestep"] = input(Dparameter[language][0])
    D["xlims"] = get_lims(Dparameter[language][9], language)
    D["ylims"] = get_lims(Dparameter[language][10], language)

    import_thread.join()
    logger.info(Dio[language]["import"])
    structures = read(D["inf"])
    initial_structure = structures[0]
    logger.info(initial_structure)
    unique_elements = list(set(str(s) for s in initial_structure.species))
    unique_atomic_numbers = [str(i) for i in range(len(initial_structure.sites))]
    select_str = get_input(
        Dselect[language][8],
        unique_elements + unique_atomic_numbers + [""],
    )
    if select_str == "":
        D["select"] = "all"
    elif ":" in select_str:  # slice, '1:3', '1:3:2'
        D["select"] = select_str
    elif " " in select_str:  # list of symbols or atom indices, '1 2 3', 'H He Li'
        raw_list = select_str.split()
        if all([i.isdigit() for i in raw_list]):
            D["select"] = [int(i) for i in raw_list]
        elif all([i in unique_elements for i in raw_list]):
            D["select"] = raw_list
        else:
            raise ValueError(select_str)
    elif select_str in unique_elements:
        D["select"] = select_str  # symbol
    elif select_str.isdigit():
        D["select"] = int(select_str)  # atom index
    else:
        raise ValueError(select_str)

    logger.info(D["select"])

    if D["timestep"] == "":
        if isinstance(D["inf"], str) or len(D["inf"]) == 1:
            ts = _get_time_step(D["inf"])
        else:
            logger.warning(Dresponse[language][12])
            ts = 1.0
    else:
        ts = float(D["timestep"])

    msd_calculator = MSD(structures, D["select"], D["msdtype"])
    msd = msd_calculator.run()

    xs = np.arange(msd_calculator.n_frames) * ts
    plot_msd(xs, msd, D["xlims"], D["ylims"], figname=D["figure"], show=False)


def s10_4(language: Literal["EN", "CN"]):
    """均方根偏差（RMSD）"""

    def imp():
        global get_lagtime_rmsd, plot_rmsd
        from dspawpy.analysis.aimdtools import get_lagtime_rmsd, plot_rmsd

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 104
    D["inf"] = prompt(Dio[language]["inf"], completer=pc)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc)
    D["timestep"] = input(Dparameter[language][0])
    if D["timestep"] == "":
        D["timestep"] = None
    else:
        D["timestep"] = float(D["timestep"])
    D["xlims"] = get_lims(Dparameter[language][9], language)
    D["ylims"] = get_lims(Dparameter[language][10], language)
    import_thread.join()
    logger.info(Dio[language]["import"])

    lagtime, rmsd = get_lagtime_rmsd(D["inf"], D["timestep"])
    plot_rmsd(lagtime, rmsd, D["xlims"], D["ylims"], D["figure"], False)


def s10_5(language: Literal["EN", "CN"]):
    """径向分布函数（RDF）"""

    def imp():
        global get_rs_rdfs, plot_rdf, read
        from dspawpy.analysis.aimdtools import get_rs_rdfs, plot_rdf
        from dspawpy.io.structure import read

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 105
    D["inf"] = prompt(Dio[language]["inf"], completer=pc)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc)
    D["rmin"] = float(input(Dparameter[language][1]) or 0)
    D["rmax"] = float(input(Dparameter[language][2]) or 10)
    D["ngrid"] = int(input(Dparameter[language][3]) or 101)
    D["sigma"] = float(input(Dparameter[language][4]) or 0)
    D["xlims"] = [D["rmin"], D["rmax"]]
    D["ylims"] = get_lims(Dparameter[language][10], language)

    import_thread.join()
    logger.info(Dio[language]["import"])
    strs = read(datafile=D["inf"])
    logger.info(f"{strs[0]}")
    unique_elements = list(set([str(i) for i in strs[0].species]))
    ele1 = get_input(Dselect[language][13], unique_elements)
    ele2 = get_input(Dselect[language][14], unique_elements)
    rs, rdfs = get_rs_rdfs(
        D["inf"],
        ele1,
        ele2,
        D["rmin"],
        D["rmax"],
        D["ngrid"],
        D["sigma"],
    )
    plot_rdf(rs, rdfs, ele1, ele2, D["xlims"], D["ylims"], D["figure"], False)


def s11(language: Literal["EN", "CN"]):
    """Polarization铁电极化数据处理"""

    def imp():
        global plot_polarization_figure
        from dspawpy.plot import plot_polarization_figure

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 11
    D["inf"] = prompt(Dio[language]["polarization"], completer=pc)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc)
    D["rep"] = int(input(Dparameter[language][5]) or 2)
    import_thread.join()
    logger.info(Dio[language]["import"])

    plot_polarization_figure(D["inf"], D["rep"], figname=D["figure"], show=False)


def s12(language: Literal["EN", "CN"]):
    """ZPE零点振动能数据处理"""

    def imp():
        global getZPE
        from dspawpy.io.utils import getZPE

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 12
    D["inf"] = prompt(Dio[language]["txt"], completer=pc)
    import_thread.join()
    logger.info(Dio[language]["import"])

    getZPE(D["inf"])


def s13_1(language: Literal["EN", "CN"]):
    """吸附质"""

    def imp():
        global getTSads
        from dspawpy.io.utils import getTSads

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 131
    D["inf"] = prompt(Dio[language]["txt"], completer=pc)
    D["T"] = float(input(Dparameter[language][6]) or 298.15)
    import_thread.join()
    logger.info(Dio[language]["import"])

    getTSads(D["inf"], D["T"])


def s13_2(language: Literal["EN", "CN"]):
    """理想气体"""

    def imp():
        global getTSgas
        from dspawpy.io.utils import getTSgas

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 132
    D["inf"] = prompt(Dio[language]["txt"], completer=pc)
    D["dataf"] = prompt(Dio[language]["datafile"], completer=pc)
    D["T"] = float(input(Dparameter[language][6]) or 298.15)
    D["P"] = float(input(Dparameter[language][7]) or 101325.0)
    import_thread.join()
    logger.info(Dio[language]["import"])

    getTSgas(
        fretxt=D["inf"],
        datafile=D["dataf"],
        temperature=D["T"],
        pressure=D["P"],
    )


def s14(language: Literal["EN", "CN"]):
    def imp():
        global parse_relax_data
        from dspawpy.io.read import parse_relax_data

    import_thread = threading.Thread(target=imp)
    import_thread.start()
    D = {}
    D["menu"] = 14
    D["logfile"] = prompt(Dio[language]["logfile"], completer=pc)

    D["printef"] = True if prompt(Dselect[language][20]).startswith("y") else False
    D["relative"] = False
    if D["printef"]:
        D["relative"] = True if prompt(Dselect[language][21]).startswith("y") else False

    D["writetraj"] = True if prompt(Dselect[language][22]).startswith("y") else False
    D["xyzfilename"] = None
    if D["writetraj"]:
        D["xyzfilename"] = prompt(Dio[language]["xyzfilename"], completer=pc)

    D["writeas"] = True if prompt(Dselect[language][23]).startswith("y") else False
    D["asfilename"] = None
    if D["writeas"]:
        D["asfilename"] = prompt(Dio[language]["asfilename"], completer=pc)

    import_thread.join()
    logger.info(Dio[language]["import"])

    parse_relax_data(
        D["logfile"],
        D["printef"],
        D["relative"],
        D["writetraj"],
        D["xyzfilename"],
        D["writeas"],
        D["asfilename"],
    )


def s15_1(language: Literal["EN", "CN"]):
    """查看hdf5数据结构.

    h5glance name.h5
    """

    D = {}
    D["menu"] = 151
    D["h5file"] = prompt(Dio[language]["h5file"], completer=pc_h5)
    os.system(f'h5glance {D["h5file"]}')


def s15_2(language: Literal["EN", "CN"]):
    """查看hdf5数据内容.

    支持查看单个key的数据，unix系统也支持查看全部key的数据（用less翻页）
    windows系统没有less，会直接打印出全部内容
    （建议直接使用HDFViewer窗口程序而不是dspawpy查看）

    h5glance name.h5 -
    ptdump -d name.h5
    """

    D = {}
    D["menu"] = 152
    D["h5file"] = prompt(Dio[language]["h5file"], completer=pc_h5)
    D["is_all"] = prompt(Dselect[language][18])
    if D["is_all"] == "y":
        from platform import system

        # requires PyTables, `pip install tables`
        if system() == "Windows":
            cmd = f"ptdump -d {D['h5file']}"
        else:
            cmd = f"ptdump -d {D['h5file']} | less"

        os.system(cmd)
    else:
        while True:
            logger.info(Dresponse[language][15])
            cmd = f'h5glance {D["h5file"]} -'
            os.system(cmd)
            if prompt(Dselect[language][19]) != "y":
                break


def s16(language: Literal["EN", "CN"]):
    pass
