"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from .basesdk import BaseSDK
from friendli import models, utils
from friendli._hooks import HookContext
from friendli.types import OptionalNullable, UNSET
from friendli.utils import eventstreaming, get_security_from_env
from typing import Optional, Union


class FriendliCompletions(BaseSDK):
    def complete(
        self,
        *,
        dedicated_completions_complete_body: Union[
            models.DedicatedCompletionsCompleteBody,
            models.DedicatedCompletionsCompleteBodyTypedDict,
        ],
        x_friendli_team: Optional[str] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> models.CompletionsResult:
        r"""Completions

        Generate text based on the given text prompt.

        :param dedicated_completions_complete_body:
        :param x_friendli_team: ID of team to run requests as (optional parameter).
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = models.DedicatedCompletionsCompleteRequest(
            x_friendli_team=x_friendli_team,
            dedicated_completions_complete_body=utils.get_pydantic_model(
                dedicated_completions_complete_body,
                models.DedicatedCompletionsCompleteBody,
            ),
        )

        req = self.build_request(
            method="POST",
            path="/dedicated/v1/completions",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(
                request.dedicated_completions_complete_body,
                False,
                False,
                "json",
                models.DedicatedCompletionsCompleteBody,
            ),
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = self.do_request(
            hook_ctx=HookContext(
                operation_id="dedicatedCompletionsComplete",
                oauth2_scopes=[],
                security_source=get_security_from_env(
                    self.sdk_configuration.security, models.Security
                ),
            ),
            request=req,
            error_status_codes=["4XX", "5XX"],
            retry_config=retry_config,
        )

        if utils.match_response(http_res, "200", "application/json"):
            return utils.unmarshal_json(http_res.text, models.CompletionsResult)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            http_res_text = utils.stream_to_text(http_res)
            raise models.SDKError(
                "API error occurred", http_res.status_code, http_res_text, http_res
            )

        content_type = http_res.headers.get("Content-Type")
        http_res_text = utils.stream_to_text(http_res)
        raise models.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res_text,
            http_res,
        )

    async def complete_async(
        self,
        *,
        dedicated_completions_complete_body: Union[
            models.DedicatedCompletionsCompleteBody,
            models.DedicatedCompletionsCompleteBodyTypedDict,
        ],
        x_friendli_team: Optional[str] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> models.CompletionsResult:
        r"""Completions

        Generate text based on the given text prompt.

        :param dedicated_completions_complete_body:
        :param x_friendli_team: ID of team to run requests as (optional parameter).
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = models.DedicatedCompletionsCompleteRequest(
            x_friendli_team=x_friendli_team,
            dedicated_completions_complete_body=utils.get_pydantic_model(
                dedicated_completions_complete_body,
                models.DedicatedCompletionsCompleteBody,
            ),
        )

        req = self.build_request_async(
            method="POST",
            path="/dedicated/v1/completions",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="application/json",
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(
                request.dedicated_completions_complete_body,
                False,
                False,
                "json",
                models.DedicatedCompletionsCompleteBody,
            ),
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = await self.do_request_async(
            hook_ctx=HookContext(
                operation_id="dedicatedCompletionsComplete",
                oauth2_scopes=[],
                security_source=get_security_from_env(
                    self.sdk_configuration.security, models.Security
                ),
            ),
            request=req,
            error_status_codes=["4XX", "5XX"],
            retry_config=retry_config,
        )

        if utils.match_response(http_res, "200", "application/json"):
            return utils.unmarshal_json(http_res.text, models.CompletionsResult)
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            http_res_text = await utils.stream_to_text_async(http_res)
            raise models.SDKError(
                "API error occurred", http_res.status_code, http_res_text, http_res
            )

        content_type = http_res.headers.get("Content-Type")
        http_res_text = await utils.stream_to_text_async(http_res)
        raise models.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res_text,
            http_res,
        )

    def stream(
        self,
        *,
        dedicated_completions_stream_body: Union[
            models.DedicatedCompletionsStreamBody,
            models.DedicatedCompletionsStreamBodyTypedDict,
        ],
        x_friendli_team: Optional[str] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> eventstreaming.EventStream[models.StreamedCompletionsResult]:
        r"""Stream completions

        Generate text based on the given text prompt.

        :param dedicated_completions_stream_body:
        :param x_friendli_team: ID of team to run requests as (optional parameter).
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = models.DedicatedCompletionsStreamRequest(
            x_friendli_team=x_friendli_team,
            dedicated_completions_stream_body=utils.get_pydantic_model(
                dedicated_completions_stream_body, models.DedicatedCompletionsStreamBody
            ),
        )

        req = self.build_request(
            method="POST",
            path="/dedicated/v1/completions#stream",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="text/event-stream",
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(
                request.dedicated_completions_stream_body,
                False,
                False,
                "json",
                models.DedicatedCompletionsStreamBody,
            ),
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = self.do_request(
            hook_ctx=HookContext(
                operation_id="dedicatedCompletionsStream",
                oauth2_scopes=[],
                security_source=get_security_from_env(
                    self.sdk_configuration.security, models.Security
                ),
            ),
            request=req,
            error_status_codes=["4XX", "5XX"],
            stream=True,
            retry_config=retry_config,
        )

        if utils.match_response(http_res, "200", "text/event-stream"):
            return eventstreaming.EventStream(
                http_res,
                lambda raw: utils.unmarshal_json(raw, models.StreamedCompletionsResult),
                sentinel="[DONE]",
            )
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            http_res_text = utils.stream_to_text(http_res)
            raise models.SDKError(
                "API error occurred", http_res.status_code, http_res_text, http_res
            )

        content_type = http_res.headers.get("Content-Type")
        http_res_text = utils.stream_to_text(http_res)
        raise models.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res_text,
            http_res,
        )

    async def stream_async(
        self,
        *,
        dedicated_completions_stream_body: Union[
            models.DedicatedCompletionsStreamBody,
            models.DedicatedCompletionsStreamBodyTypedDict,
        ],
        x_friendli_team: Optional[str] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
    ) -> Union[
        eventstreaming.EventStream[models.StreamedCompletionsResult],
        eventstreaming.EventStreamAsync[models.StreamedCompletionsResult],
    ]:
        r"""Stream completions

        Generate text based on the given text prompt.

        :param dedicated_completions_stream_body:
        :param x_friendli_team: ID of team to run requests as (optional parameter).
        :param retries: Override the default retry configuration for this method
        :param server_url: Override the default server URL for this method
        :param timeout_ms: Override the default request timeout configuration for this method in milliseconds
        """
        base_url = None
        url_variables = None
        if timeout_ms is None:
            timeout_ms = self.sdk_configuration.timeout_ms

        if server_url is not None:
            base_url = server_url

        request = models.DedicatedCompletionsStreamRequest(
            x_friendli_team=x_friendli_team,
            dedicated_completions_stream_body=utils.get_pydantic_model(
                dedicated_completions_stream_body, models.DedicatedCompletionsStreamBody
            ),
        )

        req = self.build_request_async(
            method="POST",
            path="/dedicated/v1/completions#stream",
            base_url=base_url,
            url_variables=url_variables,
            request=request,
            request_body_required=True,
            request_has_path_params=False,
            request_has_query_params=True,
            user_agent_header="user-agent",
            accept_header_value="text/event-stream",
            security=self.sdk_configuration.security,
            get_serialized_body=lambda: utils.serialize_request_body(
                request.dedicated_completions_stream_body,
                False,
                False,
                "json",
                models.DedicatedCompletionsStreamBody,
            ),
            timeout_ms=timeout_ms,
        )

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        retry_config = None
        if isinstance(retries, utils.RetryConfig):
            retry_config = (retries, ["429", "500", "502", "503", "504"])

        http_res = await self.do_request_async(
            hook_ctx=HookContext(
                operation_id="dedicatedCompletionsStream",
                oauth2_scopes=[],
                security_source=get_security_from_env(
                    self.sdk_configuration.security, models.Security
                ),
            ),
            request=req,
            error_status_codes=["4XX", "5XX"],
            stream=True,
            retry_config=retry_config,
        )

        if utils.match_response(http_res, "200", "text/event-stream"):
            return eventstreaming.EventStreamAsync(
                http_res,
                lambda raw: utils.unmarshal_json(raw, models.StreamedCompletionsResult),
                sentinel="[DONE]",
            )
        if utils.match_response(http_res, ["4XX", "5XX"], "*"):
            http_res_text = await utils.stream_to_text_async(http_res)
            raise models.SDKError(
                "API error occurred", http_res.status_code, http_res_text, http_res
            )

        content_type = http_res.headers.get("Content-Type")
        http_res_text = await utils.stream_to_text_async(http_res)
        raise models.SDKError(
            f"Unexpected response received (code: {http_res.status_code}, type: {content_type})",
            http_res.status_code,
            http_res_text,
            http_res,
        )
