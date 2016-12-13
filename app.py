# coding=utf-8
import os
import sys
import json
import requests
import time
import random
import re
from flask import Flask, request
from flask import render_template
from flask import send_file
from elibom.Client import *

app = Flask(__name__)

elibom = ElibomClient('info@novopayment.com', 'X0fAbv3Uu6')

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/termandcond', methods=['GET'])
def termandcond():
    return render_template('index.html')


@app.route('/buttons', methods=['GET'])
def buttons():
    return render_template('buttons.html')


@app.route('/img/hola', methods=['GET'])
def hola():
    filename = '/templates/images/bot-greet.png'
    return send_file(filename, mimetype='image/gif')


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
    data = request.get_json()
    # log(data)  # you may not want to log every incoming message in production, but it's good for testing
    phone = "51920058181" # This is Phone Number"
    token = "654321" # This is Phone Number"
    if data["object"] == "page":
        for entry in data["entry"]:
            try:
                for messaging_event in entry["messaging"]:
                    sender_id = messaging_event["sender"]["id"]  # the facebook ID
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID

                    s = json_loads_byteified(get_user_by_id(sender_id))
                    log(s)

                    log(messaging_event["message"])
                    if messaging_event["message"].get("text"):
                        message_text = messaging_event["message"]["text"]
                        if message_text.lower().find("hola") is not -1:
                            msg = "Hola " + s["first_name"] + ", ¿en qué te puedo ayudar?"
                            send_message(sender_id, msg)

                        elif message_text.lower().find("chao") is not -1 or message_text.lower().find(
                                "hasta luego") is not -1 \
                                or message_text.lower().find("gracias") is not -1 \
                                or message_text.lower().find("no") is not -1 \
                                or message_text.lower().find("no acepto") is not -1:

                            msg = "Gracias por su preferencia que tenga un buen dia 👋"
                            send_message(sender_id, msg)

                        elif message_text.lower().find("regist") is not -1:
                            msg = "Seguro " + s["first_name"] + ", pero primero nos gustaria que consultaras las " \
                                                                "condiciones del servicio"
                            send_message(sender_id, msg)
                            time.sleep(3)
                            send_termandc(sender_id)
                            time.sleep(3)
                            msg = "Solo escribe 'Acepto' para iniciar..."
                            send_message(sender_id, msg)

                        elif message_text.lower().find("acepto") is not -1:
                            msg = "Gracias " + s["first_name"] + \
                                  ", para continuar ¿me indicas tu numero DNI?"
                            send_message(sender_id, msg)

                        elif message_text.lower().find("saldo") is not -1 \
                                or message_text.lower().find("balance") is not -1:
                            msg = "Tu saldo es: S./ 6.00"  # + str(random.uniform(1))
                            send_message(sender_id, msg)

                        elif message_text.lower().find("aprobado") is not -1:
                            msg = "Gracias 👍, vamos a procesar tu transferencia"  # + str(random.uniform(1))
                            send_message(sender_id, msg)
                            time.sleep(5)
                            msg = "envio realizado con éxito, tu amigo ya recibio un SMS con la notificación!"
                            send_message(sender_id, msg)

                            r = elibom.send_message('51989214419', 'Recibiste un envio de dinero de S./ 4.00, '
                                                                   'cobralo en cualquier agente TDM '
                                                                   'con el Token: 689324')
                            log(r)
                            time.sleep(5)
                            msg = "¿Algo mas en lo que te pueda ayudar? 😉"
                            send_message(sender_id, msg)


                        elif message_text.lower().find("movimientos") is not -1 \
                                or message_text.lower().find("operaciones") is not -1:
                            msg = "Estos son lo ultimos 3 movimientos que tenemos regitrados en tu cuenta"
                            send_message(sender_id, msg)
                            # time.sleep(2)
                            # msg = "REFERNCIA - FECHA - DECRIPCIÓN - MONTO"
                            # send_message(sender_id, msg)
                            time.sleep(2)
                            msg = "368050462275 - 01/12/2016 - CONSULTA DE SALDO TDM - 0.00"
                            send_message(sender_id, msg)
                            time.sleep(2)
                            msg = "748009789973 - 01/12/2016 - TRANSF. TERCEROS TDM - 4.00"
                            send_message(sender_id, msg)
                            time.sleep(2)
                            msg = "748010041406 - 01/12/2016 - DEPOSITO PROMO REGISTRO FB - 10.00"
                            send_message(sender_id, msg)
                            time.sleep(2)
                            msg = "¿Algo mas en lo que te pueda ayudar? ☺"
                            send_message(sender_id, msg)

                        elif message_text.lower().find("9") is not -1 and len(message_text) == 9:
                            msg = "Ok... ¿me indicas el monto a enviar (ej. 5.99)?"
                            send_message(sender_id, msg)

                        elif message_text.lower().find(".") is not -1 and len(message_text) == 4:
                            msg = "Listo👍, para confirmar el envio solo escribe \"Aprobado\"?"
                            send_message(sender_id, msg)

                        elif message_text.lower().find("9") is not -1 and len(message_text) == 8:
                            msg = "Ok... ¿me indicas tu numero Celular Movistar?"
                            send_message(sender_id, msg)

                        elif message_text.lower().find("+519") is not -1 and len(message_text) == 12:
                            msg = " Gracias vamos a iniciar el proceso de Afiliación..."
                            send_message(sender_id, msg)
                            time.sleep(4)
                            autoafiliacion(sender_id, msg)
                            msg = "te enviamos una clave de confirmación a tu número celular."
                            send_message(sender_id, msg)
                            time.sleep(3)
                            msg = "¿me la indicas?, por favor"
                            send_message(sender_id, msg)

                        elif message_text.lower().find("6") is not -1 and len(message_text) == 6:
                            time.sleep(4)
                            msg = "Muchas Gracias por registrarte ☺, en breve te enviaremos un SMS con tu clave MPIN"
                            send_message(sender_id, msg)
                            time.sleep(4)
                            msg = "por registrarte por este canal tienes un bono de S./ 10.00"
                            send_message(sender_id, msg)
                            time.sleep(2)
                            msg = "Tu saldo es S./ 10.00"
                            send_message(sender_id, msg)
                            time.sleep(2)
                            msg = "¿Algo mas en lo que te pueda ayudar? 😉"
                            send_message(sender_id, msg)

                        elif message_text.lower().find("enviar dinero a ") is not -1 \
                                or message_text.lower().find("envio de dinero a ") is not -1 \
                                or message_text.lower().find("transferir dinero a ") is not -1 \
                                or message_text.lower().find("transferencia a ") is not -1 \
                                or message_text.lower().find("transferir a ") is not -1:

                            msg = "Muy bien, permiteme buscar a la persona"
                            nombres = message_text.split(' a ')
                            log(nombres[1])

                            send_message(sender_id, msg)
                            f = json_loads_byteified(find_user_by_name(nombres[1]))
                            log(f)
                            log(f["data"][0])

                            time.sleep(3)

                            if message_text.lower().find("Jeremi") is not -1:
                                show_profile(sender_id, "1241646672576528")
                                msg = "Indicame el monto (ej. 5.99)"
                                send_message(sender_id, msg)

                            msg = "Al parecer no lo tengo registrado..."
                            send_message(sender_id, msg)

                            msg = "indicame el número de celular (ej. 963605271)"
                            send_message(sender_id, msg)
                            # show_profile(sender_id, sender_id)

                        elif message_text.lower().find("ayuda") is not -1 or message_text.lower().find(
                                "asistencia") is not -1 \
                                or message_text.lower().find("duda") is not -1:
                            show_help(sender_id)

                        else:
                            show_what(sender_id)

            except KeyError as e:
                log(e.message)
            except AttributeError as e:
                log(e.message)
            except TypeError as e:
                log(str(e))

    return "ok", 200


def get_user_by_id(user_id):
    url = "https://graph.facebook.com/USER_ID?&access_token="
    url = url.replace("USER_ID", user_id) + os.environ["PAGE_ACCESS_TOKEN"]
    # log(url)
    r = requests.get(url)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        return r.status_code, r.text
    else:
        return r.text


def find_user_by_name(name):
    url = "https://graph.facebook.com/search?q=USER_NAME&limit=1&offset=0&type=user&format=json&access_token="
    url = url.replace("USER_NAME", name) + os.environ["PAGE_ACCESS_TOKEN"]
    # log(url)
    r = requests.get(url)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        return r.status_code, r.text
    else:
        return r.text


def getSaldo(sender_id):
    url = "http://72.46.255.110:8005/facebook-service/1.0/user/balance/" + sender_id

    r = requests.get(url)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
        return r.status_code, r.text
    else:
        return r.text


def autoafiliacion(sender_id, token):
    headers = {
        "Content - Type": "application / json",
        "x - country": "Pe"
    }

    data = {
        "idOperation": "108",
        "bean": token,
        "facebookId": sender_id
    }

    log(data)
    r = requests.post("http://72.46.255.110:8005/facebook-service/1.0/user/auto-afiliation", headers=headers, data=data)
    log(r)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def preafiliacion(sender_id, msisdn):
    headers = {
        "Content - Type": "application / json",
        "x - country": "Pe"
    }

    data = {
        "idOperation": "107",
        "bean": {
            "usuarioMsisdn": "51" + msisdn,
            "primer_nombre": "Gustavo",
            "segundo_nombre": "Adolfo",
            "primer_apellido": "Mora",
            "segundo_apellido": "Pereda",
            "fecha_nacimiento": "01-12-1992",
            "dni": "20801243", "sexo": "M",
            "email": "gmora922@gmail.com",
            "id_civil": "S",
            "operacionId": "107"
        },
        "facebookId": sender_id
    }

    log(data)
    r = requests.post("http://72.46.255.110:8005/facebook-service/1.0/user/pre-afiliation", headers=headers, data=data)

    log(r)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_termandc(recipient_id):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        }, "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Tu Dinero Móvil",
                            "subtitle": "Terminos y Condiciones del Servicio",
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": "http://www.tudineromovil.pe/wp-content/themes/np-tdm/media/documents/contrato_cuenta_simplificada_201606.pdf",
                                    "title": "+ info"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    })
    log(data)
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def show_profile(recipient_id, user_id):
    r = json_loads_byteified(get_user_by_id(user_id))
    nombres = r["first_name"] + " " + r["last_name"]

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        }, "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Deseas enviarle dinero a: ",
                            "subtitle": nombres,
                            "image_url": r["profile_pic"]

                        }
                    ]
                }
            }
        }
    })
    log(data)
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def show_what(recipient_id):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        }, "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Vamos a consultar tu solicitud en breve ",
                            "subtitle": " por favor espere 😇",
                            "image_url": "http://www.latodo.pe/wp-content/uploads/bot-what.png"
                        }
                    ]
                }
            }
        }
    })
    log(data)
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def show_help(recipient_id):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        }, "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Para mayor asistencia e información contáctenos al: ",
                            "subtitle": "0800-100-122",
                            "image_url": "http://www.latodo.pe/wp-content/uploads/bot-contact.png"
                        }
                    ]
                }
            }
        }
    })
    log(data)
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )


def _byteify(data, ignore_dicts=False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
            }
    # if it's anything else, return it in its original form
    return data


if __name__ == '__main__':
    app.run(debug=True)
