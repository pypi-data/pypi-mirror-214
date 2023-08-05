"""
Serializers for enterprise api v1.
"""

import logging

from rest_framework import serializers

from enterprise_data.models import EnterpriseLearner, EnterpriseLearnerEnrollment, EnterpriseOffer

LOGGER = logging.getLogger(__name__)


class EnterpriseLearnerEnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for EnterpriseLearnerEnrollment model.
    """
    course_api_url = serializers.SerializerMethodField()
    enterprise_user_id = serializers.SerializerMethodField()
    total_learning_time_hours = serializers.SerializerMethodField()

    class Meta:
        model = EnterpriseLearnerEnrollment
        # Do not change the order of fields below. Ordering is important becuase `progress_v3`
        # csv generated in `enterprise_reporting` should be same as csv generated on `admin-portal`
        # Order and field names below should match with `EnterpriseLearnerEnrollmentViewSet.header`
        fields = (
            'enrollment_id', 'enterprise_enrollment_id', 'is_consent_granted', 'paid_by',
            'user_current_enrollment_mode', 'enrollment_date', 'unenrollment_date',
            'unenrollment_end_within_date', 'is_refunded', 'seat_delivery_method',
            'offer_id', 'offer_name', 'offer_type', 'coupon_code', 'coupon_name', 'contract_id',
            'course_list_price', 'amount_learner_paid', 'course_key', 'courserun_key',
            'course_title', 'course_pacing_type', 'course_start_date', 'course_end_date',
            'course_duration_weeks', 'course_max_effort', 'course_min_effort',
            'course_primary_program', 'primary_program_type', 'course_primary_subject', 'has_passed',
            'last_activity_date', 'progress_status', 'passed_date', 'current_grade',
            'letter_grade', 'enterprise_user_id', 'user_email', 'user_account_creation_date',
            'user_country_code', 'user_username', 'enterprise_name', 'enterprise_customer_uuid',
            'enterprise_sso_uid', 'created', 'course_api_url', 'total_learning_time_hours',
        )

    def get_course_api_url(self, obj):
        """Constructs course api url"""
        return '/enterprise/v1/enterprise-catalogs/{enterprise_customer_uuid}/courses/{courserun_key}'.format(
            enterprise_customer_uuid=obj.enterprise_customer_uuid, courserun_key=obj.courserun_key
        )

    def get_enterprise_user_id(self, obj):
        """Returns enterprise user id of a learner's enrollment"""
        return obj.enterprise_user_id

    def get_total_learning_time_hours(self, obj):
        """Returns the learners total learning time in hours"""
        return round((obj.total_learning_time_seconds or 0.0)/3600.0, 2)


class EnterpriseOfferSerializer(serializers.ModelSerializer):
    """
    Serializer for EnterpriseOfferSerializer model.
    """

    class Meta:
        model = EnterpriseOffer
        fields = '__all__'

    def validate_offer_id(self, value) -> str:
        """
        For a given offer_id string from the requester, determine the best representation to use for db storage.

        Raises serializers.ValidationError:
            If the given string is not exclusively numeric characters, but also does not parse as a UUID (either because
            it has the wrong length, incorrect dashes, or some other reason).
        """
        LOGGER.info('Validating offer ID: %s', value)
        if len(value) < 10 and isinstance(value, int):
            LOGGER.info('Validated offer ID is int: %s', value)
            return value

        elif isinstance(value, str) and len(value) == 32:
            LOGGER.info('Validated offer ID is string/UUID: %s', value)
            return value
        else:
            raise serializers.ValidationError("requested offer_id neither a valid integer nor UUID.")

    def to_internal_value(self, data):
        """
        Convert the incoming data offer_id field to a format that can be stored in the db.
        """
        LOGGER.info('Converting offer ID to internal value to_internal_value: %s', data)
        ret = super().to_representation(data)
        if isinstance(ret['offer_id'], str):
            ret['offer_id'] = ret['offer_id'].replace('-', '')
        LOGGER.info('Converted offer ID to internal value to_internal_value: %s', ret)
        return ret

    def to_representation(self, instance):
        """
        Add `-` dashes to the outgoing data offer_id field.
        """
        ret = super().to_representation(instance)

        # A 32 character offer_id is our heuristic for whether the stored value represents a UUID or integer.  If the
        # heuristic passes, make the serialized output look like a UUID.
        if len(ret['offer_id']) == 32:
            ret['offer_id'] = '-'.join([
                    ret['offer_id'][:8],
                    ret['offer_id'][8:12],
                    ret['offer_id'][12:16],
                    ret['offer_id'][16:20],
                    ret['offer_id'][20:]
                ]
            )

        return ret


class EnterpriseLearnerSerializer(serializers.ModelSerializer):
    """
    Serializer for EnterpriseLearner model.
    """

    class Meta:
        model = EnterpriseLearner
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if hasattr(instance, 'enrollment_count'):
            representation['enrollment_count'] = instance.enrollment_count
        if hasattr(instance, 'course_completion_count'):
            representation['course_completion_count'] = instance.course_completion_count

        return representation


class LearnerCompletedCoursesSerializer(serializers.Serializer):    # pylint: disable=abstract-method
    """
    Serializer for learner's completed courses.
    """
    class Meta:
        ref_name = 'v1.LearnerCompletedCoursesSerializer'

    user_email = serializers.EmailField()
    completed_courses = serializers.IntegerField()
