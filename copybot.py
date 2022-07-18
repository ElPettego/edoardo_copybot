from telethon import TelegramClient, events
import telegram_message_bot as tmb
import asyncio
import time
import math

# DESTINAZIONE  
masterbet_copygroup_id = '-758425332' # -791394339
profilazione_copygroup_id = '-688505439'
surebet_copybot_id = '-689835776'
trial_surebet_copybot_id = '-1767340741'
siris_mto_id = '-1001556662774'
# mto_siris

bot_masterbet_id = tmb.TelegramBot(masterbet_copygroup_id, '5562268182:AAGid-46DqLIYE10NErRt0AhsCD1lks_gBc')
bot_profilazione_id = tmb.TelegramBot(profilazione_copygroup_id, '5466125587:AAH_t5swghAlVXVdrh4cs8BimLiTejXJbCY')
bot_surebet_id = tmb.TelegramBot(surebet_copybot_id, '5474218171:AAFQQLxy1kAGFcJAmSJiTJtHVhTmMhvUAe8')
bot_trial_surebet = tmb.TelegramBot(trial_surebet_copybot_id, '5562062221:AAFEDN0ktt4V59dfmlSy-madZCUyDbKDb1o')
bot_siris_mto = tmb.TelegramBot(siris_mto_id, '5146180120:AAHNamWx4jsj1oKFzrXsiovwnS8fbju2k2w')
# bot_mto_id = tmb.TelegramBot(, '')

# FONTI
masterbet_id = '-1001656670699' # -1656670699
masterbet_bot_id = '-1001578049832'
profilazione_id = '-1001455649998' # 1455649998
surebet_7_id  = '-1001719689710'
surebet_15_id = '-1001760981655'
surebet_30_id = '-1001487403480'
surebet_60_id = '-1001575267313'
prova_id = '-659491686' #'-659491686' -659491686

fonti = [masterbet_id, masterbet_bot_id, profilazione_id, prova_id]

api_id = '15639915'
api_hash = '1e2c7d01162e91681f31840eead796c9'
phone = '+393248020317'

client = TelegramClient(phone, api_id, api_hash)

@client.on(events.NewMessage)
async def handle_new_message(event):

    # print(event.chat_id, event.chat)

    if str(event.chat_id) == masterbet_id: # sender_chat_id == prova_id
        print(f'##########################{event.chat_id}#############################')
        print(event)    
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')    
        bot_masterbet_id.emit(str(event.text))

    if str(event.chat_id) == profilazione_id:
        print(f'##########################{event.chat_id}#############################')
        print(event.raw_text)   
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        if float(str(event.raw_text).splitlines()[0].replace('🚀 ROI: ', '').replace(' %', '')) >= 0.1 and 'Bet365' in str(event.raw_text).splitlines()[1]:
            bot_profilazione_id.emit(str(event.raw_text))

    if str(event.chat_id) == surebet_7_id or str(event.chat_id) == surebet_15_id or str(event.chat_id) == surebet_30_id or str(event.chat_id) == surebet_60_id:
        print(f'##########################{event.chat_id}#############################')
        print(event)    
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')  
        raw_mex = str(event.raw_text)

        raw_mex_lines = raw_mex.splitlines()

        print(raw_mex)

        first_bet = False

        # header_profit = ''
        
        for line in raw_mex_lines:
            if 'ROI' in line:
                header_profit = line.replace('ROI', 'PROFITTO MEDIO')
            if '👉' in line:
                header_books = line.replace('👉', '📚').replace('|', '-')
            if '✅' in line:
                info_match = line.replace('✅', '🆚')
            if '🗓' in line:
                info_date = line.replace('|', '-')
            if '1⃣' in line:
                stake_1 = line.split()[1].replace('€', '')
            if '2⃣' in line:
                stake_2 = line.split()[1].replace('€', '')
            if '✨' in line and not first_bet:
                bet_1 = line.replace('✨', '➡️ ').replace('|', '-')
                quota_1 = float(bet_1.split('@')[1])
                first_bet = True
            if '✨' in line and first_bet:
                bet_2 = line.replace('✨', '➡️ ').replace('|', '-')
                quota_2 = float(bet_2.split('@')[1])

        info_tour = raw_mex_lines[3]
            
        stake_1_norm = round(float(stake_1) * 100 / (float(stake_1) + float(stake_2)))
        stake_2_norm = round(float(stake_2) * 100 / (float(stake_1) + float(stake_2)))

        profitto_lordo_1 = round(stake_1_norm*quota_1, 2)
        profitto_lordo_2 = round(stake_2_norm*quota_2, 2)

        spesa = stake_1_norm+stake_2_norm

        profitto_medio = (((profitto_lordo_1 - spesa) / spesa * 100) + ((profitto_lordo_2 - spesa) / spesa * 100)) / 2

        str_to_send = '🚨 SUREBET ALERT\n\n' + header_books  + '\n' + info_tour + '\n'+ info_match + '\n' + info_date + '\n\n📝 GIOCATA 1:\n1️.  ' + str(stake_1_norm) + '€ ' + header_books.split()[1] + '\n' + bet_1 + '\n\n📝 GIOCATA 2:\n2️.  ' + str(stake_2_norm) + '€ ' + header_books.split()[3] + '\n' + bet_2 + '\n\n💰 PROFITTO:\n🛒 SPESA: ' + str(spesa) + '€\n🤑 PROFITTO LORDO: ' + str(profitto_lordo_1) + '€ - ' + str(profitto_lordo_2) + '€\n💸 PROFITTO NETTO: ' + str(round(profitto_lordo_1-spesa, 2)) + '€ - ' + str(round(profitto_lordo_2-spesa, 2)) + '€\n🚀 PROFITTO MEDIO: ' + str(round(profitto_medio, 2)) + '%'

        if profitto_medio < 7: 
            bot_surebet_id.emit(str_to_send)
            bot_trial_surebet.emit(str_to_send)
        if profitto_medio >= 7:
            bot_surebet_id.emit(str_to_send)

    if str(event.chat_id) == masterbet_bot_id:
        print(f'##########################{event.chat_id}#############################')
        print(event)    
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')   
             
        full_mex = event.raw_text
        lines_split = full_mex.splitlines()
        header = '🔊 MTO Alert 🤚\n\n'
        place = '🏟 ' + lines_split[0].replace('🎾', '')+'\n\n'
        score = '🧮 PUNTEGGIO:\n' + lines_split[2] + '\n' + lines_split[3] 
        mto_caller =  lines_split[5].split('per ')[1].split(' (')[0] 
        # print(mto_caller)
        try:
            score = score.split(mto_caller)[0] + '🚑 ' + mto_caller + ' ' + score.split(mto_caller)[1] + '\n\n'

        except:
            score = score.split(mto_caller)[0] + '🚑 ' + mto_caller + '\n\n'
        # other_player = '✅ ' + lines_split[6].split('|')[0].replace('👌', '')
        quota_match = '📊 QUOTE ' + lines_split[6].split('|')[0].replace('👌', '') + ':\nMatch: ' + lines_split[6].split('|')[1].replace('match', '') + '\nSet: ' +  lines_split[6].split('|')[2].replace('set', '')
        str_to_send = header + place + score + quota_match + '\n\n'
        if 'ITF' in place:
            link_stream = "<a href='https://live.itftennis.com/en/live-streams/'>📺 ITF Livestream</a>"

        else:
            link_stream = "<a href='https://extra.bet365.it/features/it/sports-live-streaming'>📺 BET365 Livestream</a>"

        bot_siris_mto.emit(str_to_send + link_stream)

client.start()
client.run_until_disconnected()

