from datagen_protocol.migrations.migration_base import APIVersion, MigrationBase, schema_change
from datagen_protocol.schema.humans import Expression

MIN_INTENSITY = 1.0
MAX_INTENSITY = 5.0


class Migration(MigrationBase):
    version = APIVersion(major=1, minor=0)
    migration_type = "datapoints"

    @schema_change
    def move_to_arkit_format(request: dict) -> None:
        old_expression = request["human"]["head"]["expression"]
        expression_name = old_expression["name"]
        new_expression = Expression.from_preset(
            preset_type=Migration._extract_preset(
                expression_name=expression_name, intensity=old_expression["intensity"]
            )
        )
        eyelid_closure = request["human"]["head"]["eyes"]["eyelid_closure"]
        new_expression.eye_blink_left = eyelid_closure
        new_expression.eye_blink_right = eyelid_closure
        del request["human"]["head"]["expression"]["name"]
        del request["human"]["head"]["expression"]["intensity"]
        del request["human"]["head"]["eyes"]["eyelid_closure"]
        request["human"]["head"]["expression"].update(new_expression)

    @staticmethod
    def _extract_preset(expression_name: str, intensity: int) -> str:
        mapped_intensity = int((MAX_INTENSITY - MIN_INTENSITY) * intensity + MIN_INTENSITY)
        return f"{expression_name}_{mapped_intensity}"
