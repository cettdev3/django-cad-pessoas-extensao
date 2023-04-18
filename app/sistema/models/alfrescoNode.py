from django.db import models
from datetime import datetime
import json

class AlfrescoNode(models.Model):
    is_file = models.BooleanField()
    created_by_user_id = models.CharField(max_length=255)
    created_by_user_display_name = models.CharField(max_length=255)
    modified_at = models.DateTimeField()
    node_type = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=255)
    mime_type_name = models.CharField(max_length=255)
    size_in_bytes = models.PositiveIntegerField()
    encoding = models.CharField(max_length=255)
    parent_id = models.CharField(max_length=255)
    aspect_names = models.JSONField()
    created_at = models.DateTimeField()
    is_folder = models.BooleanField()
    modified_by_user_id = models.CharField(max_length=255)
    modified_by_user_display_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    entry_id = models.CharField(max_length=255)
    version_label = models.CharField(max_length=255)
    version_type = models.CharField(max_length=255)

    class Meta:
        managed = False

    def createAlfrescoNodeFromResponse(response_content):
        entry = json.loads(response_content)['entry']
        node = AlfrescoNode(
            is_file=entry['isFile'],
            created_by_user_id=entry['createdByUser']['id'],
            created_by_user_display_name=entry['createdByUser']['displayName'],
            modified_at=datetime.strptime(entry['modifiedAt'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            node_type=entry['nodeType'],
            mime_type=entry['content']['mimeType'],
            mime_type_name=entry['content']['mimeTypeName'],
            size_in_bytes=entry['content']['sizeInBytes'],
            encoding=entry['content']['encoding'],
            parent_id=entry['parentId'],
            aspect_names=entry['aspectNames'],
            created_at=datetime.strptime(entry['createdAt'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            is_folder=entry['isFolder'],
            modified_by_user_id=entry['modifiedByUser']['id'],
            modified_by_user_display_name=entry['modifiedByUser']['displayName'],
            name=entry['name'],
            entry_id=entry['id'],
            version_label=entry['properties']['cm:versionLabel'],
            version_type=entry['properties']['cm:versionType']
        )
        return node
