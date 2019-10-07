import discord, pytz
from discord.ext import commands
from datetime import datetime, date

tz = pytz.timezone('Asia/Tokyo')

bot_name = "TimeTable Bot"

club_index_to_text = {
            0: "MYP Chill Out",
            1: "Imperial Assault",
            2: "Tinker Thinker Reader",
            3: "Band Advanced",
            4: "Let's Get Active",
            5: "Calligraphy",
            6: "Touch Footy",
            7: "Role 20",
            8: "Music Video",
            9: "Model Kit Construction",
            10: "Ikebana",
            11: "Modern Survival Skills",
            12: "Basketball"
        }

valid_inputs = (
    ("chi", "chill", "chill out", "myp chill out"),
    ("imp", "imperial assault", "star wars", "star wars imperial assault"),
    ("ttr", "tinker thinker reader", "homework"),
    ("bnd", "band", "advanced band"),
    ("lga", "let's get active"),
    ("cal", "calligraphy"),
    ("fty", "footy", "touch footy"),
    ("r20", "role 20"),
    ("mus", "music video"),
    ("mkc", "model", "model kit", "model kit construction", "model construction"),
    ("ike", "ikebana"),
    ("mss", "survival skills", "modern survival skills"),
    ("bsk", "basketball")
)



default_value = "56423198687468321576"
owner_id = "402344993391640578"

weekdays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
weekdays_lower = ("monday", "tuesday", "wednesday", "thursday", "friday")
weekdays_short = ("mon", "tue", "wed", "thu", "fri")

all_days = weekdays_short + weekdays_lower

day_indices = {
        "mon": 0,
        "monday": 0,
        "tue": 1,
        "tuesday": 1,
        "wed": 2,
        "wednesday": 2,
        "thu": 3,
        "thursday": 3,
        "fri": 4,
        "friday": 4,
    }

day_index_to_text = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

sp_NULL = "No class"
sp_NUCL = "No club"
sp_HMRM = "homeroom"
sp_AMRE = "morning recess"
sp_LNCH = "lunch"
sp_LNRE = "lunch recess"
sp_PMRE = "afternoon recess"


def GetUserGrade(id):
    with open("data/users.txt", "r") as file:
        temp = eval(file.read())
        if id in temp["7"]:
            return "7"
        elif id in temp["8"]:
            return "8"
        elif id in temp["9"]:
            return "9"
        else:
            return "null"


def GetUserClub(id, day):
    ClubList = (
        "MYP Chill Out",
        "Imperial Assault",
        "Tinker Thinker Reader",
        "Band Advanced",
        "Let's Get Active",
        "Calligraphy",
        "Touch Footy",
        "Role 20",
        "Music Video",
        "Model Kit Construction",
        "Ikebana",
        "Modern Survival Skills",
        "Basketball"
    )
    with open("data/clubs.txt", "r") as file:
        clubdata = eval(str(file.read()))
    if Day("text") == "Saturday" or Day("text") == "Sunday":
        return sp_NUCL
    count = 0
    if day == "today":
        for club in clubdata:
            if id in clubdata[club][int(Day("index"))]:
                return ClubList[count]
            count += 1
    else:
        for club in clubdata:
            if id in clubdata[club][day]:
                return ClubList[count]
            count += 1

    return sp_NUCL


def GetCurrentPeriod():
    periods = {
        "Morning": "Morning",
        "Period1": 0,
        "Period2": 1,
        "Period3": 2,
        "Period4": 3,
        "Period5": 4,
        "MorningRecess": sp_AMRE,
        "Lunch": sp_LNCH,
        "LunchRecess": sp_LNRE,
        "AfternoonRecess": sp_PMRE,
        "NoClass": sp_NULL,
        "Homeroom": sp_HMRM,
        "Club": "Club",
        "Evening": "Evening"
    }
    time = datetime.now(tz).hour + datetime.now(tz).minute / 60
    if time < 9.0:
        return periods["Morning"]
    elif time < 10.0:
        return periods["Period1"]
    elif time < 11.0:
        return periods["Period2"]
    elif time < 11.5:
        return periods["MorningRecess"]
    elif time < 12.5:
        return periods["Period3"]
    elif time < 13.0:
        return periods["Lunch"]
    elif time < 13.5:
        return periods["LunchRecess"]
    elif time < 14.5:
        return periods["Period4"]
    elif time < 14.75:
        return periods["AfternoonRecess"]
    elif time < 15.75:
        return periods["Period5"]
    elif time < 16.0:
        return periods["Homeroom"]
    elif time < 17.0:
        return periods["Club"]
    else:
        return periods["Evening"]


def CurrentPeriod(id):
    if Day("text") == "Saturday" or Day("text") == "Sunday":
        return sp_NULL
    if type(GetCurrentPeriod()) is int:
        with open("data/tt/" + str(GetUserGrade(id)) + ".txt", "r") as file:
            return eval(file.readline())[Day("index")][GetCurrentPeriod()]
    elif GetCurrentPeriod() == "Club":
        if GetUserClub(id, "today") == "No club":
            return sp_NULL
        return GetUserClub(id, "today")
    elif GetCurrentPeriod() == "Morning":
        with open("data/tt/" + str(GetUserGrade(id)) + ".txt", "r") as file:
            return eval(file.readline())[Day("index")][GetCurrentPeriod()]
    else:
        return GetCurrentPeriod()


def NextPeriod(id):
    NextPeriods = {
        "Morning": 0,
        0: 1,
        1: sp_AMRE,
        sp_AMRE: 2,
        2: sp_LNCH,
        sp_LNCH: sp_LNRE,
        sp_LNRE: 3,
        3: sp_PMRE,
        sp_PMRE: 4,
        4: sp_HMRM,
        sp_HMRM: "Club",
        "Club": "NextDay",
        "Evening": "NextDay"
    }
    UserGrade = GetUserGrade(id)
    Period = NextPeriods[GetCurrentPeriod()]
    with open("data/tt/" + UserGrade + ".txt", "r") as file:
        if Period == "Club":
            return GetUserClub(id, "today")
        elif Period == "NextDay":
            if Day("text") == "Friday" or Day("text") == "Saturday":
                return eval(file.readline())[0][0] + " (next Monday)"
            elif Day("text") == "Sunday":
                return eval(file.readline())[0][0] + " (tomorrow)"
            else:
                return eval(file.readline())[Day("index") + 1][0] + " (tomorrow)"
        elif type(Period) is int:
            return eval(file.readline())[Day("index")][Period]
        else:
            return Period


def TimeFormatted():
    if str(datetime.now(tz).hour).__len__() == 0:
        return "0" + str(datetime.now(tz).hour) + ":" + str(datetime.now(tz).minute)
    else:
        return str(datetime.now(tz).hour) + ":" + str(datetime.now(tz).minute)


def Day(type):
    if type == "text":
        return weekdays[date.weekday(datetime.now(tz))]
    elif type == "index":
        return date.weekday(datetime.now(tz))


def Date():
    basedate = str(datetime.now(tz))[8] + str(datetime.now(tz))[9]
    if basedate[0] == "0":
        basedate = basedate[1]
    if len(basedate) == 2 and basedate[0] == "1":
        return basedate + "th"
    elif len(basedate) == 2:
        if basedate[1] == "1":
            return basedate + "st"
        elif basedate[1] == "2":
            return basedate + "nd"
        elif basedate[1] == "3":
            return basedate + "rd"
        else:
            return basedate + "th"
    elif len(basedate) == 1:
        if basedate == "1":
            return basedate + "st"
        elif basedate == "2":
            return basedate + "nd"
        elif basedate == "3":
            return basedate + "rd"
        else:
            return basedate + "th"


def Month(type):
    months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    basemonth = date.today().month - 1
    if type == "text":
        return months[basemonth]
    elif type == "index":
        return str(basemonth)


def MainCommandOutput(id):
    output = ""
    output += "Today is " + Day("text") + " the " + Date() + " of " + Month("text") + " " + str(datetime.now(tz).year) + ". The time is " + TimeFormatted()

    if CurrentPeriod(id) == sp_NULL:
        output += "\n \nThere is nothing scheduled for your current period"
    else:
        output += "\n \nYour current period is " + CurrentPeriod(id)
    if GetUserClub(id, "today") == sp_NUCL:
        output += "\nYour next sceduled period is " + NextPeriod(id) + "\n \nYou do not have a club today"
    else:
        output += "\nYour next sceduled period is " + NextPeriod(id) + "\n \nYour club today is " + GetUserClub(id, "today") + " club"
    return output


def ListToString(list):
    output = "  -"
    for value in list:
        output += str(value) + "\n  -"
    return output[:-1]


def ClubInput(input):


    for day in all_days:
        input = input.replace(day, "")

    clubs_on_multiple_days = {
        12: ("tue", "tuesday", "friday", "fri"),
        0: ("tue", "tuesday", "friday", "fri"),
        2: ("mon", "monday", "tue", "tuesday", "thu", "thursday", "fri", "friday")
    }

    count = 0
    for club in valid_inputs:
        if str(input) in club:
            return count
        count += 1
    return "null"


# COMMANDS:
def SetUserGrade(id, grade):
    indices = {
        "7": 0,
        "8": 1,
        "9": 2,
    }
    with open("data/users.txt", "r") as file:
        temp = eval(file.readline())
    temp[str(grade)].append(str(id))
    with open("data/users.txt", "w") as file:
        file.write(str(temp))


def SetUserClub(id, club, day):

    with open("data/clubs.txt", "r") as file:
        temp = eval(str(file.readline()))

    temp[valid_inputs[club][0]][day].append(id)

    with open("data/clubs.txt", "w") as file:
        file.write(str(temp))


def DayView(id, inp):
    parameter = str.lower(inp)
    with open("data/tt/" + str(GetUserGrade(id)) + ".txt", "r") as file:
        if parameter == default_value or parameter == "tod" or parameter == "today":
            return eval(file.readline())[Day("index")]
        elif parameter == "tom" or parameter == "tomorrow":
            if Day("text") == "Friday" or Day("text") == "Saturday" or Day("text") == "Sunday":
                return eval(file.readline())[0]
            else:
                return eval(file.readline())[Day("index") + 1]
        else:
            return eval(file.readline())[day_indices[parameter]]


client = commands.Bot(command_prefix=".")


@client.event
async def on_ready():
    print(bot_name + " is now running")
    await client.change_presence(activity=discord.Game("Use '.tt ?' for info"))


@client.command(pass_context=True)
async def tt(ctx, modeinp=default_value, input_1=default_value, input_2=default_value, *, input_3=default_value):
    mode = str.lower(modeinp)
    id = str(ctx.message.author.id)
    message_prefix = ctx.message.author.mention + "  (G" + GetUserGrade(id) + ")  |  "
    if GetUserGrade(id) == "null" and mode != "setgrade":
        await ctx.send(ctx.message.author.mention + "  |  Hello and welcome!\n \nTo get started, type **.tt setgrade  X**, where **X** is your grade as a number")
    elif mode == "setgrade":
        if str(input_1) == "9" or str(input_1) == "8" or str(input_1) == "7":
            SetUserGrade(id, str(input_1))
            if GetUserGrade(id) == "null":
                await ctx.send(message_prefix + "Thank you! You have been set as grade " + str(input_1) + "\n \nUse **.tt ?** for information about this bot")
            else:
                await ctx.send(ctx.message.author.mention + "  |  You have been set as grade " + str(input_1))
    elif mode == default_value:
        await ctx.send(message_prefix + MainCommandOutput(id))
    elif mode == "day":
        day_alts = {
            "mon": "Monday",
            "monday": "Monday",
            "tue": "Tuesday",
            "tuesday": "Tuesday",
            "wed": "Wednesday",
            "wednesday": "Wednesday",
            "thu": "Thursday",
            "thursday": "Thursday",
            "fri": "Friday",
            "friday": "Friday",
        }
        valid_parameters = (default_value, "tod", "today", "tom", "tomorrow") + weekdays_lower + weekdays_short
        input = str.lower(input_1)
        if input in valid_parameters:
            if input in (weekdays_lower or weekdays_short):
                await ctx.send(message_prefix + "Your timetable on " + day_alts[input] + " is:\n \n" + ListToString(DayView(id, input))
                               + "\nYour club on this day is " + GetUserClub(id, day_indices[input]) + " club")
            elif input == "tod" or input == "today" or input == default_value:
                await ctx.send(message_prefix + "Your timetable for today is:\n \n" + ListToString(DayView(id, input))
                               + "\nYour club today is " + GetUserClub(id, "today") + " club")
            elif input == "tom" or input == "tomorrow":
                if Day("text") == "Friday" or Day("text") == "Saturday":
                    await ctx.send(message_prefix + "Your timetable for next Monday is:\n \n" + ListToString(DayView(id, input))
                                   + "\nYour club on this day is " + GetUserClub(id, 0) + " club")
                else:
                    await ctx.send(message_prefix + "Your timetable for tomorrow is:\n \n" + ListToString(DayView(id, input))
                                   + "\nYour club on this day is " + GetUserClub(id, day_indices[str.lower(Day("text"))] + 1) + " club")
        else:
            await ctx.send(message_prefix + "That is not the correct use of this command\n Use **.tt ?** for information about how to use commands")
    elif mode == "setclub":
        temp = str.lower(input_1) + str.lower(input_2) + str.lower(input_3)
        # .tt setclub (DAY) CLUB
        # () = optional
        temp = temp.replace(" club", "")
        temp = temp.replace(default_value, "")

        clubs_on_multiple_days = {
            12: ("tue", "tuesday", "friday", "fri"),
            0: ("tue", "tuesday", "friday", "fri"),
            2: ("mon", "monday", "tue", "tuesday", "thu", "thursday", "fri", "friday")
        }

        input_club = ClubInput(temp)

        if input_club == "null":
            await ctx.send(message_prefix + "That is not the correct use of this command\n Use **.tt ?** for information about how to use commands")
        elif input_club in clubs_on_multiple_days:
            done = False
            for day in clubs_on_multiple_days[input_club]:
                if temp.startswith(day):
                    SetUserClub(id, input_club, day_indices[day])
                    await ctx.send(message_prefix + "Your club on " + day_index_to_text[day_indices[day]] + " has been set to " + club_index_to_text[input_club])
                    done = True
            if not done:
                await ctx.send(message_prefix + "The club you have selected is on more than one day, so please specify a day")
        elif type(input_club) is int:
            single_club_days = {
                0: "",
                1: 3,
                2: "",
                3: 0,
                4: 0,
                5: 1,
                6: 2,
                7: 3,
                8: 3,
                9: 3,
                10: 4,
                11: 4,
                12: ""
            }
            SetUserClub(id, input_club, single_club_days[input_club])
            await ctx.send(message_prefix + "Your club on " + day_index_to_text[single_club_days[input_club]] + " has been set to " + club_index_to_text[input_club])
        else:
            await ctx.send(message_prefix + "That is not the correct use of this command\n Use **.tt ?** for information about how to use commands")




print(str(datetime.now(tz).hour + datetime.now(tz).minute / 60))

client.run("NjI3MDk5ODk3MjIwNDMxODcy.XY3v5Q.Q19bNJrTqvFa1eDTPEmfJjvd4HE")