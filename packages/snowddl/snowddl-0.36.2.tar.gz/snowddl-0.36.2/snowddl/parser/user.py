from snowddl.blueprint import (
    UserBlueprint,
    AccountObjectIdent,
    AuthenticationPolicyBlueprint,
    AuthenticationPolicyReference,
    NetworkPolicyBlueprint,
    NetworkPolicyReference,
    ObjectType,
    SchemaObjectIdent,
    build_role_ident,
    build_default_namespace_ident,
)
from snowddl.parser.abc_parser import AbstractParser, ParsedFile
from snowddl.parser.business_role import business_role_json_schema


# fmt: off
user_json_schema = {
    "type": "object",
    "additionalProperties": {
        "properties": {
            "login_name": {
                "type": "string"
            },
            "display_name": {
                "type": "string"
            },
            "first_name": {
                "type": "string"
            },
            "last_name": {
                "type": "string"
            },
            "email": {
                "type": "string"
            },
            "disabled": {
                "type": "boolean"
            },
            "password": {
                "type": "string"
            },
            "rsa_public_key": {
                "type": "string"
            },
            "rsa_public_key_2": {
                "type": "string"
            },
            "type": {
                "type": "string",
            },
            "default_warehouse": {
                "type": "string"
            },
            "default_namespace": {
                "type": "string"
            },
            "session_params": {
                "type": "object",
                "additionalProperties": {
                    "type": ["boolean", "number", "string"]
                }
            },
            "business_roles": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "minItems": 1
            },
            "comment": {
                "type": "string"
            },
            "authentication_policy": {
                "type": "string",
            },
            "network_policy": {
                "type": "string",
            },
        },
        "additionalProperties": False
    }
}
# fmt: on


class UserParser(AbstractParser):
    def load_blueprints(self):
        self.parse_single_file("user", user_json_schema, self.process_user)

    def process_user(self, f: ParsedFile):
        default_warehouse_map = self.get_default_warehouse_map()

        for user_name, user in f.params.items():
            business_roles = []
            default_warehouse = user.get("default_warehouse")

            for business_role_name in user.get("business_roles", []):
                business_roles.append(build_role_ident(self.env_prefix, business_role_name, self.config.BUSINESS_ROLE_SUFFIX))

                if default_warehouse is None:
                    default_warehouse = default_warehouse_map.get(business_role_name)

            full_user_name = AccountObjectIdent(self.env_prefix, user_name)

            if user.get("login_name"):
                # Login name is string, not identifier (!), special characters like '@#!' are permitted
                # But it still requires env_prefix due to unique constraint
                login_name = f"{self.config.env_prefix}{user.get('login_name')}".upper()
            else:
                login_name = str(full_user_name)

            if user.get("display_name"):
                display_name = str(user.get("display_name")).upper()
            else:
                display_name = str(full_user_name)

            bp = UserBlueprint(
                full_name=full_user_name,
                login_name=login_name,
                display_name=display_name,
                first_name=user.get("first_name"),
                last_name=user.get("last_name"),
                email=user.get("email"),
                disabled=user.get("disabled", False),
                password=user.get("password"),
                rsa_public_key=user.get("rsa_public_key").replace(" ", "") if user.get("rsa_public_key") else None,
                rsa_public_key_2=user.get("rsa_public_key_2").replace(" ", "") if user.get("rsa_public_key_2") else None,
                type=str(user.get("type")).upper() if user.get("type") else None,
                default_warehouse=AccountObjectIdent(self.env_prefix, default_warehouse) if default_warehouse else None,
                default_namespace=build_default_namespace_ident(self.env_prefix, user.get("default_namespace"))
                if user.get("default_namespace")
                else None,
                session_params=self.normalise_params_dict(user.get("session_params", {})),
                business_roles=business_roles,
                comment=user.get("comment"),
            )

            self.validate_user_type_properties(bp)
            self.config.add_blueprint(bp)

            # Authentication policy
            if user.get("authentication_policy"):
                policy_name_parts = user.get("authentication_policy").split(".")

                if len(policy_name_parts) != 3:
                    raise ValueError(
                        f"Authentication policy [{user.get('authentication_policy')}] should use fully-qualified identifier <database>.<schema>.<name> for user [{full_user_name}]"
                    )

                policy_name = SchemaObjectIdent(self.env_prefix, *policy_name_parts)

                ref = AuthenticationPolicyReference(
                    object_type=ObjectType.USER,
                    object_name=full_user_name,
                )

                self.config.add_policy_reference(AuthenticationPolicyBlueprint, policy_name, ref)

            # Network policy
            if user.get("network_policy"):
                policy_name = AccountObjectIdent(self.env_prefix, user.get("network_policy"))

                ref = NetworkPolicyReference(
                    object_type=ObjectType.USER,
                    object_name=full_user_name,
                )

                self.config.add_policy_reference(NetworkPolicyBlueprint, policy_name, ref)

            if "NETWORK_POLICY" in bp.session_params:
                raise ValueError(
                    "NETWORK_POLICY in session_params of USER is no longer supported. Please use dedicated [network_policy] parameter instead. Read more: https://docs.snowddl.com/breaking-changes-log/0.33.0-october-2024"
                )

    def get_default_warehouse_map(self):
        default_warehouse_map = {}

        business_role_config = self.parse_single_file("business_role", business_role_json_schema)

        for business_role_name, business_role in business_role_config.items():
            if "warehouse_usage" not in business_role:
                continue

            default_warehouse_map[business_role_name] = business_role["warehouse_usage"][0]

        return default_warehouse_map

    def validate_user_type_properties(self, bp: UserBlueprint):
        if bp.type in ("SERVICE", "LEGACY_SERVICE"):
            if bp.first_name:
                raise ValueError(f"Property [FIRST_NAME] is not allowed for user [{bp.full_name}] with type [{bp.type}]")

            if bp.last_name:
                raise ValueError(f"Property [LAST_NAME] is not allowed for user [{bp.full_name}] with type [{bp.type}]")

        if bp.type == "SERVICE":
            if bp.password:
                raise ValueError(f"Property [PASSWORD] is not allowed for user [{bp.full_name}] with type [{bp.type}]")
