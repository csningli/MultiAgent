#! /Users/nil/anaconda3/envs/multiagent_2/bin/python

# copyright, 2018, NiL, csningli@gmail.com

import sys, os, time, datetime, pickle, copy, readline, sqlite3
from utils import *

class MultiAgentCommandLine :
    __promote = "CMA"
    __title = "Command Line for MultiAgent"
    __copyright = "(c) copyright 2018, NiL, csningli@gmail.com"
    __database = "./multiagent_commands.db"

    def __init__(self) :
        if os.path.exists(self.__database) :
            self.__con = sqlite3.connect(self.__database)
        else :
            self.__con = sqlite3.connect(self.__database)
            try :
                cur = self.__con.cursor()
                cur.execute("CREATE TABLE Commands(timelabel CHAR(20), content TEXT)")
                self.__con.commit()
            except sqlite3.Error, e:
                self.__con.rollback()

        cur = self.__con.cursor()
        cur.execute("SELECT * from Commands ORDER BY timelabel LIMIT 10")
        for record in cur.fetchall() :
            readline.add_history("req " + record[1].replace(';', ' '))

    def run(self) :
        print("%s | %s" % (self.__title, self.__copyright))
        print("=" * 50)
        while True :
            if sys.version_info[0] == 2 :
                line = raw_input("[\033[1m%s\033[0m] " % self.__promote).strip()
            elif sys.version_info[0] == 3 :
                line = input("[" + self.__promote + "] ").strip()
            else :
                break
            if len(line.strip()) > 0 and line.split(' ') > 1 :
                op = line.strip().split(' ')[0]
                msg = ' '.join(line.strip().split(' ')[1:])
                if op in ["q", "quit"] :
                    break
                elif op == "req" :
                    self.request(msg)

    def request(self, msg) :
        """
        None -> None
        Check Angine status.
        """
        try :
            cur = self.__con.cursor()
            cur.execute("INSERT INTO Commands VALUES (\"%s\", \"%s\")" % (timelabel(), msg))
            self.__con.commit()
            print("Added successfully.")
        except sqlite3.Error, e:
            self.__con.rollback()
            print("Error in adding the msg.")


if __name__ == '__main__' :
    c = MultiAgentCommandLine()
    c.run()
