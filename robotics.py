import os
import time
import random
import calendar
from datetime import datetime

from typing import Dict

from RPA.Browser.Selenium import Selenium
from constants import HTML_CONTENT, FILENAME, INTRO_TEXT

br = Selenium(auto_close=False)


class Robot:
    """
    Robot class blueprint that serves the purpose of communicating with browser and
    fetching/calculating/displaying scientists info.
    """

    def __init__(self, name):
        self.name = name

    def print_console_message(self, message):
        """
        CHAT-GPT STYLED TYPING EFFECT TO GIVE THE ROBOTIC VIBE
        """
        typing_speed = [0.01, 0.1]
        for char in message:
            print(char, end="", flush=True)
            rand_time = random.choice(typing_speed)
            time.sleep(rand_time)
        print()

    def introduce_robot(self):
        """
        Introduce robot and what steps it will take to perform the given task
        """
        self.print_console_message(f"Hello, my name is {self.name}!\n{INTRO_TEXT}")
        self.timer_before_execution()

    def timer_before_execution(self):
        """
        Add some drama before opening the browser
        """
        seconds = 3
        while seconds > 0:
            print(seconds)
            time.sleep(1)
            seconds -= 1

    def open_webpage(self, webpage):
        br.open_available_browser(webpage, maximized=True)

    def calculate_age(self, dob, dod):
        """
        subtract years between date of death and date of birth
        """
        return dod.year - dob.year

    def extract_date_string(self, string_list):
        """
        Date of birth for each scientists can be uncleaned:
            - meaning they will not be as easy as pick up and parse..
            - For some scientists, they will have preceding (Birth Name ~ Nickname) before their Date of Birth

        This method checks for the months in the string and when found returns the str with date
        """
        months = calendar.month_name[1:]
        date_str = ""
        for string in string_list:
            month_exists = [x in months for x in string.split()]
            date_str = string if any(month_exists) else date_str
        return date_str

    def parse_date(self, date_str):
        """
        Parse the date from list of string on scientist info
        """
        date_list = date_str.split()[:3]
        date_str = " ".join(date_list)
        parsed_date = datetime.strptime(date_str, "%d %B %Y")
        return parsed_date.date()

    def find_scientist_info(self, scientist) -> Dict:
        """
        returns dict of scientist info with keys:
            - dob (Retrieve the dates the scientists were born)
            - dod (Retrieve the dates the scientists died)
            - age (calculate their age)
            - info (retrieve the first paragraph of their wikipedia page)
        """
        br.input_text_when_element_is_visible('//input[@id="searchInput"]', scientist)
        br.click_element_if_visible(
            '//button[@class="pure-button pure-button-primary-progressive"]'
        )
        dob = br.get_webelements('//td[@class="infobox-data"]')[0].text.split("\n")
        dob_str = self.extract_date_string(dob)
        dob_dt = self.parse_date(dob_str)

        dod = br.get_webelements('//td[@class="infobox-data"]')[1].text.split("\n")
        dod_str = self.extract_date_string(dod)
        dod_dt = self.parse_date(dod_str)

        age = self.calculate_age(dob_dt, dod_dt)

        # find info until we get the non empty text from the p tag
        info = ""
        find_paragraph_counter = 0
        while info == "":
            info = br.get_webelements("//p")[find_paragraph_counter].text
            if len(info) > 0:
                break
            find_paragraph_counter += 1

        return {
            "dob": dob_dt.isoformat(),
            "dod": dod_dt.isoformat(),
            "age": age,
            "info": info,
        }

    def go_back(self):
        br.go_back()

    def write_html_page(self, elapsed, content):
        """
        Write to html page and save the output, replace the contents as required
        """
        updated_content = HTML_CONTENT.replace("{{ elapsed }}", str(round(elapsed, 2)))
        updated_content = updated_content.replace("{{ content }}", content)
        with open(FILENAME, "w") as file:
            file.write(updated_content)

    def dict_to_html(self, scientists_dict):
        """
        generate html tags around scientists dict data
        """
        scientists_html_content = ""
        for scientist in scientists_dict.keys():
            scientists_html_content += f"<div class='box'>"
            scientists_html_content += f"<h4 class='is-size-4'>{scientist}</h4>"
            scientists_html_content += f"<div>Birth: <span class='has-text-weight-bold'>{scientists_dict[scientist]['dob']}</span></div>"
            scientists_html_content += f"<div>Death: <span class='has-text-weight-bold'>{scientists_dict[scientist]['dod']}</span></div>"
            scientists_html_content += f"<div>Aged: <span class='has-text-weight-bold'>{scientists_dict[scientist]['age']} years</span></div>"
            scientists_html_content += (
                f"<p class='my-5 is-italic'>{scientists_dict[scientist]['info']}</p>"
            )
            scientists_html_content += f"</div>"
        return scientists_html_content

    def display_output_file(self):
        """
        go to output page
        """
        cwd = os.getcwd()
        br.go_to(f"file://{cwd}/{FILENAME}")
