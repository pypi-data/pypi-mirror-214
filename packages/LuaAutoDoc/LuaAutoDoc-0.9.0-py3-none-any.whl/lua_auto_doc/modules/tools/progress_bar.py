""" This module provides a progress bar class for use in the LuaAutoDoc tool."""

import sys
import multiprocessing
from typing import Union


# pylint: disable=too-many-instance-attributes, too-many-arguments, unused-variable
class ProgressBar:
    """ A progress bar class for use in the LuaAutoDoc tool. """
    def __init__(self, total, description='', count=0, progress_char='█', empty_char='|', width=80,
                 progress_colour='bright green', remaining_colour='red', description_colour='bright green',
                 pipe_rec_connection=None, pipe_send_connection=None):
        """ Initialises the progress bar.

        :param total: The total number of items to be processed.
        :param description: The description of the progress bar.
        :param count: The number of items already processed.
        :param progress_char: The character to use for the completed sections of the progress bar.
        :param empty_char: The character to use for the remaining sections of the progress bar.
        :param width: The width of the progress bar.
        :param progress_colour: The colour of the completed sections of the progress bar.
        :param remaining_colour: The colour of the remaining sections of the progress bar.
        :param description_colour: The colour of the description of the progress bar.
        :param pipe_rec_connection: The connection to the pipe to receive updates from other processes.
        :param pipe_send_connection: The connection to the pipe to send updates to other processes.
        """
        self.total = total
        self.count = count
        self.width = width
        self.description = description
        self.progress_char = progress_char
        self.empty_char = empty_char
        self.progress_colour = self.parse_colour(progress_colour)
        self.remaining_colour = self.parse_colour(remaining_colour)
        self.description_colour = self.parse_colour(description_colour)
        self.pipe_rec_connection = pipe_rec_connection
        self.pipe_send_connection = pipe_send_connection

        if self.pipe_rec_connection:
            self.progress_listener = multiprocessing.Process(target=self.process_listener)
            self.progress_listener.start()

    @staticmethod
    def parse_colour(colour: str) -> str:
        """ Returns the ANSI colour code for the given colour name.

        :param colour: The name of the colour to get the ANSI code for.

        :return: The ANSI colour code for the given colour name.
        """
        colour_dict: dict[str, str] = {
            'black': '\033[30m',
            'bright red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'purple': '\033[35m',
            'magenta': '\033[35m',
            'cyan': '\033[36m',
            'grey': '\033[37m',
            'white': '\033[37m',
            'bright black': '\033[90m',
            'red': '\033[91m',
            'bright green': '\033[92m',
            'bright yellow': '\033[93m',
            'bright blue': '\033[94m',
            'bright purple': '\033[95m',
            'bright magenta': '\033[95m',
            'bright cyan': '\033[96m',
            'bright white': '\033[97m',
        }
        if colour.lower() in colour_dict:
            return colour_dict[colour]
        if colour in colour_dict.values():
            return colour

        return ''

    def update(self, count=1) -> None:
        """ Updates the progress bar by the given count and prints it.

        :param count: The amount to update the progress bar by.
        """
        self.count += int(count)
        self.print()

    def start(self) -> None:
        """ Starts the progress bar. """
        self.print()

    def extra_info(self) -> str:
        """ Returns the extra information to be displayed in the progress bar.

        :return: The extra information to be displayed in the progress bar.
        """
        total_length: int = len(str(self.total))
        right_padding: str = ' ' * (total_length - len(str(self.total - self.count)))
        return f'{str(self.count).rjust(total_length)}/{self.total} - ' \
               f'{str(self.total - self.count)} remaining{right_padding}'

    def available_space(self) -> int:
        """ Returns the amount of space available for the progress bar.

        :return: The amount of space available for the progress bar.
        """
        return self.width - len(self.description) - len(self.extra_info()) - 4  # -4 for "[" and "]" and " "

    def print(self) -> None:
        """ Prints the progress bar. """
        end_colour: str = '\033[0m'
        available_space: int = self.available_space()

        completed_sections: str = self.progress_char * min(int(self.count / self.total * available_space),
                                                           available_space)
        remaining_sections: str = self.empty_char * (available_space - len(completed_sections))
        description: str = f'{self.description} ['
        extra_info: str = f'] {self.extra_info()}'

        if self.progress_colour:
            completed_sections = f'{self.progress_colour}{completed_sections}{end_colour}'
        if self.remaining_colour:
            remaining_sections = f'{self.remaining_colour}{remaining_sections}{end_colour}'
        if self.description_colour:
            description = f'{self.description_colour}{description}{end_colour}'
            extra_info = f'{self.description_colour}{extra_info}{end_colour}'

        print(f'\r{description}{completed_sections}{remaining_sections}{extra_info}', end='', flush=True)

        # Print a new line if the progress bar is complete.
        if self.count == self.total:
            print('', flush=True)

    def process_listener(self):
        """ Listens for updates from the other processes and updates the progress bar."""
        while self.count < self.total:
            signal: Union[int, str] = self.pipe_rec_connection.recv()
            if signal == 'close':
                sys.exit(0)
            else:
                self.update(signal)

    def close_listener(self):
        """ Closes the progress bar listener. """
        self.pipe_send_connection.send('close')
        self.progress_listener.join()

    def multiprocess_update(self, count: int) -> None:
        """ Sends the given count to the child process.

        :param count: The amount to update the progress bar by.
        """
        self.pipe_send_connection.send(count)

    def __getstate__(self):
        """ Returns the state of the object to be pickled.

        :return: The state of the object to be pickled.
        """
        return self.__dict__.copy()

    def __setstate__(self, state):
        """ Sets the state of the object to be unpickled.

        :param state: The state of the object to be unpickled.
        """
        self.__dict__.update(state)
# pylint: enable=too-many-instance-attributes, too-many-arguments, unused-variable
