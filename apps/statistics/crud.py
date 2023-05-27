from sqlalchemy.orm import Session
from apps.statistics import models


# def cities(db: Session):
#     return db.query(models.City).all()


def categories(db: Session):
    return ['نوشیدنی',
            'چاشنی و افزودنی غذا',
            'آرایشی و بهداشتی',
            'خواربار و نان',
            'خانه و آشپزخانه',
            'تنقلات',
            'لبنیات و بستنی',
            'کنسرو و غذای آماده',
            'شیرینی و دسر',
            'پروتیین و تخممرغ',
            'میوه و سبزیجات تازه',
            'پروتئین و تخممرغ',
            'خواروبار و نان',
            'کودک و نوزاد',
            'ابزار و الکترونیک',
            'آجیل و خشکبار',
            'اداری و نوشتافزار',
            'الکترونیک و ابزار',
            'قهوه',
            'اداری و نوشتافزار',
            'حیوانات خانگی']


# def categories(db: Session):
#     return db.query(models.Category).all()
def cities(db: Session):
    return ["کرج",
            "تهران",
            "قم",
            "مشهد",
            "شیراز",
            "آمل",
            "اراک",
            "همدان",
            "کرمان",
            "یزد",
            "قزوین",
            "اصفهان",
            "اسلامشهر",
            "تبریز",
            "نیشابور",
            "اهواز",
            "شاهین",
            "شهر",
            "ارومیه",
            "گنبد",
            "کاووس",
            "ساری",
            "رشت",
            "سنندج",
            "قائم شهر",
            "مسجدسليمان",
            "اردبیل",
            "مریوان",
            "اندیشه",
            "سبزوار",
            "پردیس",
            "قرچک",
            "بابل",
            "نسیم",
            "شهر",
            "بوشهر",
            "بروجرد",
            "لاهیجان",
            "ایلام",
            "تربت",
            "حیدریه",
            "شوشتر",
            "بندرعباس",
            "شهریار",
            "کرمانشاه",
            "شاهرود",
            "یاسوج",
            "شهرکرد",
            "لنگرود",
            "سمنان",
            "گرگان",
            "محمود",
            "آباد",
            "رودهن",
            "خرم",
            "آباد",
            "کاشان",
            "زنجان",
            "بناب",
            "بابلسر",
            "صومعه",
            "سرا",
            "سپاهان",
            "شهر",
            "بندر",
            "انزلی",
            "بهارستان",
            "پرند",
            "رودسر",
            "قشم",
            "بستان",
            "آباد",
            "شهر",
            "قدس",
            "مراغه",
            "درود",
            "صدرا",
            "پاکدشت",
            "نورآباد",
            "محمد",
            "شهر",
            "قره",
            "ضياءالدين",
            "آستانه",
            "اشرفیه",
            "کازرون",
            "نجف",
            "آباد",
            "اهر",
            "خوی",
            "رفسنجان",
            "آستارا",
            "ساوه",
            "مرند",
            "گچساران",
            "بیجار",
            "هاديشهر",
            "هشتگرد",
            "میاندوآب",
            "تنکابن",
            "مرودشت",
            "بجنورد",
            "فسا",
            "قاین",
            "باقر",
            "شهر",
            "گناوه",
            "خواف",
            "بهشهر",
            "قیامدشت",
            "گتوند",
            "کاشمر",
            "آزادشهر",
            "جویبار",
            "فریدونکنار",
            "لرستان",
            "لار",
            "مهاباد",
            "ميانه",
            "کوهدشت", ]


def statistic_types():
    return [name.value for name in models.StatisticType]


def get_city_category_statistic(city: int, category: int, statistic_type: str, db: Session):
    ccs = db.query(
        models.CategoryAreaStatistics
    ).filter(
        models.CategoryAreaStatistics.city_id == city, models.CategoryAreaStatistics.category_id == category
    ).first()

    return get_statistics(ccs_id=ccs.id, statistic_type=statistic_type, db=db)


def get_statistics(ccs_id: int, statistic_type: str, db: Session):
    return db.query(
        models.Statistics
    ).filter(
        models.Statistics.category_area_id == ccs_id
    ).filter(
        models.Statistics.type == statistic_type
    ).all()
