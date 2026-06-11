from django.core.management.base import BaseCommand
from datetime import date
from chesshub.models import Holiday


class Command(BaseCommand):
    help = "Seed India Holidays for year 2026"

    def handle(self, *args, **kwargs):

        holidays = [
            # JAN
            (date(2026, 1, 1), "New Year's Day", "RESTRICTED"),
            (date(2026, 1, 3), "Hazarat Ali's Birthday", "RESTRICTED"),
            (date(2026, 1, 14), "Pongal", "RESTRICTED"),
            (date(2026, 1, 14), "Makar Sankranti", "RESTRICTED"),
            (date(2026, 1, 23), "Vasant Panchami", "RESTRICTED"),
            (date(2026, 1, 26), "Republic Day", "GAZETTED"),

            # FEB
            (date(2026, 2, 1), "Guru Ravidas Jayanti", "RESTRICTED"),
            (date(2026, 2, 12), "Maharishi Dayanand Saraswati Jayanti", "RESTRICTED"),
            (date(2026, 2, 15), "Maha Shivaratri", "RESTRICTED"),
            (date(2026, 2, 19), "Shivaji Jayanti", "RESTRICTED"),

            # MAR
            (date(2026, 3, 3), "Holika Dahana", "RESTRICTED"),
            (date(2026, 3, 4), "Holi", "GAZETTED"),
            (date(2026, 3, 19), "Ugadi / Gudi Padwa", "RESTRICTED"),
            (date(2026, 3, 20), "Jamat Ul-Vida", "RESTRICTED"),
            (date(2026, 3, 21), "Ramzan Id", "GAZETTED"),
            (date(2026, 3, 26), "Rama Navami", "GAZETTED"),
            (date(2026, 3, 31), "Mahavir Jayanti", "GAZETTED"),

            # APR
            (date(2026, 4, 3), "Good Friday", "GAZETTED"),
            (date(2026, 4, 14), "Vaisakhi", "RESTRICTED"),
            (date(2026, 4, 14), "Ambedkar Jayanti", "OBSERVANCE"),
            (date(2026, 4, 15), "Bahag Bihu", "RESTRICTED"),

            # MAY
            (date(2026, 5, 1), "Buddha Purnima", "GAZETTED"),
            (date(2026, 5, 9), "Rabindranath Tagore Jayanti", "RESTRICTED"),
            (date(2026, 5, 27), "Bakrid", "GAZETTED"),

            # JUN
            (date(2026, 6, 26), "Muharram / Ashura", "GAZETTED"),

            # JUL
            (date(2026, 7, 16), "Rath Yatra", "RESTRICTED"),

            # AUG
            (date(2026, 8, 15), "Independence Day", "GAZETTED"),
            (date(2026, 8, 26), "Milad un-Nabi", "GAZETTED"),
            (date(2026, 8, 26), "Onam", "RESTRICTED"),
            (date(2026, 8, 28), "Raksha Bandhan", "RESTRICTED"),

            # SEP
            (date(2026, 9, 4), "Janmashtami", "GAZETTED"),
            (date(2026, 9, 14), "Ganesh Chaturthi", "RESTRICTED"),

            # OCT
            (date(2026, 10, 2), "Gandhi Jayanti", "GAZETTED"),
            (date(2026, 10, 18), "Maha Saptami", "RESTRICTED"),
            (date(2026, 10, 19), "Maha Ashtami", "RESTRICTED"),
            (date(2026, 10, 20), "Dussehra", "GAZETTED"),
            (date(2026, 10, 26), "Valmiki Jayanti", "RESTRICTED"),
            (date(2026, 10, 29), "Karaka Chaturthi", "RESTRICTED"),

            # NOV
            (date(2026, 11, 8), "Diwali", "GAZETTED"),
            (date(2026, 11, 9), "Govardhan Puja", "RESTRICTED"),
            (date(2026, 11, 11), "Bhai Duj", "RESTRICTED"),
            (date(2026, 11, 15), "Chhath Puja", "RESTRICTED"),
            (date(2026, 11, 24), "Guru Nanak Jayanti", "GAZETTED"),

            # DEC
            (date(2026, 12, 23), "Hazarat Ali's Birthday", "RESTRICTED"),
            (date(2026, 12, 24), "Christmas Eve", "RESTRICTED"),
            (date(2026, 12, 25), "Christmas", "GAZETTED"),
        ]

        created = 0
        for holiday_date, name, holiday_type in holidays:
            obj, is_created = Holiday.objects.get_or_create(
                date=holiday_date,
                defaults={
                    "name": name,
                    "holiday_type": holiday_type
                }
            )
            if is_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(f" {created} holidays seeded for 2026")
        )
