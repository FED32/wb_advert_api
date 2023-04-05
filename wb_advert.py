import requests
from requests.exceptions import ConnectionError
import json


class WbAdvertEcom:
    def __init__(self, api_key: str, format_='normal'):

        self.api_key = api_key

        self.format = format_

        self.headers = {
            'Authorization': self.api_key,
            'Accept': 'application/json',
            "Content-Type": "application/json"
        }

    @staticmethod
    def read_res(res):
        """вспомогательная функция"""
        try:
            return res.json()
        except:
            return res.text

    def get_campaigns(self):
        """
        Получить рекламные кампании
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1count/get
        """

        url = 'https://advert-api.wb.ru/adv/v0/count'

        if self.format == 'normal':
            try:
                res = requests.get(url=url, headers=self.headers)

                if res.status_code == 200:
                    return {"code": res.status_code, "message": "success", "result": res.json()}
                elif res.status_code == 400:
                    return {"code": res.status_code, "message": "IncorrectSupplierId", "result": res.text}
                elif res.status_code == 401:
                    return {"code": res.status_code, "message": "TokenMissing", "result": res.text}
                else:
                    return {"code": res.status_code, "message": "unknown error"}
            except ConnectionError:
                return {"message": "wb connection error"}
            except:
                return {"message": "wb unknown error"}

        elif self.format == 'base':
            try:
                res = requests.get(url=url, headers=self.headers)
                return res
            except:
                return None

    def camp_list(self,
                  limit: int = 1000,
                  # offset: int = 0,
                  status: int = None,
                  type_: int = None,
                  order: str = None,
                  direction: str = "asc"
                  ):
        """
        Список РК
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1adverts/get
        """

        url = 'https://advert-api.wb.ru/adv/v0/adverts'

        params = {
            'limit': limit,
            # 'offset': offset
        }

        if status is not None:
            params.setdefault('status', status)
        if type_ is not None:
            params.setdefault('type', type_)
        if order is not None:
            params.setdefault('order', order)
        if direction is not None:
            params.setdefault('direction', direction)

        if self.format == 'normal':
            try:
                offset = 0
                params['offset'] = offset
                result = []
                while True:
                    res = requests.get(url=url, headers=self.headers, params=params)
                    if res.status_code == 200:
                        if len(res.json()) > 0:
                            result += res.json()
                            offset += limit
                            params['offset'] = offset
                        else:
                            return {"code": res.status_code, "message": "success", "result": result}

                    elif res.status_code == 204:
                        return {"code": res.status_code, "message": "no campaigns", "result": []}
                    elif res.status_code == 400:
                        return {"code": res.status_code, "message": "IncorrectSupplierId or IncorrectType", "result": res.text}
                    elif res.status_code == 401:
                        return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound", "result": res.text}
                    elif res.status_code == 422:
                        return {"code": res.status_code, "message": "ErrorProcesRequestParam"}
                    else:
                        return {"code": res.status_code, "message": "unknown error"}

            except ConnectionError:
                return {"message": "wb connection error"}
            except:
                return {"message": "wb unknown error"}

        elif self.format == 'base':
            params['offset'] = 0
            try:
                res = requests.get(url=url, headers=self.headers, params=params)
                return res
            except:
                return None

    def camp_info(self, campaign_id: int):
        """
        Информация о РК
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1advert/get
        """

        url = 'https://advert-api.wb.ru/adv/v0/advert'

        params = {'id': campaign_id}

        if self.format == 'normal':
            try:
                res = requests.get(url=url, headers=self.headers, params=params)

                if res.status_code == 200:
                    return {"code": res.status_code, "message": "success", "result": res.json()}
                elif res.status_code == 204:
                    return {"code": res.status_code, "message": "campaign not found"}
                elif res.status_code == 400:
                    return {"code": res.status_code, "message": "InvalidRcId or IncorrectSupplierId", "result": res.text}
                elif res.status_code == 401:
                    return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound", "result": res.text}
                else:
                    return {"code": res.status_code, "message": "unknown error"}

            except ConnectionError:
                return {"message": "wb connection error"}
            except:
                return {"message": "wb unknown error"}

        elif self.format == 'base':
            try:
                res = requests.get(url=url, headers=self.headers, params=params)
                return res
            except:
                return None

    def start_campaign(self, campaign_id: int):
        """
        Запускает кампанию
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1start/get
        """

        url = 'https://advert-api.wb.ru/adv/v0/start'

        params = {'id': campaign_id}

        if self.format == 'normal':
            try:
                res = requests.get(url=url, headers=self.headers, params=params)

                if res.status_code == 200:
                    return {"code": res.status_code, "message": "success"}
                elif res.status_code == 400:
                    return {"code": res.status_code, "message": "InvalidRcId or IncorrectSupplierId", "result": res.text}
                elif res.status_code == 401:
                    return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound", "result": res.text}
                elif res.status_code == 422:
                    return {"code": res.status_code, "message": "StatusNoChange", "result": res.text}
                else:
                    return {"code": res.status_code, "message": "unknown error"}

            except ConnectionError:
                return {"message": "wb connection error"}
            except:
                return {"message": "wb unknown error"}

        elif self.format == 'base':
            try:
                res = requests.get(url=url, headers=self.headers, params=params)
                return res
            except:
                return None

    def pause_campaign(self, campaign_id: int):
        """
        Ставит кампанию на паузу
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1pause/get
        """

        url = 'https://advert-api.wb.ru/adv/v0/pause'

        params = {'id': campaign_id}

        if self.format == 'normal':
            try:
                res = requests.get(url=url, headers=self.headers, params=params)

                if res.status_code == 200:
                    return {"code": res.status_code, "message": "success"}
                elif res.status_code == 400:
                    return {"code": res.status_code, "message": "InvalidRcId or IncorrectSupplierId", "result": res.text}
                elif res.status_code == 401:
                    return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound", "result": res.text}
                elif res.status_code == 422:
                    return {"code": res.status_code, "message": "StatusNoChange", "result": res.text}
                else:
                    return {"code": res.status_code, "message": "unknown error"}

            except ConnectionError:
                return {"message": "wb connection error"}
            except:
                return {"message": "wb unknown error"}

        elif self.format == 'base':
            try:
                res = requests.get(url=url, headers=self.headers, params=params)
                return res
            except:
                return None

    def stop_campaign(self, campaign_id: int):
        """
        Завершение кампании
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1stop/get
        """

        url = 'https://advert-api.wb.ru/adv/v0/stop'

        params = {'id': campaign_id}

        if self.format == 'normal':
            try:
                res = requests.get(url=url, headers=self.headers, params=params)

                if res.status_code == 200:
                    return {"code": res.status_code, "message": "success"}
                elif res.status_code == 400:
                    return {"code": res.status_code, "message": "InvalidRcId or IncorrectSupplierId", "result": res.text}
                elif res.status_code == 401:
                    return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound", "result": res.text}
                elif res.status_code == 422:
                    return {"code": res.status_code, "message": "StatusNoChange", "result": res.text}
                else:
                    return {"code": res.status_code, "message": "unknown error"}

            except ConnectionError:
                return {"message": "wb connection error"}
            except:
                return {"message": "wb unknown error"}

        elif self.format == 'base':
            try:
                res = requests.get(url=url, headers=self.headers, params=params)
                return res
            except:
                return None

    def bids_list(self,
                  type_: int,
                  param: int):
        """
        Список ставок для типа размещения
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1cpm/get
        """

        url = 'https://advert-api.wb.ru/adv/v0/cpm'

        params = {
            'type': type_,
            'param': param
        }

        if self.format == 'normal':
            try:
                res = requests.get(url=url, headers=self.headers, params=params)

                if res.status_code == 200:
                    return {"code": res.status_code, "message": "success", "result": res.json()}
                elif res.status_code == 400:
                    return {"code": res.status_code, "message": "IncorrectParam or IncorrectType or IncorrectSupplierId", "result": res.text}
                elif res.status_code == 401:
                    return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound", "result": res.text}
                elif res.status_code == 422:
                    return {"code": res.status_code, "message": "AmountNotChanged or RequestBodyProcessError", "result": res.text}
                else:
                    return {"code": res.status_code, "message": "unknown error"}

            except ConnectionError:
                return {"message": "wb connection error"}
            except:
                return {"message": "wb unknown error"}

        elif self.format == 'base':
            try:
                res = requests.get(url=url, headers=self.headers, params=params)
                return res
            except:
                return None

    def bids_edit(self,
                  campaign_id: int,
                  type_: int,
                  cpm: int,
                  param: int):
        """
        Изменение ставки кампании
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1cpm/post
        """

        url = 'https://advert-api.wb.ru/adv/v0/cpm'

        body = {
            'advertId': campaign_id,
            'type': type_,
            'cpm': cpm,
            'param': param
        }

        if self.format == 'normal':
            try:
                res = requests.post(url=url, headers=self.headers, data=json.dumps(body))

                if res.status_code == 200:
                    return {"code": res.status_code, "message": "success"}
                elif res.status_code == 400:
                    return {"code": res.status_code, "message": "IncorrectParam or IncorrectType or IncorrectSupplierId or IncorrectCpm", "result": res.text}
                elif res.status_code == 401:
                    return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound", "result": res.text}
                elif res.status_code == 422:
                    return {"code": res.status_code, "message": "AmountNotChanged or RequestBodyProcessError", "result": res.text}
                else:
                    return {"code": res.status_code, "message": "unknown error"}

            except ConnectionError:
                return {"message": "wb connection error"}
            # except BaseException as ex:
            except:
                # print(ex)
                return {"message": "wb unknown error"}

        elif self.format == 'base':
            try:
                res = requests.post(url=url, headers=self.headers, data=json.dumps(body))
                return res
            except:
                return None

    def bids_list_by_type(self,
                          type_: int,
                          param: list[int] = None):
        """
        Список ставок по типу размещения кампании
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1allcpm/post
        """

        url = 'https://advert-api.wb.ru/adv/v0/allcpm'

        params = {'type': type_}

        if param is not None:
            body = {"param": param}
        else:
            body = {}

        if self.format == 'normal':
            try:
                res = requests.post(url=url, headers=self.headers, params=params, data=json.dumps(body))

                if res.status_code == 200:
                    return {"code": res.status_code, "message": "success", "result": res.json()}
                elif res.status_code == 400:
                    return {"code": res.status_code, "message": "RequestBodyProcessError or IncorrectSupplierId", "result": res.text}
                elif res.status_code == 401:
                    return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound", "result": res.text}
                else:
                    return {"code": res.status_code, "message": "unknown error"}

            except ConnectionError:
                return {"message": "wb connection error"}
            except:
                return {"message": "wb unknown error"}

        elif self.format == 'base':
            try:
                res = requests.post(url=url, headers=self.headers, params=params, data=json.dumps(body))
                return res
            except:
                return None

    def change_activity(self,
                        id_: int,
                        subject_id: int,
                        status: int):
        """
        Изменение активности предметной группы для кампании в поиске
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1active/get
        """

        url = 'https://advert-api.wb.ru/adv/v0/active'

        params = {
            'id': id_,
            'subjectId': subject_id,
            'status': status
        }

        if self.format == 'normal':
            try:
                res = requests.get(url=url, headers=self.headers, params=params)

                if res.status_code == 200:
                    return {"code": res.status_code, "message": "success"}
                elif res.status_code == 400:
                    return {
                        "code": res.status_code,
                        "message": "IncorrectActive or IncorrectStatus or InvalidRcId or IncorrectSubjectID or IncorrectSupplierId",
                        "result": res.text}
                elif res.status_code == 401:
                    return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound", "result": res.text}
                elif res.status_code == 422:
                    return {"code": res.status_code, "message": "ActivitySubjectGroupNotChanged", "result": res.json()}
                else:
                    return {"code": res.status_code, "message": "unknown error"}

            except ConnectionError:
                return {"message": "wb connection error"}
            except:
                return {"message": "wb unknown error"}

        elif self.format == 'base':
            try:
                res = requests.get(url=url, headers=self.headers, params=params)
                return res
            except:
                return None

    def rename_campaign(self,
                        advert_id: int,
                        name: str):
        """
        Переименование кампании
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1rename/post
        """

        url = 'https://advert-api.wb.ru/adv/v0/rename'

        if len(name) > 100:
            return {"message": "incorrect name"}
        else:

            body = {
                "advertId": advert_id,
                "name": name
            }

            if self.format == 'normal':
                try:
                    res = requests.post(url=url, headers=self.headers, data=json.dumps(body))

                    if res.status_code == 200:
                        return {"code": res.status_code, "message": "success"}
                    elif res.status_code == 400:
                        return {"code": res.status_code, "message": "InvalidRcId or IncorrectName or IncorrectSupplierId", "result": res.text}
                    elif res.status_code == 401:
                        return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound", "result": res.text}
                    elif res.status_code == 422:
                        return {"code": res.status_code, "message": "RequestBodyProcessError or CompanyNameChangeErr", "result": res.text}
                    else:
                        return {"code": res.status_code, "message": "unknown error"}

                except ConnectionError:
                    return {"message": "wb connection error"}
                except:
                    return {"message": "wb unknown error"}

            elif self.format == 'base':
                try:
                    return requests.post(url=url, headers=self.headers, data=json.dumps(body))
                except:
                    return None

    def daily_budget_edit(self,
                          advert_id: int,
                          daily_budget: int):
        """
        Изменение дневного бюджета кампании
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1dailybudget/post
        """

        url = 'https://advert-api.wb.ru/adv/v0/dailybudget'

        body = {
            "advertId": advert_id,
            "dailyBudget": daily_budget
        }

        if self.format == 'normal':
            try:
                res = requests.post(url=url, headers=self.headers, data=json.dumps(body))

                if res.status_code == 200:
                    return {"code": res.status_code, "message": "success"}
                elif res.status_code == 400:
                    return {"code": res.status_code, "message": "InvalidRcId or IncorrectDailyBudget or IncorrectSupplierId",
                            "result": res.text}
                elif res.status_code == 401:
                    return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                            "result": res.text}
                elif res.status_code == 422:
                    return {"code": res.status_code, "message": "RequestBodyProcessError or DailyCampaignNotChanged",
                            "result": res.text}
                else:
                    return {"code": res.status_code, "message": "unknown error"}

            except ConnectionError:
                return {"message": "wb connection error"}
            except:
                return {"message": "wb unknown error"}

        elif self.format == 'base':
            try:
                return requests.post(url=url, headers=self.headers, data=json.dumps(body))
            except:
                return None

    def intervals_edit(self,
                       advert_id: int,
                       intervals_begin: list[int],
                       intervals_end: list[int],
                       param: int
                       ):
        """
        Изменение интервалов показа
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1intervals/post
        """

        url = 'https://advert-api.wb.ru/adv/v0/intervals'

        if len(intervals_begin) != len(intervals_end):
            return {"message": "incorrect intervals params"}
        elif len(intervals_begin) > 24 or len(intervals_end) > 24:
            return {"message": "incorrect intervals params"}
        elif not all([1 <= n <= 24 for n in intervals_begin]) or not all([1 <= n <= 24 for n in intervals_end]):
            return {"message": "incorrect intervals params"}
        else:

            intervals = [{"begin": begin, "end": end} for begin, end in zip(intervals_begin, intervals_end)]

            body = {
                "advertId": advert_id,
                "intervals": intervals,
                "param": param
            }

            if self.format == 'normal':
                try:
                    res = requests.post(url=url, headers=self.headers, data=json.dumps(body))

                    if res.status_code == 200:
                        return {"code": res.status_code, "message": "success"}
                    elif res.status_code == 400:
                        return {"code": res.status_code,
                                "message": "InvalidRcId or IncorrectParam or IncorrectNumDisplayIntervals or IncorrectDisplayInterval or IncorrectSupplierId",
                                "result": res.text}
                    elif res.status_code == 401:
                        return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                                "result": res.text}
                    elif res.status_code == 422:
                        return {"code": res.status_code,
                                "message": "RequestBodyProcessError or CampaignIntervalsNotChanged or DisplayIntervalError",
                                "result": res.text}
                    else:
                        return {"code": res.status_code, "message": "unknown error"}

                except ConnectionError:
                    return {"message": "wb connection error"}
                except:
                    return {"message": "wb unknown error"}

            elif self.format == 'base':
                try:
                    return requests.post(url=url, headers=self.headers, data=json.dumps(body))
                except:
                    return None

    def nmactive_edit(self,
                      advert_id: int,
                      active_nm: list[int],
                      active_states: list[bool],
                      param: int
                      ):
        """
        Изменение активности номенклатур кампании
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1nmactive/post
        """

        url = 'https://advert-api.wb.ru/adv/v0/nmactive'

        if len(active_nm) != len(active_states):
            return {"message": "incorrect intervals params"}
        elif len(active_nm) > 50 or len(active_states) > 50:
            return {"message": "incorrect intervals params"}
        else:
            active = [{"nm": nm, "active": active} for nm, active in zip(active_nm, active_states)]

            body = {
                "advertId": advert_id,
                "active": active,
                "param": param
            }

            if self.format == 'normal':
                try:
                    res = requests.post(url=url, headers=self.headers, data=json.dumps(body))

                    if res.status_code == 200:
                        return {"code": res.status_code, "message": "success"}
                    elif res.status_code == 400:
                        return {"code": res.status_code,
                                "message": "InvalidRcId or IncorrectParam or IncorrectActive or IncorrectNumItems or IncorrectNm or IncorrectSupplierId",
                                "result": res.text}
                    elif res.status_code == 401:
                        return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                                "result": res.text}
                    elif res.status_code == 422:
                        return {"code": res.status_code,
                                "message": "RequestBodyProcessError or ActivityNomNotChanged",
                                "result": res.text}
                    else:
                        return {"code": res.status_code, "message": "unknown error"}

                except ConnectionError:
                    return {"message": "wb connection error"}
                except:
                    return {"message": "wb unknown error"}

            elif self.format == 'base':
                try:
                    return requests.post(url=url, headers=self.headers, data=json.dumps(body))
                except:
                    return None

    def dictionary_subject_id(self,
                              id_: str | None = None):
        """
        Словарь значений параметра subjectId
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1params~1subject/get
        """

        url = 'https://advert-api.wb.ru/adv/v0/params/subject'

        if self.format == 'normal':
            try:
                if id_ is not None:
                    params = {'id': id_}
                    res = requests.get(url=url, headers=self.headers, params=params)
                else:
                    res = requests.get(url=url, headers=self.headers)

                if res.status_code == 200:
                    return {"code": res.status_code, "message": "success", "result": res.json()}
                elif res.status_code == 400:
                    return {"code": res.status_code, "message": "IncorrectSupplierId", "result": res.text}
                elif res.status_code == 401:
                    return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                            "result": res.text}
                else:
                    return {"code": res.status_code, "message": "unknown error"}

            except ConnectionError:
                return {"message": "wb connection error"}
            except:
                return {"message": "wb unknown error"}

        elif self.format == 'base':
            try:
                if id_ is not None:
                    params = {'id': id_}
                    res = requests.get(url=url, headers=self.headers, params=params)
                else:
                    res = requests.get(url=url, headers=self.headers)
                return res
            except:
                return None

    def dictionary_menu_id(self,
                           id_: str | None = None):
        """
        Словарь значений параметра menuId
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1params~1menu/get
        """

        url = 'https://advert-api.wb.ru/adv/v0/params/menu'

        if self.format == 'normal':
            try:
                if id_ is not None:
                    params = {'id': id_}
                    res = requests.get(url=url, headers=self.headers, params=params)
                else:
                    res = requests.get(url=url, headers=self.headers)

                if res.status_code == 200:
                    return {"code": res.status_code, "message": "success", "result": res.json()}
                elif res.status_code == 400:
                    return {"code": res.status_code, "message": "IncorrectSupplierId", "result": res.text}
                elif res.status_code == 401:
                    return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                            "result": res.text}
                else:
                    return {"code": res.status_code, "message": "unknown error"}

            except ConnectionError:
                return {"message": "wb connection error"}
            except:
                return {"message": "wb unknown error"}

        elif self.format == 'base':
            try:
                if id_ is not None:
                    params = {'id': id_}
                    res = requests.get(url=url, headers=self.headers, params=params)
                else:
                    res = requests.get(url=url, headers=self.headers)
                return res
            except:
                return None

    def dictionary_set_id(self, id_: int):
        """
        Словарь значений параметра setId
        https://openapi.wildberries.ru/#tag/Reklama/paths/~1adv~1v0~1params~1set/get
        """

        url = 'https://advert-api.wb.ru/adv/v0/params/set'

        if self.format == 'normal':
            try:
                if id_ is not None:
                    params = {'id': id_}
                    res = requests.get(url=url, headers=self.headers, params=params)
                else:
                    res = requests.get(url=url, headers=self.headers)

                if res.status_code == 200:
                    return {"code": res.status_code, "message": "success", "result": res.json()}
                elif res.status_code == 400:
                    return {"code": res.status_code, "message": "IncorrectSupplierId", "result": res.text}
                elif res.status_code == 401:
                    return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                            "result": res.text}
                else:
                    return {"code": res.status_code, "message": "unknown error"}

            except ConnectionError:
                return {"message": "wb connection error"}
            except:
                return {"message": "wb unknown error"}

        elif self.format == 'base':
            try:
                if id_ is not None:
                    params = {'id': id_}
                    res = requests.get(url=url, headers=self.headers, params=params)
                else:
                    res = requests.get(url=url, headers=self.headers)
                return res
            except:
                return None

    def unanswered_questions(self):
        """
        Неотвеченные вопросы
        https://openapi.wildberries.ru/#tag/Voprosy/paths/~1api~1v1~1questions~1count-unanswered/get
        """

        url = 'https://feedbacks-api.wildberries.ru/api/v1/questions/count-unanswered'

        try:
            res = requests.get(url=url, headers=self.headers)

            if res.status_code == 200:
                return {"code": res.status_code, "message": "success", "result": res.json()}
            elif res.status_code == 400:
                return {"code": res.status_code, "message": "params error", "result": self.read_res(res)}
            elif res.status_code == 401:
                return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                        "result": self.read_res(res)}
            else:
                return {"code": res.status_code, "message": "unknown error"}

        except ConnectionError:
            return {"message": "wb connection error"}
        except:
            return {"message": "wb unknown error"}

    def new_feedback_questions(self):
        """
        Непросмотренные отзывы и вопросы
        https://openapi.wildberries.ru/#tag/Voprosy/paths/~1api~1v1~1new-feedbacks-questions/get
        """

        url = 'https://feedbacks-api.wildberries.ru/api/v1/new-feedbacks-questions'

        try:
            res = requests.get(url=url, headers=self.headers)

            if res.status_code == 200:
                return {"code": res.status_code, "message": "success", "result": res.json()}
            elif res.status_code == 401:
                return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                        "result": self.read_res(res)}
            elif res.status_code == 403:
                return {"code": res.status_code, "message": "authorization error", "result": self.read_res(res)}
            else:
                return {"code": res.status_code, "message": "unknown error"}

        except ConnectionError:
            return {"message": "wb connection error"}
        except:
            return {"message": "wb unknown error"}

    def products_rating(self, size: int):
        """
        Часто спрашиваемые товары
        https://openapi.wildberries.ru/#tag/Voprosy/paths/~1api~1v1~1questions~1products~1rating/get
        """

        url = 'https://feedbacks-api.wildberries.ru/api/v1/questions/products/rating'

        if size > 100:
            return {"message": "incorrect size"}
        else:
            params = {'size': size}

            try:
                res = requests.get(url=url, headers=self.headers, params=params)

                if res.status_code == 200:
                    return {"code": res.status_code, "message": "success", "result": res.json()}
                elif res.status_code == 400:
                    return {"code": res.status_code, "message": "params error", "result": self.read_res(res)}
                elif res.status_code == 401:
                    return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                            "result": self.read_res(res)}
                elif res.status_code == 403:
                    return {"code": res.status_code, "message": "authorization error", "result": self.read_res(res)}
                else:
                    return {"code": res.status_code, "message": "unknown error"}

            except ConnectionError:
                return {"message": "wb connection error"}
            except:
                return {"message": "wb unknown error"}

    def questions(self,
                  is_answered: bool,
                  take: int,
                  skip: int,
                  nm_id: int = None,
                  order: str = "dateDesc"
                  ):
        """
        Список вопросов
        https://openapi.wildberries.ru/#tag/Voprosy/paths/~1api~1v1~1questions/get
        """

        url = 'https://feedbacks-api.wildberries.ru/api/v1/questions'

        params = {
            'isAnswered': is_answered,
            'take': take,
            'skip': skip,
            'order': order
        }

        if nm_id is not None:
            params['nmId'] = nm_id

        if take > 10000:
            return {"message": "incorrect take"}
        else:
            try:
                res = requests.get(url=url, headers=self.headers, params=params)

                if res.status_code == 200:
                    return {"code": res.status_code, "message": "success", "result": res.json()}
                elif res.status_code == 400:
                    return {"code": res.status_code, "message": "params error", "result": self.read_res(res)}
                elif res.status_code == 401:
                    return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                            "result": self.read_res(res)}
                elif res.status_code == 403:
                    return {"code": res.status_code, "message": "authorization error", "result": self.read_res(res)}
                else:
                    return {"code": res.status_code, "message": "unknown error"}

            except ConnectionError:
                return {"message": "wb connection error"}
            except:
                return {"message": "wb unknown error"}

    def questions_work(self,
                       question_id: str,
                       action: str,
                       was_viewed: bool = None,
                       answer: str = None,
                       state: str = None
                       ):
        """
        Работа с вопросами
        https://openapi.wildberries.ru/#tag/Voprosy/paths/~1api~1v1~1questions/patch
        """

        url = 'https://feedbacks-api.wildberries.ru/api/v1/questions'

        if action == "viewed":

            body = {"id": question_id,
                    "wasViewed": was_viewed,
                    }

        elif action == "declined" or action == "answered":

            body = {"id": question_id,
                    "answer": {"text": answer},
                    "state": state
                    }
        else:
            body = {}

        try:
            res = requests.patch(url=url, headers=self.headers, data=json.dumps(body))

            if res.status_code == 200:
                return {"code": res.status_code, "message": "success"}
            elif res.status_code == 400:
                return {"code": res.status_code, "message": "params error", "result": self.read_res(res)}
            elif res.status_code == 401:
                return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                        "result": self.read_res(res)}
            elif res.status_code == 403:
                return {"code": res.status_code, "message": "authorization error", "result": self.read_res(res)}
            elif res.status_code == 404:
                return {"code": res.status_code, "message": "error - not found", "result": self.read_res(res)}
            else:
                return {"code": res.status_code, "message": "unknown error"}

        except ConnectionError:
            return {"message": "wb connection error"}
        except:
            return {"message": "wb unknown error"}

    def questions_xlsx_report(self, is_answered: bool):
        """
        Получение вопросов в формате XLSX
        https://openapi.wildberries.ru/#tag/Voprosy/paths/~1api~1v1~1questions~1report/get
        """

        url = 'https://feedbacks-api.wildberries.ru/api/v1/questions/report'

        params = {'isAnswered': is_answered}

        try:
            res = requests.get(url=url, headers=self.headers, params=params)

            if res.status_code == 200:
                return {"code": res.status_code, "message": "success", "result": res.json()}
            elif res.status_code == 400:
                return {"code": res.status_code, "message": "params error", "result": self.read_res(res)}
            elif res.status_code == 401:
                return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                        "result": self.read_res(res)}
            elif res.status_code == 403:
                return {"code": res.status_code, "message": "authorization error", "result": self.read_res(res)}
            else:
                return {"code": res.status_code, "message": "unknown error"}

        except ConnectionError:
            return {"message": "wb connection error"}
        except:
            return {"message": "wb unknown error"}

    def unanswered_feedbacks(self):
        """
        Необработанные отзывы
        https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks~1count-unanswered/get
        """

        url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks/count-unanswered'

        try:
            res = requests.get(url=url, headers=self.headers)

            if res.status_code == 200:
                return {"code": res.status_code, "message": "success", "result": res.json()}
            elif res.status_code == 400:
                return {"code": res.status_code, "message": "params error", "result": self.read_res(res)}
            elif res.status_code == 401:
                return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                        "result": self.read_res(res)}
            else:
                return {"code": res.status_code, "message": "unknown error"}

        except ConnectionError:
            return {"message": "wb connection error"}
        except:
            return {"message": "wb unknown error"}

    def parent_subjects(self):
        """
        Родительские категории товаров
        https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1parent-subjects/get
        """

        url = 'https://feedbacks-api.wildberries.ru/api/v1/parent-subjects'

        try:
            res = requests.get(url=url, headers=self.headers)

            if res.status_code == 200:
                return {"code": res.status_code, "message": "success", "result": res.json()}
            elif res.status_code == 400:
                return {"code": res.status_code, "message": "params error", "result": self.read_res(res)}
            elif res.status_code == 401:
                return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                        "result": self.read_res(res)}
            elif res.status_code == 403:
                return {"code": res.status_code, "message": "authorization error", "result": self.read_res(res)}
            else:
                return {"code": res.status_code, "message": "unknown error"}

        except ConnectionError:
            return {"message": "wb connection error"}
        except:
            return {"message": "wb unknown error"}

    def feedback_products_rating(self, subject_id: int):
        """
        Средняя оценка товаров по родительской категории
        https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks~1products~1rating/get
        """

        url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks/products/rating'

        params = {'subjectId': subject_id}

        try:
            res = requests.get(url=url, headers=self.headers, params=params)

            if res.status_code == 200:
                return {"code": res.status_code, "message": "success", "result": res.json()}
            elif res.status_code == 400:
                return {"code": res.status_code, "message": "params error", "result": self.read_res(res)}
            elif res.status_code == 401:
                return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                        "result": self.read_res(res)}
            elif res.status_code == 403:
                return {"code": res.status_code, "message": "authorization error", "result": self.read_res(res)}
            else:
                return {"code": res.status_code, "message": "unknown error"}

        except ConnectionError:
            return {"message": "wb connection error"}
        except:
            return {"message": "wb unknown error"}

    def feedback_products_rating_top(self, subject_id: int):
        """
        Товары с наибольшей и наименьшей средней оценкой по родительской категории
        https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks~1products~1rating~1top/get
        """

        url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks/products/rating/top'

        params = {'subjectId': subject_id}

        try:
            res = requests.get(url=url, headers=self.headers, params=params)

            if res.status_code == 200:
                return {"code": res.status_code, "message": "success", "result": res.json()}
            elif res.status_code == 400:
                return {"code": res.status_code, "message": "params error", "result": self.read_res(res)}
            elif res.status_code == 401:
                return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                        "result": self.read_res(res)}
            elif res.status_code == 403:
                return {"code": res.status_code, "message": "authorization error", "result": self.read_res(res)}
            else:
                return {"code": res.status_code, "message": "unknown error"}

        except ConnectionError:
            return {"message": "wb connection error"}
        except:
            return {"message": "wb unknown error"}

    def feedbacks(self,
                  is_answered: bool,
                  take: int,
                  skip: int,
                  nm_id: int = None,
                  order: str = "dateDesc",
                  has_supplier_complaint: bool = None
                  ):
        """
        Список отзывов
        https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks/get
        """

        url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks'

        params = {
            'isAnswered': is_answered,
            'take': take,
            'skip': skip,
            'order': order
        }

        if nm_id is not None:
            params['nmId'] = nm_id
        if has_supplier_complaint is not None:
            params['hasSupplierComplaint'] = has_supplier_complaint

        if take > 10000:
            return {"message": "incorrect take"}

        try:
            res = requests.get(url=url, headers=self.headers, params=params)

            if res.status_code == 200:
                return {"code": res.status_code, "message": "success", "result": res.json()}
            elif res.status_code == 400:
                return {"code": res.status_code, "message": "params error", "result": self.read_res(res)}
            elif res.status_code == 401:
                return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                        "result": self.read_res(res)}
            elif res.status_code == 403:
                return {"code": res.status_code, "message": "authorization error", "result": self.read_res(res)}
            else:
                return {"code": res.status_code, "message": "unknown error"}

        except ConnectionError:
            return {"message": "wb connection error"}
        except:
            return {"message": "wb unknown error"}

    def feedback_work(self,
                      feedback_id: str,
                      action: str,
                      was_viewed: bool = None,
                      answer_text: str = None,
                      create_supplier_complaint: bool = None
                      ):
        """
        Работа с отзывом
        https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks/patch
        """

        url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks'

        if action == "viewed":
            body = {"id": feedback_id,
                    "wasViewed": was_viewed,
                    }
        elif action == "answered":
            body = {"id": feedback_id,
                    "text": answer_text
                    }
        elif action == "complained":
            body = {"id": feedback_id,
                    "createSupplierComplaint": create_supplier_complaint
                    }
        else:
            body = {}

        try:
            res = requests.patch(url=url, headers=self.headers, data=json.dumps(body))

            if res.status_code == 200:
                return {"code": res.status_code, "message": "success"}
            elif res.status_code == 400:
                return {"code": res.status_code, "message": "params error", "result": self.read_res(res)}
            elif res.status_code == 401:
                return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                        "result": self.read_res(res)}
            elif res.status_code == 403:
                return {"code": res.status_code, "message": "authorization error", "result": self.read_res(res)}
            elif res.status_code == 404:
                return {"code": res.status_code, "message": "error - not found", "result": self.read_res(res)}
            elif res.status_code == 422:
                return {"code": res.status_code, "message": "error - unknown", "result": self.read_res(res)}
            else:
                return {"code": res.status_code, "message": "unknown error"}

        except ConnectionError:
            return {"message": "wb connection error"}
        except:
            return {"message": "wb unknown error"}

    def feedbacks_xlsx_report(self,
                              is_answered: bool,
                              has_supplier_complaint: bool = None
                              ):
        """
        Получение отзывов в формате XLSX
        https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks~1report/get
        """

        url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks/report'

        params = {'isAnswered': is_answered}

        if has_supplier_complaint is not None:
            params['hasSupplierComplaint'] = has_supplier_complaint

        try:
            res = requests.get(url=url, headers=self.headers, params=params)

            if res.status_code == 200:
                return {"code": res.status_code, "message": "success", "result": res.json()}
            elif res.status_code == 400:
                return {"code": res.status_code, "message": "params error", "result": self.read_res(res)}
            elif res.status_code == 401:
                return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                        "result": self.read_res(res)}
            elif res.status_code == 403:
                return {"code": res.status_code, "message": "authorization error", "result": self.read_res(res)}
            else:
                return {"code": res.status_code, "message": "unknown error"}

        except ConnectionError:
            return {"message": "wb connection error"}
        except:
            return {"message": "wb unknown error"}

    def feedbacks_archived(self,
                           take: int,
                           skip: int,
                           nm_id: int = None,
                           order: str = "dateDesc",
                           has_supplier_complaint: bool = None
                           ):
        """
        Список архивных отзывов
        https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks~1archive/get
        """

        url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks/archive'

        params = {
            'take': take,
            'skip': skip,
            'order': order
        }

        if nm_id is not None:
            params['nmId'] = nm_id
        if has_supplier_complaint is not None:
            params['hasSupplierComplaint'] = has_supplier_complaint

        try:
            res = requests.get(url=url, headers=self.headers, params=params)

            if res.status_code == 200:
                return {"code": res.status_code, "message": "success", "result": res.json()}
            elif res.status_code == 400:
                return {"code": res.status_code, "message": "params error", "result": self.read_res(res)}
            elif res.status_code == 401:
                return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                        "result": self.read_res(res)}
            elif res.status_code == 403:
                return {"code": res.status_code, "message": "authorization error", "result": self.read_res(res)}
            else:
                return {"code": res.status_code, "message": "unknown error"}

        except ConnectionError:
            return {"message": "wb connection error"}
        except:
            return {"message": "wb unknown error"}

    def products_rating_nm_id(self, nm_id: int):
        """
        Средняя оценка товара по nmId
        https://openapi.wildberries.ru/#tag/Otzyvy/paths/~1api~1v1~1feedbacks~1products~1rating~1nmid/get
        """

        url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks/products/rating/nmid'

        params = {'nmId': nm_id}

        try:
            res = requests.get(url=url, headers=self.headers, params=params)

            if res.status_code == 200:
                return {"code": res.status_code, "message": "success", "result": res.json()}
            elif res.status_code == 400:
                return {"code": res.status_code, "message": "params error", "result": self.read_res(res)}
            elif res.status_code == 401:
                return {"code": res.status_code, "message": "TokenMissing or TokenInvalid or TokenNotFound",
                        "result": self.read_res(res)}
            elif res.status_code == 403:
                return {"code": res.status_code, "message": "authorization error", "result": self.read_res(res)}
            else:
                return {"code": res.status_code, "message": "unknown error"}

        except ConnectionError:
            return {"message": "wb connection error"}
        except:
            return {"message": "wb unknown error"}






