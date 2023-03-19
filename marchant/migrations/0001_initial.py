# Generated by Django 4.1.7 on 2023-03-14 00:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(upload_to='')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='')),
                ('image4', models.ImageField(blank=True, null=True, upload_to='')),
                ('image5', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('H', 'House'), ('A', 'Apartment'), ('O', 'Office'), ('R', 'Room')], default='R', max_length=1)),
                ('timeframe', models.CharField(choices=[('L', 'Lifetime'), ('M', 'Monthly'), ('Y', 'Yearly')], default='Y', max_length=1)),
                ('size', models.CharField(max_length=30)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('images', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='marchant.images')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate1', models.IntegerField(default=1)),
                ('rate2', models.IntegerField(default=1)),
                ('rate3', models.IntegerField(default=1)),
                ('rate4', models.IntegerField(default=1)),
                ('rate5', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='marchant.product')),
                ('rating', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='marchant.rating')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='marchant.reviewreply')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='marchant.rating'),
        ),
    ]
