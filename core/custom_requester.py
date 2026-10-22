"""Кастомный реквестер для API запросов."""

import json
import requests
import logging
import os
from typing import Optional, Union, Dict, Any, List

from pydantic import BaseModel


class CustomRequester:
    """
    Кастомный реквестер для стандартизации и упрощения отправки HTTP-запросов.
    """
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, session: requests.Session, base_url: str):
        self.session = session
        self.base_url = base_url.rstrip('/')  # Убираем trailing slash
        self.headers = self.base_headers.copy()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(self, method, endpoint, data=None, params=None,
                     expected_status=200, need_logging=True, base_url=None, **kwargs):

        # 1. Выбираем базовый URL: либо переданный, либо дефолтный
        actual_base_url = base_url.rstrip('/') if base_url else self.base_url

        # 2. Аккуратно склеиваем URL
        endpoint = endpoint.lstrip('/')
        url = f"{actual_base_url}/{endpoint}"

        # 3. Превращаем Pydantic-модель в словарь, если нужно
        if isinstance(data, BaseModel):
            data = json.loads(data.model_dump_json(exclude_unset=True))

        # 4. Делаем запрос (теперь base_url не попадет в kwargs)
        response = self.session.request(method, url, json=data, params=params, **kwargs)

        if need_logging:
            self.log_request_and_response(response)

        # 5. Проверяем статус (добавим поддержку списка статусов)
        if isinstance(expected_status, (list, tuple, set)):
            if response.status_code not in expected_status:
                raise ValueError(
                    f"Unexpected status code: {response.status_code}. Expected one of: {expected_status}"
                )
        elif expected_status is not None:
            if response.status_code != expected_status:
                raise ValueError(
                    f"Unexpected status code: {response.status_code}. Expected: {expected_status}"
                )

        return response

    def set_headers(self, **kwargs):
        """Обновление заголовков сессии."""
        self.headers.update(kwargs)
        self.session.headers.update(self.headers)

    def set_auth_token(self, token: str):
        """Установка Bearer токена для авторизации."""
        self.set_headers(Authorization=f"Bearer {token}")

    def log_request_and_response(self, response):
        """Логирование запросов и ответов."""
        try:
            request = response.request
            GREEN = '\033[32m'
            RED = '\033[31m'
            RESET = '\033[0m'
            headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
                body = f"-d '{body}' \n" if body != '{}' else ''

            # Логируем запрос
            self.logger.info(f"\n{'=' * 40} REQUEST {'=' * 40}")
            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            # Обрабатываем ответ
            response_status = response.status_code
            is_success = response.ok
            response_data = response.text

            # Попытка форматировать JSON
            try:
                response_data = json.dumps(json.loads(response.text), indent=4, ensure_ascii=False)
            except json.JSONDecodeError:
                pass

            # Логируем ответ
            self.logger.info(f"\n{'=' * 40} RESPONSE {'=' * 40}")
            if not is_success:
                self.logger.info(
                    f"\tSTATUS_CODE: {RED}{response_status}{RESET}\n"
                    f"\tDATA: {RED}{response_data}{RESET}"
                )
            else:
                self.logger.info(
                    f"\tSTATUS_CODE: {GREEN}{response_status}{RESET}\n"
                    f"\tDATA:\n{response_data}"
                )
            self.logger.info(f"{'=' * 80}\n")
        except Exception as e:
            self.logger.error(f"\nLogging failed: {type(e)} - {e}")