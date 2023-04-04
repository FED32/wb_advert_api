from flask import Flask, jsonify, request
from flask import Response
from werkzeug.exceptions import BadRequestKeyError
from flasgger import Swagger, swag_from
from config import Configuration
import logger_api
import os
from wb_advert import WbAdvertEcom


app = Flask(__name__)
app.config.from_object(Configuration)
app.config['SWAGGER'] = {"title": "GTCOM-WbAdvert", "uiversion": 3}

logger = logger_api.init_logger()

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json()",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/",
}

swagger = Swagger(app, config=swagger_config)


class HttpError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


def to_boolean(x):
    if x == "true":
        return True
    elif x == "false":
        return False
    else:
        return None


@app.after_request
def apply_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "content-type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST"
    return response


@app.route('/wbadvert/getcampaigns', methods=['POST'])
@swag_from("swagger_conf/get_campaigns.yml")
def get_campaigns():
    """Получить рекламные кампании"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.get_campaigns()
        logger.info(f"get_campaigns: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("get campaigns: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("get campaigns: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'get campaigns: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/camplist', methods=['POST'])
@swag_from("swagger_conf/camp_list.yml")
def camp_list():
    """Получить список рекламных кампаний"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']

        wb_advert = WbAdvertEcom(api_key=api_key)

        status = json_file.get('status', None)
        type_ = json_file.get('type', None)
        order = json_file.get('order', None)
        direction = json_file.get('direction', 'asc')

        res = wb_advert.camp_list(status=status,
                                  type_=type_,
                                  order=order,
                                  direction=direction)
        logger.info(f"camp_list: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("camp list: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("camp list: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'camp list: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/campinfo', methods=['POST'])
@swag_from("swagger_conf/camp_info.yml")
def camp_info():
    """Информация о рекламной кампании"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        campaign_id = json_file['campaign_id']

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.camp_info(campaign_id=campaign_id)
        logger.info(f"camp_info: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("camp info: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("camp info: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'camp info: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/campaignstart', methods=['POST'])
@swag_from("swagger_conf/camp_start.yml")
def camp_start():
    """Запустить кампанию"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        campaign_id = json_file['campaign_id']

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.start_campaign(campaign_id=campaign_id)
        logger.info(f"camp_start: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("camp start: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("camp start: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'camp start: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/campaignpause', methods=['POST'])
@swag_from("swagger_conf/camp_pause.yml")
def camp_pause():
    """Поставить кампанию на паузу"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        campaign_id = json_file['campaign_id']

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.pause_campaign(campaign_id=campaign_id)
        logger.info(f"camp_pause: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("camp pause: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("camp pause: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'camp pause: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/campaignstop', methods=['POST'])
@swag_from("swagger_conf/camp_stop.yml")
def camp_stop():
    """Завершение кампании"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        campaign_id = json_file['campaign_id']

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.stop_campaign(campaign_id=campaign_id)
        logger.info(f"camp_stop: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("camp stop: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("camp stop: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'camp stop: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/bidslist', methods=['POST'])
@swag_from("swagger_conf/bids_list.yml")
def bids_list():
    """Список ставок для типа размещения"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        type_ = json_file['type']
        param = json_file['param']

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.bids_list(type_=type_, param=param)
        logger.info(f"bids_list: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("bids list: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("bids list: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'bids list: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/bidsedit', methods=['POST'])
@swag_from("swagger_conf/bids_edit.yml")
def bids_edit():
    """Изменение ставки кампании"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        campaign_id = json_file['campaign_id']
        type_ = json_file['type']
        cpm = json_file['cpm']
        param = json_file['param']

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.bids_edit(campaign_id=campaign_id, type_=type_, cpm=cpm, param=param)
        logger.info(f"bids_edit: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("bids edit: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("bids edit: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'bids edit: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/bidslistbytype', methods=['POST'])
@swag_from("swagger_conf/bids_list_by_type.yml")
def bids_list_by_type():
    """Получить список ставок по типу размещения кампании"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        type_ = json_file['type']
        param = json_file.get("param", None)

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.bids_list_by_type(type_=type_, param=param)
        logger.info(f"bids_list_by_type: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("bids_list_by_type: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("bids_list_by_type: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'bids_list_by_type: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/changeactivity', methods=['POST'])
@swag_from("swagger_conf/change_activity.yml")
def change_activity():
    """Изменение активности предметной группы для кампании в поиске"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        id_ = json_file["id"]
        subject_id = json_file["subject_id"]
        status = json_file["status"]

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.change_activity(id_=id_, subject_id=subject_id, status=status)
        logger.info(f"change_activity: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("change_activity: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("change_activity: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'change_activity: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/campaignrename', methods=['POST'])
@swag_from("swagger_conf/campaign_rename.yml")
def campaign_rename():
    """Переименование кампании"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        advert_id = json_file["advert_id"]
        name = json_file["name"]

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.rename_campaign(advert_id=advert_id, name=name)
        logger.info(f"campaign_rename: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("campaign_rename: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("campaign_rename: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'campaign_rename: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/dailybudgetedit', methods=['POST'])
@swag_from("swagger_conf/daily_budget_edit.yml")
def daily_budget_edit():
    """Изменение дневного бюджета кампании"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        advert_id = json_file["advert_id"]
        daily_budget = json_file["daily_budget"]

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.daily_budget_edit(advert_id=advert_id, daily_budget=daily_budget)
        logger.info(f"daily_budget_edit: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("daily_budget_edit: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("daily_budget_edit: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'daily_budget_edit: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/intervalsedit', methods=['POST'])
@swag_from("swagger_conf/intervals_edit.yml")
def intervals_edit():
    """Изменение интервалов показа кампании"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        advert_id = json_file["advert_id"]
        intervals_begin = json_file["intervals_begin"]
        intervals_end = json_file["intervals_end"]
        param = json_file["param"]

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.intervals_edit(advert_id=advert_id, intervals_begin=intervals_begin,
                                       intervals_end=intervals_end, param=param)
        logger.info(f"intervals_edit: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("intervals_edit: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("intervals_edit: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'intervals_edit: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/nmactiveedit', methods=['POST'])
@swag_from("swagger_conf/nmactive_edit.yml")
def nmactive_edit():
    """Изменение активности номенклатур кампании"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        advert_id = json_file["advert_id"]
        active_nm = json_file["active_nm"]
        active_states = json_file["active_states"]
        param = json_file["param"]

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.nmactive_edit(advert_id=advert_id, active_nm=active_nm, active_states=active_states,
                                      param=param)
        logger.info(f"nmactive_edit: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("nmactive_edit: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("nmactive_edit: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'nmactive_edit: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/dictsubjectid', methods=['POST'])
@swag_from("swagger_conf/dictionary_subject_id.yml")
def dictionary_subject_id():
    """Словарь значений параметра subjectId"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        id_ = json_file.get("id", None)

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.dictionary_subject_id(id_=id_)
        logger.info(f"dictionary_subject_id: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("dictionary_subject_id: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("dictionary_subject_id: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'dictionary_subject_id: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/dictmenuid', methods=['POST'])
@swag_from("swagger_conf/dictionary_menu_id.yml")
def dictionary_menu_id():
    """Словарь значений параметра menuId"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        id_ = json_file.get("id", None)

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.dictionary_menu_id(id_=id_)
        logger.info(f"dictionary_menu_id: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("dictionary_menu_id: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("dictionary_menu_id: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'dictionary_menu_id: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbadvert/dictsetid', methods=['POST'])
@swag_from("swagger_conf/dictionary_set_id.yml")
def dictionary_set_id():
    """Словарь значений параметра setId"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        id_ = json_file.get("id", None)

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.dictionary_set_id(id_=id_)
        logger.info(f"dictionary_set_id: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("dictionary_set_id: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("dictionary_set_id: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'dictionary_set_id: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbquestions/unanswered', methods=['POST'])
@swag_from("swagger_conf/questions_unanswered.yml")
def questions_unanswered():
    """Неотвеченные вопросы"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.unanswered_questions()
        logger.info(f"questions_unanswered: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("questions_unanswered: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("questions_unanswered: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'questions_unanswered: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbquestions/new', methods=['POST'])
@swag_from("swagger_conf/questions_new.yml")
def questions_new():
    """Непросмотренные отзывы и вопросы"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.new_feedback_questions()
        logger.info(f"questions_new: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("questions_new: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("questions_new: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'questions_new: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbquestions/prodrating', methods=['POST'])
@swag_from("swagger_conf/questions_products_rating.yml")
def questions_products_rating():
    """Часто спрашиваемые товары"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        size = json_file["size"]

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.products_rating(size=size)
        logger.info(f"questions_products_rating: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("questions_products_rating: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("questions_products_rating: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'questions_products_rating: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbquestions/questionslist', methods=['POST'])
@swag_from("swagger_conf/questions_list.yml")
def questions_list():
    """Список вопросов"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        is_answered = to_boolean(json_file["is_answered"])
        take = json_file["take"]
        skip = json_file["skip"]
        nm_id = json_file.get("nm_id", None)
        order = json_file.get("order", "dateDesc")

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.questions(is_answered, take, skip, nm_id, order)
        logger.info(f"questions_list: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("questions_list: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("questions_list: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'questions_list: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbquestions/questionswork', methods=['POST'])
@swag_from("swagger_conf/questions_work.yml")
def questions_work():
    """Работа с вопросами"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        question_id = json_file["question_id"]
        action = json_file["action"]
        was_viewed = to_boolean(json_file.get("was_viewed", None))
        answer = json_file.get("answer", None)
        state = json_file.get("state", None)

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.questions_work(question_id, action, was_viewed, answer, state)
        logger.info(f"questions_work: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("questions_work: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("questions_work: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'questions_work: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbquestions/questionsreport', methods=['POST'])
@swag_from("swagger_conf/questions_report.yml")
def questions_report():
    """Получение вопросов в формате XLSX"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        is_answered = to_boolean(json_file["is_answered"])

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.questions_xlsx_report(is_answered)
        logger.info(f"questions_report: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("questions_report: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("questions_report: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'questions_report: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbfeedbacks/unanswered', methods=['POST'])
@swag_from("swagger_conf/feedbacks_unanswered.yml")
def feedbacks_unanswered():
    """Необработанные отзывы"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.unanswered_feedbacks()
        logger.info(f"feedbacks_unanswered: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("feedbacks_unanswered: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("feedbacks_unanswered: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'feedbacks_unanswered: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbfeedbacks/parentsubjects', methods=['POST'])
@swag_from("swagger_conf/feedbacks_parent_subjects.yml")
def feedbacks_parent_subjects():
    """Родительские категории товаров"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.parent_subjects()
        logger.info(f"feedbacks_parent_subjects: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("feedbacks_parent_subjects: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("feedbacks_parent_subjects: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'feedbacks_parent_subjects: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbfeedbacks/productsrating', methods=['POST'])
@swag_from("swagger_conf/feedbacks_products_rating.yml")
def feedbacks_products_rating():
    """Средняя оценка товаров по родительской категории"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        subject_id = json_file["subject_id"]

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.feedback_products_rating(subject_id)
        logger.info(f"feedbacks_products_rating: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("feedbacks_products_rating: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("feedbacks_products_rating: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'feedbacks_products_rating: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbfeedbacks/productsratingtop', methods=['POST'])
@swag_from("swagger_conf/feedbacks_products_rating_top.yml")
def feedbacks_products_rating_top():
    """Товары с наибольшей и наименьшей средней оценкой по родительской категории"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        subject_id = json_file["subject_id"]

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.feedback_products_rating_top(subject_id)
        logger.info(f"feedbacks_products_rating_top: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("feedbacks_products_rating_top: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("feedbacks_products_rating_top: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'feedbacks_products_rating_top: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbfeedbacks/feedbackslist', methods=['POST'])
@swag_from("swagger_conf/feedbacks_list.yml")
def feedbacks_list():
    """Список отзывов"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        is_answered = to_boolean(json_file["is_answered"])
        take = json_file["take"]
        skip = json_file["skip"]
        nm_id = json_file.get("nm_id", None)
        order = json_file.get("order", "dateDesc")
        has_supplier_complaint = to_boolean(json_file.get("has_supplier_complaint", None))

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.feedbacks(is_answered, take, skip, nm_id, order, has_supplier_complaint)
        logger.info(f"feedbacks_list: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("feedbacks_list: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("feedbacks_list: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'feedbacks_list: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbfeedbacks/feedbackswork', methods=['POST'])
@swag_from("swagger_conf/feedbacks_work.yml")
def feedbacks_work():
    """Работа с отзывом"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']

        feedback_id = json_file["feedback_id"]
        action = json_file["action"]
        was_viewed = to_boolean(json_file.get("was_viewed", None))
        answer_text = json_file.get("answer_text", None)
        create_supplier_complaint = to_boolean(json_file.get("create_supplier_complaint", None))

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.feedback_work(feedback_id, action, was_viewed, answer_text, create_supplier_complaint)
        logger.info(f"feedbacks_work: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("feedbacks_work: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("feedbacks_work: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'feedbacks_work: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbfeedbacks/feedbacksreport', methods=['POST'])
@swag_from("swagger_conf/feedbacks_report.yml")
def feedbacks_report():
    """Получение отзывов в формате XLSX"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        is_answered = to_boolean(json_file["is_answered"])
        has_supplier_complaint = to_boolean(json_file.get("has_supplier_complaint", None))

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.feedbacks_xlsx_report(is_answered, has_supplier_complaint)
        logger.info(f"feedbacks_report: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("feedbacks_report: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("feedbacks_report: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'feedbacks_report: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbfeedbacks/feedbacksarchived', methods=['POST'])
@swag_from("swagger_conf/feedbacks_archived.yml")
def feedbacks_archived():
    """Список архивных отзывов"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        take = json_file["take"]
        skip = json_file["skip"]
        nm_id = json_file.get("nm_id", None)
        order = json_file.get("order", "dateDesc")
        has_supplier_complaint = to_boolean(json_file.get("has_supplier_complaint", None))

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.feedbacks_archived(take, skip, nm_id, order,has_supplier_complaint)
        logger.info(f"feedbacks_archived: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("feedbacks_archived: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("feedbacks_archived: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'feedbacks_archived: {ex}')
        raise HttpError(400, f'{ex}')


@app.route('/wbfeedbacks/productsratingnmid', methods=['POST'])
@swag_from("swagger_conf/feedbacks_products_rating_nm_id.yml")
def feedbacks_products_rating_nm_id():
    """Средняя оценка товара по nmId"""

    try:
        json_file = request.get_json(force=False)
        api_key = json_file['api_key']
        nm_id = json_file["nm_id"]

        wb_advert = WbAdvertEcom(api_key=api_key)
        res = wb_advert.products_rating_nm_id(nm_id)
        logger.info(f"feedbacks_products_rating_nm_id: {res.get('code')} {res.get('message')}")

        return jsonify(res)

    except BadRequestKeyError:
        logger.error("feedbacks_products_rating_nm_id: BadRequest")
        return Response(None, 400)
    except KeyError:
        logger.error("feedbacks_products_rating_nm_id: KeyError")
        return Response(None, 400)
    except BaseException as ex:
        logger.error(f'feedbacks_products_rating_nm_id: {ex}')
        raise HttpError(400, f'{ex}')



