# Purpose: empty baseline migration (T-012). It proves the migration tool works against
# PostgreSQL. Business tables arrive in later tasks, each with its own reviewed migration.
from django.db import migrations


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = []
