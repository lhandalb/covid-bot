from flask import Flask, request
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    #print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    text = ""
    menu_txt = '\n\nSend a *country name*, or *global*, for the latest report\nSend *symptoms* to learn how the virus spreads\nSend *prevent* to see how to prevent the disease'

    if 'hi' in incoming_msg or 'hey' in incoming_msg:
        text = 'Hey! \nThis is Ms Rona with the latest COVID-19 updates. How can I help you?'
        msg.body(text + menu_txt)

    elif 'menu' in incoming_msg or 'instructions' in incoming_msg:
        msg.body(menu_txt)

    elif 'symptoms' in incoming_msg:
        text = f'COVID-19 sympotoms:\n\nCommonn symptoms:\n-fever\n-dry cough\n-tiredness\n\nLess common symptoms:\n-aches and pains\n-sore throat\n-diarrhoea\n-conjunctivitis\n-headache\n-loss of taste or smell\n-a rash on skin, or discolouration of fingers or toes\n\nSerious symptoms:\n-difficulty breathing or shortness of breath\n-chest pain or pressure\n-loss of speech or movement\n\nSeek immediate medical attention if you have serious symptoms. Always call before visiting your doctor or health facility.\nPeople with mild symptoms who are otherwise healthy should manage their symptoms at home.\nOn average it takes 5–6 days from when someone is infected with the virus for symptoms to show, however it can take up to 14 days.\n\nLearn more on https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/q-a-coronaviruses#:~:text=symptoms'
        msg.body(text + menu_txt)
        # msg.media('https://user-images.githubusercontent.com/34777376/77290801-f2421280-6d02-11ea-8b08-fdb516af3d5a.jpeg')

    elif 'prevent' in incoming_msg or 'spread' in incoming_msg:
        text = f'_COVID-19 spread can be prevented through the following means_\n\n*Stay* home as much as you can\n*Keep* a safe distance\n*Wash* hands often\n*Cover* your nose and mouth\n\nlearn more on https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public'
        msg.body(text + menu_txt)
        # msg.media('https://user-images.githubusercontent.com/34777376/77290864-1c93d000-6d03-11ea-96fe-18298535d125.jpeg')

    elif 'world' in incoming_msg or 'planet' in incoming_msg or 'global' in incoming_msg or 'all' == incoming_msg:
        # send global report
        r = requests.get('https://coronavirus-19-api.herokuapp.com/all')
        if r.status_code == 200:
            try:
                data = r.json()
                fatality_rate = round((100 * data["deaths"]/data["cases"]), 2)
                recovery_rate = round((100 * data["recovered"]/data["cases"]), 2)
                text = f'_Worldwide Covid-19 Report_ \n\nConfirmed Cases: *{data["cases"]:,d}*\nDeaths: *{data["deaths"]:,d}*\nRecovered: *{data["recovered"]:,d}*\n\nFatality rate: *{fatality_rate}*%\nRecovery rate: *{recovery_rate}*%'
            except Exception as e:
                text = 'I could not retrieve global results at this time, sorry.'
        else:
            text = 'I could not retrieve global results at this time, sorry.'
        msg.body(text + menu_txt)

    else:
        # send country report
        if 'us' == incoming_msg or 'united states' == incoming_msg:
            incoming_msg = 'usa'
        elif 'united kingdom' == incoming_msg:
            incoming_msg = 'uk'
        elif 'emirates' in incoming_msg:
            incoming_msg = 'uae'


        r = requests.get('https://coronavirus-19-api.herokuapp.com/countries/' + incoming_msg)
        if r.status_code == 200:
            try:
                data = r.json()
                for key in data:
                    if not data[key]:
                        data[key] = 'N/A'
                    elif type(data[key]) == int:
                        data[key] = f'{data[key]:,d}'

                fatality_rate = 'N/A'
                recovery_rate = 'N/A'

                if data["cases"] != 'N/A':
                    if data["deaths"] != 'N/A':
                        fatality_rate = round((100 * data["deaths"]/data["cases"]), 2)
                    if data["recovered"] != 'N/A':
                        recovery_rate = round((100 * data["recovered"]/data["cases"]), 2)

                text = f'_{data["country"]} Covid-19 Report_ \n\nConfirmed Cases: *{data["cases"]}*\nToday Cases: *{data["todayCases"]}*\nDeaths: *{data["deaths"]}*\nRecovered: *{data["recovered"]}*\nActive: *{data["active"]}*\nCritical: *{data["critical"]}*\nTotal tests: *{data["totalTests"]}*\n\nCases per Million: *{data["casesPerOneMillion"]}*\nDeaths per Million: *{data["deathsPerOneMillion"]}*\nTests per Million: *{data["testsPerOneMillion"]}*\n\nFatality rate: *{fatality_rate}%*\nRecovery rate: *{recovery_rate}%*'
            except Exception as e:
                text = f'I could not retrieve the results for {incoming_msg} at this time, sorry.'
        else:
            text = f'I could not retrieve the results for {incoming_msg} at this time, sorry.'

        msg.body(text + menu_txt)

    return str(resp)

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
