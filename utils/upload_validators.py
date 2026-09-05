"""
Per-field upload size validators.

Kept as a single blanket size limit is wrong here: a photo and a video have
very different reasonable ceilings. Use the specific validator for the
content type instead of writing a new inline one each time.

IMPORTANT: settings.DATA_UPLOAD_MAX_MEMORY_SIZE must be >= the largest limit
used below, or Django rejects the upload before these ever run.
"""
from django.core.exceptions import ValidationError


def validate_max_size(value, max_mb):
    if value and value.size > max_mb * 1024 * 1024:
        raise ValidationError(
            f"File too large ({value.size / 1024 / 1024:.1f} MB). "
            f"Maximum is {max_mb} MB."
        )


def validate_image_10mb(value):
    validate_max_size(value, 10)


def validate_video_60mb(value):
    validate_max_size(value, 60)
