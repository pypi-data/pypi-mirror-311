from snowddl.blueprint import DatabaseBlueprint, DatabaseIdent, Grant, ObjectType, build_role_ident
from snowddl.parser.abc_parser import AbstractParser


# fmt: off
database_json_schema = {
    "type": "object",
    "properties": {
        "permission_model": {
            "type": "string",
        },
        "is_transient": {
            "type": "boolean"
        },
        "retention_time": {
            "type": "integer"
        },
        "is_sandbox": {
            "type": "boolean"
        },
        "owner_database_read": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "owner_database_write": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "owner_share_read": {
            "share_read": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
        },
        "owner_integration_usage": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "owner_warehouse_usage": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "owner_account_grants": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "owner_global_roles": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "comment": {
            "type": "string"
        }
    },
    "additionalProperties": False
}
# fmt: on


class DatabaseParser(AbstractParser):
    def load_blueprints(self):
        for database_name in self.get_database_names():
            database_params = self.parse_single_file(f"{database_name}/params", database_json_schema)

            # fmt: off
            databases_permission_model_name = database_params.get("permission_model", self.config.DEFAULT_PERMISSION_MODEL).upper()
            database_permission_model = self.config.get_permission_model(databases_permission_model_name)
            # fmt: on

            if not database_permission_model.ruleset.create_database_owner_role:
                for k in database_params:
                    if k.startswith("owner_"):
                        raise ValueError(
                            f"Cannot use parameter [{k}] for database [{database_name}] due to schema-level permission model. "
                            f"This parameter should be configured on schema level"
                        )

            owner_additional_grants = []
            owner_additional_account_grants = []

            for grant_database_name in database_params.get("owner_database_read", []):
                owner_additional_grants.append(self.build_database_role_grant(grant_database_name, self.config.READ_ROLE_TYPE))

            for grant_database_name in database_params.get("owner_database_write", []):
                owner_additional_grants.append(self.build_database_role_grant(grant_database_name, self.config.WRITE_ROLE_TYPE))

            for share_name in database_params.get("owner_share_read", []):
                owner_additional_grants.append(self.build_share_role_grant(share_name))
                self.config.add_blueprint(self.build_share_role_blueprint(share_name))

            for integration_name in database_params.get("owner_integration_usage", []):
                owner_additional_grants.append(self.build_integration_usage_grant(integration_name))

            for warehouse_name in database_params.get("owner_warehouse_usage", []):
                owner_additional_grants.append(self.build_warehouse_role_grant(warehouse_name, self.config.USAGE_ROLE_TYPE))

            for account_grant in database_params.get("owner_account_grants", []):
                owner_additional_account_grants.append(self.build_account_grant(account_grant))

            for global_role_name in database_params.get("owner_global_roles", []):
                owner_additional_grants.append(self.build_global_role_grant(global_role_name))

            bp = DatabaseBlueprint(
                full_name=DatabaseIdent(self.env_prefix, database_name),
                permission_model=databases_permission_model_name,
                is_transient=database_params.get("is_transient", False),
                retention_time=database_params.get("retention_time", None),
                is_sandbox=database_params.get("is_sandbox", False),
                owner_additional_grants=owner_additional_grants,
                owner_additional_account_grants=owner_additional_account_grants,
                comment=database_params.get("comment", None),
            )

            self.config.add_blueprint(bp)

    def build_database_role_grant(self, database_name, role_type):
        return Grant(
            privilege="USAGE",
            on=ObjectType.ROLE,
            name=build_role_ident(self.env_prefix, database_name, role_type, self.config.DATABASE_ROLE_SUFFIX),
        )
