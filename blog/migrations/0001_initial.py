# Generated by Django 3.1.7 on 2021-04-28 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('post_name', models.CharField(max_length=50)),
                ('subheading', models.CharField(default=' ', max_length=50)),
                ('category_tag', models.CharField(default=' ', max_length=50)),
                ('writer', models.CharField(default=' ', max_length=50)),
                ('code', models.CharField(default=' ', max_length=5000)),
                ('content', models.CharField(max_length=4000)),
                ('pub_date', models.DateField()),
                ('thumbnail', models.ImageField(default=' ', upload_to='shop/images')),
                ('subimage', models.ImageField(default=' ', upload_to='shop/images')),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
    ]
