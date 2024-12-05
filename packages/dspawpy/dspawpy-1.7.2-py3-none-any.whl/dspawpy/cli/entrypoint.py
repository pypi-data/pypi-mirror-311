print("... loading dspawpy cli ...")


def get_args():
    """Get command line arguments"""
    from argparse import ArgumentParser

    ap = ArgumentParser("dspawpy命令行交互小工具/cli")
    ap.add_argument("--hide", default=False, help="隐藏图标/hide logo")
    ap.add_argument("-c", "--check", default=False, help="检查新版本/check new version")
    ap.add_argument("-m", "--menu", default=None, help="选择菜单/select menu")
    ap.add_argument(
        "-l",
        "--language",
        default="CN",
        help="语言/language",
        choices=["CN", "EN"],
    )
    args = ap.parse_args()

    return args


def main():
    """Cli requires main function to run."""
    from loguru import logger

    from dspawpy.cli import auxiliary
    from dspawpy.cli.menu_prompts import Dresponse, Dupdate, logo, menus

    args = get_args()
    lan = args.language

    if not args.hide:
        logger.info(logo[lan])

    auxiliary.verify_dspawpy_version(args.check, lan)

    while True:
        if args.menu:
            menu = args.menu
        else:
            all_supported_tasks = [str(i + 1) for i in range(15)]  # 1-15
            all_supported_subtasks = [
                "31",
                "32",
                "33",
                "41",
                "42",
                "43",
                "44",
                "45",
                "46",
                "51",
                "52",
                "53",
                "54",
                "55",
                "56",
                "61",
                "62",
                "81",
                "82",
                "83",
                "84",
                "85",
                "86",
                "87",
                "91",
                "92",
                "93",
                "101",
                "102",
                "103",
                "104",
                "105",
                "131",
                "132",
                "151",
                "152",
            ]  # for program
            menu = auxiliary.get_input(
                menus[lan][0],
                all_supported_tasks + all_supported_subtasks + ["q"],
            )

        if menu == "1":
            D = {}
            cmd = "pip install -U dspawpy"
            yn = auxiliary.get_input(
                f"{Dupdate[lan][0]}\n {cmd}\n (y/n)? ",
                ["y", "n"],
                allow_empty=True,
                default_user_input="n",
            )
            D["menu"] = 1
            D["yn"] = yn
            if yn.lower() == "y":
                from os import system

                if system(cmd) == 0:
                    result = [f">>>>>> {Dupdate[lan][1]}", f"{Dupdate[lan][2]}"]
                else:
                    result = [f"!!!!!! {Dupdate[lan][3]}"]
                logger.info("\n".join(result))

        elif menu == "2":
            auxiliary.s2(lan)

        elif menu == "3":
            valid_selection = [str(i) for i in range(4)]
            submenu = auxiliary.get_input(menus[lan][3], valid_selection)
            if submenu == "1":
                auxiliary.s3_1(lan)
            elif submenu == "2":
                auxiliary.s3_2(lan)
            elif submenu == "3":
                auxiliary.s3_3(lan)
            else:
                continue
        elif menu == "31":
            auxiliary.s3_1(lan)
        elif menu == "32":
            auxiliary.s3_2(lan)
        elif menu == "33":
            auxiliary.s3_3(lan)

        elif menu == "4":
            valid_selection = [str(i) for i in range(7)]
            submenu = auxiliary.get_input(menus[lan][4], valid_selection)
            if submenu == "1":
                auxiliary.s4_1(lan)
            elif submenu == "2":
                auxiliary.s4_2(lan)
            elif submenu == "3":
                auxiliary.s4_3(lan)
            elif submenu == "4":
                auxiliary.s4_4(lan)
            elif submenu == "5":
                auxiliary.s4_5(lan)
            elif submenu == "6":
                auxiliary.s4_6(lan)
            else:
                continue
        elif menu == "41":
            auxiliary.s4_1(lan)
        elif menu == "42":
            auxiliary.s4_2(lan)
        elif menu == "43":
            auxiliary.s4_3(lan)
        elif menu == "44":
            auxiliary.s4_4(lan)
        elif menu == "45":
            auxiliary.s4_5(lan)
        elif menu == "46":
            auxiliary.s4_6(lan)

        elif menu == "5":
            valid_selection = [str(i) for i in range(7)]
            submenu = auxiliary.get_input(menus[lan][5], valid_selection)
            if submenu == "1":
                auxiliary.s5_1(lan)
            elif submenu == "2":
                auxiliary.s5_2(lan)
            elif submenu == "3":
                auxiliary.s5_3(lan)
            elif submenu == "4":
                auxiliary.s5_4(lan)
            elif submenu == "5":
                auxiliary.s5_5(lan)
            elif submenu == "6":
                auxiliary.s5_6(lan)
            else:
                continue
        elif menu == "51":
            auxiliary.s5_1(lan)
        elif menu == "52":
            auxiliary.s5_2(lan)
        elif menu == "53":
            auxiliary.s5_3(lan)
        elif menu == "54":
            auxiliary.s5_4(lan)
        elif menu == "55":
            auxiliary.s5_5(lan)
        elif menu == "56":
            auxiliary.s5_6(lan)

        elif menu == "6":
            valid_selection = [str(i) for i in range(3)]
            submenu = auxiliary.get_input(menus[lan][6], valid_selection)
            if submenu == "1":
                auxiliary.s6_1(lan)
            elif submenu == "2":
                auxiliary.s6_2(lan)
            else:
                continue
        elif menu == "61":
            auxiliary.s6_1(lan)
        elif menu == "62":
            auxiliary.s6_2(lan)

        elif menu == "7":
            auxiliary.s7(lan)

        elif menu == "8":
            valid_selection = [str(i) for i in range(8)]
            submenu = auxiliary.get_input(menus[lan][8], valid_selection)
            if submenu == "1":
                auxiliary.s8_1(lan)
            elif submenu == "2":
                auxiliary.s8_2(lan)
            elif submenu == "3":
                auxiliary.s8_3(lan)
            elif submenu == "4":
                auxiliary.s8_4(lan)
            elif submenu == "5":
                auxiliary.s8_5(lan)
            elif submenu == "6":
                auxiliary.s8_6(lan)
            elif submenu == "7":
                auxiliary.s8_7(lan)
            else:
                continue
        elif menu == "81":
            auxiliary.s8_1(lan)
        elif menu == "82":
            auxiliary.s8_2(lan)
        elif menu == "83":
            auxiliary.s8_3(lan)
        elif menu == "84":
            auxiliary.s8_4(lan)
        elif menu == "85":
            auxiliary.s8_5(lan)
        elif menu == "86":
            auxiliary.s8_6(lan)
        elif menu == "87":
            auxiliary.s8_7(lan)

        elif menu == "9":
            valid_selection = [str(i) for i in range(4)]
            submenu = auxiliary.get_input(menus[lan][9], valid_selection)
            if submenu == "1":
                auxiliary.s9_1(lan)
            elif submenu == "2":
                auxiliary.s9_2(lan)
            elif submenu == "3":
                auxiliary.s9_3(lan)
            else:
                continue
        elif menu == "91":
            auxiliary.s9_1(lan)
        elif menu == "92":
            auxiliary.s9_2(lan)
        elif menu == "93":
            auxiliary.s9_3(lan)

        elif menu == "10":
            valid_selection = [str(i) for i in range(6)]
            submenu = auxiliary.get_input(menus[lan][10], valid_selection)
            if submenu == "1":
                auxiliary.s10_1(lan)
            elif submenu == "2":
                auxiliary.s10_2(lan)
            elif submenu == "3":
                auxiliary.s10_3(lan)
            elif submenu == "4":
                auxiliary.s10_4(lan)
            elif submenu == "5":
                auxiliary.s10_5(lan)
            else:
                continue
        elif menu == "101":
            auxiliary.s10_1(lan)
        elif menu == "102":
            auxiliary.s10_2(lan)
        elif menu == "103":
            auxiliary.s10_3(lan)
        elif menu == "104":
            auxiliary.s10_4(lan)
        elif menu == "105":
            auxiliary.s10_5(lan)

        elif menu == "11":
            auxiliary.s11(lan)

        elif menu == "12":
            auxiliary.s12(lan)

        elif menu == "13":
            valid_selection = [str(i) for i in range(3)]
            submenu = auxiliary.get_input(menus[lan][13], valid_selection)
            if submenu == "1":
                auxiliary.s13_1(lan)
            elif submenu == "2":
                auxiliary.s13_2(lan)
            else:
                continue
        elif menu == "131":
            auxiliary.s13_1(lan)
        elif menu == "132":
            auxiliary.s13_2(lan)

        elif menu == "14":
            auxiliary.s14(lan)
        elif menu == "15":
            valid_selection = [str(i) for i in range(3)]
            submenu = auxiliary.get_input(menus[lan][15], valid_selection)
            if submenu == "1":
                auxiliary.s15_1(lan)
            elif submenu == "2":
                auxiliary.s15_2(lan)
            else:
                continue
        elif menu == "151":
            auxiliary.s15_1(lan)
        elif menu == "152":
            auxiliary.s15_2(lan)

        elif menu == "q":
            logger.info(Dresponse[lan][13])
            import sys

            sys.exit()

        icontinue = input(Dresponse[lan][14])
        if icontinue != "y":
            logger.info(Dresponse[lan][13])
            import sys

            sys.exit()


if __name__ == "__main__":
    main()
