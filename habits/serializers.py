from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ['user']

    def validate(self, data):
        if data.get("reward") and data.get("related_habit"):
            raise serializers.ValidationError(
                "Cannot have both a reward and a related habit."
            )

        if data.get("estimated_time", 0) > 120:
            raise serializers.ValidationError(
                "Estimated time must be 120 seconds or less."
            )

        if data.get("frequency", 1) > 7:
            raise serializers.ValidationError(
                "Frequency must be at least once every 7 days."
            )

        if data.get("is_pleasant") and (
            data.get("reward") or data.get("related_habit")
        ):
            raise serializers.ValidationError(
                "Pleasant habits cannot have rewards or related habits."
            )

        return data
