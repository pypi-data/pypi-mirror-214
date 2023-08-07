import json
import logging
from json import (
    load,
)
from pathlib import (
    Path,
)

from openapi_core.contrib.requests import (
    RequestsOpenAPIRequest,
)
from openapi_core.spec.shortcuts import (
    create_spec,
)
from requests.models import (
    PreparedRequest,
    Response,
)
from requests.sessions import (
    Session,
)
from uploader_client.interfaces.rest import (
    OpenAPIInterface,
)

from uploader_client.contrib.rdm.interfaces.validation import (
    RequestValidator,
)


logger = logging.getLogger('uploader_client')


class OpenAPIInterfaceEmulation(OpenAPIInterface):

    def _send_request(
        self, session: Session, http_request: PreparedRequest, **http_kwargs
    ) -> Response:
        """Эмуляция запроса-ответа.

        Получает запрос, вместо отправки валидирует его.
        Код ответа зависит от успешности валидации.
        """

        openapi_request = RequestsOpenAPIRequest(http_request)

        spec_dict = self._get_spec()
        validator = self._get_request_validator()

        result = validator.validate(openapi_request)

        response = Response()

        assert http_request.url
        response.url = http_request.url
        response.status_code = 200
        response.data = json.dumps(
            spec_dict['paths'][result.path.pattern][http_request.method.lower()]['responses']['200']['content'][
                'application/json']['schema']['example'])

        if result.errors:
            logger.error('; '.join(str(err) for err in result.errors))
            response.status_code = 400
        else:
            logger.info('Запрос прошел валидацию')
            response.status_code = 200

        return response

    def _get_spec(self):
        """Получения объекта json-спецификации."""
        with Path(__file__).parent.joinpath('rdm.json').open('r') as spec_file:
            return load(spec_file)

    def _get_request_validator(self):
        """Получение валидатора запроса в витрину."""
        spec_dict = self._get_spec()
        return RequestValidator(create_spec(spec_dict))
