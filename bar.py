import os,sys
import time
from datetime import datetime

# dian@duck.com

class ColorStr:

    green_start = "\N{ESC}[32m"
    gray_start = "\N{ESC}[90m"
    color_end   = "\u001b[0m"

    @classmethod
    def green(cls, s:str) -> str:
        return cls.green_start + s + cls.color_end

    @classmethod
    def gray(cls, s:str) -> str:
        return cls.gray_start + s + cls.color_end


class Money:
    def __init__(self,
                 work_days:float = 20,
                 month:float = 100,
                 daily:float = 3,
                 year:float = 1200,
                 start:float = 9,
                 end:float = 18):

        if daily:
            self.day = daily
        elif month:
            self.day = month / work_days
        elif year:
            self.day = year / (12 * work_days)
        else:
            raise ValueError("The salary is needed!")

        self.start_hour = int(start)
        self.start_min  = int(60 * (start - self.start_hour))

        self.end_hour = int(end)
        self.end_min  = int(60 * (end - self.end_hour))

        self._time_out = 600

        self.update_start_end()

    def update_start_end(self):
        now = datetime.now()
        self.last_update = now.timestamp()

        _s = now.replace(hour=self.start_hour, minute=self.start_min, second=0, microsecond=0)
        self.start = _s.timestamp()

        _e = now.replace(hour=self.end_hour, minute=self.end_min, second=0, microsecond=0)
        self.end = _e.timestamp()

        self.len = self.end - self.start

    def now(self):
        now = datetime.now().timestamp()
        
        if (now - self.last_update) > self._time_out:
            self.update_start_end()

        if now < self.start:
            return 0,0
        if now > self.end:
            return 1, self.day

        finish = (now - self.start) / self.len
        salary = finish * self.day
        return finish, salary

class Bar:
    sc = chr(27) + "[2J"
    label = "■"
    def __init__(self, salary: Money):
        os.system("clear")
        self.m = salary

    def format_str(self) -> str:
        total = os.get_terminal_size().columns - 15
        empty = ['' for i in range(total)]
        finish, money = self.m.now()
        count = int(finish * total)
        f_str = self.label.join(empty[:count])
        e_str = self.label.join(empty[count:])
        show_str = "\n" + ColorStr.green(f_str) +  ColorStr.gray(e_str) 
        show_str = show_str + " %.2f%% %.0f¥"%(finish * 100, money) + "\n"
        return show_str

    def run(self):
        while True:
            s = self.format_str()
            # sys.stdout.write("\033c")
            # sys.stdout.flush()
            print("\033c", end = "")
            sys.stdout.write(self.format_str())
            sys.stdout.flush()
            time.sleep(1)

def main():
    m = Money(daily = 100, start = 9, end = 18)
    bar = Bar(m)
    bar.run()


if __name__ == "__main__":
    main()
