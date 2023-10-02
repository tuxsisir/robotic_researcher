import time
from robotics import Robot

from constants import WIKIPEDIA_LINK, SCIENTISTS
from typing import Tuple

robot = Robot("Quandrinaut")


def introduce_robot():
    """
    Give intro on the task and short info about the robo conducting the task
    """
    robot.introduce_robot()


def fetch_scientist_info() -> Tuple:
    """
    Opens up the browser and gather all the related scientist info for every scientists
    """
    result = {}
    st = time.time()
    try:
        robot.open_webpage(WIKIPEDIA_LINK)
    except Exception as ex:
        print(
            "Sorry, no internet connection! Please check on with your connection and run the script again. Thanks."
        )
        print(ex)
        return "Error in elapsed", {}
    for scientist in SCIENTISTS:
        result[scientist] = robot.find_scientist_info(scientist)
        robot.go_back()
    et = time.time()
    elapsed = et - st
    return elapsed, result


def save_output(elapsed, results):
    """
    Saves output to output.html where user can view accumulated results
    """
    scientist_html_content = robot.dict_to_html(results)
    robot.write_html_page(elapsed, scientist_html_content)


def display_results():
    """
    display the output page to the user
    """
    robot.display_output_file()


def main():
    introduce_robot()
    elapsed, results = fetch_scientist_info()
    save_output(elapsed, results)
    display_results()


if __name__ == "__main__":
    main()
