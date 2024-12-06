"""Import content types."""

from gorps.content_types.cooklang import format_cooklang_body
from gorps.model import PLAIN_TEXT, ContentType

COOKLANG = ContentType(mime_type="text/cooklang", to_plain_text=format_cooklang_body)

CONTENT_TYPES = {
    content_type.mime_type: content_type for content_type in (COOKLANG, PLAIN_TEXT)
}
