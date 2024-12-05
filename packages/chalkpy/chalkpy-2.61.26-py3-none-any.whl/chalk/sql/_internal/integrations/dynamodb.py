from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Any, Dict

from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine
    from sqlalchemy.engine.url import URL


_logger = get_logger(__name__)


class DynamoDBSourceImpl(BaseSQLSource):
    kind = SQLSourceKind.dynamodb

    def __init__(
        self,
        name: str | None = None,
        aws_client_id_override: str | None = None,
        aws_client_secret_override: str | None = None,
        aws_role_arn_override: str | None = None,
        aws_region_override: str | None = None,
        endpoint_override: str | None = None,
        engine_args: Dict[str, Any] | None = None,
    ):
        try:
            import boto3
            import pydynamodb
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[dynamodb]")
        del boto3, pydynamodb  # unused

        self.ingested_tables: Dict[str, Any] = {}
        self.aws_client_id_override = aws_client_id_override or load_integration_variable(
            integration_name=name, name="DYNAMODB_AWS_CLIENT_ID_OVERRIDE"
        )
        self.aws_client_secret_override = aws_client_secret_override or load_integration_variable(
            integration_name=name, name="DYNAMODB_AWS_CLIENT_SECRET_OVERRIDE"
        )
        self.aws_role_arn_override = aws_role_arn_override or load_integration_variable(
            integration_name=name, name="DYNAMODB_AWS_ROLE_ARN_OVERRIDE"
        )
        self.aws_region_override = aws_region_override or load_integration_variable(
            integration_name=name, name="DYNAMODB_AWS_REGION_OVERRIDE"
        )
        self.endpoint_override = endpoint_override or load_integration_variable(
            integration_name=name, name="DYNAMODB_ENDPOINT_OVERRIDE"
        )
        if self.aws_role_arn_override is not None and (
            self.aws_client_id_override is not None or self.aws_client_secret_override is not None
        ):
            raise ValueError(
                "If you provide an AWS role ARN override, you cannot provide an AWS client ID or secret override."
            )
        if self.aws_client_id_override is not None and self.aws_client_secret_override is None:
            raise ValueError(
                "If you provide an AWS client ID override, you must also provide an AWS client secret override."
            )
        if self.aws_client_secret_override is not None and self.aws_client_id_override is None:
            raise ValueError(
                "If you provide an AWS client secret override, you must also provide an AWS client ID override."
            )
        eargs = {}
        if engine_args is not None:
            eargs = engine_args
        else:
            found = load_integration_variable(
                integration_name=name,
                name="DYNAMODB_ENGINE_ARGUMENTS",
                parser=json.loads,
            )
            if found is not None:
                eargs = found

        # The SQL sources are read-only, so transactions are not needed.
        # Setting the isolation level on the engine, instead of the connection, avoids
        # a DBAPI statement to reset the transactional level back to the default before returning the
        # connection to the pool.
        eargs.setdefault(
            "isolation_level",
            os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"),
        )

        # # Dynamo defaults to ReadWrite, but Chalk only reads data from dynamo.
        # eargs.setdefault("read_only", True)

        BaseSQLSource.__init__(self, name=name, engine_args=eargs, async_engine_args={})

    def get_engine(self) -> "Engine":
        try:
            from pydynamodb.sqlalchemy_dynamodb.pydynamodb import DynamoDBDialect
            from sqlalchemy.engine import create_engine
        except ImportError:
            raise missing_dependency_exception("chalkpy[dynamodb]")

        if self._engine is None:  # pyright: ignore[reportUnnecessaryComparison]
            self._engine = create_engine(
                self.local_engine_url().render_as_string(), executor=DynamoDBDialect()
            ).execution_options(**self.engine_args)

        return self._engine

    def local_engine_url(self) -> "URL":
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="dynamodb",
            host=self.endpoint_override
            or (f"dynamodb.{self.aws_region_override}.amazonaws.com" if self.aws_region_override else None),
            username=self.aws_client_id_override,
            password=self.aws_client_secret_override,
        )

    # def get_sqlglot_dialect(self) -> str | None:
    #     return "partiql"
