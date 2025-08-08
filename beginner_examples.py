"""
أمثلة بسيطة للمبتدئين - HUSKYLENS
Simple examples for beginners
"""

from huskylens import HuskyLens
import time

def basic_connection_test():
    """اختبار الاتصال الأساسي"""
    print("🔌 اختبار الاتصال مع HUSKYLENS...")
    
    # إنشاء كائن HUSKYLENS
    # غير COM3 إلى المنفذ الصحيح في نظامك
    husky = HuskyLens('COM3')
    
    # محاولة الاتصال
    if husky.connect():
        print("✅ نجح الاتصال!")
        print("📡 HUSKYLENS جاهز للاستخدام")
        
        # قطع الاتصال
        husky.disconnect()
        return True
    else:
        print("❌ فشل الاتصال!")
        print("🔧 تحقق من:")
        print("   - توصيل الكابل")
        print("   - المنفذ الصحيح (COM3, COM4, etc.)")
        print("   - تشغيل HUSKYLENS")
        return False

def simple_face_detection():
    """كشف الوجوه البسيط"""
    print("👤 كشف الوجوه البسيط...")
    
    husky = HuskyLens('COM3')
    
    if not husky.connect():
        print("❌ لا يمكن الاتصال بـ HUSKYLENS")
        return
    
    # تعيين وضع كشف الوجوه
    husky.set_algorithm(HuskyLens.FACE_RECOGNITION)
    print("🎯 ابحث عن وجه أمام الكاميرا...")
    
    # البحث عن الوجوه لمدة 10 ثوانٍ
    for i in range(10):
        print(f"⏱️ البحث... {i+1}/10")
        
        faces = husky.get_blocks()
        
        if faces:
            print(f"🎉 وجدت {len(faces)} وجه!")
            face = faces[0]  # أول وجه
            print(f"📍 الوجه في الموقع: س={face.center_x}, ص={face.center_y}")
            break
        else:
            print("🔍 لا يوجد وجه... ابحث أكثر")
        
        time.sleep(1)
    
    husky.disconnect()
    print("✅ انتهى اختبار كشف الوجوه")

def simple_object_following():
    """تتبع كائن بسيط"""
    print("📦 تتبع كائن بسيط...")
    
    husky = HuskyLens('COM3')
    
    if not husky.connect():
        return
    
    # تعيين وضع تتبع الكائنات
    husky.set_algorithm(HuskyLens.OBJECT_TRACKING)
    print("🎯 ضع كائناً أمام الكاميرا وحركه...")
    
    # تتبع لمدة 15 ثانية
    for i in range(30):  # 30 قراءة × 0.5 ثانية = 15 ثانية
        objects = husky.get_blocks()
        
        if objects:
            obj = objects[0]  # أول كائن
            x = obj.center_x
            y = obj.center_y
            
            print(f"📍 الكائن في: ({x}, {y})", end=" -> ")
            
            # تحديد الاتجاه (افتراض عرض الشاشة 320 بكسل)
            if x < 107:      # الثلث الأيسر
                print("⬅️ يسار")
            elif x > 213:    # الثلث الأيمن  
                print("➡️ يمين")
            else:            # الوسط
                print("🎯 وسط")
        else:
            print("❓ لا يوجد كائن مرئي...")
        
        time.sleep(0.5)
    
    husky.disconnect()
    print("✅ انتهى تتبع الكائن")

def simple_color_learning():
    """تعلم لون بسيط"""
    print("🎨 تعلم لون بسيط...")
    
    husky = HuskyLens('COM3')
    
    if not husky.connect():
        return
    
    # تعيين وضع التعرف على الألوان
    husky.set_algorithm(HuskyLens.COLOR_RECOGNITION)
    
    print("📝 خطوات تعلم اللون:")
    print("1. ضع كائناً ملوناً أمام الكاميرا")
    print("2. اضغط Enter لتعليم HUSKYLENS هذا اللون")
    
    input("👉 اضغط Enter عندما تكون جاهزاً...")
    
    # تعليم اللون
    husky.learn_object(1)  # تعلم كلون رقم 1
    print("🧠 تم تعلم اللون!")
    
    print("🔍 الآن حرك الكائن أو ضع كائنات أخرى بنفس اللون...")
    
    # البحث عن اللون المتعلم
    for i in range(20):
        colors = husky.get_blocks()
        
        if colors:
            print(f"🎯 وجدت {len(colors)} كائن بنفس اللون:")
            for j, color in enumerate(colors):
                print(f"   الكائن {j+1}: موقع ({color.center_x}, {color.center_y})")
        else:
            print("🔍 لا يوجد كائن بهذا اللون...")
        
        time.sleep(1)
    
    husky.disconnect()
    print("✅ انتهى تعلم الألوان")

def interactive_beginner_menu():
    """قائمة تفاعلية للمبتدئين"""
    print("🌟 مرحباً بك في عالم HUSKYLENS!")
    print("=" * 40)
    
    # اختبار الاتصال أولاً
    if not basic_connection_test():
        print("\n💡 نصائح لحل مشكلة الاتصال:")
        print("1. تأكد من توصيل كابل USB/Serial بشكل صحيح")
        print("2. تحقق من تشغيل HUSKYLENS")
        print("3. جرب منافذ مختلفة: COM1, COM2, COM3, etc.")
        print("4. أعد تشغيل HUSKYLENS والبرنامج")
        return
    
    while True:
        print("\n🎯 ماذا تريد أن تجرب؟")
        print("1️⃣  كشف الوجوه البسيط")
        print("2️⃣  تتبع كائن")
        print("3️⃣  تعلم لون جديد")
        print("4️⃣  اختبار الاتصال مرة أخرى")
        print("0️⃣  خروج")
        
        choice = input("\n👉 اختر رقماً: ").strip()
        
        if choice == '1':
            simple_face_detection()
        elif choice == '2':
            simple_object_following()
        elif choice == '3':
            simple_color_learning()
        elif choice == '4':
            basic_connection_test()
        elif choice == '0':
            print("👋 إلى اللقاء! استمتع بـ HUSKYLENS!")
            break
        else:
            print("❌ اختيار غير صحيح، جرب مرة أخرى")

def quick_demo():
    """عرض سريع لجميع الوظائف"""
    print("🚀 عرض سريع لوظائف HUSKYLENS")
    print("-" * 35)
    
    husky = HuskyLens('COM3')
    
    if not husky.connect():
        print("❌ لا يمكن بدء العرض - تحقق من الاتصال")
        return
    
    # جربة كل الأوضاع لفترة قصيرة
    modes = [
        (HuskyLens.FACE_RECOGNITION, "👤 التعرف على الوجوه"),
        (HuskyLens.OBJECT_TRACKING, "📦 تتبع الكائنات"),
        (HuskyLens.COLOR_RECOGNITION, "🎨 التعرف على الألوان"),
        (HuskyLens.LINE_TRACKING, "📏 تتبع الخطوط"),
    ]
    
    for mode, name in modes:
        print(f"\n{name}...")
        husky.set_algorithm(mode)
        
        # جربة لمدة 3 ثوانٍ
        for i in range(3):
            detections = husky.get_blocks()
            if detections:
                print(f"  ✅ تم كشف {len(detections)} كائن")
            else:
                print(f"  🔍 بحث... {i+1}/3")
            time.sleep(1)
    
    husky.disconnect()
    print("\n🎉 انتهى العرض السريع!")

if __name__ == "__main__":
    print("🤖 أمثلة HUSKYLENS للمبتدئين")
    print("🔧 تأكد من توصيل HUSKYLENS قبل البدء")
    print()
    
    # تشغيل القائمة التفاعلية
    interactive_beginner_menu()
