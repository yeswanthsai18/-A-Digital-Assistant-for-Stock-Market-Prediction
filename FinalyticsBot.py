#================================================================================================Bot Commands
"""
General:
/start
/help
/about
/contact
/terms
/developers
/clear
/subscribe

Financial:
/riskprofiletest
/acceptedstocks
/stocks
/tips
"""
#============================================================================================Import Libraries
import csv
import time
import random
import hashlib
import logging
import requests
import telegram
import pandas as pd
from telegram import *
from telegram.ext import *
from telegram.ext.handler import *

#=============================================================>  [Initialize the Telegram Bot API Token]   <=
api_token = "1704757799:AAGJRzgiQP-m4YINSAfWrRsYbcikFtTJryo"
#==============================================================================================Enable Logging
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
#============================================================================================Global Variables
score = ""
delete_msg_flag = 0
tips_list = ['<u><i>Create a Budget</i></u>\n\nThis is arguably the most essential piece of money advice out there: Make a budget (and stick to it).\n\nThe author John C. Maxwell explains budgeting perfectly, <b>"A budget is telling your money where to go instead of wondering where it went."</b>',
             '<u><i>Create a Financial Calendar</i></u>\n\nOkay, if you’re like many people, this list may already be making you anxious! If that’s you, it’s okay – you got this.\n\nPlus, this personal finance tip isn’t as scary as it sounds.\n\nTo create a financial calendar, set reminders for important financial tasks, such as paying quarterly taxes and checking your credit report. This quick financial tip can help to save you a ton of hassle down the road.',
             '<u><i>Track Your Net Worth</i></u>\n\nYour net worth is the total sum of your assets minus the total sum of your debts. \n\nFor example, say you have ₹75,000 in the bank, a car worth ₹75,000, and ₹37,500 of credit card debt. Your assets are worth ₹1,50,000 and your debts are ₹37,500. So, your total net worth is ₹1,12,500.\n\nMonitor your net worth and keep trying to improve it. \n\nIf you have a ton of student loans, it’s not uncommon to have a net worth of – ₹75,00,000. If this is you, don’t stress – just take it one step at a time.\n\n(Oh, and remember that your net worth is not how much you’re worth as a person – you’re worth more than you can imagine!)',
             '<u><i>Don’t Make Impulse Purchases</i></u>\n\nEveryone makes impulse purchases from time to time, but they can quickly drain your bank account.\n\nSo, the next time you see something you just ‘have’ to buy, wait a week before you hand over your cash.\n\nThe time will give you room for some perspective. Then, if you still want to buy it, you’ll know it’s definitely worth your money. Chances are, you’ll decide to keep your money.\n\nAs the cartoonist and journalist Kin Hubbard said, <b>"The safest way to double your money is to fold it over and put it in your pocket."</b>',
             '<u><i>Get Clear About Your Debt</i></u>\n\nGulp. Really? Yep.\n\nStart by writing down the total amounts of everything you owe, as well as the interest rates, monthly minimum payments, and any loan payback lengths. Then, keep this document up to date.\n\n<b>"Remember, knowledge is power."</b>',
             '<u><i>Understand Interest Rates</i></u>\n\nInterest rates are significant. \n\nThey determine which debts to pay off first and which credit cards to avoid. They also help us understand how debt works – compound interest is a cruel master.\n\nI mean, even Albert Einstein noted the importance of the concept: <b>"Compound interest is the eighth wonder of the world. He who understands it, earns it; he who doesn’t, pays it."</b>\n\nSo, make sure you understand the interest rates that affect your finances.',
             '<u><i>Start Investing Today</i></u>\n\nWhen it comes to investing, time is key.\n\nCompound interest can revolutionize your finances over time, so start investing now and you’ll reap the rewards later. So, put your money to work for you now.']
questions_dict = {
    '1':"How much is your net worth?\n\n<u>Note</u>:\nNet Worth = Investment Assets - Liabilities\nInvestment Assets = {Gold, Shares, Mutual Funds, Saving Deposits, etc.}\nLiabilities = {Home loan, Car loan, Personal loan, etc.}",
    '2':"How much is your income saving rate?\n\n<u>Note</u>:\nIncome Saving Rate = Percentage of your average monthly saving",
    '3':"How many people are dependent on your income?\n\n<u>Note</u>:\nPeople who rely on your income, such as spouse, children, etc.",
    '4':"What is the consistency of your job and your income?\n\n<u>Note</u>:\nLow = Fear of losing job\nModerate = Unsatisfied with job\nHigh = Satisfied with the job",
    '5':"What's your level of expertise in share market?\n\n<u>Note</u>:\nNo knowledge = First time investor\nBeginner = Already a investor\nIntermediate = Investor with understanding of market\nExpert = Investor with analytical research and thinking\nProfessional =  Self investment and professional management",
    '6':"Considering an investment of INR 1 Lakh, how much fall can you tolerate in one month time period?\n\n<u>Note</u>:\nCalculate accurately to the proportions",
    '7':"What's the maximum amount of time for which you can  tolerate the loss?\n\n<u>Note</u>:\nCalculate accurately to the proportions"}
options_dict = {
    '1':[["Having only liabilities (Negative net worth)"],["Upto 12 times monthly expenses"],["13 - 36 times monthly expenses"],["37 - 48 times monthly expenses"],["49 - 60 times monthly expenses"]],
    '2':[["Upto 5%"],["6 - 15%"],["16 - 25%"],["26 - 50%"],["51 - 75%"]],
    '3':[["No dependencies"],["1 dependency"],["2 dependencies"],["3 dependencies"],["4 or more dependecies"]],
    '4':[["High"],["Moderate"],["Low"]],
    '5':[["No knowledge"],["Beginner level"],["Intermediate level"],["Expert level"],["Professional level"]],
    '6':[["0 - 5%"],["6 - 10%"],["11 - 20%"],["21 - 30%"],["More than 30%"]],
    '7':[["Less than 3 months"],["Between 4 months - 1 year"],["Between 1 - 2 years"],["Between 2 - 3 years"],["Between 3 - 5 years"]]}
connect_quest = {
    "Having only liabilities (Negative net worth)":[1, 1], 
    "Upto 12 times monthly expenses":[1, 2], 
    "13 - 36 times monthly expenses":[1, 3], 
    "37 - 48 times monthly expenses":[1, 4], 
    "49 - 60 times monthly expenses":[1, 5], 
    "Upto 5%":[2, 1], 
    "6 - 15%":[2, 2], 
    "16 - 25%":[2, 3], 
    "26 - 50%":[2, 4], 
    "51 - 75%":[2, 5], 
    "No dependencies":[3, 5], 
    "1 dependency":[3, 4], 
    "2 dependencies":[3, 3], 
    "3 dependencies":[3, 2], 
    "4 or more dependecies":[3, 1], 
    "High":[4, 3], 
    "Moderate":[4, 2], 
    "Low":[4, 1], 
    "No knowledge":[5, 1], 
    "Beginner level":[5, 2], 
    "Intermediate level":[5, 3], 
    "Expert level":[5, 4], 
    "Professional level":[5, 5], 
    "0 - 5%":[6, 1], 
    "6 - 10%":[6, 2], 
    "11 - 20%":[6, 3], 
    "21 - 30%":[6, 4], 
    "More than 30%":[6, 5], 
    "Less than 3 months":[7, 1], 
    "Between 4 months - 1 year":[7, 2], 
    "Between 1 - 2 years":[7, 3], 
    "Between 2 - 3 years":[7, 4], 
    "Between 3 - 5 years":[7, 5]}
options_list = ['Having only liabilities (Negative net worth)', 'Upto 12 times monthly expenses', '13 - 36 times monthly expenses', '37 - 48 times monthly expenses', '49 - 60 times monthly expenses', 'Upto 5%', '6 - 15%', '16 - 25%', '26 - 50%', '51 - 75%', 'No dependencies', '1 dependency', '2 dependencies', '3 dependencies', '4 or more dependecies', 'High', 'Moderate', 'Low', 'No knowledge', 'Beginner level', 'Intermediate level', 'Expert level', 'Professional level', '0 - 5%', '6 - 10%', '11 - 20%', '21 - 30%', 'More than 30%', 'Less than 3 months', 'Between 4 months - 1 year', 'Between 1 - 2 years', 'Between 2 - 3 years', 'Between 3 - 5 years']

#===========================================================================================Command Functions
def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=f"Hello {update.message.from_user.first_name} ✋🏻, I can help you in assisting with your risk profile, financial information, personal finance tips, stock suggestions, predictions and many other financial services 💰\n\nBy using @FinalyticsBot, you are agreeing to our terms and conditions => Refer here - /terms 📋\n\nFor other information take my /help",
                             parse_mode="html")

def help(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    context.bot.send_message(chat_id=update.message.chat_id, 
                             text="I can help you in providing most of the financial information I know!\n\nYou can control me by sending these commands\n\n<b><i>General</i>:</b>\n/start - (re)start the bot\n/help - commands list\n/about - bot information\n/contact - queries and feedback\n/terms - terms & conditions\n/developers - developers information\n/clear - delete chat history\n/subscribe - alerts & news updates\n\n<b><i>Financial</i>:</b>\n/riskprofiletest - know your risk profile\n/acceptedstocks - accepted  stocks document\n/stocks - stock predictions and information\n/tips - personal finance tips\n\nEnjoy yourslef by saving time with me in 📉📈📊",
                             parse_mode="html")

def about(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    context.bot.send_message(chat_id=update.message.chat_id, 
                             text="FinalyticsBot 🤖 is the final year project bagged by the students of Amrita Vishwa Vidyapeetham, Bengaluru. Also, the project was taking towards excellence under the guidance of Amrita School of Engg. faculty 👥 \n\nContact <a href='https://t.me/yvsravan'>Admin</a> if you have any queries about the Bot API.",
                             parse_mode="html",
                             disable_web_page_preview=True)

def contact(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    context.bot.send_message(chat_id=update.message.chat_id, 
                             text="You can contact any of the ⬇️ below Admins in case of queries 🤔 or to provide your valuable feedback. \n\n💬 <a href='https://t.me/yvsravan'>Admin - 1</a>\n💬 <a href='https://t.me/Seb_5'>Admin - 2</a>\n💬 <a href='https://t.me/BobbyY4uH'>Admin - 3</a>\n💬 <a href='https://t.me/ajithpai07'>Admin - 4</a>\n",
                             parse_mode="html",
                             disable_web_page_preview=True)

def terms(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    context.bot.send_message(chat_id=update.message.chat_id,  
                             text="Please find all the terms and conditions from the below ⬇️ PDF document.",
                             parse_mode="html")
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="upload_document")
    context.bot.sendDocument(
        chat_id=update.effective_chat.id,
        document = open(r'C:/Users\Sravan Kumar/Desktop/FinalyticsBot/assets/terms and conditions.pdf', 'rb'),
    )

def developers(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    developer_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Sravan Kumar", url="https://yvsravan2000.github.io/", callback_data='Sravan Kumar'),
         InlineKeyboardButton("Ajith Pai", url="https://www.linkedin.com/in/ajith-pai-237a66171/", callback_data='Ajith Pai')],
        [InlineKeyboardButton("Yeswanth Sai", url="https://www.facebook.com/profile.php?id=100009412482740", callback_data='Yeswanth Sai'),
         InlineKeyboardButton("Sai Surya", url="https://www.facebook.com/sai.surya.77377", callback_data='Sai Surya')]
    ])
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=f"Hello {update.effective_user.first_name}, here you go for the FinalyticsBot developers 👇🏻",
                             reply_markup=developer_buttons)

def clear(update: Update, context: CallbackContext) -> None:
    flag_message_id = update.message.message_id
    null_counter = 0
    for i in range(flag_message_id, 0, -1):
        try:
            context.bot.delete_message(update.message.chat_id, i)
            null_counter = 0
        except:
            null_counter += 1
        if(null_counter == 25):
            break

def subscribe(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")    
    global subscriber_ids
    if(update.message.from_user.id not in subscriber_ids['id']):
        subscriber_ids['id'].append(update.message.from_user.id)
        writeCSV(subscriber_ids, 'data/subscriber_ids.csv')
        context.bot.send_message(chat_id=update.message.chat_id, 
                                 text=f"🎉 Congratulations {update.message.from_user.first_name}, you have got subscribed 💌 to our bot updates and posts",
                                 parse_mode="html")
    else:
        context.bot.send_message(chat_id=update.message.chat_id, 
                                 text="🤩 Hurray! " + str(update.message.from_user.first_name) + ", you have already subscribed to our bot updates and posts!",
                                 parse_mode="html")

def riskProfileTest(update: Update, context: CallbackContext) -> None:
    global delete_msg_flag
    delete_msg_flag = update.message.message_id
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    response_buttons = ReplyKeyboardMarkup([['Yes', 'Later']],
                                           one_time_keyboard=True,
                                           resize_keyboard=True)     
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=f"Hi {update.effective_user.first_name}, do you want to take risk profile test now?",
                             reply_markup=response_buttons)      
        
def acceptedStocks(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    context.bot.send_message(chat_id=update.message.chat_id,  
                             text="Please find all the accepted stock details and symbols from the below ⬇️ PDF document.",
                             parse_mode="html")
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="upload_document")
    context.bot.sendDocument(
        chat_id=update.effective_chat.id,
        document = open(r'C:/Users\Sravan Kumar/Desktop/FinalyticsBot/assets/stock symbols and names list.pdf', 'rb'),
    )

def stocks(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    if(update.message.text=="/stocks" or update.message.text=="/stocks "):
        context.bot.send_message(chat_id=update.message.chat_id, 
                                 text="You can find the accepted stocks symbols list at /acceptedstocks for getting desired stock details or value predictions.\n\nFor getting stocks details or stock value predictions input the below given command.\n<i><u>Syntax</u>:</i><code> /stocks [argument] [stock_symbol]</code>\n\narguments: {'-d' for details, '-p' for value predictions}",
                                 parse_mode="html")
    else:
        command_list = update.message.text.split()
        try:
            argument = command_list[1]
            stock_name = command_list[2]
        except:
            argument = ""
            stock_name = ""
        if(not('-d'==argument or '-p'==argument or stock_name!="")):
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="<b>Data missing 😥\n\n</b><em>Please enter appropriate data along with command to get access to the content.\n\n</em><i><u>Syntax</u>:</i><code> /stocks [argument] [stock_name]</code>",
                                     parse_mode="html")
        else:
            if(argument=='-d'):
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=stockDetails(stock_name),
                                         parse_mode="html")
            elif(argument=='-p'):
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=stockPredictions(stock_name),
                                         parse_mode="html")
            else:
                context.bot.send_message(chat_id=update.message.chat_id,
                                        text="<b>Data missing 😥\n\n</b><em>Please enter appropriate data along with command to get access to the content.\n\n</em><i><u>Syntax</u>:</i><code> /stocks [argument] [stock_name]</code>",
                                        parse_mode="html")

def tips(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=random.choice(tips_list),
                             parse_mode="html")

#===========================================================================================Process Functions
def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def writeCSV(data , file_name) -> None:
    data_obj = pd.DataFrame(data) 
    data_obj.to_csv(file_name, index = False) 
            
def readCSV(file_name) -> dict:
    data = pd.read_csv(file_name)
    data_dict = dict(data)
    return data_dict

def userDetails(update: Update, context: CallbackContext) -> list:
    # user = update.message.from_user
    # print(user.username)
    # print(user.id)
    # print(user.first_name)
    # print(user.last_name)
    pass

def questions(update: Update, context: CallbackContext, qno) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    options = ReplyKeyboardMarkup(options_dict[qno],
                                  one_time_keyboard=True,
                                  resize_keyboard=True)
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=questions_dict[qno],
                             parse_mode="html",
                             reply_markup=options)

def riskReply(score, update: Update, context: CallbackContext) -> None:
    finRisk = 0
    psychRisk = 0
    score = list(int(x) for x in list(score))
    for i in range(0, 4):
        finRisk += score[i]
    for i in range(4, 7):
        psychRisk += score[i]
    
    if(finRisk in range(0, 8)):
        finRisk = "Very Low"
    elif(finRisk in range(8, 12)):
        finRisk = "Low"
    elif(finRisk in range(12, 15)):
        finRisk =  "Moderate"
    elif(finRisk in range(15, 17)):
        finRisk = "High"
    else:
        finRisk = "Very High"
    
    if(psychRisk in range(0, 6)):
        psychRisk = "Very Low"
    elif(psychRisk in range(6, 9)):
        psychRisk = "Low"
    elif(psychRisk in range(9, 12)):
        psychRisk =  "Moderate"
    elif(psychRisk in range(12, 14)):
        psychRisk = "High"
    else:
        psychRisk = "Very High"
    
    riskConclusionDict = {
        1:"You have zero risk-taking capacity and tolerate the maximum loss of 5%. Moreover loss can only be tolerated for maximum of 3 months time period.",
        2:"You have low risk-taking capacity and tolerate the maximum loss of 10%. Moreover loss can only be tolerated for maximum of 1 year time period.",
        3:"You have moderate risk-taking capacity and tolerate the maximum loss of 20%. Moreover loss can only be tolerated for maximum of 2 years time period.",
        4:"You have high risk-taking capacity and tolerate the maximum loss of 30%. Moreover loss can only be tolerated for maximum of 3 years time period.",
        5:"You have very high risk-taking capacity and tolerate the maximum loss of 30%. Moreover loss can only be tolerated for maximum of 5 years time period.",
    }
    riskMeterDict = {"Very Low":1, "Low":2, "Moderate":3, "High":4, "Very High":5}
    risk_reply = "Hi " + update.message.from_user.first_name + ", your financial risk profile is " + finRisk + ", and psychological risk profile is " + psychRisk + ".\n\n"
    risk_reply += riskConclusionDict[max(riskMeterDict[finRisk], riskMeterDict[psychRisk])] + "\n\n"
    risk_reply += "Click /stocks for more stock invevstments information. By using this @FinalyticsBot you are agreeing to our <b>Terms and Conditions</b>; Refer here - /terms 🤝"
    return risk_reply

def stockDetails(stock_name, update: Update, context: CallbackContext) -> str:
    return ""

def stockPredictions(stock_name, update: Update, context: CallbackContext) -> str:
    return ""
    
def normalMsg(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    global score
    global options_list
    received_msg = update.message.text
    if(received_msg == "Yes"):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Getting questions...",
                                 parse_mode="html",
                                 reply_markup=ReplyKeyboardRemove())
        questions(update, context , '1')
    elif(received_msg == "Later"):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Okay, feel free to take test without haste ☺️",
                                 parse_mode="html",
                                 reply_markup=ReplyKeyboardRemove())
    elif(received_msg in options_list):
        score += str(connect_quest[update.message.text][1])
        if(connect_quest[update.message.text][0]!=7):
            questions(update, context , str(connect_quest[update.message.text][0]+1))
        else:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="Calculating your risk profile...",
                                     parse_mode="html",
                                     reply_markup=ReplyKeyboardRemove())
            for i in range(update.message.message_id, delete_msg_flag, -1):
                context.bot.delete_message(update.message.chat_id, i)
            time.sleep(10)
            context.bot.delete_message(update.message.chat_id, update.message.message_id+1)
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="<b>Risk profile calculated!</b>",
                                     parse_mode="html",
                                     reply_markup=ReplyKeyboardRemove())
            time.sleep(2)
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=riskReply(score, update, context),
                                     parse_mode="html",
                                     reply_markup=ReplyKeyboardRemove())   
            score = ""          
    
    else:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Pardon me 🤷🏻‍♂️",
                                 parse_mode="html",
                                 reply_markup=ReplyKeyboardRemove())
        
#============================================================================================Admin Variables
try:
    admin_ids = readCSV('data/admin_ids.csv')   # Create an CSV file manually with added Admin ids
except:
    admin_ids = {'id': []}
try:
    subscriber_ids = readCSV('data/subscriber_ids.csv')   # Create an CSV file manually with added id column
except:
    subscriber_ids = {'id': []}
for Id in admin_ids:
    admin_ids[Id] = list(admin_ids[Id])
for Id in subscriber_ids:
    subscriber_ids[Id] = list(subscriber_ids[Id])
#=============================================================================================Admin Functions
def admin(update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    originalHash = "a87973c7cf5f564be5abccef41ac8ca35addc4e95580cffa368fd1f70834d7e8"
    global admin_ids
    global subscriber_ids
    if(update.message.text == "/admin" or update.message.text == "/admin "):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="<b>Data missing 😥\n\n</b><em>Please enter appropriate data along with command to get access to the content.\n\n</em><i><u>Syntax</u>:</i><code> /admin [argument] [password]</code>",
                                 parse_mode="html")
    else:
        command_list = update.message.text.split()
        try:
            argument = command_list[1]
            hashPwd = hashlib.sha256(command_list[2].encode()).hexdigest()
        except:
            hashPwd = "0"            
        try:
            message = ""
            for var in range(3, len(command_list)):
                message = message + " " + command_list[var]
            message = message.replace(" ", "%20")
            message = message.replace("'", "%27")
            message = "<b>📬 <u>Subsciption Message</u>:</b>"+ "\n\n" + message
        except:
            message = ""
        if(hashPwd == originalHash):
            if(argument == "-a"):
                if(update.message.from_user.id not in admin_ids['id']):
                    admin_ids['id'].append(update.message.from_user.id)
                    context.bot.send_message(chat_id=update.message.chat_id, 
                                             text="<b>Access granted 😌</b>", 
                                             parse_mode="html")
                else:
                    context.bot.send_message(chat_id=update.message.chat_id, 
                                             text="<b>Admin already exist 😁</b>", 
                                             parse_mode="html")
            
            elif(argument == "-c"):
                admin_ids = {'id': []}
                writeCSV(admin_ids, 'data/admin_ids.csv')
                context.bot.send_message(chat_id=update.message.chat_id, 
                                         text="<b>Admins data cleared and updated 👍🏻</b>", 
                                         parse_mode="html")
            
            elif(argument == "-u"):
                writeCSV(admin_ids, 'data/admin_ids.csv')
                context.bot.send_message(chat_id=update.message.chat_id, 
                                         text="<b>Admins data updated 👍🏻</b>", 
                                         parse_mode="html")
            elif(argument == "-s"):
                if(update.message.from_user.id in admin_ids['id']):
                    subscribers_count = len(subscriber_ids['id'])
                    context.bot.send_message(chat_id=update.message.chat_id, 
                                             text="At present, total subscribers 👥 are of count " + str(subscribers_count), 
                                             parse_mode="html")
                else:
                    context.bot.send_message(chat_id=update.message.chat_id, 
                                             text="<b>Oops! You are not added to admin network or else admin details are not updated</b> 🧐", 
                                             parse_mode="html")
                    
            elif(argument == "-m"):
                if(update.message.from_user.id in admin_ids['id']):
                    if(message == ""):
                        context.bot.send_message(chat_id=update.message.chat_id,
                                                 text="Message should not be empty 📃",
                                                 parse_mode="html")
                    elif(len(subscriber_ids['id'])==0):
                        context.bot.send_message(chat_id=update.message.chat_id,
                                                 text="Oops 😥, we don't have any subcribers.",
                                                 parse_mode="html")
                    else:
                        context.bot.send_message(chat_id=update.message.chat_id,
                                                 text="Approximate waiting time ⏳ is " + str(len(subscriber_ids['id'])+1) + " seconds.",
                                                 parse_mode="html")  
                        for Id in subscriber_ids['id']:
                            msg_request = "https://api.telegram.org/bot"+ api_token +"/sendMessage?chat_id=" + str(Id) + "&text=" + message + "&parse_mode=html"
                            requests.get(msg_request)
                            time.sleep(1)                 
                        context.bot.delete_message(update.message.chat_id, update.message.message_id+1)
                        context.bot.send_message(chat_id=update.message.chat_id,
                                                 text="Message sent to all subscribers 🙌🏻",
                                                 parse_mode="html")
                else:
                    context.bot.send_message(chat_id=update.message.chat_id, 
                                             text="<b>Oops! You are not added to admin network or else admin details are not updated</b> 🧐", 
                                             parse_mode="html")
            else:
                context.bot.send_message(chat_id=update.message.chat_id, 
                                         text="Invalid argument ⌨️", 
                                         parse_mode="html")
        else:
            context.bot.send_message(chat_id=update.message.chat_id, 
                                     text="<b>Unauthorised user, data error 😥</b>", 
                                     parse_mode="html") 

#===============================================================================================Main Function
def main() -> None:    
    #=========================================================Create the Updater and pass it your bot's token
    updater = Updater(api_token)
    
    #=================================================================Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("about", about))
    dispatcher.add_handler(CommandHandler("contact", contact))
    dispatcher.add_handler(CommandHandler("terms", terms))
    dispatcher.add_handler(CommandHandler("developers", developers))
    dispatcher.add_handler(CommandHandler("clear", clear))
    dispatcher.add_handler(CommandHandler("subscribe", subscribe))
    
    dispatcher.add_handler(CommandHandler("riskprofiletest", riskProfileTest))   
    dispatcher.add_handler(CommandHandler("acceptedstocks", acceptedStocks))
    dispatcher.add_handler(CommandHandler("stocks", stocks))
    dispatcher.add_handler(CommandHandler("tips", tips))
        
    dispatcher.add_handler(CommandHandler("admin", admin))
    """
    ----------------------------------------------Admin Commands---------------------------------------------
    Add new admin                   =>      /admin -a <password>
    Clear and update admins data    =>      /admin -c <password>
    Update admin Ids                =>      /admin -u <password>
    Get subscribers count           =>      /admin -s <password>
    Send messages to subscribers    =>      /admin -m <password> <message>
    ----------------------------------------------Admin Commands---------------------------------------------    
    """
    
    
    dispatcher.add_handler(MessageHandler(Filters.text, normalMsg))
        
    dispatcher.add_error_handler(error) # Log all errors
    
    #===========================================================================================Start the Bot
    updater.start_polling()
    updater.idle()
    
if __name__ == "__main__": 
    main()