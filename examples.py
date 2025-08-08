"""
أمثلة على استخدام HUSKYLENS
Examples for using HUSKYLENS

تشغيل هذا الملف لاختبار وظائف HUSKYLENS المختلفة
"""

from huskylens import HuskyLens, HuskyLensError
import time

def test_face_recognition():
    """اختبار التعرف على الوجوه"""
    print("🟦 اختبار التعرف على الوجوه...")
    
    # إنشاء كائن HUSKYLENS
    husky = HuskyLens('COM3')  # غير المنفذ حسب نظامك
    
    try:
        # الاتصال
        if not husky.connect():
            print("❌ فشل الاتصال مع HUSKYLENS")
            return
        
        # تعيين وضع التعرف على الوجوه
        husky.set_algorithm(HuskyLens.FACE_RECOGNITION)
        
        print("👤 ابحث عن الوجوه لمدة 10 ثوانٍ...")
        start_time = time.time()
        
        while time.time() - start_time < 10:
            faces = husky.get_blocks()
            
            if faces:
                print(f"🎯 تم العثور على {len(faces)} وجه:")
                for i, face in enumerate(faces):
                    print(f"  الوجه {i+1}: {face}")
            else:
                print("🔍 لا توجد وجوه مكتشفة...")
            
            time.sleep(1)
    
    except Exception as e:
        print(f"❌ خطأ: {e}")
    
    finally:
        husky.disconnect()

def test_object_tracking():
    """اختبار تتبع الكائنات"""
    print("🟩 اختبار تتبع الكائنات...")
    
    husky = HuskyLens('COM3')
    
    try:
        if not husky.connect():
            return
        
        husky.set_algorithm(HuskyLens.OBJECT_TRACKING)
        
        print("📦 ضع كائناً أمام الكاميرا وحركه...")
        
        for i in range(20):
            objects = husky.get_blocks()
            
            if objects:
                obj = objects[0]  # أول كائن
                print(f"📍 الكائن في الموقع: ({obj.center_x}, {obj.center_y})")
                
                # تحديد اتجاه الحركة
                if obj.center_x < 160:  # يسار (افتراض عرض الشاشة 320)
                    print("⬅️ الكائن على اليسار")
                elif obj.center_x > 160:
                    print("➡️ الكائن على اليمين")
                else:
                    print("🎯 الكائن في المنتصف")
            else:
                print("🔍 لا يوجد كائن مكتشف...")
            
            time.sleep(0.5)
    
    except Exception as e:
        print(f"❌ خطأ: {e}")
    
    finally:
        husky.disconnect()

def test_color_recognition():
    """اختبار التعرف على الألوان"""
    print("🟨 اختبار التعرف على الألوان...")
    
    husky = HuskyLens('COM3')
    
    try:
        if not husky.connect():
            return
        
        husky.set_algorithm(HuskyLens.COLOR_RECOGNITION)
        
        print("🎨 أولاً، علّم HUSKYLENS لوناً معيناً...")
        print("ضع كائناً ملوناً أمام الكاميرا واضغط Enter لتعليمه...")
        input()
        
        husky.learn_object(1)
        print("✅ تم تعلم اللون!")
        
        print("🔍 الآن ابحث عن نفس اللون...")
        
        for i in range(15):
            colors = husky.get_blocks()
            
            if colors:
                print(f"🎯 تم العثور على {len(colors)} كائن بنفس اللون:")
                for j, color in enumerate(colors):
                    print(f"  اللون {j+1}: {color}")
            else:
                print("🔍 لا يوجد لون مطابق...")
            
            time.sleep(1)
    
    except Exception as e:
        print(f"❌ خطأ: {e}")
    
    finally:
        husky.disconnect()

def test_line_tracking():
    """اختبار تتبع الخطوط"""
    print("🟪 اختبار تتبع الخطوط...")
    
    husky = HuskyLens('COM3')
    
    try:
        if not husky.connect():
            return
        
        husky.set_algorithm(HuskyLens.LINE_TRACKING)
        
        print("📏 ضع خطاً أسود على خلفية بيضاء أمام الكاميرا...")
        
        for i in range(10):
            arrows = husky.get_arrows()
            
            if arrows:
                print(f"📐 تم العثور على {len(arrows)} خط:")
                for j, arrow in enumerate(arrows):
                    print(f"  الخط {j+1}: من ({arrow[0]}, {arrow[1]}) إلى ({arrow[2]}, {arrow[3]})")
            else:
                print("🔍 لا توجد خطوط مكتشفة...")
            
            time.sleep(1)
    
    except Exception as e:
        print(f"❌ خطأ: {e}")
    
    finally:
        husky.disconnect()

def interactive_demo():
    """عرض تفاعلي لجميع الوظائف"""
    print("🚀 مرحباً بك في عرض HUSKYLENS التفاعلي!")
    print("=" * 50)
    
    while True:
        print("\n🎯 اختر الوظيفة التي تريد اختبارها:")
        print("1️⃣  التعرف على الوجوه")
        print("2️⃣  تتبع الكائنات")
        print("3️⃣  التعرف على الألوان")
        print("4️⃣  تتبع الخطوط")
        print("5️⃣  أخذ لقطة شاشة")
        print("0️⃣  خروج")
        
        choice = input("\n👉 اختيارك: ").strip()
        
        if choice == '1':
            test_face_recognition()
        elif choice == '2':
            test_object_tracking()
        elif choice == '3':
            test_color_recognition()
        elif choice == '4':
            test_line_tracking()
        elif choice == '5':
            test_screenshot()
        elif choice == '0':
            print("👋 وداعاً!")
            break
        else:
            print("❌ اختيار غير صحيح، حاول مرة أخرى")

def test_screenshot():
    """اختبار أخذ لقطة شاشة"""
    print("📸 اختبار أخذ لقطة شاشة...")
    
    husky = HuskyLens('COM3')
    
    try:
        if not husky.connect():
            return
        
        timestamp = int(time.time())
        filename = f"huskylens_photo_{timestamp}.jpg"
        
        if husky.take_screenshot(filename):
            print(f"✅ تم حفظ الصورة: {filename}")
        else:
            print("❌ فشل في أخذ لقطة الشاشة")
    
    except Exception as e:
        print(f"❌ خطأ: {e}")
    
    finally:
        husky.disconnect()

if __name__ == "__main__":
    print("🤖 HUSKYLENS Python Controller")
    print("🔗 تأكد من توصيل HUSKYLENS بالمنفذ التسلسلي")
    print("⚙️  قم بتغيير المنفذ في الكود حسب نظامك (COM3, /dev/ttyUSB0, إلخ)")
    print()
    
    interactive_demo()
