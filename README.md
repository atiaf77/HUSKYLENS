# HUSKYLENS Python Controller

🤖 مكتبة Python شاملة للتحكم في HUSKYLENS - مستشعر الرؤية الذكي

## ما هو HUSKYLENS؟

HUSKYLENS هو مستشعر رؤية ذكي سهل الاستخدام مع خوارزميات ذكاء اصطناعي مدمجة. يمكنه القيام بـ:

- 👤 **التعرف على الوجوه** - كشف وتتبع الوجوه البشرية
- 📦 **تتبع الكائنات** - تتبع الكائنات المتحركة
- 🎯 **التعرف على الكائنات** - التعرف على كائنات محددة مسبقاً
- 📏 **تتبع الخطوط** - تتبع الخطوط والمسارات
- 🎨 **التعرف على الألوان** - كشف الألوان المحددة
- 🏷️ **التعرف على العلامات** - قراءة AprilTags
- 📱 **قراءة رموز QR والباركود** - قراءة الرموز المختلفة

## متطلبات التشغيل

```bash
pip install -r requirements.txt
```

### المكتبات المطلوبة:
- `pyserial` - للاتصال التسلسلي مع HUSKYLENS
- `opencv-python` - لمعالجة الصور (اختياري للميزات المتقدمة)
- `numpy` - للعمليات الرياضية
- `pillow` - لمعالجة الصور

## التوصيل

### اتصال تسلسلي (UART)
```
HUSKYLENS -> Arduino/Raspberry Pi
T (TX)    -> Pin 2 (RX)
R (RX)    -> Pin 3 (TX)
- (GND)   -> GND
+ (VCC)   -> 3.3V أو 5V
```

### اتصال USB
- قم بتوصيل HUSKYLENS مباشرة بالكمبيوتر عبر كابل USB
- تأكد من تثبيت التعريفات المناسبة

## الاستخدام السريع

### مثال بسيط للتعرف على الوجوه

```python
from huskylens import HuskyLens

# إنشاء اتصال (غير المنفذ حسب نظامك)
husky = HuskyLens('COM3')  # Windows
# husky = HuskyLens('/dev/ttyUSB0')  # Linux
# husky = HuskyLens('/dev/cu.usbserial-XXX')  # macOS

# الاتصال
if husky.connect():
    # تعيين وضع التعرف على الوجوه
    husky.set_algorithm(HuskyLens.FACE_RECOGNITION)
    
    # البحث عن الوجوه
    faces = husky.get_blocks()
    
    if faces:
        print(f"تم العثور على {len(faces)} وجه!")
        for face in faces:
            print(f"الوجه في الموقع: ({face.center_x}, {face.center_y})")
    
    husky.disconnect()
```

### تشغيل الأمثلة التفاعلية

```bash
python examples.py
```

## الميزات المتاحة

### 🔧 الوظائف الأساسية

| الوظيفة | الوصف |
|---------|--------|
| `connect()` | إنشاء اتصال مع HUSKYLENS |
| `disconnect()` | قطع الاتصال |
| `set_algorithm(mode)` | تغيير وضع الكشف |
| `get_blocks()` | الحصول على الكائنات المكتشفة |
| `get_arrows()` | الحصول على الخطوط والاتجاهات |
| `learn_object()` | تعلم كائن جديد |
| `forget_object()` | نسيان كائن متعلم |

### 🎯 أوضاع الكشف المتاحة

```python
# أوضاع HUSKYLENS
HuskyLens.FACE_RECOGNITION      # التعرف على الوجوه
HuskyLens.OBJECT_TRACKING       # تتبع الكائنات
HuskyLens.OBJECT_RECOGNITION    # التعرف على الكائنات
HuskyLens.LINE_TRACKING         # تتبع الخطوط
HuskyLens.COLOR_RECOGNITION     # التعرف على الألوان
HuskyLens.TAG_RECOGNITION       # التعرف على العلامات
HuskyLens.QR_CODE_RECOGNITION   # قراءة رموز QR
HuskyLens.BARCODE_RECOGNITION   # قراءة الباركود
```

## أمثلة متقدمة

### تتبع الكائنات مع التحكم في الحركة

```python
from huskylens import HuskyLens
import time

husky = HuskyLens('COM3')

if husky.connect():
    husky.set_algorithm(HuskyLens.OBJECT_TRACKING)
    
    while True:
        objects = husky.get_blocks()
        
        if objects:
            obj = objects[0]  # أول كائن
            
            # تحديد الاتجاه بناءً على موقع الكائن
            if obj.center_x < 100:
                print("🔄 تحرك يساراً")
                # كود التحكم في المحرك هنا
            elif obj.center_x > 220:
                print("🔄 تحرك يميناً")
                # كود التحكم في المحرك هنا
            else:
                print("✅ الكائن في المنتصف")
        
        time.sleep(0.1)
```

### التعرف على الألوان مع التصنيف

```python
from huskylens import HuskyLens
from utils import ColorAnalyzer

husky = HuskyLens('COM3')
analyzer = ColorAnalyzer()

if husky.connect():
    husky.set_algorithm(HuskyLens.COLOR_RECOGNITION)
    
    # تعلم لون جديد
    print("ضع كائناً ملوناً أمام الكاميرا...")
    input("اضغط Enter لتعليم اللون...")
    husky.learn_object(1)
    
    # البحث عن اللون
    while True:
        colors = husky.get_blocks()
        
        for color_obj in colors:
            # يمكن إضافة تحليل لون متقدم هنا
            print(f"🎨 لون مكتشف في: ({color_obj.center_x}, {color_obj.center_y})")
        
        time.sleep(0.5)
```

## الأدوات المساعدة

يتضمن المشروع أدوات مساعدة في `utils.py`:

- **ObjectTracker**: لتتبع الكائنات عبر الإطارات
- **ColorAnalyzer**: لتحليل وتصنيف الألوان
- **HuskyLensUtils**: أدوات رسم وتحليل عامة

```python
from utils import ObjectTracker, ColorAnalyzer

# متتبع الكائنات
tracker = ObjectTracker()
tracked_objects = tracker.update(detections)

# محلل الألوان
analyzer = ColorAnalyzer()
color_name = analyzer.classify_color((255, 0, 0))  # "أحمر"
```

## استكشاف الأخطاء

### مشاكل الاتصال

1. **تأكد من المنفذ الصحيح**:
   ```python
   # Windows
   husky = HuskyLens('COM3')
   
   # Linux
   husky = HuskyLens('/dev/ttyUSB0')
   
   # macOS
   husky = HuskyLens('/dev/cu.usbserial-XXX')
   ```

2. **تحقق من الاتصال**:
   ```bash
   # Windows
   # تحقق من إدارة الأجهزة
   
   # Linux
   ls /dev/ttyUSB*
   
   # macOS
   ls /dev/cu.*
   ```

3. **تأكد من سرعة الاتصال**:
   - السرعة الافتراضية: 9600 baud
   - يمكن تغييرها من إعدادات HUSKYLENS

### مشاكل الكشف

- تأكد من الإضاءة الجيدة
- نظف عدسة HUSKYLENS
- اضبط المسافة المناسبة من الكائن
- تأكد من وضوح الكائن المراد كشفه

## المساهمة

نرحب بالمساهمات! إذا كان لديك تحسينات أو ميزات جديدة:

1. Fork المشروع
2. أنشئ branch جديد للميزة
3. Commit التغييرات
4. افتح Pull Request

## الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف LICENSE للتفاصيل.

## الدعم

- 📧 للاستفسارات: اكتب issue في GitHub
- 📖 وثائق HUSKYLENS الرسمية: [docs.huskylens.com](https://docs.huskylens.com)
- 🎥 فيديوهات تعليمية: ابحث عن "HUSKYLENS tutorial" على YouTube

## تطوير المشروع

### خطط التطوير القادمة:
- [ ] دعم واجهة I2C
- [ ] تحسين بروتوكول الاتصال
- [ ] إضافة مزيد من أمثلة الاستخدام
- [ ] دعم أنواع مختلفة من الكائنات
- [ ] تحسين أداء تتبع الكائنات
- [ ] إضافة واجهة مستخدم رسومية

---

🚀 **ابدأ رحلتك مع HUSKYLENS اليوم!**

جرب الأمثلة المختلفة واكتشف إمكانيات الرؤية الحاسوبية المدهشة!
