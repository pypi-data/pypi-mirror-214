# Generated by Django 4.2 on 2023-04-14 09:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_blocks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentblock',
            name='css_class',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='contentblockfield',
            name='field_type',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='contentblocktemplatefield',
            name='css_class',
            field=models.CharField(blank=True, help_text='Set a custom CSS class for this field in the editor.', max_length=64),
        ),
        migrations.AlterField(
            model_name='contentblocktemplatefield',
            name='field_type',
            field=models.CharField(choices=[('TextField', 'Text Field'), ('ContentField', 'Content Field'), ('ImageField', 'Image Field'), ('VideoField', 'Video Field'), ('FileField', 'File Field'), ('EmbeddedVideoField', 'Embedded Video Field'), ('NestedField', 'Nested Field'), ('ModelChoiceField', 'Model Choice Field'), ('ChoiceField', 'Choice Field'), ('CheckboxField', 'Checkbox Field')], max_length=32),
        ),
        migrations.AlterField(
            model_name='contentblocktemplatefield',
            name='key',
            field=models.SlugField(help_text='Must be unique to this content block template. Lowercase letters, numbers and underscores only.', max_length=64, validators=[django.core.validators.RegexValidator('[a-z0-9_]+', 'Lowercase letters, numbers and underscores only.')]),
        ),
    ]
